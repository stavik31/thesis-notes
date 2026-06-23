---
title: "Stage 3 — GAT Risk Model"
type: build-stage
stage: 3
date: "2026-06-23"
tags: [phase3, build, gat, risk-model, thesis-core]
---

# Stage 3 — GAT Risk Model

## What this stage does

Trains a Graph Attention Network (GAT) with vehicle-type-conditioned attention on the segmented road network. The model learns the relationship between road features, spatial context, and crash frequency per vehicle type. Output is a risk score per (segment, vehicle type).

## Input

- `segments.csv` — segment features from Stage 2
- `crashes_segmented.csv` — crashes with segment_id from Stage 2
- `graph_edges.csv` — graph structure from Stage 2

## Output

- `risk_scores.csv` — one row per (segment_id, vehicle_type): predicted severity-weighted crash rate (predicted count / exposure)

---

## Architecture

**Graph Attention Network (GAT) with vehicle-type embeddings**

- **Nodes**: road segments
- **Edges**: junction connections between segments
- **Node features**: road_class (one-hot), speed_limit, length, AADF, crash history per type per year (training years only)
- **Vehicle type embeddings**: `nn.Embedding(num_vehicle_types, embedding_dim)` — each type gets a learned vector (start with embedding_dim = 16)
- **Type-conditioned attention**: when computing attention coefficients α_ij for an edge, concatenate the vehicle type embedding to the node features before the attention calculation. This shifts the model's neighbourhood focus depending on which type it's computing risk for
- **Output layer**: per-node risk score per vehicle type (one forward pass per type, or batch all types together with the embedding as input)

---

## Build steps

**1. Set up PyTorch Geometric (PyG)**
- Install: `pip install torch torch_geometric`
- PyG handles graph data structures, GAT layers, and batching

**2. Build the PyG graph object**
- `x` = node feature matrix (num_segments × num_features)
- `edge_index` = adjacency from `graph_edges.csv` (2 × num_edges tensor)
- Store as a `torch_geometric.data.Data` object

**3. Define training targets**
- For each (segment, vehicle_type, year) in training years: compute severity-weighted crash count
- Severity weight: fatal=3, serious=2, slight=1 — sum across all crashes of that type on that segment in that year
- Organise as a matrix: num_segments × num_types × num_train_years

**4. Check dispersion per vehicle type**
- Before fixing the loss function, run a quick dispersion check on the crash counts per type:
  - Compute mean and variance of crash counts per type across segments
  - If variance >> mean → over-dispersed → use Negative Binomial loss
  - If variance ≈ mean → Poisson loss
  - If variance < mean → under-dispersed (CMP territory) — note this and decide
- This picks the loss function; don't skip it

**5. Implement the GAT with type conditioning**
- Use `torch_geometric.nn.GATConv` as the base layer
- Before passing node features to GATConv: concatenate the vehicle type embedding to each node's feature vector
- Stack 2–3 GAT layers (start with 2)
- Add a linear output head: maps final node representations to a single risk score per type

**6. Define loss and training loop**
- Loss: Poisson NLL or NB NLL depending on dispersion check result
- Optimiser: Adam, learning rate 1e-3 (start here, tune if needed)
- Train/val split: years 1–3 train, year 4 validation, year 5 holdout (never touched until Stage 6)
- Train until validation loss plateaus

**7. Extract risk scores**
- Run the trained model on all segments for all vehicle types
- Divide predicted count by exposure: `risk_score = predicted_count / (AADF_type × length × num_years)`
- If per-type AADF is unavailable: use `AADF_total × type_share_fraction`
- Save as `risk_scores.csv`

---

## Open questions

- **Loss function**: determined by dispersion check in step 4 — do not assume
- **Embedding dimension**: start with 16, tune if validation loss suggests underfitting
- **Number of GAT layers**: start with 2; more layers = larger receptive field (neighbourhood radius), but risk of oversmoothing on dense urban networks
- **Edge features**: junction type (roundabout, T-junction, crossroads) could be added as edge attributes in PyG — adds complexity, revisit if the basic model underperforms
- **Per-type AADF**: if unavailable per type, use national vehicle-type share fractions as a proxy and document the approximation

---

## Tools

- PyTorch
- PyTorch Geometric (PyG)
- pandas, numpy

## Key papers

- Gao 2024 (AAP) — STATS19 GNN baseline; ZITD loss; MPIW/PICP/AccHR@20 metrics
- Zhu 2025 (T-ITS) — GNN for vehicle-group crash risk; architecture reference

## Links

- [[build/system-overview]] — full pipeline context
- [[build/stage-2-segmentation]] — previous stage
- [[build/stage-4-risk-surface-filtering]] — next stage (consumes risk_scores.csv)
