# JSONL Builder

## Code

```python
import json

# pre-group so we're not searching the full df every iteration
veh_grouped = veh_clean.groupby('collision_index')
cas_grouped = cas_clean.groupby(['collision_index', 'vehicle_reference'])

with open("output.jsonl", "w") as f:
    for _, collision in col_clean.iterrows():
        record = collision.to_dict()
        idx = record['collision_index']

        vehicles = veh_grouped.get_group(idx).to_dict('records') if idx in veh_grouped.groups else []
        
        for veh in vehicles:
            key = (idx, veh['vehicle_reference'])
            veh['casualties'] = cas_grouped.get_group(key).to_dict('records') if key in cas_grouped.groups else []
        
        record['vehicles'] = vehicles
        f.write(json.dumps(record) + "\n")
```

## Line by Line

**`veh_grouped = veh_clean.groupby('collision_index')`**
Pre-group vehicles by collision so lookups are fast instead of scanning the full dataframe each time.

**`cas_grouped = cas_clean.groupby(['collision_index', 'vehicle_reference'])`**
Same but casualties need both keys since they belong to a specific vehicle within a collision.

**`for _, collision in col_clean.iterrows():`**
Loop through every collision one at a time.

**`record = collision.to_dict()`**
Convert the collision row to a dictionary.

**`idx = record['collision_index']`**
Store the collision index so we can look up matching vehicles and casualties.

**`vehicles = veh_grouped.get_group(idx).to_dict('records') if idx in veh_grouped.groups else []`**
Get all vehicles for this collision as a list of dicts. If none exist, use an empty list.

**`for veh in vehicles:`**
Loop through each vehicle belonging to this collision.

**`key = (idx, veh['vehicle_reference'])`**
Build the combined key to look up casualties for this specific vehicle.

**`veh['casualties'] = cas_grouped.get_group(key).to_dict('records') if key in cas_grouped.groups else []`**
Get all casualties for this vehicle as a list of dicts and nest them inside the vehicle.

**`record['vehicles'] = vehicles`**
Attach the completed vehicles list (with casualties nested) to the collision record.

**`f.write(json.dumps(record) + "\n")`**
Write the full record as a single JSON line to the file.
