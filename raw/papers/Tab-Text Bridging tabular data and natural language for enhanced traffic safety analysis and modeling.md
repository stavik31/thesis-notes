---
title: "Tab-Text: Bridging tabular data and natural language for enhanced traffic safety analysis and modeling"
source: "https://www.sciencedirect.com/science/article/pii/S095741742502069X"
author:
  - "[[AbstractTraffic safety analysis has traditionally relied on tabular crash data]]"
  - "[[featuring variables in categorical or numeric forms. However]]"
  - "[[the conventional statistical approaches have inherent limitations in capturing intricate nonlinear feature interactions and struggle with the scales of large datasets available today. Consequently]]"
  - "[[modern machine learning techniques]]"
  - "[[especially tree ensembles]]"
  - "[[have emerged as dominant tools for analyzing tabular data due to their predictive capability and interpretability. Despite these advances]]"
  - "[[relying solely on preprocessed tabular data]]"
  - "[[structured through human-crafted coding]]"
  - "[[can lead to significant information loss]]"
  - "[[particularly when the nuances of crash narratives are not fully captured. To address this issue]]"
published:
created: 2026-04-08
description: "Traffic safety analysis has traditionally relied on tabular crash data, featuring variables in categorical or numeric forms. However, the conventional…"
tags:
  - "clippings"
---
[https://doi.org/10.1016/j.eswa.2025.128450](https://doi.org/10.1016/j.eswa.2025.128450 "Persistent link using digital object identifier")

Full text access

## Highlights

- •
	Pioneering LLM use in traffic safety domain through construction of [narratives](https://www.sciencedirect.com/topics/social-sciences/narrative).
- •
	Introduction of a multi-modal paradigm for leveraging the power of LLMs.
- •
	Improved accuracy in crash severity inference compared with diverse baselines.
- •
	Model Interpretation with permutation importance analysis.
- •
	Embedding visualization through UMAP.

- [Next article in issue](https://www.sciencedirect.com/science/article/pii/S0957417425020329)

## Keywords

Traffic safety

Crash severity inference

Crash event narrative generation

Multi-modal paradigm

Machine learning

Large language models

## 1\. Introduction

Traffic crashes claim an estimated 42,000 lives annually in the United States (). Despite advancements in vehicle safety features, [roadway design](https://www.sciencedirect.com/topics/social-sciences/roadway-design), and safety policies, mitigating accident frequency and severity remains a persistent challenge () due to the complex nature of traffic crashes, which involve intricate interactions among human behavior, vehicle dynamics, roadway characteristics, and environmental conditions. [Human factors](https://www.sciencedirect.com/topics/engineering/ergonomics) such as variation in attention, aggressiveness, and responsibility, combined with complex vehicle-environment interactions, create a multifaceted problem requiring a holistic approach.

Traditionally, traffic safety research has focused on understanding causality through [observational data](https://www.sciencedirect.com/topics/computer-science/observational-data) (), employing statistical and [econometric](https://www.sciencedirect.com/topics/social-sciences/econometrics) methods to identify relationships between factors and crash outcomes (,,,,, ). This approach [faces](https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/face) two key challenges: functional form constraints and distributional assumptions, leading to inconsistent results across datasets and confounding effects that result in incomplete understanding of influencing factors. Various models have been proposed to mitigate these issues, including random parameters [multinomial logit models](https://www.sciencedirect.com/topics/computer-science/multinomial-logit-model) (,,, ), random parameters ordered probability models (, ), and [latent class models](https://www.sciencedirect.com/topics/social-sciences/latent-class-model) (, ). A comprehensive overview of such models can be found in. However, designing a causal structure and properly considering potential confounding effects requires substantial domain knowledge but also introduces subjectivity.

While causality remains central to traffic safety research, [predictive modeling](https://www.sciencedirect.com/topics/pharmacology-toxicology-and-pharmaceutical-science/predictive-modeling) has gained prominence with the emergence of modern [machine learning methods](https://www.sciencedirect.com/topics/engineering/machine-learning-method). These approaches demonstrate superior [predictive power](https://www.sciencedirect.com/topics/computer-science/predictive-power), particularly for large datasets, leading to practical applications in predictive crash modeling. Recent advancements in explainable [artificial intelligence](https://www.sciencedirect.com/topics/computer-science/artificial-intelligence) (XAI) (, ), including perturbation-based methods (), local interpretable model-agnostic explanations (LIME) (), [SHapley Additive exPlanations](https://www.sciencedirect.com/topics/computer-science/shapley-additive-explanation) (SHAP) (), and attention heatmmaps () have enhanced [interpretability](https://www.sciencedirect.com/topics/computer-science/interpretability) of [machine learning](https://www.sciencedirect.com/topics/computer-science/machine-learning) methods (,,, ). Additionally, causal artificial intelligence approaches are emerging in traffic safety modeling (,,, ). Recent study () has shown not only the prediction capability but also the interpretability of tabular transformer with semantic grouped data using attention heatmap analysis for traffic crash modeling.

Previous research in traffic safety modeling has predominantly relied on structured tabular crash data. While this format supports efficient record-keeping, it fails to capture richer semantic [information embedded](https://www.sciencedirect.com/topics/computer-science/embedded-information) in textual descriptions of crash events found in police reports. Recent advances in [natural language processing](https://www.sciencedirect.com/topics/engineering/natural-language-processing) (NLP), particularly [representation learning](https://www.sciencedirect.com/topics/computer-science/representation-learning) techniques via pre-training of large transformer-based models on massive corpora (,, ), offer promising solutions to this limitation by effectively compressing textual data while preserving its [semantic context](https://www.sciencedirect.com/topics/social-sciences/semantic-context).

Motivated by this gap, our research addresses the following questions:
- 1.
	Can tabular crash data be augmented to textual [narratives](https://www.sciencedirect.com/topics/social-sciences/narrative) that can leverage pre-trained [Large Language Models](https://www.sciencedirect.com/topics/social-sciences/large-language-model) (LLMs) to incorporate existing [human knowledge](https://www.sciencedirect.com/topics/computer-science/human-knowledge)?
- 2.
	How can tabular data and textual narratives be synergistically combined in crash modeling?
- 3.
	Does the inclusion of textual narratives improve model performance?

To answer these questions, we propose Tab-Text: a data-centric multi-modal paradigm that integrates tabular data with augmented textual narratives for crash severity modeling. Our “data-centric” approach emphasizes enriching and transforming the data itself, rather than focusing on model architecture. The “multi-modal” refers to combination of conventional tabular crash data and constructed textual narratives within the modeling process.

For evaluation, we compare Tab-Text with four [baseline models](https://www.sciencedirect.com/topics/computer-science/baseline-model) including: 1) CatBoost tree ensemble model trained with only tabular data; 2) T2T-Transformer trained with only generated textual narratives; 3) AT-Transformer trained with directly textualized tabular data; and 4) a classic Multinominal logit model (MNL). Model performance is assessed using Victoria crash data from Australia, with a focus on crash severity prediction framed as a multi-class [classification task](https://www.sciencedirect.com/topics/computer-science/classification-task).

The key contributions of our study are as follows:
- 1.
	Pioneering LLM use in traffic safety: This study represents one of the early explorations on how LLMs can enhance traffic safety inference by leveraging textual narratives constructed from tabular data.
- 2.
	Introduction of Tab-Text: We propose a novel multi-modal paradigm that effectively integrates traditional tabular crash data with semantic insights derived from constructed textual narratives using pre-trained LLMs.
- 3.
	Improved accuracy in severity inference: Our results demonstrate that incorporating generated textual narratives improves the accuracy of inferring fatal and serious crashes.
- 4.
	Consistent identification of key factors: Permutation importance analysis shows that Tab-Text identifies and ranks key influential factors in a manner consistent with those revealed by classic multinomial logit models.

## 2\. Literature reviews

This section provides a comprehensive literature review focusing on two main perspectives: the application of [machine learning techniques](https://www.sciencedirect.com/topics/engineering/machine-learning-technique) and the integration of [natural language processing](https://www.sciencedirect.com/topics/computer-science/natural-language-processing) methods in traffic safety research. Together, these perspectives offer a broader understanding of the context and rationale for our study.

### 2.1. Machine learning in traffic safety prediction

Early studies in traffic safety research explored [machine learning algorithms](https://www.sciencedirect.com/topics/engineering/machine-learning-algorithm), primarily focusing on comparative assessments against traditional statistical models. Hassan and Mohamed () investigated the use of Multi-Layer [Perceptron](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/self-organizing-systems) (MLP) and fuzzy adaptive resonance theory [neural networks](https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/neural-network) to predict driver [injury](https://www.sciencedirect.com/topics/pharmacology-toxicology-and-pharmaceutical-science/injury) [severity levels](https://www.sciencedirect.com/topics/engineering/severity-level) at signalized intersections. Their results showed that the MLP model outperformed the traditional ordered logit model, achieving improved accuracies of 6.7 % and 3.3 % on the training set and the validation set, respectively.

developed an SVM model for predicting [injury severity](https://www.sciencedirect.com/topics/pharmacology-toxicology-and-pharmaceutical-science/injury-severity) in individual crashes and compared its performance against a baseline ordered probit model. The SVM model demonstrated 4.8 % increase in overall accuracy, with notable improvements in minority classes such as incapacitating injury (2.3 %) and fatal injury (1.7 %), while maintaining comparable effectiveness in evaluating [explanatory variables](https://www.sciencedirect.com/topics/computer-science/explanatory-variable). Expanding the application of SVM, utilized this approach with a set of screened important variables to assess driver injury severity in rollover crashes in New [Mexico](https://www.sciencedirect.com/topics/social-sciences/mexico). They conducted variable screening process using a Classification and Regression Tree (CART) model and employed pseudo-elasticity analysis to demonstrate the influence of variables on injury outcomes.

More recently, tree-based algorithms, particularly tree ensembles (), have proven highly effective in traffic safety analysis due to their capacity to model non-linear relationships and handle [categorical variables](https://www.sciencedirect.com/topics/computer-science/categorical-variable). were among the first to apply CART for predicting traffic injury severity, incorporating variables related to drivers, environment, crash circumstances, and vehicles. Their study underscored CART’s potential as a robust tool for [predictive modeling](https://www.sciencedirect.com/topics/pharmacology-toxicology-and-pharmaceutical-science/predictive-modeling) and analysis. As [decision tree](https://www.sciencedirect.com/topics/computer-science/decision-trees) methods evolved, researchers began evaluating their performance against other techniques. assessed several models for classifying injury severity levels, including [Logistic Regression](https://www.sciencedirect.com/topics/computer-science/logistic-regression), Decision Trees, Neural Networks, [Gradient Boosting](https://www.sciencedirect.com/topics/computer-science/gradient-boosting) Models, and Naïve [Bayes classifiers](https://www.sciencedirect.com/topics/computer-science/bayes-classifier). They reported the highest classification performance using a bagging ensemble of decision trees, particularly when combined with over-sampling to address [class imbalance](https://www.sciencedirect.com/topics/computer-science/class-imbalance). Further advancing tree-based methods, introduced a hybrid algorithm based on the Light Gradient Boosting Tree, which outperformed other [machine learning algorithms](https://www.sciencedirect.com/topics/computer-science/machine-learning-algorithm) across multiple [evaluation metrics](https://www.sciencedirect.com/topics/computer-science/evaluation-metric). Similarly, found that the [Random Forest](https://www.sciencedirect.com/topics/computer-science/random-decision-forest) algorithm delivered superior accuracy in predicting traffic crash severity compared to Logistic Regression, Naive Bayes, and [AdaBoost](https://www.sciencedirect.com/topics/engineering/adaboost).

With the emergence of [deep learning techniques](https://www.sciencedirect.com/topics/computer-science/deep-learning-technique), researchers began applying [Convolutional Neural Networks](https://www.sciencedirect.com/topics/computer-science/convolutional-neural-network) (CNNs) and [Recurrent Neural Networks](https://www.sciencedirect.com/topics/engineering/recurrent-neural-network) (RNNs) to traffic safety modeling. employed a Long Short-Term Memory (LSTM) model for predicting [traffic accident](https://www.sciencedirect.com/topics/engineering/highway-accidents) severity, demonstrating its superior performance compared to conventional MLP and Bayesian [Logistic Regression models](https://www.sciencedirect.com/topics/computer-science/logistic-regression-model). Taking a different approach, introduced the Traffic Accident Severity Prediction-CNN (TASP-CNN) to enhance prediction accuracy by considering combination relationships among accident features and utilizing the Feature Matrix to Gray Image algorithm. Their model outperformed nine [baseline methods](https://www.sciencedirect.com/topics/computer-science/baseline-method), particularly excelling in predicting fatal crashes. Building on CNN-based methods, implemented a 2-D [CNN model](https://www.sciencedirect.com/topics/computer-science/neural-network-model) for crash severity prediction and introduced an innovative approach to interpreting factor influence by leveraging the model’s learned embedded representations rather than relying on conventional [SHAP](https://www.sciencedirect.com/topics/computer-science/shapley-additive-explanation) values.

The latest advancement in traffic safety modeling is the exploration of transformer-based architectures (). A recent study by introduced the Feature Group Tabular Transformer (FGTT), a novel approach that organizes traffic crash data into [semantic feature](https://www.sciencedirect.com/topics/computer-science/semantic-feature) groups, represented as tokens within a transformer framework. Their model leverages a comprehensive dataset fused from multiple sources including weather data, crash reports, traffic information, and pavement characteristics, enabling a more comprehensive and contextualized analysis of crash events. Evaluation results showed that FGTT outperformed traditional tree [ensemble methods](https://www.sciencedirect.com/topics/computer-science/ensemble-method) (Random Forest, [XGBoost](https://www.sciencedirect.com/topics/computer-science/extreme-gradient-boosting), and CatBoost) in predicting crash types. Furthermore, attention [weight analysis](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/weight-analysis) revealed that event-specific attributes and their interactions with driver-related features were most influential in determining crash outcomes. This work demonstrates the potential of transformer architectures to enhance both [predictive performance](https://www.sciencedirect.com/topics/computer-science/predictive-performance) and [interpretability](https://www.sciencedirect.com/topics/computer-science/interpretability) in traffic safety modeling.

In summary, recent studies have shown that [deep learning models](https://www.sciencedirect.com/topics/computer-science/deep-learning-model) not only outperform traditional methods in traffic safety modeling but also offer promising avenues for interpretability (, ). As the field continues to progress, [deep learning](https://www.sciencedirect.com/topics/chemical-engineering/deep-learning) models are expected to become more accurate, transparent and explainable.

### 2.2. Natural language model (NLP) in traffic safety

Narrative text has long served as a vital source of information in human society. The field of NLP, originally focused on enabling machines to understand human language, has evolved significantly since the 1950s, particularly in recent years, fueled by the emergence of the transformer architecture (). These advancements are now being increasingly applied to traffic safety research, opening new opportunities to extract valuable insights from textual data contained in crash reports.

Among the early endeavors, researchers utilized NLP techniques to classify crash types or severity based on crash reports (). employed diverse text mining [classification techniques](https://www.sciencedirect.com/topics/computer-science/classification-technique) to categorize 11 types of construction accidents. The evaluation involved uni-grams and bi-grams tokenization () with various machine learning algorithms, including SVM, linear regression, random forest, k-nearest neighbor, decision tree and Naive Bayes. Their results indicated linear and [radial basis function](https://www.sciencedirect.com/topics/engineering/radial-basis-function) SVMs with unigram tokenization as the most effective classifiers.

devised a framework to classify various pedestrian-related crash types from unstructured text, using diverse machine-learning models with bigrams such as random forest, SVM, and XGBoost. Notably, the XGBoost model outperformed others as the most effective classifier in classifying [pedestrian](https://www.sciencedirect.com/topics/social-sciences/pedestrian) crash types. Similarly, developed a text mining approach to improve the identification of secondary crashes from crash reports, transforming unstructured content into numeric vectors for machine learning. Their evaluation revealed that logistic regression, using a single-word representation of the narrative reports, produced the most accurate classification.

Researchers also applied NLP techniques to understand crash scenarios and severity levels. employed semantic analysis to ascertain the most probable crash scenarios at signal-controlled junctions for hazardous activities, considering driver maneuvers. Using unigram and bigram tokenization, SVM and boosted classification trees were trained to classify hazardous action citations such as “disregard traffic control” and “fail to yield,” helping to reason about crash events by detailing pre-crash scenarios. In a different context, used machine learning text mining to classify the severity levels of tree and utility pole crashes. They employed LIME () to assess crashes in Louisiana between 2010 and 2017, finding that the XGBoost model demonstrated superior prediction performance in severity modeling with narrative data. Expanding on interpretability aspects, introduced a novel approach combining machine learning and Global Cross-Validation LIME (GCV-LIME) to analyze crash [narratives](https://www.sciencedirect.com/topics/social-sciences/narrative) and identify factors contributing to injury severity in heavy vehicle accidents in Queensland, Australia. Their approach revealed significant associations between certain features and fatal outcomes, offering deeper insights compared to traditional regression analyses.

The aforementioned studies primarily utilized traditional NLP approaches. However, the field has been revolutionized by the emergence of the transformer architecture (), which introduced [attention mechanisms](https://www.sciencedirect.com/topics/computer-science/attention-machine-learning) that have dramatically improved performance across various language tasks (). This architecture has become the foundation for [Large Language Models](https://www.sciencedirect.com/topics/social-sciences/large-language-model) (LLMs), which represent a significant advancement in [natural language processing](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/natural-language-processing). These pre-trained models, characterized by their substantial parameter count from hundreds of millions to billions, can capture complex linguistic patterns, contextual relationships, and semantic nuances far more effectively than previous approaches.

The evolution of LLMs began with models like [BERT](https://www.sciencedirect.com/topics/social-sciences/bidirectional-encoder-representations-from-transformers) () and [GPT](https://www.sciencedirect.com/topics/pharmacology-toxicology-and-pharmaceutical-science/alanine-aminotransferase) (), which employ transformer architectures to process input sequences in parallel rather than sequentially. This [parallel processing](https://www.sciencedirect.com/topics/computer-science/parallel-processing) allows the models to capture long-range dependencies and contextual information more effectively. Pre-training is fundamental to these models; they learn general language representations by predicting masked words (BERT) or next words in a sequence (GPT), then can be fine-tuned on specific downstream tasks with relatively smaller labeled datasets.

In the context of analyzing complex textual data, LLMs offer several key advantages. First, they excel at understanding context and semantics beyond simple keyword matching. Second, they can identify subtle patterns and relationships within text that might escape human analysts. Third, they demonstrate impressive [transfer learning](https://www.sciencedirect.com/topics/engineering/transfer-learning) capabilities, allowing knowledge from one domain to be applied to another. These capabilities make LLMs particularly promising for traffic safety applications, where extracting meaningful insights from narrative crash reports requires understanding complex relationships, contextual factors, and semantic nuances that may not be explicitly encoded in structured data.

Despite these impressive capabilities and [potential applications](https://www.sciencedirect.com/topics/computer-science/potential-application), the use of Transformers and LLMs in traffic safety analysis remains largely unexplored. Among the few studies in this domain, developed a system utilizing [BERT](https://www.sciencedirect.com/topics/computer-science/bidirectional-encoder-representations-from-transformers) to detect pedal misapplication crashes from crash narratives. They validated the system’s accuracy through training and testing on dataset from North Carolina and the National Motor Vehicle Crash Causation Survey. However, their evaluation focused solely on a [binary classification](https://www.sciencedirect.com/topics/computer-science/binary-classification) model, providing limited insight into multi-class labeling capabilities for traffic safety applications. More recently, applied BERT to classify traffic crash severity using crash narrative reports from Louisiana, demonstrating the value of advanced language models in traffic safety analysis, although their study did not include comparisons with other baseline approaches.

It is noteworthy that much of the existing research deals exclusively with crash data recorded by police, which may result in information loss or the omission of certain aspects of crashes. For example, a numeric code (e.g., “7”) denoting a specific category of vehicle movement may actually represent ‘Overtaking’. In such cases, the natural language description of vehicle movement provides more meaningful context than the assigned numeric code.

In traffic safety analysis, effectively handling diverse features within tabular data is essential. While traditional approaches typically process categorical and numerical features separately, recent advancements in storage technology have enabled the integration of large textual datasets. This shift underscores the necessity of harnessing modern NLP techniques, especially in the context of evolving LLMs. The application of advanced NLP methods to textual features within tabular data, particularly for capturing nuanced semantic meanings, represents a promising yet relatively unexplored research area. In traffic safety, where structured tabular data predominates, this potential remains largely untapped. This presents an opportunity to harness the power of modern NLP methods to advance our understanding of dynamic interactions among various factors in traffic safety.

A particularly promising avenue involves conducting multi-modal analyses, integrating textual accident narratives with conventional structured crash data. This integration has the potential to enhance precision in risk assessments, support proactive accident [prevention strategies](https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/prevention-strategies), and optimize [resource allocation](https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/resource-allocation) for emergency services. Contemporary NLP techniques can extract semantic nuances from accident narratives and facilitate their fusion with structured [quantitative data](https://www.sciencedirect.com/topics/computer-science/quantitative-data), thereby enriching insights into traffic safety dynamics.

In conclusion, while the application of [modern language](https://www.sciencedirect.com/topics/social-sciences/modern-languages) modeling architectures within traffic safety analysis, particularly for integrating tabular data with textual narratives, remains limited, it represents an exciting research frontier for innovation. The strategic deployment of contemporary NLP techniques will enable effective integration of diverse [data sources](https://www.sciencedirect.com/topics/engineering/data-source), leading to the development of data-centric modeling frameworks for enhanced traffic safety understanding and prediction.

## 3\. Methods

This section delves into the details of the proposed method and the comparison baselines. We begin with a brief overview of the transformer-based [backbone](https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/spine), ELECTRA (Efficiently Learning an Encoder that Classifies Token Replacements Accurately) () model, which is selected for narrative embedding in the proposed Tab-Text and baselines (AT-transformer, T2T-transformer) due to its remarkable balance between efficiency and performance. While various transformer-based encoders are available, ELECTRA was selected as a representative example for demonstrating our framework. Next, we present the proposed Tab-Text model, followed by a detailed discussion of the [baseline models](https://www.sciencedirect.com/topics/computer-science/baseline-model) constructed for comparison to evaluate the performance and the efficacy of our Tab-Text model.

### 3.1. Transformer-based backbone: ELECTRA

ELECTRA () represents an innovative approach to self-supervised language [representation learning](https://www.sciencedirect.com/topics/computer-science/representation-learning). It offers the capability to pre-train transformer networks with relatively lower computational demands compared to [BERT](https://www.sciencedirect.com/topics/social-sciences/bidirectional-encoder-representations-from-transformers) (). Similar to the [discriminator](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/discriminator) of a [generative adversarial network](https://www.sciencedirect.com/topics/computer-science/generative-adversarial-networks) (), ELECTRA models are trained to perform a replaced token detection task, that is to distinguish between “real” input tokens and “fake” input tokens generated by another [neural network](https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/neural-network), as illustrated in. This unique training objective, focusing on detecting replaced tokens, leads to robust representation, beneficial for the nuanced understanding required in traffic safety domain.

![Fig. 1](https://ars.els-cdn.com/content/image/1-s2.0-S095741742502069X-gr1.jpg)

Download: Download high-res image (131KB)

The ELECTRA model is the [discriminator](https://www.sciencedirect.com/topics/engineering/discriminator) part of the framework. The pipeline of the ELECTRA application involves retaining the [discriminator](https://www.sciencedirect.com/topics/computer-science/discriminator), i.e., ELECTRA, and fine-tuning it on the target downstream text dataset. The generator, a small masked [language model](https://www.sciencedirect.com/topics/social-sciences/language-modeling), is trained concurrently with the discriminator. Despite the structural resemblance to a generative adversarial network, it is important to note that the generator in ELECTRA is trained using [maximum likelihood](https://www.sciencedirect.com/topics/computer-science/maximum-likelihood) rather than through an adversarial process.

Usually, the Generator G and Discriminator D are both transformer-based networks, each mapping a sequence of input tokens into a sequence of contextualized [vector representations](https://www.sciencedirect.com/topics/engineering/representation-vector). For a given position t, the generator outputs a probability for generating a particular token $X_{t}$ with a softmax layer:(1) $P_{G} \left(\right. x_{t} \left|\right. \mathbf{x} \left.\right) & = & e x p \left(\right. e \left(\left(\right. x_{t} \left.\right)\right)^{T} h_{G} \left(\left(\right. \mathbf{x} \left.\right)\right)_{t} \left.\right) / \underset{x^{'}}{\sum} e x p \left(\right. e \left(\left(\right. x^{'} \left.\right)\right)^{T} h_{G} \left(\left(\right. \mathbf{x} \left.\right)\right)_{t} \left.\right)$ where e denotes token embeddings. For a given position t, the discriminator predicts whether the token $X_{t}$ is “real,” with a sigmoid output layer:(2) $D \left(\right. \mathbf{x}_{t} , t \left.\right) = s i g m o i d \left(\right. w^{T} h_{D} \left(\right. \mathbf{x}_{t} \left.\right) \left.\right)$ The generator is still trained to predict the original identities of masked tokens, which is classic masked language modeling while the discriminator is trained to distinguish tokens in the data from tokens that have been replaced by generator samples. The loss function for ELECTRA, the discriminator, is:(3) $L \left(\right. x , \theta_{D} \left.\right) & = E \left(\right. \sum_{t = 1}^{n} - 1 \left(\right. x_{t}^{c o r r u p t e d} = x_{t} \left.\right) l o g D \left(\right. x^{c o r r u p t e d} , t \left.\right) \\ - 1 \left(\right. x_{t}^{c o r r u p t e d} \neq x_{t} \left.\right) l o g \left(\right. 1 - D \left(\right. x^{c o r r u p t e d} , t \left.\right) \left.\right) \left.\right)$ $x^{c o r r u p t}$ is a corrupted example by replacing the masked-out tokens with generator samples. The ELECTRA is trained to predict which tokens in $x^{c o r r u p t}$ match the original input $x$.

### 3.2. Tab-Text: a multi-modal paradigm for traffic safety modeling

In this paper, multi-modal tabular data refers to structured tabular data, including categorical, numerical, and textual fields, distingushing it from conventiobnal tabular data in the traffic safety studies, which typically contains only categorical and numerical attributes. However, even in traditional tabular datasets, [categorical variables](https://www.sciencedirect.com/topics/computer-science/categorical-variable) often represent information through string values, which contain a layer of textual context. As an illustrative example, consider the variable “ROAD\_GEOMETRY”, which denotes road geometry at traffic incident locations with 9 categories, including 0: “Not at the intersection”, 1: “T intersection”, 2: “Cross intersection”, 3: “Multiple intersections”, 4: “Y intersection”, 5: “Dead end”, 6: “Private property”, 7: “Road closure”, and 99: “Unknown”. While these are usually treated as discrete structured categories, encoding them as dummy or one-hot vectors discards valuable [information embedded](https://www.sciencedirect.com/topics/computer-science/embedded-information) in the string values. Intuitively, besides the classic numeric treatment of these categorical variables, retaining their meanings through the language embedding of tokenized textual features could be beneficial for safety modeling.

To maximize the utility of information present in [categorical data](https://www.sciencedirect.com/topics/computer-science/categorical-data), particularly the linguistic content within string categories, we introduce a pre-defined template to convert structured tabular data to cohesive textual narratives. This uncomplicated yet powerful technique aggregates tabular data to generate contextualized narrative passages, enabling semantic encoding by pre-trained LLMs. Leveraging this semantically rich encoding is expected to further enhance model performance.

#### 3.2.1. Textual narrative generation

To transform structured tabular data into coherent, informative textual narratives, we built a simple yet effective template to perform translation into detailed, human-readable narratives, encapsulating vital information about [traffic accidents](https://www.sciencedirect.com/topics/engineering/highway-accidents), as depicted in. Initially, the process takes tabular data as input, where each row presents an individual record containing fields such as accident data, day of the week etc. A predefined template with placeholders for these fields is then applied to convert each row into a coherent textual narrative. For example, for field “DAY\_OF\_WEEK”, the field domain is 1–7, we transformed the numbers to corresponding description (Monday, Tuesday,..., Sunday) based on the metadata description in VicRoads ().

![Fig. 2](https://ars.els-cdn.com/content/image/1-s2.0-S095741742502069X-gr2.jpg)

Download: Download high-res image (490KB)

The constructed textual narratives allow us to unlock the capabilities of pre-trained LLMs, enabling a nuanced understanding of each incident. The [primary objective](https://www.sciencedirect.com/topics/computer-science/primary-objective) is to augment applicability and relevance of tabular data as suitable input for pre-trained LLMs, facilitating more context-aware inference for tasks like accident severity assessment. Additionally, traffic safety engineers can supplement it with established facts or domain-specific knowledge to further enrich the understanding. For instance, “Children and [elders](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/elderly-age-groups) are typically more vulnerable in accidents without seat belts.” However, it is important to note that, for this study, we do not delve into the intricate design of [scientific knowledge](https://www.sciencedirect.com/topics/computer-science/scientific-knowledge) in the template. In other words, the narratives are generated based on the facts captured in the original tabular data.

#### 3.2.2. Model architecture

Our proposed pipeline processes original categorical data, numeric data, and the textual narratives constructed from tabular data, treating them collectively as multi-modal data. With this data multi-modality, the question is how to design an end-to-end [deep learning](https://www.sciencedirect.com/topics/chemical-engineering/deep-learning) paradigm that is capable of concurrently learning latent knowledge from different modalities (Textual, Categorical, and Numerical), ensuring optimal information retention. To address this question, we proposed Tab-Text, a multi-modal paradigm, depicted in, where, ’Cat’ denotes the categorical features, and ’Num’ denotes the numerical features. We employ pre-trained transformers to encode textual features, while [MLP](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/self-organizing-systems) are used to handle categorical and numerical features. The crux for achieving [optimal performance](https://www.sciencedirect.com/topics/engineering/optimal-performance) with multi-modal traffic tabular data lies in modeling traditional tabular and textual data in an end-to-end fashion, enabling fine-tuning different parts with various data modes. This approach could serve as a promising foundation for handling traffic tabular data with string information in the context of traffic safety. In this framework, the fine-tuning process for pre-trained Transformers, such as ELECTRA, involves contextual categorical and numerical tabular information. This stands in contrast to a simple fine-tuning process that only considers text data. Further evidence supporting this distinction can be observed through a comparison of T2T-Transformer and Tab-Text, which is discussed in the Experiments section.

![Fig. 3](https://ars.els-cdn.com/content/image/1-s2.0-S095741742502069X-gr3.jpg)

Download: Download high-res image (495KB)

In this paper, the multi-modal paradigm is specifically designed for predicting traffic crash [severity levels](https://www.sciencedirect.com/topics/engineering/severity-level). Firstly, the original crash tabular data is augmented with built cohesive textual narratives. This narrative, treated as an additional textual column, is then integrated with the original tabular data, forming the multi-modal tabular dataset. Subsequently, the Tab-Text paradigm is executed on this multi-modal tabular data. In this paradigm, one branch consists of a pre-trained Transformer network dedicated to processing the textual narrative, while other branches invovle MLPs responsible for handling numeric and categorical inputs. The higher-level vector representations from each branch are aggregated into a unified multi-modal vector representation through concatenation.

For the generated textual narrative, we feed the embedded textual narratives into a pre-trained Transformer to get intermediate representation. The embedded textual narratives are obtained by the addition of elements of token embedding, and [position embedding](https://www.sciencedirect.com/topics/computer-science/embedding-position). For the token embedding, we use ElectraTokenizer to tokenize the textual narratives built. Then the \[CLS\] token is added in front of the textual narrative example, which is the typical setting in encoder-only language models (). Since self-attention functions in a permutation-equivalent manner, we include an additional vector for encoding positional information, known as positional embedding. This enables the transformer model to distinguish between identical tokens that may appear at different positions within the input text, as described in. Each token is associated with an embedding that incorporates contextual information from surrounding tokens. In instances where the cumulative length of tokenized text fields exceeds the predefined maximum limit of 512, we implement a truncation strategy. This approach involves systematically removing one token at a time from the tokenized textual narrative field until the specified length restriction is satisfied. The representation for the textual narrative in the multi-modal tabular data, which is a single embedding vector with dimension $D =$ 768, is \[CLS\] representation obtained () after feeding the embedded textual narrative into the pre-trained Transformer. In this setting, we evaluated pre-trained transformers, ELECTRA (), in their [base](https://www.sciencedirect.com/topics/pharmacology-toxicology-and-pharmaceutical-science/base) versions featuring 12 layers of transformer encoder blocks.

Meanwhile, we used a single-hidden-layer [MLP](https://www.sciencedirect.com/topics/engineering/perceptron) as the [basic building block](https://www.sciencedirect.com/topics/computer-science/basic-building-block) for encoding categorical and numerical features and projecting the hidden states. This [MLP](https://www.sciencedirect.com/topics/chemical-engineering/multilayer-neural-networks) comprises one bottleneck layer and uses layer normalization. A leaky ReLU activation with a slope set to 0.1 is employed for all basic [MLP](https://www.sciencedirect.com/topics/computer-science/multilayer-perceptron) layers. For the categorical features, we utilize factorized embedding () to initially embed the one-hot encoded categorical features. This involves an embedding layer with 32 units, followed by projection with a basic MLP layer comprising 64 bottleneck units. Subsequently, we concatenate all the embedded categorical features and encode them using a second MLP layer. This layer has 128 bottleneck units and the output unit number matches the dimensionality of output embedding of the pre-trained ELECTRA, which is 768 dimension. Numeric features undergo max-min normalization before being concatenated and encoded with a basic MLP layer. The MLP for encoding the numerical features mirrors the second MLP layer used for the embedded categorical features. The topmost vector representation is the concatenation of embeddings of all three heads, from which predictions are generated through two dense layers.

### 3.3. Baseline models

#### 3.3.1. Multinominal logit model (MNL)

The MNL model, a prevalent statistical method in traffic accident severity modeling, offers a robust framework for examining the factors influencing accident severity outcomes. Rooted in random utility maximization theory, the MNL model assumes that the probability of a particular accident severity level is a function of observed characteristics and unobserved factors.

Given a set of accident severity outcomes $Y = \left{\right. 1 , 2 , \ldots , j \left.\right}$ for an accident $i$, where $j = 3$ and $Y = 1$ represents minor [injury](https://www.sciencedirect.com/topics/pharmacology-toxicology-and-pharmaceutical-science/injury) accidents, $Y = 2$ represents serious accidents while $Y = 3$ represents fatal accidents, the utility $U_{i j}$ that accident $i$ derives from choosing severity level $j$ can be expressed as:(4) $U_{i j} = X_{i} \beta_{j} + \epsilon_{i j}$ where $X_{i}$ is a vector of observed variables related to the accident, $\beta_{j}$ is a vector of coefficients to be estimated for each severity level $j$, and $\epsilon_{i j}$ is the [error term](https://www.sciencedirect.com/topics/engineering/error-term), capturing the unobserved factors affecting the utility of each severity level.

The probability $P_{i j}$ that an accident $i$ results in severity level $j$ is given by the [softmax function](https://www.sciencedirect.com/topics/computer-science/softmax-function):(5) $P_{i j} = \frac{e^{X_{i} \beta_{j}}}{\sum_{k = 1}^{J} e^{X_{i} \beta_{k}}}$ where the denominator ensures that the probabilities across all $J$ outcomes sum to one.

The model parameters $\beta_{j}$ are estimated using [maximum likelihood estimation](https://www.sciencedirect.com/topics/engineering/maximum-likelihood-estimation) (MLE), optimizing the likelihood function:(6) $L \left(\right. \beta \left.\right) = \prod_{i = 1}^{N} \prod_{j = 1}^{J} P_{i j}^{y_{i j}}$ where $y_{i j}$ is an indicator variable that equals 1 if accident $i$ results in severity level $j$ and 0 otherwise, and $N$ is the total number of accidents.

In applying the MNL model to accident severity analysis, we categorize accident severity into three discrete levels as minor injury, serious, and fatal accidents. In this paper, the MNL baseline is evaluated as an epitomic example of classic statistical models for comparison with the tree model CatBoost and transformer-based models. The MNL model is estimated using the training dataset. Its inference performance on severity classification is assessed by applying the estimated model to the [testing dataset](https://www.sciencedirect.com/topics/engineering/testing-dataset). Additionally, it is utilized to further interpret the proposed Tab-Text model by comparing the identified influential variables and their importance.

#### 3.3.2. CatBoost

CatBoost () or Categorical Boosting, is a gradient-boosting algorithm designed specifically to handle categorical data through target statistics, coupled with ordered boosting to avoid target leakage in subsequent boosting. CatBoost stands out among popular boosted tree algorithms like [AdaBoost](https://www.sciencedirect.com/topics/engineering/adaboost) (), [XGBoost](https://www.sciencedirect.com/topics/computer-science/extreme-gradient-boosting) (), LightGBM (). In the context of traffic safety tabular data, where variables like weather and [situational factors](https://www.sciencedirect.com/topics/computer-science/situational-factor) are categorical in nature, which makes CatBoost a well-suited choice for traffic accident severity inference. The hyperparameters are tuned by the grid search method.

#### 3.3.3. T2T-transformer and AT-transformer

To evaluate the performance of the proposed Tab-Text, we also introduce a single-modal transformer model, named tabular-to-text-Transformer (T2T-Transformer) as shows, which uses only textual narrative input to demonstrate the effectiveness of the multi-modal approach. The T2T-Transformer involves fine-tuning a pre-trained Transformer using textual narratives constructed from the original crash tabular categorical and [numerical data](https://www.sciencedirect.com/topics/computer-science/numerical-data), following a simple yet effective template detailed in. Similar to the textual head in Tab-Text, the T2T-Transformer feeds the embedded textual narratives into the ELECTRA (). These embedded narratives are the sum of token embedding and position embedding, as in Tab-Text. The embedded input is then processed by ELECTRA and subsequently passed through two dense layers to infer the crash severity outcome.

![Fig. 4](https://ars.els-cdn.com/content/image/1-s2.0-S095741742502069X-gr4.jpg)

Download: Download high-res image (318KB)

Another straightforward approach to leverage pre-trained Transformers with tabular data is to directly transform categorical and numeric fields into strings, treating them as textual fields in a process known as textualization. We propose the AT-Transformer, as depicted in, to represent this setting and compare it with the T2T-Transformer. The key difference between these two models lies in their input: the T2T-transformer use constructed textual narratives, while the AT-Transformer directly uses textualized tabular data. To process tabular data, we first convert all categorical variables into strings, treating each category as a separate text field. For [numerical values](https://www.sciencedirect.com/topics/computer-science/numerical-value), we round them to three significant digits in their string representations. It should be noted that the categorical and numerical fields are also grouped similarly to the constructed textual narratives. After converting categorical fields, denoted as $\left(C a t\right)_{1} , \ldots , C a t_{n}$, and numerical fields, denoted as $N u m_{1} , \ldots , N u m_{p}$, into text, we encode them using a combination of token embedding, segmentation embedding, and position embedding. Token embedding are created by tokenizing the inputs from different fields, merging them with special \[SEP\] delimiter tokens between fields, and adding a \[CLS\] prefix token at the beginning of the merged input. Segmentation embedding uses alternating 0s and 1s as segment IDs to clearly differentiate the boundaries between adjacent fields. The encoded vectors are then fed into the ELECTRA model, followed by two dense layers to infer crash severity outcome. Intuitively, the coherent textual narratives should perform better than directly textulized tabular data. We are interested in comparing these approaches to determine whether the proposed template for constructing textual narrative plays an important role in the process.

![Fig. 5](https://ars.els-cdn.com/content/image/1-s2.0-S095741742502069X-gr5.jpg)

Download: Download high-res image (263KB)

## 4\. Dataset and experimental settings

In this section, we first discuss the dataset employed for the study. Next, we demonstrate the textual narratives built with our pre-defined template applied to crash tabular data. Subsequently, we discuss our experimental settings, including [data partition](https://www.sciencedirect.com/topics/computer-science/data-partition) and [evaluation metrics](https://www.sciencedirect.com/topics/computer-science/evaluation-metric).

### 4.1. Dataset

Our empirical analysis utilizes data sourced from CrashStats data from Victoria, Australia spanning from 2006 to 2020. This dataset includes information reported by Victorian police officers for crashes involving at least one motor vehicle traveling on a roadway and resulting in crashes, which are then compiled by VicRoads, a statutory body responsible for road transport in the state of Victoria. The crash database has a record of vehicles involved in crashes. A four-point [ordinal scale](https://www.sciencedirect.com/topics/engineering/ordinal-scale) is used in the database to represent the severity or seriousness of the accident: (1) non-injury accident, (2) other injury (minor injury) accident, (3) serious injury accident, and (4) fatal accident. In this dataset, each sample denotes a vehicle involved in a crash with driver’s information.

This study focuses on the severity of accidents, which are categorized as single-vehicle crash or multi-vehicle crash. The original dataset contains several separate files for describing different variables such as time, location, accident characteristics, driver, vehicle, and [situational factors](https://www.sciencedirect.com/topics/engineering/situational-factor). We did the file concatenation based on the accident number (ACCIDENT\_NO), which is a unique value for each accident. After removing samples with [missing information](https://www.sciencedirect.com/topics/computer-science/missing-information) for essential attributes, the dataset contains 292,110 samples, including 4 non-injury accidents (0.001 %), 197,421 other (minor) injury accidents (67.584 %), 89,925 serious accidents (30.785 %), and 4760 fatal accidents (1.630 %). The final dataset has an extremely low representation of non-injury accidents, accounting for less than 0.001 %. Consequently, the 4 non-injury accidents have been excluded from the current analysis. The [data distribution](https://www.sciencedirect.com/topics/computer-science/data-distribution) is shown in. It should be noted that we understand the imbalance of the data could influence the performance of the built model. However, the imbalance issue is not a focus of this study. Possible upsampling and downsampling methods could improve the performance combined with our proposed methods ().

![Fig. 6](https://ars.els-cdn.com/content/image/1-s2.0-S095741742502069X-gr6.jpg)

Download: Download high-res image (88KB)

The traffic accident attributes considered in our empirical study can be grouped into six categories: crash characteristics, driver characteristics, vehicle characteristics, roadway attributes, environmental factors, and [situational factors](https://www.sciencedirect.com/topics/computer-science/situational-factor). The detailed description of each attribute can be checked in. Among all the variables, apart from the variables “SUB\_DCA\_SEQ”, “NO\_PERSONS”, “TOTAL\_NO\_OCCUPANTS”, “VEHICLE\_AGE”, “VEHICLE\_WEIGHT”, “NO\_OF\_WHEELS”, and “SEATING\_CAPACITY” are numerical variables, all other variables are categorical variables with string fields, corresponding to the notation “Cat” and “Num” in. We listed the detailed ACCIDENT\_TYPE, EVENT\_TYPE, Definition for Classifying Accidents (DCA), and SUB\_DCA in the appendix.

Table 1. Traffic accident attributes.

| Variables | Description |
| --- | --- |
| **Crash characteristics** |  |
| ACCIDENT\_TYPE | The type of accident. |
| EVENT\_TYPE | Type of incident event. |
| VEHICLE\_1\_COLL\_PT | Collision point on the first vehicle involved in the event. |
| VEHICLE\_2\_COLL\_PT | Collision point on the second vehicle involved in the event. |
| OBJECT\_TYPE | Object involved in the specific accident event. |
| DCA | The definitions for classifying accidents. |
| ACCIDENT\_MONTH | The month in which the accident occurred, derived from “ACCIDENT\_DATE”. |
| TIME\_PERIOD | The period the accident occurred, derived from “ACCIDENT\_TIME”. |
| DAY\_OF\_WEEK | The day of the week the accident occurred. |
| LGA\_NAME | The name of local government areas. |
| REGION\_NAME | The region where the accident occurred. |
| DEG\_URBAN\_NAME | The type of urbanized area for the crash site. |
| **Driver characteristics** |  |
| DRIVER\_SEX | The sex of the driver. |
| AGE\_GROUP | The age group of the driver, derived from “DRIVER\_AGE”. |
| ROAD\_USER\_TYPE | The role of the person was at the time of the accident. |
| **Vehicle characteristics** |  |
| VEHICLE\_TYPE | The type or category of vehicle. |
| VEHICLE\_WEIGHT | The weight or mass of the vehicle. The unit of measurement is kilograms. |
| NO\_OF\_WHEELS | The number of wheels that the vehicle has. |
| SEATING\_CAPACITY | The number of seats in the vehicle. |
| FUEL\_TYPE | The type of fuel used by the vehicle. |
| VEHICLE\_AGE | The age of the vehicle when the accident occurred. |
| VEHICLE\_BODY\_STYLE | The body type of the vehicle. |
| TRAILER\_TYPE | The type of trailer towed by the vehicle involved in the accident. |
| **Roadway attributes** |  |
| ROAD\_TYPE | Type of the highest priority road at the intersection or the road the accident occurred. |
| ROAD\_GEOMETRY | The layout of the road where the accident occurred. |
| SPEED\_ZONE | The speed zone at the location of the accident. |
| ROAD\_SURFACE\_TYPE | The type of road surface: 1: Paved 2: Unpaved 3: Gravel 9: Not known. |
| ROAD\_TYPE\_INT | The type or suffix of the intersecting road. |
| COMPLEX\_INT\_NO | Whether or not the segment is part of a complex intersection. |
| **Environmental factors** |  |
| LIGHT\_CONDITION | The light condition or level of brightness at the time of the accident. |
| SURFACE\_COND | Road surface condition: dry, wet, muddy, snowy, icy, unknown. |
| SURFACE\_COND\_SEQ | Starts with 1 and incremented by 1 if more than one road surface condition. |
| ATMOSPH\_COND | Atmospheric condition. |
| ATMOSPH\_COND\_SEQ | 1 and incremented by 1 if more than one atmospheric condition is entered. |
| **Situational factors** |  |
| HELMET\_BELT\_WORN | Whether or not the person was wearing a helmet or seatbelt at the time of the accident |
| NO\_OF\_VEHICLES | The number of vehicles involved in the accident. |
| LAMPS | Whether the lamps or headlights for the vehicle were alight (on). |
| VEHICLE\_MOVEMENT | The actual movement of the vehicle before the accident. |
| TRAFFIC\_CONTROL | The type of traffic control measure in the location where the accident occurred. |
| NO\_PERSONS | The number of people involved in the accident. |
| NO\_OCCUPANTS | The number of occupants or people in the vehicle at the time of the accident. |
| SUB\_DCA | SUB\_DCA code and description of the accident. |
| SUB\_DCA\_SEQ | Starts with 1 and is incremented by 1 if more than one sub\_dca is entered. |
| DRIVER\_INTENT | The intent of the driver initially. |

### 4.2. Textual narrative generated

For each sample in the dataset, we use a predefined template to build a descriptive narrative to be consumed by pretrained LLMs, as detailed in. This constructed narrative can be seen as one special feature column in the augmented traffic crash data. The token length distribution of all the constructed narratives is shown in. One example of our constructed textual narrative is demonstrated below:

![Fig. 7](https://ars.els-cdn.com/content/image/1-s2.0-S095741742502069X-gr7.jpg)

Download: Download high-res image (213KB)

“On 25/01/2006, Wednesday, early morning, an accident occurred on a clear day with streetlights on. The lamp or headlights for the vehicle were on. The road surface was dry. The accident type was Collision with vehicle, involving 2 vehicles. The [collision point](https://www.sciencedirect.com/topics/engineering/collision-point) of the primary vehicle involved in the crash is front while the second vehicle is front. It happened at an intersection with a paved road surface. The speed zone for the location was 80 km/h with stop-go lights in place. The event type for the crash is collision, and the object involved in the accident is Not Applicable. The DCA code for this accident is Vehicles from adjacent directions(intersection only)(113) under RIGHT NEAR (INTERSECTIONS ONLY). The accident involved 2 individuals, with 1 occupant in the primary vehicle. The driver is a male aged 30. The driver was wearing a seatbelt. The driver was not driving an oversize or over-mass large vehicle. It did happen at a complex intersection. Prior to the accident, the driver was trying to turn right. The vehicle was turning right. The vehicle, 10 years old, was a car running on gasoline. It weighed 1235 kg, and had 4 wheels. The vehicle had 5 seats with a body style of ‘Sedan - Car with external boot’. The accident occurred in GEELONG, within the SOUTH WESTERN region in an area described as LARGE\_PROVINCIAL\_CITIES. The sub-DCA code description is Not Required.”

### 4.3. Experiments setting

All text $/$ multi-modal neural networks are trained with a slanted triangular [learning rate](https://www.sciencedirect.com/topics/computer-science/learning-rate) scheduler () with a maximal learning rate of 5 $\times$ $10^{- 5}$. The warmup is set to 0.1. We use a batch size of 128, the AdamW optimizer () with a weight decay of $10^{- 4}$. Given the Tab-Text is a multi-modal tabular pipeline, we use AutoGluon (, ) for automated supervised learning on multi-modal tabular data.

#### 4.3.1. Data splitting

The dataset in our experiments is provided with a prespecified training/test split (20 % of the original data reserved for model testing). Methods are not allowed to access the test set during training, and for validation (hyperparameter-tuning, etc.) instead must hold out some data from the provided [training data](https://www.sciencedirect.com/topics/computer-science/training-data). Notably, the numerical variables are scaled to \[0,1\] by min-max scaling.

#### 4.3.2. Evaluation metrics

In the context of multi-class classification, it is essential to use appropriate metrics to assess the performance of a [predictive model](https://www.sciencedirect.com/topics/computer-science/predictive-model). To compare the performance of the proposed Tab-Text with the three baseline models, i.e., CatBoost, AT-Transformer, and T2T-Transformer, we adopted the commonly used classification metrics: Accuracy, F1-score, Precision, and Recall. These metrics collectively offer a comprehensive evaluation of the model’s performance in [classifying traffic](https://www.sciencedirect.com/topics/computer-science/classifying-traffic) crash severity levels. *Accuracy*

Accuracy measures the proportion of correctly classified instances in the entire dataset. It is calculated as:$\text{Accuracy} = \frac{\text{Correct} \text{Predictions}}{\text{Total} \text{Predictions}}$ where:
- •
	Correct Predictions: The number of correctly classified instances.
- •
	Total Predictions: The total number of instances in the [testing dataset](https://www.sciencedirect.com/topics/engineering/testing-dataset).

It should be noted that it is on the micro-level not the average accuracy of each class. The detailed accuracy for each class could be directly calculated with the [confusion matrix](https://www.sciencedirect.com/topics/engineering/confusion-matrix), which is also included in our results discussion parts.

*Precision*

Precision quantifies the accuracy of positive predictions for a specific class. It is computed as:$\text{Precision} = \frac{\text{True} \text{Positives}}{\text{True} \text{Positives} + \text{False} \text{Positives}}$ where:
- •
	[True Positives](https://www.sciencedirect.com/topics/computer-science/true-positive): The number of correctly predicted instances of the class.
- •
	[False Positives](https://www.sciencedirect.com/topics/computer-science/false-positive): The number of instances wrongly classified as the class.

The reported Precision in the results discussion section is on the macro-level, which is an averaged Precision treating each class equally. *Recall* Recall, also known as sensitivity or true positive rate, measures the ability of the model to correctly identify instances of a specific class. It is calculated as:$\text{Recall} = \frac{\text{True} \text{Positives}}{\text{True} \text{Positives} + \text{False} \text{Negatives}}$ where:
- •
	[False Negatives](https://www.sciencedirect.com/topics/computer-science/false-negative): The number of instances of the class wrongly classified as something else.

The reported Recall in the results discussion section is on the macro-level, which is an averaged Recall for each class.

*F1-score* The F1-score is the [harmonic mean](https://www.sciencedirect.com/topics/social-sciences/harmonic-mean) of precision and recall and provides a balance between these two metrics. It is computed as:$\text{F1}-\text{score} = \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$ The reported F1-score in the results discussion section is on the macro-level, which is an averaged F1 for each class.

## 5\. Results

The experimental results are presented in this section, covering [predictive analysis](https://www.sciencedirect.com/topics/computer-science/predictive-analysis) of Tab-Text against baseline models, the impact of [class balancing](https://www.sciencedirect.com/topics/computer-science/class-balancing), interpretation of Tab-Text using permutation importance, and a comparison with MNL.

### 5.1. Predictive analysis

The performance evaluation of the proposed Tab-Text model and other baseline models are summarized in and the detailed accuracies by severity levels are presented in.

Table 2. Performance of Tab-Text and other baselines.

| Empty Cell | Macro F1-score | Macro precision | Macro recall | Micro-accuracy |
| --- | --- | --- | --- | --- |
| MNL | 0.3317 | **0.6641** | 0.3569 | 0.7054 |
| CatBoost | 0.4118 | 0.5453 | 0.4041 | 0.6962 |
| AT-Transformer | 0.4024 | 0.5647 | 0.3984 | 0.6965 |
| T2T-Transformer | 0.4179 | 0.5565 | 0.4088 | 0.7008 |
| Tab-Text | **0.4587** | 0.6024 | **0.4378** | **0.7152** |

Table 3. Accuracy by accident severity.

| Model | Fatal accidents (%) | Serious accidents (%) | Minor injury accidents (%) | Macro-average (%) |
| --- | --- | --- | --- | --- |
| MNL | 1.47 | 8.24 | **97.37** | 35.69 |
| CatBoost | 5.25 | 24.36 | 91.62 | 40.41 |
| AT-Transformer | 3.50 | 24.26 | 91.75 | 39.84 |
| T2T-Transformer | 5.25 | 25.69 | 91.70 | 40.88 |
| Tab-Text | **9.63** | **28.88** | 91.83 | **43.45** |

The reported metrics are notably low considering the challenging nature of accident severity prediction from pre-event features. Overall, the Tab-Text model outperforms other models, indicating its superior capability in predicting accident severity. Tab-Text with ELECTRA [backbone](https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/spine) exhibits the highest macro-accuracy of 43.45 %, the top F1-score of 0.4587, and the best recall of 0.4378. These results suggests that Tab-Text maintains a balanced in terms of precision and recall across severity categories, making it particularly effective for datasets with imbalanced class distributions.

Particularly, the Tab-Text model outperforms other baseline models in predicting fatal and serious accidents. This highlights Tab-Text’s enhanced sensitivity to the less frequent but more severe accident outcomes, which is essential for prioritizing interventions in traffic [safety measures](https://www.sciencedirect.com/topics/engineering/safety-measure).

The MNL model demonstrates the highest macro-precision and accuracy in predicting minor injury accidents, suggesting a bias towards classifying each sample as such accidents. Despite CatBoost beingwell-suited for tabular data with categorical features, our results show that the Transformer, coupled with constructed textual narratives, outperforms the CatBoost model.

In addition, the T2T-Transformer surpasses the Transformer (All-Text) with a higher Macro F1-score of 0.4587, highlighting the advantages of the constructed textual narratives. Our way of using knowledge-infused template for building textual narratives is inherently data-centric, enriching the data with [engineering knowledge](https://www.sciencedirect.com/topics/computer-science/knowledge-engineering). The coherent narratives generated from tabular data align more closely with the underlying knowledge embedded in the pre-trained ELECTRA backbone.

Despite the marginal difference in overall accuracy, the results clearly show the incorporation of narratives constructed improves model overall performance, especially in predicting the fatal and serious accidents. This underscores the efficacy of narratives derived from pre-trained language models. The detailed ablation study and interpretation elucidating the superior performance of Tab-Text model are discussed subsequently.

#### 5.1.1. Ablation study for Tab-Text

To evaluate the importance of textual narratives in Tab-Text, we carry out the ablation study, in which we compare the performance of original Tab-Text with a modified version of Tab-Text by excluding textual narratives.

As shown in, without the narratives derived from the structured tabular data, the performance of Tab-Text exhibits a noticeable decrement in all the metrics compared with Tab-Text with the constructed narratives, as evidenced by metrics such as F1-score, accuracy, precision, and recall. Specifically, as demonstrated in, while the accuracy for minor injury accidents of Tab-Text without narratives shows improved accuracy compared to Tab-Text with ELECTRA-backbone, the accuracy drops by 6.9 % for fatal accidents and 7.48 % for the serious accidents. Accurate prediction of fatal and serious accidents is crucial due to their profound human, economic, and [societal impacts](https://www.sciencedirect.com/topics/social-sciences/societal-impact). The narratives generated, combined with the textual head with the ELECTRA backbone, play a important role in effectively identifying and characterizing fatal and serious accidents.

Table 4. Ablation study results.

| Empty Cell | Accuracy | F1-score | Precision | Recall |
| --- | --- | --- | --- | --- |
| Tab-Text | **0.7152** | **0.4587** | **0.6024** | **0.4378** |
| Tab-Text - w/o textual narrative | 0.7024 | 0.3946 | 0.5803 | 0.3948 |

Table 5. [Confusion matrix](https://www.sciencedirect.com/topics/computer-science/confusion-matrix).

| Actual | Predicted | Empty Cell | Empty Cell | Empty Cell |
| --- | --- | --- | --- | --- |
| Empty Cell | Fatal accidents | Serious accidents | Minor injury accidents | Total |
| **Tab-Text - ELECTRA-based** |  |  |  |  |
| Fatal accidents | 88 (**9.63 %**) | 511 (55.91 %) | 315 (34.46 %) | 914 (100 %) |
| Serious accidents | 78 (0.43 %) | 5360 (**29.88 %**) | 12,501 (69.69 %) | 17,939 (100 %) |
| Minor injury accidents | 18 (0.04 %) | 3216 (8.13 %) | 36,335 (91.83 %) | 39,569 (100 %) |
| **Tab-Text - w/o Textual narrative** |  |  |  |  |
| Fatal accidents | 25 (2.73 %) | 539 (58.97 %) | 350 (38.29 %) | 914 (100 %) |
| Serious accidents | 24 (0.13 %) | 3954 (22.4 %) | 13,961 (77.83 %) | 17,939 (100 %) |
| Minor injury accidents | 6 (0.02 %) | 2506 (6.33 %) | 37,057 (**93.65 %**) | 39,569 (100 %) |

#### 5.1.2. Visualization of embeddings

Uniform Manifold [Approximation](https://www.sciencedirect.com/topics/computer-science/approximation-algorithm) and Projection (UMAP) is a manifold learning technique used for dimension reduction, especially effective for visualizing high-dimensional data. Our aim is to visualize the learned embedding of the trained Tab-Text for three severity classes of traffic crashes, and compare it with the original input tabular features and the embedding of only the tabular part. The original input tabular features comprise one-hot-encoded categorical features and numeric features. The tabular embedding refers to the concatenation of the categorical embedding from the categorical head and the numeric embedding from the numeric head, resulting in 1536 dimensions. Additionally, the embedding of Tab-Text with the textual part through the pretrained ELECTRA-backbone adds 768 dimensions, bringing the total to 2304 dimensions. As all these embeddings are high-dimensional, we employ UMAP for dimension reduction and project them into a 2-D space for visualization. The results are shown in.

![Fig. 8](https://ars.els-cdn.com/content/image/1-s2.0-S095741742502069X-gr8.jpg)

Download: Download high-res image (933KB)

From the (a), which represents the original features, we observe a high degree of [entanglement](https://www.sciencedirect.com/topics/engineering/entanglement) among the three levels of accident severity, lacking distinct clusters. This indicates that the three severity classes are not readily separable.

In contrast, the Tab-Text embeddings of numeric and categorical features ((b)) exhibit more pronounced, separable clusters by severity levels. Incorporating the textual narratives ((c)) further breaks down to large clusters into smaller ones, revealing improved separation. This is evidenced in the clear differentiation of fatal (red dots) and severe (green dots) accidents from minor (blue dots) accidents. The scattered smaller clusters may represent various fine-grained contexts provided through the narratives. This argument warrants further exploration in future studies.

Upon examining the results, it becomes evident that the projection of combined feature embeddings from Tab-Text - numerical, categorical, and textual - yields a more nuanced view, potentially unraveling patterns that are not discernible when considering numerical and [categorical data](https://www.sciencedirect.com/topics/computer-science/categorical-data) alone. This transition from dense overlap to more discernible clusters as we move from the original [feature space](https://www.sciencedirect.com/topics/engineering/feature-space) to embedded spaces suggests that the feature transformation and embedding process effectively captures and emphasizes underlying [data structures](https://www.sciencedirect.com/topics/computer-science/data-structure) and relationships related to accident severity.

#### 5.1.3. Class balancing via downsampling

As noted in, our dataset exhibits a significant [class imbalance](https://www.sciencedirect.com/topics/computer-science/class-imbalance), with fatal accidents (1.630 %) being substantially less represented than serious accidents (30.785 %) and minor injury accidents (67.584 %). To investigate the impact of this imbalance on model performance and the robustness of our findings, we conducted additional experiments using a balanced dataset, which contains an equal number of samples from each severity class. For the downsampling procedure, we preserve all samples from the underrepresented “Fatal” class and randomly draw samples from the “No apparent or minor injury“ class and “Serious injury” class to achieve a balanced dataset across all classes.

presents the performance of all models on the balanced dataset. Several observations can be made from these results. First, all models demonstrate improved macro-level metrics compared to those on the imbalanced dataset in. This is expected as downsampling reduces the dominance of the [majority class](https://www.sciencedirect.com/topics/computer-science/majority-class) and allows models to better distinguish patterns in minority classes.

Table 6. Performance on downsampled balanced dataset.

| Empty Cell | Macro F1-score | Macro precision | Macro recall | Micro-accuracy |
| --- | --- | --- | --- | --- |
| MNL | 0.5026 | 0.5021 | 0.5045 | 0.5357 |
| CatBoost | 0.5470 | 0.5440 | 0.5500 | 0.5510 |
| AT-Transformer | 0.5511 | 0.5493 | 0.5629 | 0.5657 |
| T2T-Transformer | 0.5597 | 0.5572 | 0.5642 | 0.5657 |
| Tab-Text | **0.5629** | **0.5612** | **0.5695** | **0.5717** |

Importantly, the [relative performance](https://www.sciencedirect.com/topics/computer-science/relative-performance) ranking among models remains consistent with the results from the imbalanced dataset. Tab-Text continues to outperform all baseline models across all evaluation metrics, with a macro F1-score of 0.5629, macro precision of 0.5612, macro recall of 0.5695, and micro-accuracy of 0.5717. This consistent superiority on both balanced and imbalanced datasets reinforces our conclusion about the effectiveness of integrating textual narratives and tabular data for crash severity modeling.

The T2T-Transformer model remains the second-best performer with a macro F1-score of 0.5597, further supporting our finding that textual narratives constructed from tabular data significantly improve model performance. The relatively smaller gap between Tab-Text and T2T-Transformer on the balanced dataset (compared to the imbalanced one) suggests that the multi-modal approach offers particular advantages in handling class imbalance, possibly by extracting complementary information from different data modalities.

These findings demonstrate that while class imbalance influences the overall model performance, it does not alter the conclusion on the superiority of our proposed Tab-Text approach. Future work could explore additional techniques to address class imbalance, such as oversampling methods like SMOTE, resampling methods, or class-weighted loss functions, which might further enhance model performance, particularly for the minority class.

### 5.2. Tab-Text interpretation

In this paper, the permutation importance is chosen for model interpretation due to its computational efficiency although it has limitations with the independent feature assumption. Compared to the high [computational complexity](https://www.sciencedirect.com/topics/computer-science/computational-complexity) of SHAP values ($\mathcal{O} \left(\right. 2^{n} \left.\right)$ for exact calculations), the complexity of permutation importance is only $\mathcal{O} \left(\right. n \times P \times E \left.\right)$. Here, $n$ represents the total number of variables, $P$ is the number of permutations, and $E$ is the time complexity of evaluating the model.

The permutation importance method entails shuffling the values of a [single feature](https://www.sciencedirect.com/topics/computer-science/single-feature) in the test set and measuring the average drop in predicted accuracy of the target across multiple permutations. To ensure unbiased importance scores, we exclusively shuffle the original column values, independent of preprocessing and featurization choices. Specifically, for the textual narratives, we split each text entry into individual words, shuffled the words within each text narrative to disrupt the [semantic structure](https://www.sciencedirect.com/topics/social-sciences/semantic-structure) while preserving the overall word distribution. For the tabular data, we handled numerical and categorical features separately: [numerical values](https://www.sciencedirect.com/topics/computer-science/numerical-value) were randomly permuted within their column, maintaining their [data type](https://www.sciencedirect.com/topics/engineering/data-type) but disrupting their order, and categorical values were similarly shuffled within their column. We calculate the mean permutation importance of all the variables in Tab-Text across $P = 20$ different permutations, including categorical and numeric features, as well as textual narratives generated. illustrates the top 10 variables ranked by permutation importance. The horizontal [bar chart](https://www.sciencedirect.com/topics/engineering/bar-chart) provides a visual representation of the permutation importance of these variables, arranged in [descending order](https://www.sciencedirect.com/topics/computer-science/descending-order). Notable variables, including DCA, SPEED\_ZONE, VEHICLE\_MOVEMENT, ACCIDENT\_TYPE, VEHICLE\_2\_COLL\_PT, AGE\_GROUP, REGION\_NAME, VEHICLE\_1\_COLL\_PT, LGA\_NAME, and HELMET\_BELT\_WORN, have significant impact on the accuracy of Tab-Text in traffic severity modeling. Particularly, the DCA code, signifying the manner of the accidents, emerges as the most influential factor. Studies have demonstrate a close link between the manner of accidents and accident severity (). Additionally, other identified variables are expected to influence the severity outcome of accidents to varying degrees.

![Fig. 9](https://ars.els-cdn.com/content/image/1-s2.0-S095741742502069X-gr9.jpg)

Download: Download high-res image (230KB)

### 5.3. Interpretation comparison with MNL

The MNL, a classic statistical model, has long been employed to understand the effect of various factors on accident severity. For comparison, we would like to check whether the important variables identified through the permutation importance in align with the significant predictors identified by the MNL model. and [^1] shows the significant factors contributing to serious (Severity = 1) and fatal (Severity = 2) accidents with *p* -values less than 0.05 respectively. The baseline class is minor-injury accidents (SEVERITY=0).

Table 7. Significant factors for serious accidents (SEVERITY=1) with *p* -value $<$ 0.05.

| Variable | Coefficient | Std. error | *p* -value |
| --- | --- | --- | --- |
| **VEHICLE\_2\_COLL\_PT** |  |  |  |
| Vehicle 2 Coll Pt: None | \-0.604 | 0.252 | 0.017 |
| **DCA: Maneuvering** |  |  |  |
| 145: Reversing in stream of traffic | $-$ 0.722 | 0.162 | $<$ 0.001 |
| 146: Reversing into fixed object/parked vehicle | 0.373 | 0.180 | 0.038 |
| 148: Vehicle off footpath strikes veh on carriageway | 0.418 | 0.082 | $<$ 0.001 |
| **DCA: Off path on straight** |  |  |  |
| 171: Left off carriageway into object/parked vehicle | 0.376 | 0.168 | 0.025 |
| 173: Right off carriageway into object/parked vehicle | 0.652 | 0.185 | $<$ 0.001 |
| 175: Off end of road/T-intersection | 1.143 | 0.351 | 0.001 |
| **DCA: On path** |  |  |  |
| 160: Vehicle collides with vehicle parked on left of road | 0.709 | 0.060 | $<$ 0.001 |
| 162: Accident or broken down | 0.476 | 0.122 | $<$ 0.001 |
| 164: Permanent obstruction on carriageway | 0.673 | 0.216 | 0.002 |
| 165: Temporary roadworks | 1.032 | 0.396 | 0.009 |
| 169: Other on path | 0.852 | 0.100 | $<$ 0.001 |
| **DCA: Overtaking** |  |  |  |
| 150: Head on(overtaking) | 0.820 | 0.096 | $<$ 0.001 |
| 152: Pulling out (overtaking) | 0.198 | 0.083 | 0.017 |
| 154: Pulling out -rear end | 0.494 | 0.133 | $<$ 0.001 |
| **DCA: Passenger and miscellaneous** |  |  |  |
| 192: Struck train | 1.181 | 0.241 | $<$ 0.001 |
| **DCA: Vehicles from adjacent directions(intersection only)** |  |  |  |
| 110: Cross traffic(intersections only) | 0.178 | 0.047 | $<$ 0.001 |
| 113: Right near (intersections only) | 0.157 | 0.048 | 0.001 |
| 114: Two right turning (intersections only) | $-$ 0.396 | 0.143 | 0.006 |
| 116: Left near (intersections only) | 0.128 | 0.062 | 0.040 |
| 119: Other adjacent (intersections only) | 0.281 | 0.080 | $<$ 0.001 |
| **DCA: Vehicles from opposing directions** |  |  |  |
| 120: Head on (not overtaking) | 0.845 | 0.049 | $<$ 0.001 |
| 121: Right through | 0.174 | 0.047 | $<$ 0.001 |
| 129: Other opposing maneuvers not included | 0.413 | 0.135 | 0.002 |
| **DCA: Vehicles from same directions** |  |  |  |
| 131: Left rear | $-$ 0.457 | 0.073 | $<$ 0.001 |
| 135: Lane change left (not overtaking) | $-$ 0.225 | 0.064 | $<$ 0.001 |
| **VEHICLE\_MOVEMENT** |  |  |  |
| VEHICLE\_MOVEMENT: Stationary broken down | 0.446 | 0.202 | 0.027 |
| **SPEED\_ZONE** |  |  |  |
| SPEED\_ZONE: 70 | 0.445 | 0.189 | 0.018 |
| SPEED\_ZONE: 80 | 0.550 | 0.189 | 0.004 |
| SPEED\_ZONE: 90 | 1.015 | 0.200 | $<$ 0.001 |
| SPEED\_ZONE: 100 | 0.859 | 0.189 | $<$ 0.001 |
| SPEED\_ZONE: 110 | 0.886 | 0.197 | $<$ 0.001 |

Table 8. Significant predictors for fatal accidents (SEVERITY=2) with *p* -value $<$ 0.05.

| Variable | Coefficient | Std. Error | *p* -value |
| --- | --- | --- | --- |
| **VEHICLE\_2\_COLL\_PT** |  |  |  |
| VEHICLE\_2\_COLL\_PT: Top/Roof | 2.490 | 1.054 | 0.018 |
| **DCA: Maneuvering** |  |  |  |
| 141: U-turn into fixed object/parked vehicle | 2.453 | 0.985 | 0.013 |
| 146: Reversing into fixed object/parked vehicle | 2.128 | 0.795 | 0.007 |
| 147: Vehicle strikes another vehicle when emerging from driveway | 0.587 | 0.271 | 0.030 |
| 148: Vehicle off footpath strikes veh on carriageway | 1.241 | 0.385 | 0.001 |
| 149: Other Maneuvering | 1.553 | 0.444 | $< 0.001$ |
| **DCA: On path** |  |  |  |
| 160: Vehicle collides with vehicle parked on left of road | 1.335 | 0.303 | $< 0.001$ |
| 162: Accident or broken down | 1.300 | 0.408 | 0.001 |
| 169: Other on path | 2.041 | 0.417 | $< 0.001$ |
| **DCA: Overtaking** |  |  |  |
| 150: Head on(overtaking) | 2.654 | 0.257 | $< 0.001$ |
| 151: Out of control (overtaking) | 1.604 | 0.574 | 0.005 |
| 152: Pulling out (overtaking) | 0.901 | 0.307 | 0.003 |
| 153: Cutting in (overtaking) | 1.031 | 0.449 | 0.022 |
| 154: Pulling out -rear end | 1.056 | 0.478 | 0.027 |
| **DCA: Passenger and miscellaneous** |  |  |  |
| 192: Struck train | 3.909 | 0.366 | $< 0.001$ |
| **DCA: Vehicles from adjacent directions(intersection only)** |  |  |  |
| 110: Cross-traffic(intersections only) | 0.589 | 0.220 | 0.007 |
| 113: Right Near (intersections only) | 0.489 | 0.227 | 0.031 |
| 118: Two left turning (intersections only) | 2.838 | 0.797 | $< 0.001$ |
| 119: Other adjacent (intersections only) | 1.220 | 0.306 | $< 0.001$ |
| **DCA: Vehicles from opposing directions** |  |  |  |
| 120: Head on (not overtaking) | 2.412 | 0.215 | $< 0.001$ |
| **DCA: Vehicles from same directions** |  |  |  |
| 132: Right rear | 0.696 | 0.283 | 0.014 |
| 135: Lane change left (not overtaking) | $-$ 0.756 | 0.336 | 0.025 |
| **VEHICLE\_MOVEMENT** |  |  |  |
| VEHICLE\_MOVEMENT: Not known | 1.472 | 0.667 | 0.027 |
| VEHICLE\_MOVEMENT: Out of control | 1.335 | 0.648 | 0.039 |
| VEHICLE\_MOVEMENT: Parked legally | 1.660 | 0.716 | 0.020 |
| VEHICLE\_MOVEMENT: U-turning | 1.513 | 0.692 | 0.029 |
| **SPEED\_ZONE** |  |  |  |
| SPEED\_ZONE: 80 | 1.559 | 0.774 | 0.044 |
| SPEED\_ZONE: 90 | 2.033 | 0.800 | 0.011 |
| SPEED\_ZONE: 100 | 2.738 | 0.774 | $< 0.001$ |
| SPEED\_ZONE: 110 | 3.070 | 0.785 | $< 0.001$ |

As shown in and [^1], the majority of significant factors are related to DCA. Furthermore, other variables, such as VEHICLE\_2\_COLL\_PT, VEHICLE\_MOVEMENT, and SPEED\_ZONE, show significance for both serious and fatal accidents. Notably, these four variables also rank among the top 5 important variables identified by permutation importance in the Tab-Text model, highlighting the Tab-Text’s ability to capture the effects of the impactful factors similar to the traditional MNL model.

In and [^1], the “Coefficient” column represents the estimated effect of each variable on the log-odds of the outcome relative to the [base](https://www.sciencedirect.com/topics/pharmacology-toxicology-and-pharmaceutical-science/base) category (minor-injury accidents). Positive coefficients indicate that the variable increases the likelihood of serious or fatal accidents compared to minor injuries, while negative coefficients indicate a decreased likelihood. The “Std. Error” column shows the standard error of the coefficient estimate, indicating the precision of the estimate. The “ *p* -value” column displays the *p* -value, which is a measure of statistical significance. The *p* -value indicates the probability of observing an effect as extreme as the one estimated, assuming the null hypothesis of no effect is true. Smaller *p* -values (typically below 0.05) suggest that the observed relationship is unlikely to have occurred by chance, providing evidence to reject the null hypothesis and conclude that the variable has a significant influence on accident severity.

For both serious and fatal accidents, certain maneuvers like reversing into a fixed object or parked vehicle (DCA 146) are significant predictors. This suggests that maneuvers requiring high precision or those performed in complex environments can increase the risk of severe outcomes.

Incidents involving vehicles parked on the left of the road (DCA 160) are significant for both serious and fatal accidents, indicating that parked vehicles on the left side of the road can pose a substantial risk to moving traffic.

Head-on collisions while overtaking (DCA 150) are highly significant in both serious and fatal accidents, highlighting the dangers associated with overtaking maneuvers, especially when they result in a head-on configuration.

Higher speed zones (90, 100, and 110 km/h) are significant predictors for both serious and fatal accidents, underlining the increased risk associated with higher speeds. The higher the speed, the more severe the outcome of the crash tends to be, likely due to the increased impact force and decreased reaction time.

Factors like vehicle collision with the top/roof and striking a train (DCA 192) are significantly associated with fatal outcomes. These factors typically involve more catastrophic scenarios with high energy impact or situations where passengers are extremely vulnerable.

## 6\. Conclusions

In this paper, we introduced Tab-Text: a multi-modal paradigm for inferring traffic crash severity outcome. Tab-Text employs a multi-modal approach by enriching traditional tabular data with template-constructed textual narratives. Our study aimed to evaluate the efficacy of Tab-Text for the traffic crash severity inference task compared to non-multi-modal baselines. These baselines include: 1) CatBoost, a tree ensemble model using only tabular data; 2) T2T-Transformer, trained only with textual narratives; 3) AT-Transformer, trained only with directly textualized tabular data; and 4) Multi-nominal logit model. The experiments used crash data from Victoria, Australia. This dataset encompasses [essential features](https://www.sciencedirect.com/topics/computer-science/essential-feature) related to road, vehicle, human, and situational factors influencing crash severity outcome.

Our results demonstrate that the constructed textual narratives improve crash severity inference, especially for fatal and serious crashes. Tab-Text outperformed non-multi-modal baselines, demonstrating the effectiveness of our proposed approach. Moreover, it highlights the potential synergy between domain-specific knowledge in traffic safety and pre-trained LLMs. Converting tabular data to natural language narratives allows the pre-trained LLMs to better consume this information. This conversion helps better understand contextualized semantic nuances, thereby improving crash severity inference. Permutation importance analysis further confirms the significance of several factors in crash severity inference. These include the manner of collision (DCA), speed zone, and vehicle movement.

Despite the promising advancements, this research [faces](https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/face) limitations common to the broader integration of [AI](https://www.sciencedirect.com/topics/computer-science/artificial-intelligence) in engineering, particularly in the traffic safety domain. A critical challenge is the growing need for [Explainable AI](https://www.sciencedirect.com/topics/computer-science/explainable-artificial-intelligence) (XAI) techniques. These techniques should provide deeper insights into how models capture [causal relationships](https://www.sciencedirect.com/topics/computer-science/causal-relationship) and make decisions. Future research should prioritize incorporating domain-specific knowledge into model design. Developing methods that integrate XAI principles is also important. Additionally, fine-tuning open-source LLMs with domain knowledge in traffic safety could directly enhance their applicability in traffic crash analysis and modeling.

While our template-based approach for narrative generation demonstrated effectiveness, we acknowledge several limitations that warrant future exploration. The fixed template structure applies the same [linguistic structure](https://www.sciencedirect.com/topics/social-sciences/structural-linguistics) across all crash types, potentially overlooking contextual nuances specific to different crash scenarios. Future research could explore more sophisticated approaches. These include dynamic template systems that adapt narrative structures based on crash characteristics and large language models to produce more natural descriptions. These alternative approaches could potentially enhance [generalizability](https://www.sciencedirect.com/topics/computer-science/generalizability) across different geographic contexts.

## CRediT authorship contribution statement

**Hao Zhen:** Conceptualization, Methodology, [Data curation](https://www.sciencedirect.com/topics/computer-science/data-curation), Visualization, Software, Writing – original draft, Investigation, Formal analysis. **Jidong J. Yang:** Conceptualization, Methodology, Investigation, Formal analysis, Supervision, Resources, Writing – review & editing.

## Declaration of competing interest

The authors declare that they have no conflict of interest.

## Appendix A. Appendix

Accident type, event type, the definition of classifying addicents (DCA), accident distribution by DCA code, and accident distribution by vehicle movement are presented in,,, and [^2], respectively.

Table 9. Accident type.

| Empty Cell | Empty Cell | Minor | Empty Cell | Empty Cell | Empty Cell |
| --- | --- | --- | --- | --- | --- |
| Empty Cell | Empty Cell | injury | Serious | Fatal | Empty Cell |
| ACCIDENT\_TYPE | Counts | accidents | accidents | accidents | Percentage |
| Collision with vehicle | 232,864 | 165,112 | 64,994 | 2758 | 79.719 % |
| Collision with a fixed object | 31,235 | 16,076 | 13,957 | 1202 | 10.693 % |
| Struck Pedestrian | 16,676 | 9092 | 6999 | 585 | 5.709 % |
| Vehicle overturned (no collision) | 5400 | 3090 | 2169 | 141 | 1.849 % |
| No collision and no object struck | 2434 | 1670 | 742 | 22 | 0.833 % |
| Collision with some other object | 1254 | 896 | 341 | 17 | 0.429 % |
| Struck animal | 1232 | 925 | 289 | 18 | 0.422 % |
| Fall from or in moving vehicle | 942 | 510 | 416 | 16 | 0.322 % |
| Other accident | 69 | 50 | 18 | 1 | 0.024 % |
| Total | 292,106 | 197,421 | 89,925 | 4760 | 100 % |

Table 10. Event type.

| Empty Cell | Empty Cell | Minor | Empty Cell | Empty Cell | Empty Cell |
| --- | --- | --- | --- | --- | --- |
| Empty Cell | Empty Cell | injury | Serious | Fatal | Empty Cell |
| EVENT\_TYPE | Counts | accidents | accidents | accidents | Percentage |
| Collision | 251,073 | 175,501 | 72,249 | 3323 | 85.953 % |
| Ran off carriageway | 33,519 | 17,415 | 14,885 | 1219 | 11.475 % |
| Rollover on/off carriageway | 5008 | 2869 | 1955 | 184 | 1.714 % |
| Fell from vehicle | 1340 | 791 | 530 | 19 | 0.459 % |
| Other | 348 | 269 | 77 | 2 | 0.119 % |
| Struck by stone/projectile/load | 325 | 251 | 71 | 3 | 0.111 % |
| Fell in vehicle | 286 | 182 | 102 | 2 | 0.098 % |
| Mechanical failure | 148 | 94 | 46 | 8 | 0.051 % |
| Not known | 54 | 45 | 9 | 0 | 0.018 % |
| Not applicable | 5 | 4 | 1 | 0 | 0.002 % |
| Total | 292,106 | 197,421 | 89,925 | 4760 | 100 % |

Table 11. Definitions of classifying accidents (DCA).

<table><thead><tr><th>DCA</th><td>Empty Cell</td></tr><tr><th>CODE</th><th>Description</th></tr></thead><tbody><tr><td colspan="2"><em>PEDESTRAIAN ON FOOT IN TOY/PRAM</em></td></tr><tr><td>100</td><td>PED NEAR SIDE. PED HIT BY VEHICLE FROM THE RIGHT.</td></tr><tr><td>101</td><td>PED EMERGES FROM IN FRONT OF PARKED OR STATIONARY VEHICLE</td></tr><tr><td>102</td><td>FAR SIDE. PED HIT BY VEHICLE FROM THE LEFT</td></tr><tr><td>103</td><td>PED PLAYING/LYING/WORKING/STANDING ON CARRIAGEWAY.</td></tr><tr><td>104</td><td>PED WALKING WITH TRAFFIC</td></tr><tr><td>105</td><td>PED WALKING AGAINST TRAFFIC.</td></tr><tr><td>106</td><td>VEH STRIKES PED ON FOOTPATH/MEDIAN/TRAFFIC ISLAND.</td></tr><tr><td>107</td><td>PED ON FOOTHPATH STRUCK BY VEHENTERING/LEAVING DRIVEWAY.</td></tr><tr><td>108</td><td>PED STRUCK WALKING TO/FROM OR BOARDING/ALIGHTING VEHICLE.</td></tr><tr><td>109</td><td>ANY MANOEUVRE INVOLVING PED NOT INCLUDED IN DCAs 100–108.</td></tr><tr><td colspan="2"><em>VEHICLES FROM ADJACENT DIRECTIONS(INTERSECTIONS ONLY</em>)</td></tr><tr><td>110</td><td>CROSS TRAFFIC(INTERSECTIONS ONLY)</td></tr><tr><td>111</td><td>RIGHT FAR (INTERSECTIONS ONLY)</td></tr><tr><td>112</td><td>LEFT FAR (INTERSECTIONS ONLY)</td></tr><tr><td>113</td><td>RIGHT NEAR (INTERSECTIONS ONLY)</td></tr><tr><td>114</td><td>TWO RIGHT TURNING (INTERSECTIONS ONLY)</td></tr><tr><td>115</td><td>RIGHT/LEFT FAR (INTERSECTIONS ONLY)</td></tr><tr><td>116</td><td>LEFT NEAR (INTERSECTIONS ONLY)</td></tr><tr><td>117</td><td>LEFT/RIGHT FAR (INTERSECTIONS ONLY)</td></tr><tr><td>118</td><td>TWO LEFT TURNING (INTERSECTIONS ONLY)</td></tr><tr><td>119</td><td>OTHER ADJACENT (INTERSECTIONS ONLY)</td></tr><tr><td colspan="2"><em>VEHICLES FROM OPPOSING DIRECTIONS</em></td></tr><tr><td>120</td><td>HEAD ON (NOT OVERTAKING)</td></tr><tr><td>121</td><td>RIGHT THROUGH</td></tr><tr><td>122</td><td>LEFT THROUGH</td></tr><tr><td>123</td><td>RIGHT/LEFT. ONE VEH TURNING RIGHT THE OTHER LEFT.</td></tr><tr><td>124</td><td>RIGHT/RIGHT BOTH VEHs FROM OPPOSITE DIRECTIONS TURNING RIGHT</td></tr><tr><td>125</td><td>LEFT/LEFT. BOTH VEHs FROM OPPOSITE DIRECTIONS TURNING LEFT.</td></tr><tr><td>129</td><td>OTHER OPPOSING MANOEUVRES NOT INCLUDED IN DCAs 120–125.</td></tr><tr><td colspan="2"><em>VEHICLES FROM SAME DIRECTION</em></td></tr><tr><td>130</td><td>REAR END(VEHICLES IN SAME LANE)</td></tr><tr><td>131</td><td>LEFT REAR</td></tr><tr><td>132</td><td>RIGHT REAR.</td></tr><tr><td>133</td><td>LANE SIDE SWIPE (VEHICLES IN PARALLEL LANES)</td></tr><tr><td>134</td><td>LANE CHANGE RIGHT (NOT OVERTAKING)</td></tr><tr><td>135</td><td>LANE CHANGE LEFT (NOT OVERTAKING)</td></tr><tr><td>136</td><td>RIGHT TURN SIDESWIPE</td></tr><tr><td>137</td><td>LEFT TURN SIDESWIPE</td></tr><tr><td>139</td><td>OTHER SAME DIRECTION-MANOUEVRES NOT INCLUDED IN DCAs 130–137</td></tr><tr><td colspan="2"><em>MANOEUVRING</em></td></tr><tr><td>140</td><td>U TURN</td></tr><tr><td>141</td><td>U TURN INTO FIXED OBJECT/PARKED VEHICLE</td></tr><tr><td>142</td><td>LEAVING PARKING</td></tr><tr><td>143</td><td>ENTERING PARKING</td></tr><tr><td>144</td><td>PARKED VEHICLES ONLY</td></tr><tr><td>145</td><td>REVERSING IN STREAM OF TRAFFIC</td></tr><tr><td>146</td><td>REVERSING INTO FIXED OBJECT/PARKED VEHICLE</td></tr><tr><td>147</td><td>VEHICLE STRIKES ANOTHER VEH WHILE EMERGING FROM DRIVEWAY</td></tr><tr><td>148</td><td>VEHICLE OFF FOOTPATH STRIKES VEH ON CARRIAGEWAY</td></tr><tr><td>149</td><td>OTHER MANOEUVRING NOT INCLUDED IN DCAs 140–148</td></tr><tr><td colspan="2"><em>OVERTAKING</em></td></tr><tr><td>150</td><td>HEAD ON(OVERTAKING)</td></tr><tr><td>151</td><td>OUT OF CONTROL (OVERTAKING)</td></tr><tr><td>152</td><td>PULLING OUT (OVERTAKING)</td></tr><tr><td>153</td><td>CUTTING IN (OVERTAKING)</td></tr><tr><td>154</td><td>PULLING OUT -REAR END</td></tr><tr><td>159</td><td>OTHER OVERTAKING MANOEUVRES NOT INCLUDED IN DCAs 150–154</td></tr><tr><td colspan="2"><em>ON PATH</em></td></tr><tr><td>160</td><td>VEHICLE COLLIDES WITH VEHICLE PARKED ON LEFT OF ROAD</td></tr><tr><td>161</td><td>DOUBLE PARKED</td></tr><tr><td>162</td><td>ACCIDENT OR BROKEN DOWN</td></tr><tr><td>163</td><td>VEHICLE STRIKES DOOR OF PARKED/STATIONARY VEHICLE</td></tr><tr><td>164</td><td>PERMANENT OBSTRUCTION ON CARRIAGEWAY</td></tr><tr><td>165</td><td>TEMPORARY ROADWORKS</td></tr><tr><td>166</td><td>STRUCK OBJECT ON CARRIAGEWAY</td></tr><tr><td>167</td><td>STRUCK ANIMAL</td></tr><tr><td>169</td><td>OTHER ON PATH</td></tr><tr><td colspan="2"><em>OFF PATH ON STRAIGHT</em></td></tr><tr><td>170</td><td>OFF CARRIAGEWAY TO LEFT</td></tr><tr><td>171</td><td>LEFT OFF CARRIAGEWAY INTO OBJECT/PARKED VEHICLE</td></tr><tr><td>172</td><td>OFF CARRIAGEWAY TO RIGHT</td></tr><tr><td>173</td><td>RIGHT OFF CARRIAGEWAY INTO OBJECT/PARKED VEHICLE</td></tr><tr><td>174</td><td>OUT OF CONTROL ON CARRIAGEWAY (ON STRAIGHT)</td></tr><tr><td>175</td><td>OFF END OF ROAD/T-INTERSECTION.</td></tr><tr><td>179</td><td>OTHER ACCIDENTS-OFF STRAIGHT NOT INCLUDED IN DCAs 170–175</td></tr><tr><td colspan="2"><em>OFF PATH ON CURVE</em></td></tr><tr><td>180</td><td>OFF CARRIAGEWAY ON RIGHT BEND</td></tr><tr><td>181</td><td>OFF RIGHT BEND INTO OBJECT/PARKED VEHICLE</td></tr><tr><td>182</td><td>OFF CARRIAGEWAY ON LEFT BEND</td></tr><tr><td>183</td><td>OFF LEFT BEND INTO OBJECT/PARKED VEHICLE</td></tr><tr><td>184</td><td>OUT OF CONTROL ON CARRIAGEWAY (ON BEND)</td></tr><tr><td>189</td><td>OTHER ACCIDENTS ON CURVE NOT INCLUDED IN DCAs 180–184</td></tr><tr><td colspan="2"><em>PASSENGER AND MISCELLANEOUS</em></td></tr><tr><td>190</td><td>FELL IN/FROM VEHICLE</td></tr><tr><td>191</td><td>LOAD OR MISSILE STRUCK VEHICLE</td></tr><tr><td>192</td><td>STRUCK TRAIN</td></tr><tr><td>193</td><td>STRUCK RAILWAY CROSSING FURNITURE</td></tr><tr><td>194</td><td>PARKED CAR RUN AWAY</td></tr><tr><td>198</td><td>OTHER ACCIDENTS NOT CLASSIFIABLE ELSEWHERE</td></tr><tr><td>199</td><td>UNKNOWN-NO DETAILS ON MANOEUVRES OF ROAD-USERS IN ACCIDENT</td></tr><tr><td><strong>Total</strong></td><td></td></tr></tbody></table>

Table 12. Accident distribution by DCA code.

<table><thead><tr><td>Empty Cell</td><td>Empty Cell</td><td>Empty Cell</td><td>Empty Cell</td><th>Minor</th><td>Empty Cell</td></tr><tr><th>DCA</th><td>Empty Cell</td><th>Fatal</th><th>Serious</th><th>injury</th><td>Empty Cell</td></tr><tr><th>CODE</th><th>Counts</th><th>accidents</th><th>accidents</th><th>accidents</th><th>Percentage</th></tr></thead><tbody><tr><td colspan="6">PEDESTRAIAN ON FOOT IN TOY/PRAM</td></tr><tr><td>100</td><td>6302</td><td>221</td><td>2668</td><td>3413</td><td>2.157 %</td></tr><tr><td>101</td><td>1101</td><td>11</td><td>514</td><td>576</td><td>0.377 %</td></tr><tr><td>102</td><td>4198</td><td>145</td><td>1916</td><td>2137</td><td>1.437 %</td></tr><tr><td>103</td><td>875</td><td>55</td><td>279</td><td>541</td><td>0.300 %</td></tr><tr><td>104</td><td>384</td><td>49</td><td>171</td><td>164</td><td>0.131 %</td></tr><tr><td>105</td><td>177</td><td>17</td><td>84</td><td>76</td><td>0.061 %</td></tr><tr><td>106</td><td>368</td><td>20</td><td>143</td><td>205</td><td>0.126 %</td></tr><tr><td>107</td><td>905</td><td>20</td><td>335</td><td>550</td><td>0.310 %</td></tr><tr><td>108</td><td>525</td><td>6</td><td>176</td><td>343</td><td>0.180 %</td></tr><tr><td>109</td><td>1880</td><td>41</td><td>726</td><td>1113</td><td>0.644 %</td></tr><tr><td colspan="6">VEHICLES FROM ADJACENT DIRECTIONS(INTERSECTIONS ONLY)</td></tr><tr><td>110</td><td>25,983</td><td>332</td><td>8012</td><td>17,639</td><td>8.895 %</td></tr><tr><td>111</td><td>4037</td><td>19</td><td>1022</td><td>2996</td><td>1.382 %</td></tr><tr><td>112</td><td>652</td><td>8</td><td>189</td><td>455</td><td>0.223 %</td></tr><tr><td>113</td><td>17,437</td><td>202</td><td>5700</td><td>11,535</td><td>5.969 %</td></tr><tr><td>114</td><td>441</td><td>0</td><td>91</td><td>350</td><td>0.151 %</td></tr><tr><td>115</td><td>237</td><td>0</td><td>72</td><td>165</td><td>0.081 %</td></tr><tr><td>116</td><td>4018</td><td>11</td><td>1092</td><td>2915</td><td>1.376 %</td></tr><tr><td>117</td><td>15</td><td>0</td><td>4</td><td>11</td><td>0.005 %</td></tr><tr><td>118</td><td>55</td><td>2</td><td>15</td><td>38</td><td>0.019 %</td></tr><tr><td>119</td><td>1337</td><td>36</td><td>436</td><td>865</td><td>0.458 %</td></tr><tr><td colspan="6">VEHICLES FROM OPPOSING DIRECTIONS</td></tr><tr><td>120</td><td>12,978</td><td>1056</td><td>6139</td><td>5783</td><td>4.443 %</td></tr><tr><td>121</td><td>31,479</td><td>216</td><td>10,265</td><td>20,998</td><td>10.777 %</td></tr><tr><td>122</td><td>111</td><td>0</td><td>32</td><td>79</td><td>0.038 %</td></tr><tr><td>123</td><td>290</td><td>1</td><td>73</td><td>216</td><td>0.099 %</td></tr><tr><td>124</td><td>97</td><td>0</td><td>22</td><td>75</td><td>0.033 %</td></tr><tr><td>125</td><td>3</td><td>0</td><td>0</td><td>3</td><td>0.001 %</td></tr><tr><td>129</td><td>366</td><td>4</td><td>131</td><td>231</td><td>0.125 %</td></tr><tr><td colspan="6">VEHICLES FROM SAME DIRECTION</td></tr><tr><td>130</td><td>74,101</td><td>283</td><td>15,509</td><td>58,309</td><td>25.368 %</td></tr><tr><td>131</td><td>3913</td><td>6</td><td>543</td><td>3364</td><td>1.340 %</td></tr><tr><td>132</td><td>9025</td><td>58</td><td>2180</td><td>6787</td><td>3.090 %</td></tr><tr><td>133</td><td>3560</td><td>36</td><td>1094</td><td>2430</td><td>1.219 %</td></tr><tr><td>134</td><td>3435</td><td>32</td><td>1011</td><td>2392</td><td>1.176 %</td></tr><tr><td>135</td><td>3923</td><td>19</td><td>974</td><td>2930</td><td>1.343 %</td></tr><tr><td>136</td><td>1654</td><td>15</td><td>416</td><td>1223</td><td>0.566 %</td></tr><tr><td>137</td><td>2172</td><td>13</td><td>481</td><td>1678</td><td>0.744 %</td></tr><tr><td>139</td><td>1233</td><td>4</td><td>367</td><td>862</td><td>0.422 %</td></tr><tr><td colspan="6">MANOEUVRING</td></tr><tr><td>140</td><td>6345</td><td>57</td><td>1920</td><td>4368</td><td>2.172 %</td></tr><tr><td>141</td><td>198</td><td>1</td><td>71</td><td>126</td><td>0.068 %</td></tr><tr><td>142</td><td>1306</td><td>3</td><td>260</td><td>1043</td><td>0.447 %</td></tr><tr><td>143</td><td>572</td><td>1</td><td>126</td><td>445</td><td>0.196 %</td></tr><tr><td>144</td><td>72</td><td>0</td><td>10</td><td>62</td><td>0.025 %</td></tr><tr><td>145</td><td>513</td><td>2</td><td>64</td><td>447</td><td>0.176 %</td></tr><tr><td>146</td><td>412</td><td>5</td><td>123</td><td>284</td><td>0.141 %</td></tr><tr><td>147</td><td>6549</td><td>48</td><td>1651</td><td>4850</td><td>2.242 %</td></tr><tr><td>148</td><td>1279</td><td>11</td><td>405</td><td>863</td><td>0.438 %</td></tr><tr><td>149</td><td>576</td><td>8</td><td>154</td><td>414</td><td>0.197 %</td></tr><tr><td colspan="6">OVERTAKING</td></tr><tr><td>150</td><td>881</td><td>97</td><td>396</td><td>388</td><td>0.302 %</td></tr><tr><td>151</td><td>477</td><td>30</td><td>217</td><td>230</td><td>0.163 %</td></tr><tr><td>152</td><td>1361</td><td>34</td><td>435</td><td>892</td><td>0.466 %</td></tr><tr><td>153</td><td>378</td><td>8</td><td>105</td><td>265</td><td>0.129 %</td></tr><tr><td>154</td><td>396</td><td>6</td><td>149</td><td>241</td><td>0.136 %</td></tr><tr><td>159</td><td>245</td><td>6</td><td>76</td><td>163</td><td>0.084 %</td></tr><tr><td colspan="6">ON PATH</td></tr><tr><td>160</td><td>4773</td><td>39</td><td>1741</td><td>2993</td><td>1.634 %</td></tr><tr><td>161</td><td>25</td><td>0</td><td>4</td><td>21</td><td>0.009 %</td></tr><tr><td>162</td><td>538</td><td>17</td><td>236</td><td>285</td><td>0.184 %</td></tr><tr><td>163</td><td>2265</td><td>6</td><td>522</td><td>1737</td><td>0.775 %</td></tr><tr><td>164</td><td>240</td><td>3</td><td>89</td><td>148</td><td>0.082 %</td></tr><tr><td>165</td><td>58</td><td>0</td><td>26</td><td>32</td><td>0.020 %</td></tr><tr><td>166</td><td>565</td><td>9</td><td>143</td><td>413</td><td>0.193 %</td></tr><tr><td>167</td><td>1225</td><td>18</td><td>285</td><td>922</td><td>0.419 %</td></tr><tr><td>169</td><td>709</td><td>9</td><td>294</td><td>406</td><td>0.243 %</td></tr><tr><td colspan="6">OFF PATH ON STRAIGHT</td></tr><tr><td>170</td><td>1972</td><td>48</td><td>758</td><td>1166</td><td>0.675 %</td></tr><tr><td>171</td><td>12,774</td><td>382</td><td>5773</td><td>6619</td><td>4.373 %</td></tr><tr><td>172</td><td>1233</td><td>33</td><td>535</td><td>665</td><td>0.422 %</td></tr><tr><td>173</td><td>9358</td><td>396</td><td>4438</td><td>4524</td><td>3.204 %</td></tr><tr><td>174</td><td>1793</td><td>20</td><td>547</td><td>1226</td><td>0.614 %</td></tr><tr><td>175</td><td>973</td><td>17</td><td>462</td><td>494</td><td>0.333 %</td></tr><tr><td>179</td><td>801</td><td>8</td><td>278</td><td>515</td><td>0.274 %</td></tr><tr><td colspan="6">OFF PATH ON CURVE</td></tr><tr><td>180</td><td>1181</td><td>30</td><td>460</td><td>691</td><td>0.404 %</td></tr><tr><td>181</td><td>4515</td><td>217</td><td>1790</td><td>2508</td><td>1.546 %</td></tr><tr><td>182</td><td>693</td><td>22</td><td>265</td><td>406</td><td>0.237 %</td></tr><tr><td>183</td><td>3237</td><td>170</td><td>1378</td><td>1689</td><td>1.108 %</td></tr><tr><td>184</td><td>368</td><td>8</td><td>152</td><td>208</td><td>0.126 %</td></tr><tr><td>189</td><td>129</td><td>1</td><td>53</td><td>75</td><td>0.044 %</td></tr><tr><td colspan="6">PASSENGER AND MISCELLANEOUS</td></tr><tr><td>190</td><td>868</td><td>14</td><td>390</td><td>464</td><td>0.297 %</td></tr><tr><td>191</td><td>310</td><td>2</td><td>62</td><td>246</td><td>0.106 %</td></tr><tr><td>192</td><td>123</td><td>31</td><td>51</td><td>41</td><td>0.042 %</td></tr><tr><td>193</td><td>21</td><td>1</td><td>6</td><td>14</td><td>0.007 %</td></tr><tr><td>194</td><td>79</td><td>1</td><td>23</td><td>55</td><td>0.027 %</td></tr><tr><td>198</td><td>295</td><td>2</td><td>78</td><td>215</td><td>0.101 %</td></tr><tr><td>199</td><td>158</td><td>1</td><td>42</td><td>115</td><td>0.054 %</td></tr><tr><td><strong>Total</strong></td><td>292,106</td><td>4760</td><td>89,925</td><td>197,421</td><td>100 %</td></tr></tbody></table>

Table 13. Accident distributioin by vehicle movement.

| Empty Cell | Empty Cell | Minor | Empty Cell | Empty Cell | Empty Cell |
| --- | --- | --- | --- | --- | --- |
| VEHICLE | Empty Cell | injury | Serious | Fatal | Empty Cell |
| \_MOVEMENT | Counts | accidents | accidents | accidents | Percentage |
| Going straight ahead | 139,290 | 93,248 | 43,471 | 2571 | 47.68 % |
| Turning right | 37,181 | 24,842 | 11,995 | 344 | 12.73 % |
| Out of control | 30,000 | 15,834 | 13,012 | 1154 | 10.27 % |
| Slow/stopping | 23,613 | 18,420 | 5082 | 111 | 8.08 % |
| Other stationary | 18,817 | 14,347 | 4373 | 97 | 6.44 % |
| Turning left | 10,437 | 7851 | 2516 | 70 | 3.57 % |
| Changing lanes | 6529 | 4455 | 1968 | 106 | 2.24 % |
| Not known | 4244 | 2865 | 1290 | 89 | 1.45 % |
| U-turning | 3933 | 2683 | 1212 | 38 | 1.35 % |
| Leaving a driveway | 2953 | 2170 | 764 | 19 | 1.01 % |
| Stationary accident | 2815 | 2165 | 635 | 15 | 0.96 % |
| Reversing | 2397 | 1739 | 637 | 21 | 0.82 % |
| Parked legally | 2277 | 1639 | 621 | 17 | 0.78 % |
| Overtaking | 1736 | 1093 | 583 | 60 | 0.59 % |
| Merging | 1662 | 1209 | 442 | 11 | 0.57 % |
| Avoiding animals | 1590 | 1072 | 511 | 7 | 0.54 % |
| Parking or unparking | 1541 | 1163 | 374 | 4 | 0.53 % |
| Wrong way | 614 | 340 | 254 | 20 | 0.21 % |
| Stationary broken down | 305 | 171 | 128 | 6 | 0.10 % |
| Parked illegally | 172 | 115 | 57 | 0 | 0.06 % |
| **Total** | 292,106 | 197,421 | 89,925 | 4760 | 100 % |

## Data availability

Some or all the data, models, and codes that support the findings of this study are available from the corresponding author upon reasonable request.

## References

- ### TRAFFIC SIGNAL CONTROL AT DISPLACED LEFT-TURN INTERSECTIONS USING AN LLM-BASED ACTOR-CRITIC ALGORITHM
	2026, Expert Systems with Applications
- ### Large language models driven adaptive proximal policy optimization for clean energy system frequency stability control
	2025, Sustainable Energy Technologies and Assessments
- ### Analytic Framework for Imbalanced Traffic Crash Type Classification and Management Using a Hybrid Tabular Transformer Approach
	2026, Transportation Research Record
- ### Risk prediction of road traffic accidents: a human-centered multi-factor analysis framework
	2025, Cognition Technology and Work

[View Abstract](https://www.sciencedirect.com/science/article/abs/pii/S095741742502069X)

[^1]: Table 8. Significant predictors for fatal accidents (SEVERITY=2) with *p* -value $<$ 0.05.

| Variable | Coefficient | Std. Error | *p* -value |
| --- | --- | --- | --- |
| **VEHICLE\_2\_COLL\_PT** |  |  |  |
| VEHICLE\_2\_COLL\_PT: Top/Roof | 2.490 | 1.054 | 0.018 |
| **DCA: Maneuvering** |  |  |  |
| 141: U-turn into fixed object/parked vehicle | 2.453 | 0.985 | 0.013 |
| 146: Reversing into fixed object/parked vehicle | 2.128 | 0.795 | 0.007 |
| 147: Vehicle strikes another vehicle when emerging from driveway | 0.587 | 0.271 | 0.030 |
| 148: Vehicle off footpath strikes veh on carriageway | 1.241 | 0.385 | 0.001 |
| 149: Other Maneuvering | 1.553 | 0.444 | $< 0.001$ |
| **DCA: On path** |  |  |  |
| 160: Vehicle collides with vehicle parked on left of road | 1.335 | 0.303 | $< 0.001$ |
| 162: Accident or broken down | 1.300 | 0.408 | 0.001 |
| 169: Other on path | 2.041 | 0.417 | $< 0.001$ |
| **DCA: Overtaking** |  |  |  |
| 150: Head on(overtaking) | 2.654 | 0.257 | $< 0.001$ |
| 151: Out of control (overtaking) | 1.604 | 0.574 | 0.005 |
| 152: Pulling out (overtaking) | 0.901 | 0.307 | 0.003 |
| 153: Cutting in (overtaking) | 1.031 | 0.449 | 0.022 |
| 154: Pulling out -rear end | 1.056 | 0.478 | 0.027 |
| **DCA: Passenger and miscellaneous** |  |  |  |
| 192: Struck train | 3.909 | 0.366 | $< 0.001$ |
| **DCA: Vehicles from adjacent directions(intersection only)** |  |  |  |
| 110: Cross-traffic(intersections only) | 0.589 | 0.220 | 0.007 |
| 113: Right Near (intersections only) | 0.489 | 0.227 | 0.031 |
| 118: Two left turning (intersections only) | 2.838 | 0.797 | $< 0.001$ |
| 119: Other adjacent (intersections only) | 1.220 | 0.306 | $< 0.001$ |
| **DCA: Vehicles from opposing directions** |  |  |  |
| 120: Head on (not overtaking) | 2.412 | 0.215 | $< 0.001$ |
| **DCA: Vehicles from same directions** |  |  |  |
| 132: Right rear | 0.696 | 0.283 | 0.014 |
| 135: Lane change left (not overtaking) | $-$ 0.756 | 0.336 | 0.025 |
| **VEHICLE\_MOVEMENT** |  |  |  |
| VEHICLE\_MOVEMENT: Not known | 1.472 | 0.667 | 0.027 |
| VEHICLE\_MOVEMENT: Out of control | 1.335 | 0.648 | 0.039 |
| VEHICLE\_MOVEMENT: Parked legally | 1.660 | 0.716 | 0.020 |
| VEHICLE\_MOVEMENT: U-turning | 1.513 | 0.692 | 0.029 |
| **SPEED\_ZONE** |  |  |  |
| SPEED\_ZONE: 80 | 1.559 | 0.774 | 0.044 |
| SPEED\_ZONE: 90 | 2.033 | 0.800 | 0.011 |
| SPEED\_ZONE: 100 | 2.738 | 0.774 | $< 0.001$ |
| SPEED\_ZONE: 110 | 3.070 | 0.785 | $< 0.001$ |

[^2]: Table 13. Accident distributioin by vehicle movement.

| Empty Cell | Empty Cell | Minor | Empty Cell | Empty Cell | Empty Cell |
| --- | --- | --- | --- | --- | --- |
| VEHICLE | Empty Cell | injury | Serious | Fatal | Empty Cell |
| \_MOVEMENT | Counts | accidents | accidents | accidents | Percentage |
| Going straight ahead | 139,290 | 93,248 | 43,471 | 2571 | 47.68 % |
| Turning right | 37,181 | 24,842 | 11,995 | 344 | 12.73 % |
| Out of control | 30,000 | 15,834 | 13,012 | 1154 | 10.27 % |
| Slow/stopping | 23,613 | 18,420 | 5082 | 111 | 8.08 % |
| Other stationary | 18,817 | 14,347 | 4373 | 97 | 6.44 % |
| Turning left | 10,437 | 7851 | 2516 | 70 | 3.57 % |
| Changing lanes | 6529 | 4455 | 1968 | 106 | 2.24 % |
| Not known | 4244 | 2865 | 1290 | 89 | 1.45 % |
| U-turning | 3933 | 2683 | 1212 | 38 | 1.35 % |
| Leaving a driveway | 2953 | 2170 | 764 | 19 | 1.01 % |
| Stationary accident | 2815 | 2165 | 635 | 15 | 0.96 % |
| Reversing | 2397 | 1739 | 637 | 21 | 0.82 % |
| Parked legally | 2277 | 1639 | 621 | 17 | 0.78 % |
| Overtaking | 1736 | 1093 | 583 | 60 | 0.59 % |
| Merging | 1662 | 1209 | 442 | 11 | 0.57 % |
| Avoiding animals | 1590 | 1072 | 511 | 7 | 0.54 % |
| Parking or unparking | 1541 | 1163 | 374 | 4 | 0.53 % |
| Wrong way | 614 | 340 | 254 | 20 | 0.21 % |
| Stationary broken down | 305 | 171 | 128 | 6 | 0.10 % |
| Parked illegally | 172 | 115 | 57 | 0 | 0.06 % |
| **Total** | 292,106 | 197,421 | 89,925 | 4760 | 100 % |