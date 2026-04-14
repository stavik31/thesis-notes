---
title: "CrashSage: A large language model-centered framework for contextual and interpretable traffic crash analysis"
source: "https://www.sciencedirect.com/science/article/pii/S3050860625000304"
author:
  - "[[AbstractRoad crashes claim over 1.3 million lives annually worldwide and incur global economic losses exceeding $1.8 trillion. Such profound societal and financial impacts underscore the urgent need for road safety research that uncovers crash mechanisms and delivers actionable insights. Conventional statistical models]]"
  - "[[machine learning along with modern deep learning models]]"
  - "[[typically rely on structured crash data]]"
  - "[[overlooking contextual nuances]]"
  - "[[such as narrative elements related to multi-vehicle interactions]]"
  - "[[crash progression]]"
  - "[[and rare event characteristics]]"
  - "[[and struggling to capture complex interactions and underlying semantics. This study presents CrashSage]]"
  - "[[a novel Large Language Model (LLM)-centered framework designed to transcend these limitations and advance traffic safety analysis and modeling. Particularly]]"
  - "[[CrashSage introduces four key innovations to transform raw data into actionable intelligence. First]]"
published:
created: 2026-04-08
description: "Road crashes claim over 1.3 million lives annually worldwide and incur global economic losses exceeding $1.8 trillion. Such profound societal and fina…"
tags:
  - "clippings"
---
[https://doi.org/10.1016/j.ait.2025.100030](https://doi.org/10.1016/j.ait.2025.100030 "Persistent link using digital object identifier")

Under a Creative Commons [license](http://creativecommons.org/licenses/by-nc-nd/4.0/)

Open access

## Highlights

- •
	Introduces CrashSage, an LLM framework for interpretable crash analysis.
- •
	Fine-tunes LLaMA3-8B, outperforming state-of-the-art tabular models and baseline LLMs.
- •
	Gradient-based attribution reveals word-level crash severity risk factors.
- •
	Co-occurrence analysis uncovers interdependent patterns among safety dimensions.

- [Next article in issue](https://www.sciencedirect.com/science/article/pii/S3050860625000328)

## Keywords

Road safety

Traffic crashes

Crash severity inference

Large language models

Explainable AI (XAI)

Tabular-to-text transformation

Supervised fine-tuning

Gradient-based explanation

Agentic AI

## 1\. Introduction

Traffic crashes remain a persistent global public health crisis, resulting in over 1.3 million fatalities annually and imposing economic costs estimated at more than $1.8 trillion. In the United States alone, approximately 42,000 lives are lost each year, despite continuous advancements in vehicle safety features, roadway design improvements, and safety policy implementation (). This enduring challenge highlights the inherently complex and multifaceted nature of traffic crashes, which result from dynamic interactions among human factors, vehicle characteristics, environmental conditions, and infrastructure elements.

The complexity of traffic safety analysis lies in capturing the intricate relationships between these factors. Human factors (e.g., variations in physical and physiological status, attentiveness levels, risk-taking behaviors, and social responsibility) interact with dynamic vehicle movements, changing weather conditions, and diverse roadway conditions and characteristics. This complexity necessitates sophisticated analytical approaches that can effectively model these high-dimensional interactions to develop context-aware, targeted interventions and policies.

For decades, the cornerstone of traffic crash analysis has been the application of statistical and econometric methods to infer potential relationships from observational data (). Depending on the target, these classic models often have well-defined model structures, with specific considerations on proxy variables and error distributions to account for overdispersion and/or unobserved heterogeneity (,,,,,,,, ). While with simplified structures, these models offer the distinct advantage of explicit interpretability, their efficacy is fundamentally constrained by restrictive underlying assumptions, including predefined functional forms and specific error distributions. These limitations inhibit their capacity to capture the complex non-linearity and high-order interactions inherent in real-world crash phenomena. Besides, designing a clear causal structure and properly considering potential confounding effects requires substantial domain knowledge, which also introduces subjectivity. Moreover, these models rely exclusively on structured tabular data, thereby discarding the rich contextual information contained in the crash records.

In response to these constraints, and driven by a well-documented trade-off between explanatory power and predictive performance, the field has increasingly turned to machine learning (ML) and deep learning approaches (). A progression of models, from early explorations with Support Vector Machines and neural networks to the more recent dominance of tree-based ensembles like Random Forest (, ), XGBoost (), and CatBoost (, ), demonstrated superior predictive accuracy by flexibly modeling complex data relationships without rigid a priori assumptions (, ). Transformer-based architectures have recently pushed performance boundaries even further (, ). To interpret model outcomes, post-hoc explainability techniques, such as permutation importance (, ), SHapley Additive exPlanations (SHAP) (, ), and attention heatmaps (), have been employed. Nevertheless, these explanations often offer fragmentary descriptions of variable salience without revealing progressive logic or temporal sequencing.

Despite their methodological differences, both classic statistical and ML approaches share a more profound, unifying limitation: their nearly exclusive reliance on structured, tabular data (). This data format, while efficient for storage and retrieval, is inherently limited to capture the rich, sequential, and semantic context embedded in the textual narratives of crash records. For instance, a numeric code like ‘7’ may be used to represent both “Left or Right turn” and “U-turn” maneuvers. While computationally convenient, this encoding discards the critical distinction between maneuvers with fundamentally different risk profiles and strips away the narrative fabric of an incident, reducing it to a set of disconnected variables, where left turns at intersections typically involve conflict with oncoming traffic while U-turns present unique sight distance and gap acceptance challenges. It also discards the semantic meaning that is readily understandable to a human and, now importantly, to an advanced language model. Critical contextual information, such as the specific sequence of pre-crash maneuvers, driver intent and decision-making process, environmental conditions that influenced the maneuver choice, sight line obstructions, the presence of traffic control device, and the complex interactions among multiple vehicles during turning movements, is often lost or oversimplified in the simple categorical coding. In traffic safety analysis, this information granularity sometimes are crucial because different crash circumstances, maneuvers, environmental conditions, and behavioral factors are associated with distinct crash patterns, severity outcomes, and potential causal mechanisms that require tailored countermeasures and interventions.

The recent revolution in Natural Language Processing (NLP), spurred by the development of the transformer architecture (), offers a possible solution to this long-standing challenge. The evolution of large language models, from encoder-only architectures like BERT (), RoBERTa (), and ELECTRA () to decoder-only variants including the GPT series (, ) and LLaMA (), has demonstrated remarkable generalization capabilities across diverse domains (,, ). The unique advantages of LLMs in crash analysis stem from two key strengths: (1) their ability to process and derive insights from unstructured textual narratives, which often contain rich contextual information that is lost in structured tabular formats; and (2) the extensive world knowledge embedded within their pretrained parameters, which may enable reasoning about complex circumstances described in textual narratives.

The application of Large Language Models (LLMs) within the transportation sector is experiencing a significant and rapid transformation (,,, ). Initial studies demonstrated the utility of LLMs in enhancing specific tasks (), such as traffic prediction with spatiotemporal semantic context (), multimodal traffic scenario understanding with point cloud, image, and language data pairs (), video-based traffic accident analysis with multimodal large language models (), chatbot for transportation surveillance and management (), optimization of real-time traffic control through natural language interfaces (), high-fidelity simulation environments generation (), communication facilitation between vehicles and users (). However, the LLMs application in traffic safety domain remain limited, especially for traffic crash analysis.

Some recent studies on applying LLMs to traffic safety have shown strong promise. For example, a multi-modal approach combining structured data with textual narratives using a pre-trained ELECTRA encoder () demonstrated improved performance in crash severity inference, particularly for underrepresented fatal and serious injury cases (). Importantly, its interpretability aligned with findings from classic statistical models, validating its ability to capture domain-relevant insights (). A subsequent study systematically evaluated the zero-shot and few-shot reasoning capabilities of general-purpose LLMs, revealing that while prompting strategies like Chain-of-Thought can elicit domain-relevant insights, these models still face limitations in specialized traffic safety reasoning (). Despite these advances, critical gaps persist: current methods often treat crashes as isolated incidents, failing to leverage the relational structure of crash databases; they rely on generic models that lack domain-specific knowledge; and their interpretability is confined to high-level feature importance, lacking systematic, granular reasoning traces.

provides a comparative overview of the different methodological approaches to crash analysis, highlighting their respective input data requirements, interpretability characteristics, and key limitations. By leveraging unstructured crash narratives, LLMs can preserve the richness and completeness of crash events by utilizing extensive contextual information, maintaining sequential flow of actions as the event unfolds, and capturing multi-vehicle interactions that are often fragmented or lost in traditional tabular formats. Furthermore, LLMs are capable of generating natural language explanations that mirror human reasoning, offering intuitive and comprehensive insights into the dynamics of crash events. Unlike abstract feature importance scores, these explanations are easily interpretable by transportation officials and safety practitioners, even without specialized technical expertise.

Table 1. Comparison of methods used in crash severity analysis.

| Method | Input Data | Interpretability | Limitations |
| --- | --- | --- | --- |
| Econometric and Statistical Methods | Structured data | Explicit, model-based | Assumes fixed functional forms, limited complexity, lacks context |
| Tree Ensemble Models | Structured data | SHAP-based feature importance | Lacks context, needs feature engineering |
| Large Language Models (LLMs) | Unstructured data with context | Natural language explanations | Computationally expensive, potential biases |

This study presents CrashSage, a novel framework specifically designed to address critical gaps in crash analysis through four principal contributions. First, we develop a comprehensive *tabular-to-text transformation* method along with relational data integration schema that converts raw, heterogeneous crash data from Washington State datasets into richly detailed textual narratives, thereby preserving crucial structural and relational information commonly lost in conventional tabular formats. Second, we implement *context-aware data augmentation* via LLaMA-8B, enhancing the coherence of these crash narratives while rigorously maintaining factual accuracy. Third, we perform *supervised fine-tuning* of a LLaMA3-8B model () tailored for crash severity inference, demonstrating competitive and better performance against a comprehensive suite of baselines, including state-of-the-art tabular models (CatBoost, TabTransformer, FT-Transformer) and various prompting strategies (zero-shot, zero-shot with chain-of-thought, and few-shot learning) with popular LLM models (GPT-4o, GPT-4o-mini, LLaMA3-70B ). Finally, we integrate a *gradient-based explainability* strategy to illuminate model decisions at both the individual crash level and in broader risk factor co-occurrence analyses. This interpretability mechanism not only enhances transparency and trustworthiness in model outputs but also provides actionable insights for targeted interventions in road safety management through a deeper understanding of how diverse factors interact to influence crash outcomes. This level of granular, context-aware interpretability yields explanations that are intuitive and directly understandable at a linguistic level, making the insights more accessible to safety practitioners and especially valuable for informing targeted traffic safety interventions. It goes beyond identifying isolated risk factors to uncovering their complex interplay, revealing, for example, how driver behaviors like intoxication act as central nodes that connect with environmental and infrastructure risks. This deep analysis highlights dangerous synergistic effects, such as the combination of impairment and excessive speed, offering a more holistic view of underlying crash mechanisms.

The CrashSage framework represents a paradigm shift in traffic safety analysis by introducing a specialized analytical agent for crash investigation and traffic safety analysis. In this role, CrashSage is designed to emulate the cognitive workflow of a human expert, transforming sparse crash records into actionable narratives. This approach enables transportation agencies to effectively identify comprehensive risk factors and associated mitigation strategies owning to the agent’s reasoning capability. By leveraging the semantic understanding capabilities of LLMs while maintaining explainability, our framework bridges the gap between advancement in AI and practical deployment in safety-critical transportation applications, serving as a cognitive assistant for safety professionals.

## 2\. Literature reviews

This section provides a comprehensive review of the methodological advancements that have shaped crash modeling over time, beginning with traditional econometric and statistical methods, through the rise of machine learning and deep learning techniques, and to recent integration of natural language processing (NLP) and large language models (LLMs). By examining the strengths, limitations, and interpretability of each approach, this section lays the foundation for our Crashsage framework introduced in this study. Specifically, we examine recent NLP- and LLM-based studies, including interpretability methods pertinent to safety-critical deployment, and situate our work within the broader context of LLM applications in transportation systems. Collectively, this review highlights the gap for domain-adapted, interpretable LLMs capable of leveraging narrative crash data, which directly motivates the design of CrashSage.

### 2.1. Econometric and statistical methods in traffic crash modeling

The analysis of traffic crashes is inherently complex due to the multifaceted nature of their occurrence. Crashes seldom result from a single cause but rather from a confluence of interacting factors related to human behavior, vehicle characteristics, roadway design and conditions, and prevailing traffic and environmental contexts. Determining the precise causal chain for any given crash, or crash patterns, is a challenging task. Modeling efforts in traffic safety are therefore directed towards unraveling these intricate interactions, with a significant focus on understanding and modeling crash outcomes, such as crash types, injuries, and severity.

Key tasks in this domain include the accurate modeling of crash severity levels, such as fatal, serious injury, minor injury, or property damage only, to better inform road safety measures and reduce casualties (, ). This involves analyzing the complex relationships between various accident characteristics and the resultant injury severity. Modeling efforts also extend to differentiating and analyzing various crash types, such as single-vehicle versus multi-vehicle collisions (), or specific impact types like run-off incidents (), to understand their distinct causal mechanisms. A primary objective across these tasks is the identification of significant contributing factors to specific crash outcomes and their relative importance. These insights help to develop targeted safety measures to reduce crash severity and improve road safety.

Traffic safety research is fundamentally concerned with understanding the causality of crashes. Since controlled experiments are impractical and ethically unfeasible in this domain, researchers have long relied on analyzing historical observational data to infer causal relationships (). The traditional approach has been to employ statistical and econometric methods to model the relationships between crash outcomes, often referred as endogenous variables, and a wide range of contributing factors, referred as exogenous variables, such as driver behaviors, vehicle characteristics, roadway design, and environmental conditions (,,,,,, ). This line of work has been the cornerstone of traffic safety research, providing critical insights for developing safety guidelines and countermeasures.

However, crash data possesses unique statistical properties that demand more specialized methodologies. Recognizing characteristics such as the discrete count nature of crashes, overdispersion, where variance exceeds the mean, and the presence of a high proportion of zero counts, referred as zero-inflation, researchers progressively adopted more sophisticated models (). To handle datasets with excess zeros, for instance, specialized models are employed. Zero-Inflated Poisson (ZIP) () and Zero-Inflated Negative Binomial (ZINB) models () assume that zero counts arise from distinct processes: a “structural zero” state, where an event is inherently impossible and a “sampling zero” state where an event was possible but not observed. The ZINB model is particularly adept at handling both excess zeros and overdispersion simultaneously. Hurdle models offer an alternative two-part approach (), first modeling the probability of a zero versus a positive outcome, and then modeling the magnitude of the positive outcomes, providing a better statistical fit and more nuanced interpretations.

Beyond the data distribution properties, a more profound challenge lies in addressing the critical issue of unobserved heterogeneity: the unmeasured factors that vary across the dataset and influence crash outcomes. To tackle this, the field has developed more sophisticated models. Random parameters (mixed) logit models (,,, ) address this by allowing the parameters of explanatory variables to vary across observations, following a specified probability distribution, thus capturing continuous heterogeneity. Other examples include random parameters ordered probability models (, ). Latent class models (, ) offer another approach, assuming the data are drawn from a finite number of unobserved segments or classes, each with distinct relationships between variables, thereby capturing discrete heterogeneity. Furthermore, because traditional models often assume static relationships over time, markov switching models () have been introduced to capture temporal dynamics and state-dependent behaviors. These models assume the process can stochastically switch between multiple unobserved safety states (e.g., “low-risk” vs. “high-risk” regimes), allowing the effects of covariates to change depending on the prevailing state.

The progression of these statistical models, from basic econometric forms to advanced techniques accounting for zero-inflation, overdispersion, unobserved heterogeneity, and temporal dynamics, reflects a continuous effort to move beyond mere correlational findings towards more robust, and ideally, causal inferences. Each layer of complexity represents an attempt to control for unobserved confounding variables or to more accurately represent the true data, with the overarching goal of minimizing biases in estimating the endogenous variables. A comprehensive review of these techniques can be found in.

However, despite their sophistication, these statistical models have fundamental limitations. Their efficacy is constrained by restrictive underlying assumptions, including predefined functional forms and specific error distributions, which limit their ability to capture the complex nonlinearity and high-order interactions that are pervasive in real-world crash data. Moreover, while they offer the significant advantage of explicit interpretability, their specification requires substantial domain knowledge, which sometimes controversial, introducing a degree of subjectivity into the modeling process. Consequently, addressing unobserved effects remains an active and challenging area of research, and the choice of a specific model must be rigorously justified.

As previously mentioned, their reliance on structured data leads to a more profound limitation, common to both traditional statistical and conventional machine learning methods. The structured, tabular format, while efficient for storage and retrieval, is inherently limited to capture the rich, sequential, and semantic context embedded in the textual narratives of police crash reports.

A central debate in the field has been the well-documented tradeoff between a model’s explanatory power and its predictive performance (). While traditional econometric models excel at providing interpretable parameters, their predictive fidelity is often constrained by rigid functional forms that cannot adequately model the complex, non-linear, and high-order interactions inherent in crash mechanisms. In contrast, machine learning (ML) and deep learning models achieve superior predictive power because of their expressivity to flexibly model intricate relationships directly from data. Historically, the adoption of these advanced models has been constrained by concerns over their transparency, often characterized as “black boxes”.

However, due to the rapid evolvement of eXplainable AI (XAI) (), the conventional dichotomy between predictive accuracy and interpretability is dissolving. Contemporary research, including the frameworks recently developed (), demonstrates that it becomes more feasible to construct models that unify high predictive accuracy with granular, meaningful interpretability (). This synthesis facilitates a more powerful form of analysis that addresses two key limitations of classical methods: their restricted capacity to model complex, non-linear interactions and their structural inability to utilize rich, unstructured data.

### 2.2. Machine learning in traffic crash inference and modeling

Early studies in traffic safety research, specifically in crash modeling, explored machine learning algorithms, primarily focusing on comparative assessments against traditional statistical models. Among the early efforts, Hassan and Mohamed () investigated the use of Multi-Layer Perceptron (MLP) and fuzzy adaptive resonance theory neural networks to predict driver injury severity levels at signalized intersections. Their results showed that the MLP model outperformed the traditional ordered logit model, achieving improved accuracies of 6.7 % and 3.3 % on the training set and the validation set, respectively. Building on these neural network approaches, developed an support vector machine (SVM) model for predicting injury severity in individual crashes and compared its performance against a baseline ordered probit model. The SVM model demonstrated 4.8 % increase in overall accuracy, with notable improvements in minority classes such as incapacitating injury (2.3 %) and fatal injury (1.7 %), while maintaining comparable effectiveness in evaluating explanatory variables. These early studies collectively demonstrated that machine learning techniques could offer meaningful performance improvements over traditional statistical approaches, particularly in handling complex patterns and minority class predictions.

More recently, tree-based algorithms, particularly tree ensembles (), have proven highly effective in crash modeling due to their capacity to capture non-linear relationships and handle categorical variables. were among the first to apply CART for predicting traffic injury severity, incorporating variables related to drivers, environment, crash circumstances, and vehicles. Their study underscored CART’s potential as a robust tool for predictive modeling and analysis. As decision tree methods evolved, researchers began evaluating their performance against other techniques. utilized this approach with a set of screened important variables to assess driver injury severity in rollover crashes in New Mexico. They conducted variable screening process using a Classification and Regression Tree (CART) model and employed pseudo-elasticity analysis to demonstrate the influence of variables on injury outcomes. assessed several models for classifying injury severity levels, including Logistic Regression, Decision Trees, Neural Networks, Gradient Boosting Models, and Naïve Bayes classifiers. They reported the highest classification performance using a bagging ensemble of decision trees, particularly when combined with over-sampling to address class imbalance. Further advancing tree-based methods, introduced a hybrid algorithm based on the Light Gradient Boosting Tree, which outperformed other machine learning algorithms across multiple evaluation metrics. Similarly, found that the Random Forest algorithm delivered superior accuracy in predicting traffic crash severity compared to Logistic Regression, Naive Bayes, and AdaBoost.

With the emergence of deep learning techniques, researchers began applying Convolutional Neural Networks (CNNs) and Recurrent Neural Networks (RNNs) to traffic safety modeling. employed a Long Short-Term Memory (LSTM) model for predicting traffic accident severity, demonstrating its superior performance compared to conventional MLP and Bayesian Logistic Regression models. Taking a different approach, introduced the Traffic Accident Severity Prediction-CNN (TASP-CNN) to enhance prediction accuracy by considering combination relationships among accident features and utilizing the Feature Matrix to Gray Image algorithm. Their model outperformed nine baseline methods, particularly excelling in predicting fatal crashes. Building on CNN-based methods, implemented a 2D CNN model for crash severity prediction and introduced an innovative approach to interpreting factor influence by leveraging the model’s learned embedded representations rather than relying on conventional SHAP values.

The latest advancement in traffic safety modeling is the exploration of transformer-based architectures (). A recent study by introduced the Feature Group Tabular Transformer (FGTT), a novel approach that organizes traffic crash data into semantic feature groups, represented as tokens within a transformer framework. Their model leverages a comprehensive dataset fused from multiple sources including weather data, crash reports, traffic information, and pavement characteristics, enabling a more comprehensive and contextualized analysis of crash events. Evaluation results showed that FGTT outperformed traditional tree ensemble methods (Random Forest, XGBoost, and CatBoost) in predicting crash types. Furthermore, attention weight analysis revealed that event-specific attributes and their interactions with driver-related features were most influential in determining crash outcomes. This work demonstrates the potential of transformer architectures to enhance both predictive performance and interpretability in traffic safety modeling.

In summary, recent studies have shown that deep learning models not only outperform traditional methods in traffic safety modeling but also offer promising avenues for interpretability (, ). As the field continues to progress, deep learning models are expected to become more accurate, transparent and explainable within the traffic safety domain.

### 2.3. LLMs in traffic crash modeling and analysis

While machine learning and deep learning approaches have demonstrated advanced predictive performance over traditional statistical methods, they share a critical limitation with their econometric and statistical method predecessors: a fundamental reliance on structured, tabular data. This dependency necessitates that all information, including the rich contextual details embedded in the crash records, be pre-processed and encoded into numerical or categorical features. Such encoding inevitably leads to substantial information loss, as crucial narrative elements regarding pre-crash sequences, driver intent, witness observations, and the complex interplay of contributing factors are either oversimplified or discarded. The field of Natural Language Processing (NLP), particularly following the emergence of the transformer architecture (), offers a compelling solution to this long-standing limitation.

Early applications of NLP in traffic safety focused primarily on information mining from unstructured text. Researchers employed traditional text mining techniques, utilizing uni-gram and bi-gram tokenization () combined with established machine learning classifiers. These foundational studies demonstrated the feasibility of automated text analysis in safety contexts, with support vector machines and random forests successfully categorizing construction accidents (), XGBoost proving effective for pedestrian crash classification (), and logistic regression identifying secondary crashes from narrative reports (). More sophisticated applications incorporated semantic analysis to identify hazardous driver maneuvers () and employed interpretable machine learning techniques like local interpretable model-agnostic explanations (LIME) () to extract injury severity determinants from narratives involving specific crash types (, ).

A recent line of work moves beyond using NLP purely as a feature extractor and instead treats language as a main modality in traffic crash modeling. In Tab-Text (), the authors propose a multi-modal paradigm that integrates numeric and categorical crash attributes with constructed textual narratives, learned end-to-end via a transformer-based ELECTRA encoder () for text and MLP heads for tabular features, followed by feature fusion. This design preserves semantic richness and reduces the information loss. Empirically, Tab-Text outperforms strong baselines—MNL, CatBoost, T2T-Transformer, and AT-Transformer—on multi-class crash severity inference, achieving higher macro-F1 (0.4587) and micro-accuracy (0.7152), with the greatest gains on rare but critical fatal and serious injury level crash cases. The ablation study confirm that narratives are essential, as removing them lowers performance (macro-F1 from 0.4587 to 0.3946) and reduces accuracy on fatal/serious injury classes. Visualization and confusion-matrix analyses further show clearer severity separation when narratives are included. For interpretability, permutation importance highlights predictors consistent with econometric models (e.g., DCA, speed zone, vehicle movement).

Nonetheless, these early explorations primarily utilized NLP as a feature extractor, ultimately feeding processed text features into conventional machine learning pipelines. The true paradigm shift arrived with the advent of Large Language Models (LLMs), beginning with encoder architectures like BERT () and evolving through decoder-only models including the GPT series () and LLaMA (). These foundation models, pre-trained on vast text corpora, show emergent properties and behaviors to understand context, capture semantic relationships, and perform complex reasoning tasks (). The transformer-based architecture enables them to model long-range dependencies and extract detailed patterns from textual data, capabilities particularly useful for analyzing the multifaceted narratives found in crash reports.

Despite this transformative potential, the application of modern LLMs in traffic safety analysis remains limited. The few existing studies have shown promise but suffer from significant constraints. Applications using BERT have typically been restricted to narrow, binary classification tasks () or have lacked rigorous comparison to established baselines (). Early explorations in the broader transportation sector, including transit optimization () and traffic forecasting (), have revealed additional challenges: most approaches employ general-purpose models without domain-specific adaptation. They treat LLMs as isolated analytical tools rather than integrated components of comprehensive frameworks. Most importantly, they fail to address the transparency or interpretability concern, which is an essential requirement for safety-critical applications.

Complementary to the data-centric, multi-modal direction, investigates model-centric use of state-of-the-art LLMs as zero/few-shot analysts via prompt engineering and chain-of-thought (CoT) reasoning. The study (i) constructs textual inputs from crash records and (ii) systematically benchmarks general-purpose LLMs under standard prompting, in-context learning, and CoT variants, reporting performance against conventional baselines and analyzing where reasoning helps or fails. Recognizing that generic models may lack the specialized knowledge required for traffic safety analysis, it is essential to explore how domain-specific fine-tuning can create models that not only achieve better inference performance but also provide transparent, actionable insights through advanced interpretability mechanisms, which is the main motivation of this study.

#### 2.3.1. LLM interpretability for traffic safety

The application of machine learning in high-stakes domains such as traffic safety is contingent upon interpretability, which is essential for building stakeholder trust, enabling scientific discovery, and ensuring accountability (, ). While traditional statistical methods offer transparency through model coefficients, the architectural complexity of Large Language Models (LLMs) often renders their internal logic opaque. This lack of transparency is a critical impediment to adoption, as understanding why a model makes a certain inference is as vital as the inference itself for validation, refinement, and real-world implementation. This section reviews the primary paradigms of LLM explainability, with a particular focus on the gradient-based methods that inform the design of our CrashSage framework.

To address the “opaque-box” nature of LLMs, researchers have developed robust local explanation techniques, which clarify how a model arrives at a prediction or inference for a specific input (). Early approaches often relied on visualizing attention mechanisms (); however, subsequent studies revealed that attention weights are not always a faithful proxy for a model’s reasoning process (, ). Consequently, more rigorous explainability methods have emerged. Among them, feature attribution is the most widely used, assigning a relevance score to each input token to quantify its contribution to the final prediction (). Feature attribution encompasses several approaches, including perturbation-based methods that systematically alter input features to measure the corresponding change in the model’s output (); surrogate models, such as LIME () and SHAP (), which approximate the complex LLM’s behavior with a simpler, interpretable model in the local vicinity of a single prediction; and gradient-based methods, including Integrated Gradients (), which leverage the model’s internal architecture to directly calculate the influence of input features. Complementing these are example-based methods, which explain predictions by identifying which training instances were most critical for a given outcome through techniques, such as influence functions ().

While each approach offers valuable insights, we chose gradient-based attribution in light of several key advantages. Firs it is highly computationally efficient compared to perturbation-based techniques, which require numerous model evaluations. More importantly, it provides a high degree of faithfulness by directly using the model’s learned parameters to calculate feature importance (). It avoids the use of simplified surrogate models and bypasses the main pitfall of perturbation: the generation of artificial, potentially out-of-distribution data samples that can lead to unreliable explanations (). Furthermore, gradient-based techniques are grounded in strong theoretical foundations, satisfying axioms like completeness and input invariance that ensure a principled and reliable attribution of a prediction to its input features ().

The interpretation of our CrashSage framework builds upon gradient-based attribution to assess the influence of input tokens on specific model outputs. Specifically, a Taylor approximation is used to quantify how the presence or absence of individual tokens influences output probabilities. By normalizing these attribution scores, the method yields a robust measure of each token’s contribution to the model’s prediction.

Nonetheless, adapting general explanation methods to transportation safety requires domain-specific considerations. Crash narratives contain specialized terminology and causal sequences that must be interpreted through the lens of traffic engineering principles. Accordingly, our framework refines general attribution methods by tailoring model hyperparameters and fine-tuning procedures to align with valuable historical crash data. These adaptations ensure that the resulting explanations accurately reflect model behavior, which captures the reality. Our interpretability approach operates across multiple levels of granularity. At the individual crash level, token-level attributions identify critical factors influencing severity predictions. At a broader scale, as demonstrated in, analyzing attribution patterns across numerous incidents reveals systemic safety issues, particularly through the co-occurrence analysis of high-attribution factors. This multi-level strategy moves beyond isolated factor analysis to uncover compound effects and interaction dynamics, providing a more holistic understanding of potential crash mechanisms that are critical for developing targeted safety interventions.

### 2.4. LLMs application in transportation

Modern transportation systems are characterized by a profound cyber-physical-social complexity, facing persistent challenges of congestion, sustainability, and resilience in dynamic urban environments (). For decades, Intelligent Transportation Systems (ITS) have been developed to manage these challenges, leading to significant advances in traffic management and operational efficiency. However, traditional ITS architectures often rely on static models and fragmented data pipelines (), struggling to leverage the rich contextual information embedded in unstructured data sources such as accident reports or real-time social media feeds. This reliance on structured data and specialized algorithms limits their adaptability and responsiveness to real-world transportation challenges.

The recent and rapid transformation of the transportation sector has been spurred by the application of Large Language Models (LLMs) (,,, ). With emergent capabilities in natural language understanding, in-context learning, and human-like reasoning, LLMs represent a critical transition from sensor data-driven ITS to more sophisticated human-level perception and reasoning systems. Unlike traditional models, LLMs are pre-trained on vast corpora, imbuing them with extensive world knowledge that allows them to harness and interpret transportation data from various sources through the lens of hierarchical semantic contexts, moving from statistical prediction toward a smarter form of perception and reasoning.

Initial applications have demonstrated the versatility of LLMs by casting them into distinct agent roles across operational and planning tasks (). Frameworks like LLMLight (), for instance, use LLMs as human-like decision-makers to optimize traffic signal timing, offering better generalization and explainability than traditional reinforcement learning methods (,, ). In autonomous driving, models such as DriveGPT4 () and GPT-Driver () position the LLM as a central cognitive engine capable of end-to-end control while generating natural language rationales for its actions (, ). Concurrently, another line of research deploys LLMs as simulation agents, acting as proxies for human travelers within Agent-Based Models (ABMs) to simulate complex travel behaviors and forecast system outcomes under new policies (,, ). A third emerging role is the interfacing agent, which democratizes access to complex tools. Applications like ChatSUMO (), for example, allow planners to generate traffic scenarios using natural language commands, transforming the user experience from technical programming to conversational instruction. This conversation-style has been extended to broader applications where LLMs function as conversational assistants to help planners query databases, interpret simulation outputs, and even draft policy documents ().

Complementing these agent-centric roles, other initial studies have demonstrated the utility of LLMs in enhancing specific understanding and perception tasks. These include improving traffic prediction by incorporating spatiotemporal semantic context (), benchmarking LLM capabilities in crash analysis (), enabling multimodal traffic scenario understanding from point cloud, image, and language data pairs (), performing video-based traffic accident analysis (), and powering chatbots for transportation monitoring and management ().

These pioneering efforts primarily focus on LLMs as either operational agents for real-time control or as simulation agents for predictive planning. However, despite their promise, a significant gap remains in their applications to retrospective traffic safety analysis, a domain critical for developing effective, evidence-based interventions. Existing safety studies have been limited, often employing general-purpose models without domain-specific adaptation () and failing to provide interpretability required for safety-critical applications ().

To bridge the gap, this paper introduces the CrashSage framework, which proposes a novel role for LLMs as a specialized analytical agent focused on crash investigation and reasoning. In contrast to operational agents that optimize traffic flow, CrashSage is designed to emulate the cognitive workflow of a transportation safety expert to understand potential crash causality. The framework moves beyond generic prompting () by introducing a systematic methodology that first transforms structured, tabular crash records into rich contextualized narratives. Subsequently, a domain-specific LLM is fine-tuned for crash severity inference. Importantly, CrashSage integrates a gradient-based explanation mechanism that provides word-level attribution, illuminating precisely which factors influence the model’s crash severity inference. By focusing on deep, interpretable, and domain-adapted analysis, the CrashSage framework demonstrates a unique and vital application of LLMs, bridging the gap between advanced AI and the need of transportation safety professionals for explainable, evidence-driven crash analysis.

## 3\. Data sources and processing

This study leverages Washington traffic crash datasets, sourced from the Washington State Department of Transportation (WSDOT), encompassing crash records from 2020 to 2022. It has four different table, including crash table, road segment table, vehicle/unit table, and person table. Transportation crash data is typically stored in structured relational databases with complex schema that separate information across multiple tables. While this structure was designed for storage and querying, it presents challenges for natural language processing applications. To address this, we utilized relational database schema combined with tabular-to-text transformation technique, introduced in the subsequent section, to convert structured crash data into coherent narrative descriptions.

### 3.1. Relational schema for crash data integration

Our framework employs a relational schema, detailed in ) to integrate heterogeneous crash data sources through four normalized tables: Crash, Road Segment, Vehicle, and Person. The crash table forms the core entity with primary key CASENO, containing spatiotemporal attributes (location, timestamp) and environmental conditions. Through foreign key relationships, each crash record links to its corresponding Road Segment via spatial matching between MILEPOST and segment boundaries (FROM\_MEASURE, TO\_MEASURE), ensuring accurate geolocation mapping.

![Fig. 1](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-gr1.jpg)

Download: Download high-res image (477KB)

The schema maintains data integrity through hierarchical one-to-many relationships: each crash record connects to multiple vehicle entries through CASENO, and each vehicle/unit links to multiple person records. This structure preserves the natural hierarchy of crash events while enabling efficient querying of participant-level details. We implemented this schema through a nested dictionary structure, with JSONL serialization facilitating language model integration through instruction-based learning templates.

Initial analysis revealed a severe disparity between ‘No Apparent or Minor Injury’ cases ($n = 49 , 648$) and ‘Serious injury or fatal’ crashes ($n = 1 , 779$). To address the class imbalance, we employed a stratified down-sampling approach, resulting in a more balanced dataset, comprising 2654 no apparent or minor injury cases and 1779 serious injury or fatal cases.

### 3.2. Tabular-to-text transformation

The tabular-to-text conversion pipeline transforms structured crash records into natural language narratives through a two-phase process: semantic normalization and template-based generation. In the normalization phase, numerical codes are mapped to natural language descriptors using domain-specific lexicons, translating categorical encoding into human-interpretable terms while removing duplicates and non-informative null values. The subsequent template-based generation uses fill-in-the-blank templates, illustrated below, to construct coherent, chronological event sequences that highlight key crash dynamics, enabling the generation of context-rich crash narratives suitable for analysis by LLMs.

> On \[date\], a \[day of week\] at \[time\], an accident involving \[number\] vehicles occurred \[lighting conditions\], with \[weather conditions\]. The road condition at the time was \[surface condition\]. The accident took place on \[road name\] (\[road type\])...

Particularly, we structurally separate descriptive narratives (pre-crash conditions, collision mechanics) from outcome related narratives (injury severity, vehicle damage). This division support supervised learning objectives and enables models to learn potential causal relationships between antecedent conditions and resulting consequences.

Consequently, the transformation yields LLM-readable narratives that preserve relational semantics through natural language encoding. This methodology effectively bridges structured crash analytics with unstructured text processing capabilities, facilitating direct application of LLMs to transportation safety analysis while maintaining computational tractability.

## 4\. CrashSage framework

In this section, we introduce the design of the CrashSage, which integrates structured crash records with large language models (LLMs) to enable domain-adapted inference and interpretation in traffic safety analysis. We first introduce the overall system architecture, followed by the description of its three key components: (1) context-aware data augmentation to improve narrative coherence while preserving factual integrity, (2) supervised fine-tuning of LLMs for crash severity inference, and (3) gradient-based explanation techniques that provide interpretable, aspect-aware insights into model decisions. Together, these components form a cohesive pipeline for both accurate prediction and transparent explanation in crash analysis.

### 4.1. System architecture overview

Our CrashSage framework presented in offers a comprehensive approach to traffic safety analysis through the integration of LLMs with structured crash data. At its foundation, the framework utilizes entity-oriented analysis, leveraging the *Crash, Vehicle, Person, and Road/Unit* tables, each containing specific attributes that characterize different aspects of crash events. These structured data sources undergo a sequential transformation process beginning with a relational database schema that organizes the hierarchical relationships between entities (), followed by a Tabular-to-Text Transformation that converts structured records into coherent narratives (described previously in ). The resulting template-based narratives are further refined through context-aware data augmentation using a pretrained LLM agent (referred to as the base LLM in this paper), which improves textual coherence while preserving factual accuracy. The augmented narratives serve as the training data for the following supervised fine-tuning of our CrashSage agent, another LLM specialized in traffic safety domain. Additionally, the analytical capabilities of our framework are enhanced through gradient-based explainability methods, which offer interpretable insights via attribution analysis. This enables the generation of entity- or aspect-aware explanations, focusing on contributing factors grouped in to key categories: environmental conditions, vehicle and occupant characteristics, driver behavior, and infrastructure related elements, as shown in the right panel of. As the final step in the workflow, these explanations are then assessed through human evaluation to validate their accuracy and practical utility.

![Fig. 2](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-gr2.jpg)

Download: Download high-res image (1MB)

It is important to clarify that the orchestration of this process, including external preprocessing and database operations such as relational matching and tabular-to-text transformation, is conducted outside the LLM’s direct workflow. To ensure data fidelity, these antecedent steps are managed via traditional code-based pipelines rather than being triggered or controlled by a LLM agent. Future advancements in LLM capabilities may enable the automation of this data processing pipeline. Within the current architecture, a pretrained LLM is used to refine the template-constructed narrative and our supervised fine-tuned LLM serves as a specialized analytical agent, functioning as the core engine for performing complex crash analysis and interpretation. The core components of our CrashSage framework, including *Context-Aware Data Augmentation, Supervised Fine-Tuning, and Gradient-Based Explanation*, are detailed in the following sections.

### 4.2. Context-aware data augmentation

To enhance the quality of our input data, our framework implements a semantic preservation augmentation technique that utilizes a separate, pre-trained instance of the LLaMA3-8B model (). This “base LLM” functions as a specialized rewriting agent, tasked with improving narrative coherence while maintaining the factual fidelity of the original crash data. The use of a distinct, pre-trained model for this preprocessing step ensures that the subsequent fine-tuning of our primary CrashSage model begins with clean, consistent, and highly coherent narratives. The augmentation pipeline operates through a linguistic transformation process formalized as:(1) $R sim P_{\theta} \left(\right. \cdot \left|\right. x , \left(\left{\right. c_{i} \left.\right}\right)_{i = 1}^{n} , p_{t} \left.\right)$ where $R$ represents the enhanced narrative that is sampled from (denoted by $sim$) the probability distribution $P_{\theta}$. This distribution is generated by the LLM (with parameters $\theta$) and is conditioned on the inputs: the original text $x$, a set of preservation constraints $\left(\left{\right. c_{i} \left.\right}\right)_{i = 1}^{n}$, and the specialized instructions $p_{t}$.

In our implementation, we utilize the chat template to standardize input-output formats. The system prompt designates the model as a “professional editor specializing in rewriting traffic accident reports”, with explicit preservation requirements communicated through detailed guidelines. These include maintaining all factual information (times, dates, locations, vehicle details), removing uninformative placeholders (e.g., “nan”, “unknown”), preserving chronological order, and employing consistent professional language. The augmentation process handles batch processing of instances for computational efficiency. One example is shown in the appendix for demonstration, see Appendix.

This methodology delivers three significant improvements over conventional preprocessing approaches: standardization of linguistic variability across temporal and jurisdictional dimensions; enhancement of narrative fluidity without introducing factual distortion; and preservation of complex crash dynamics involving human, vehicular, and environmental factors. By maintaining semantic integrity while improving textual coherence, our technique creates crash narratives that are more consistent and amenable to downstream natural language processing tasks.

### 4.3. Supervised fine-tuning of LLM

During the fine-tuning phase, the traffic crash severity inference task is framed as a next-token generation task. This process can be described as:(2) $p_{\theta} \left(\right. T_{i} \left.\right) = \prod_{j = 1}^{\left|\right. T_{i} \left|\right.} p_{\theta} \left(\right. t_{j}^{\left(\right. i \left.\right)} \left|\right. t_{1}^{\left(\right. i \left.\right)} , \ldots , t_{j - 1}^{\left(\right. i \left.\right)} \left.\right) ,$ where $T_{i}$ is the $i$ -th example in the training data, $p_{\theta}$ is the LLM model, $t_{j}^{\left(\right. i \left.\right)}$ denotes the $j$ -th token in $T_{i}$.

The LLM’s parameters are fine-tuned by maximizing the likelihood $p_{\theta} \left(\right. T \left.\right) = \prod_{i = 1}^{N} p_{\theta} \left(\right. T_{i} \left.\right)$. Both the system prompt and the user prompt are masked for loss computation during training (). In our setting, the model is fine-tuned to predict crash severity levels, a task that demands a deep understanding of crash dynamics.

### 4.4. Gradient-based explanation

To interpret the decisions of our fine-tuned model, we employ a gradient-based explanation technique that attributes predictions to specific input words, helping to identify which words in a crash narrative mostly influence the model’s severity inference. It is important, however, to acknowledge the inherent limitations of this method. Its application assumes that model outputs are differentiable and that the influence of input tokens is continuous. In practice, the discrete nature of tokenization and the highly non-linear behavior of LLMs introduce discontinuities, meaning these assumptions are not strictly satisfied. Consequently, the resulting gradient-based attributions are approximations. Regardless, they offer practical and computationally efficient insights into the model’s decision-making process.

#### 4.4.1. Gradient-based attribution

To ensure trustworthiness, we seek to understand the complex inner workings of our supervised fine-tuned LLM in the traffic safety domain by applying a gradient-based explanation method ().

Gradient-based attribution techniques, which have been widely used to explain deep learning models (), can help identify which words in an input text have the greatest influence on the model’s output. In the context of traffic safety, this could enable pinpointing specific terms or phrases in incident reports that the model deems most indicative of safety issues. Following, we will use a first-order Taylor approximation of the difference in output probabilities when including or excluding each input token. Normalizing and thresholding these attribution scores yield a robust measure of each input token’s importance. The importance $I_{n , m}$ of input token $x_{n}$ to output token $y_{m}$ is defined as:(3) $I_{n , m} = p \left(\right. y_{m} \left|\right. Z_{m} \left.\right) - p \left(\right. y_{m} \left|\right. Z_{m , / n} \left.\right)$ where $Z_{m}$ is the context for generating $y_{m}$ consisting of the concatenation of prompt $X$ and the first $m - 1$ tokens of response $Y$, and $Z_{m , / n}$ omits token $x_{n}$ from $Z_{m}$. This is approximated using a first-order Taylor expansion:(4) $I_{n , m} \approx 〈 \frac{\partial f \left(\right. y_{m} \left|\right. Z_{m} \left.\right)}{\partial E_{i} \left[\right. x_{n} \left]\right.} , E_{i} \left[\right. x_{n} \left]\right. 〉$ where $E_{i} \left[\right. x_{n} \left]\right.$ is the input word embedding of token $x_{n}$ extracted from the fine-tuned LLM. The normalized pairwise importance score $\left(\hat{S}\right)_{n , m}$ is then defined as:(5) $\left(\hat{S}\right)_{n , m} = \left{\right. \lceil \frac{L \times I_{n , m}}{max_{n^{'}}^{N} I_{n^{'} , m}} \rceil & \text{if} \lceil \frac{L \times I_{n , m}}{max_{n^{'}}^{N} I_{n^{'} , m}} \rceil > b \\ 0 & \text{otherwise}$ where a scaling factor $L$ and a binary threshold $b$ are hyperparameters. In this study, we set $L = 100$ and $b = 1$.

#### 4.4.2. Crash severity analysis with word-level attribution

The foundation of our analytical framework relies on word-level attribution, which assigns importance scores to individual words or phrases within crash narratives based on the gradient attribution, described previously in. The attribution scores quantify each token’s contribution to the final prediction. Higher attribution scores suggest stronger associations with crash severity outcomes.

To enable aspect-aware explanation, our methodology decomposes crash narratives with word-level attribution into five key categories of contributing factors: 1) environmental conditions (weather, lighting, road surface quality, etc.); 2) vehicle and occupant characteristics (vehicle types, protection systems, etc.); 3) driver behavioral elements (speed, intoxication, maneuvers, etc.); 4) infrastructure features (road design, traffic control devices); and 5) unusual aspects with unexpectedly high attribution scores that may represent unique contributing factors. This multi-aspect approach enables comprehensive assessment of crash severity determinants.

The implementation consists of a semi-automated pipeline utilizing GPT-4o () to process and interpret word-level attribution data, as demonstrated in. Raw crash narratives, augmented with attribution scores, undergo systematic analysis through a carefully engineered prompt structure. This prompt directs the language model to process text with embedded attribution values, identify high-scoring words relevant to each factor category, and provide concise analytical summaries while maintaining output consistency.

To facilitate systematic analysis, we standardized the output using a JSON structure that preserves organizational consistency across all analyzed reports. For each factor category, the output includes a narrative summary capturing key insights and an array of high-scoring words with their associated attribution values. This structured approach enables qualitative assessment through the summaries as well as quantitative analysis via the attribution scores.

The core advantage of this approach lies in the combination of domain-specific prompting with robust natural language processing capabilities of LLMs, resulting in precisely formatted analyses that highlight each crash’s salient risk factors in a transparent, interpretable manner. It advances crash severity analysis by leveraging the linguistic pattern recognition capabilities of LLMs while maintaining analytical rigor through attribution-based evidence.

## 5\. CrashSage: Inference on crash severity outcome

In this section, we present the experimental framework and findings of our proposed CrashSage model for traffic crash severity inference. We first describe the training protocol and hyperparameter configurations employed for supervised fine-tuning of Llama3-8B model. Next, we introduce the baseline methods, including both state-of-the-art tabular models and large language models (LLMs) under various prompting strategies, which serve as comparative references. Finally, we report and analyze the results across multiple evaluation metrics, highlighting the relative strengths of our approach and discussing the implications for traffic safety modeling.

### 5.1. Training protocol and hyperparameter

We performed supervised fine-tuning on the Llama3-8B model () using parameter-efficient fine-tuning via LoRA (). The model was using AdamW () as optimizer and trained for 30 epochs using the DeepSpeed framework (). We employed a LoRA configuration with rank (r) of 128, alpha scaling factor of 256, and dropout rate of 0.1, targeting all linear layers in the model. Training was conducted with a learning rate of 3e-5 using a cosine scheduler with 5 % warmup, weight decay of 1e-4, and maximum gradient norm of 1.0. For optimization efficiency, we utilized gradient checkpointing and accumulated gradients over 16 steps with a per-device batch size of 1. The model processed sequences with a maximum length of 2048 tokens and was trained in bfloat16 precision. This configuration balances computational efficiency with effective knowledge transfer while maintaining reasonable memory requirements. The experiments are conducted on a server with four Nvidia A6000 48GB GPUs.

### 5.2. Baseline methods

This study establishes a diverse set of baseline configurations to comprehensively evaluate the performance of our supervised fine-tuned LLaMA3-8B () model. The task is to classify traffic crash severity into two levels: “No apparent or minor injury” or “Serious injury or fatal”. Our baselines are organized into two main categories: state-of-the-art tabular data models and large language models (LLMs).

The first category includes CatBoost (), a powerful, state-of-the-art gradient-boosting algorithm for tabular data, alongside TabTransformer () and FT-Transformer (), which are deep learning models specifically designed for tabular data. These models serve as robust benchmarks for comparison purposes.

The second category features several advanced LLMs, including LLaMA3-8B (), LLaMA3-70B (), GPT-4o mini (), and GPT-4o (). For these models, we implemented three distinct prompting strategies to assess their in-context learning capabilities (): Zero-shot, Zero-shot with Chain-of-Thought, and Few-shot. Together, this comprehensive set of baselines provides crucial reference points for evaluating the efficacy of our supervised fine-tuning approach against both specialized tabular methods and general-purpose LLMs. The experimental settings and abbrevations are presented in.

Table 2. Experimental Settings and Abbreviations.

<table><thead><tr><th colspan="2">Tabular Model Baselines</th></tr></thead><tbody><tr><td>CatBoost ()</td><td>A high-performance gradient boosting on decision trees library</td></tr><tr><td>TabTransformer ()</td><td>A Transformer-based model for tabular data</td></tr><tr><td>FT-Transformer ()</td><td>An advanced Transformer-based model for tabular data</td></tr><tr><td colspan="2"><strong>LLM Baselines</strong></td></tr><tr><td colspan="2"><em>Models Evaluated</em></td></tr><tr><td>LLaMA3-8B ()</td><td>8 billion parameter open-source model</td></tr><tr><td>LLaMA3-70B ()</td><td>70 billion parameter open-source model</td></tr><tr><td>GPT-4o-mini ()</td><td>gpt-4o-mini-2024-07-18, multimodal model from OpenAI</td></tr><tr><td>GPT-4o ()</td><td>gpt-4o-2024-11-20, advanced multimodal model from OpenAI</td></tr><tr><td colspan="2"><em>Prompting Strategies</em></td></tr><tr><td>Zero-shot</td><td>Models evaluated without any in-context examples</td></tr><tr><td>Zero-shot with Chain-of-Thought</td><td>Models prompted to explain reasoning step-by-step</td></tr><tr><td>Few-shot</td><td>Models provided with a small number of in-context examples</td></tr><tr><td colspan="2"><em>Sampling Strategy</em></td></tr><tr><td>Greedy Decoding</td><td>Used for all LLM inferences to ensure determinism</td></tr><tr><td colspan="2"><strong>Our Approach</strong></td></tr><tr><td>Supervised Fine-Tuned LLaMA3-8B</td><td>The LLaMA3-8B model fine-tuned for crash severity inference task</td></tr></tbody></table>

#### 5.2.1. CatBoost

CatBoost () or Categorical Boosting, is a gradient-boosting algorithm designed specifically to handle categorical data through target statistics, coupled with ordered boosting to avoid target leakage in subsequent boosting. CatBoost stands out among popular boosted tree algorithms like AdaBoost (), XGBoost (), LightGBM (). In the context of traffic safety tabular data, where variables like weather and situational factors are categorical in nature, which makes CatBoost a well-suited choice for traffic accident severity inference.

#### 5.2.2. TabTransformer

To benchmark our proposed method, we chose the TabTransformer (), a deep learning architecture specifically designed for tabular data that adapts the Transformer architecture. Unlike traditional models that learn simple, context-free embeddings for categorical features, the TabTransformer leverages self-attention to generate contextual embeddings. This allows the model to capture complex relationships and interactions among relevant features, making it a powerful baseline.

The model’s architecture consists of three main stages. First, each categorical feature is mapped to a dense vector through a trainable column embedding layer. These initial embeddings are then processed by a stack of $N$ Transformer layers. Each Transformer layer uses a multi-head self-attention mechanism to transform the embeddings, allowing each feature’s representation to be influenced or contextualized by all other features.

Let $x_{c a t} = \left{\right. x_{1} , x_{2} , \hdots , x_{m} \left.\right}$ be the set of $m$ categorical features for a given sample. Each feature $x_{i}$ is converted into a parametric embedding $e_{\phi_{i}} \left(\right. x_{i} \left.\right) \in \mathbb{R}^{d}$. This set of embeddings is then passed through the stack of Transformer layers (), denoted by the function $f_{\theta}$, to produce a set of contextual embeddings $\left{\right. h_{1} , \hdots , h_{m} \left.\right}$, where $h_{i} \in \mathbb{R}^{d}$.

Finally, these contextual embeddings are concatenated with the continuous features, $x_{c o n t}$, and fed into a MLP, $g_{\psi}$, to produce the final prediction. The entire model is trained end-to-end by minimizing a loss function $\mathcal{L} \left(\right. x , y \left.\right)$ for binary classification task in this study. This process enables the TabTransformer to learn rich, contextualized feature representations that have been shown to be robust against noisy and missing data.

#### 5.2.3. FT-Transformer

Another powerful Transformer-based architecture for tabular data is the FT-Transformer (Feature Tokenizer Transformer) (). A key distinction of this model is its ability to handle both categorical and numerical features within the same Transformer architecture.

The process begins with a Feature Tokenizer module, which converts all features into embeddings. For a numerical feature $x_{j}^{\left(\right. n u m \left.\right)}$, the transformation is a simple linear projection. For a categorical feature $x_{j}^{\left(\right. c a t \left.\right)}$, it is an embedding lookup. Each resulting feature embedding is augmented with a trainable bias:$T_{j}^{\left(\right. n u m \left.\right)} & = b_{j}^{\left(\right. n u m \left.\right)} + x_{j}^{\left(\right. n u m \left.\right)} \cdot W_{j}^{\left(\right. n u m \left.\right)} \\ T_{j}^{\left(\right. c a t \left.\right)} & = b_{j}^{\left(\right. c a t \left.\right)} + e_{j}^{T} W_{j}^{\left(\right. c a t \left.\right)}$ where $T_{j} \in \mathbb{R}^{d}$ is the resulting embedding for feature $j$, $b_{j}$ is a feature bias, $W_{j}$ is a weight matrix, and $e_{j}$ is a one-hot vector for the categorical feature.

These feature embeddings are then stacked to form a sequence $T \in \mathbb{R}^{k \times d}$, where $k$ is the total number of features. A special ‘\[CLS\]’ token embedding is prepended to this sequence as $T_{0}$. This combined sequence is then processed by a stack of $L$ Transformer layers, $F_{1} , \hdots , F_{L}$:$T_{i} = F_{i} \left(\right. T_{i - 1} \left.\right)$ The representation of the ‘\[CLS\]’ token from the last layer, $T_{L}^{\left[\right. \text{CLS} \left]\right.}$, encapsulates the aggregated information from all original features. This learned representation is then passed to a MLP to generate the final output. This approach allows FT-Transformer to learn deep, contextualized interactions among relevant features, regardless of their data type, making it a highly effective and universal model for tabular data.

#### 5.2.4. LLM with zero-shot prompting

Our first baseline employs a zero-shot prompting strategy, wherein models receive a concise instruction without examples. The model is prompted with domain-specific context identifying it as a professional road safety engineer and tasked with classifying crash severity based solely on the provided crash description. The prompt used is shown below:

> *You are a professional road safety engineer.*
> 
> *You are given a detailed description for a traffic crash.*
> 
> *Please classify the severity of the crash into one of two categories: ’No apparent or minor injury’, ’Serious injury or fatal accident’.*
> 
> *You can only output one of the classification result in your answer.*

This approach evaluates the model’s inherent ability to perform the classification task without prior examples, relying exclusively on its pre-trained knowledge on traffic safety.

#### 5.2.5. LLM with zero-shot chain-of-thought

The second baseline implements a zero-shot chain-of-thought (CoT) approach, which extends the zero-shot prompting by explicitly instructing the model to analyze the traffic crash before outputting the classification result. The prompt used for this approach is:

> *You are a professional road safety engineer.*
> 
> *You are given a detailed description for a traffic crash.*
> 
> *Please analyze this traffic crash with careful reasoning first, and then classify the severity of the crash into one of the two categories: ’No apparent or minor injury’, ’Serious injury or fatal accident’.*
> 
> *You can only output one of the classification result at the end of your answer.*

This modification encourages the model to engage in a more deliberate reasoning process, potentially leading to improved decision-making. The CoT approach is designed to assess whether explicit instructions for analytical reasoning enhance classification accuracy compared to direct zero-shot prompting.

#### 5.2.6. LLM with few-shot learning

The third baseline utilizes a few-shot learning paradigm, presenting the model with two exemplar traffic crashes, one in each severity category, and their corresponding severity outcomes prior to requesting classification of the target case. The prompt includes carefully selected examples that serve as implicit demonstrations of the reasoning process and decision criteria:

> *You are a professional road safety engineer.*
> 
> *Here are two examples of traffic crashes and their severity classification:*
> 
> *\[Example 1 with label ’No apparent or minor injury’\]*
> 
> *No apparent or minor injury*
> 
> *\[Example 2 with label ’Serious injury or fatal’\]*
> 
> *Serious injury or fatal*
> 
> *You are given a detailed description for a traffic crash.*
> 
> *Please classify the severity of the crash into one of two categories: ’No apparent or minor injury’, ’Serious injury or fatal’.*
> 
> *You can only output one of the classification result in your answer.*

The few-shot approach leverages LLMs’ in-context learning capabilities to learn from a minimal set of examples and apply that knowledge to new cases, a strategy demonstrated to improve performance across a range of natural language processing tasks.

### 5.3. Results

In evaluating the outcomes of our experimental comparisons, we examine both traditional tabular approaches and various LLM-based methods for traffic crash severity inference. As summarized in, our Supervised Fine-Tuning (SFT) approach using LLaMA3-8B achieves a Macro-F1 score of 0.7361, surpassing all baseline methods. This result highlights the significant benefits of specialized domain adaptation of LLMs, validating our initial hypothesis that traffic crash narratives require careful domain grounding that general-purpose prompting alone cannot provide.

Table 3. Performance comparison of different models across evaluation metrics.

<table><thead><tr><th>Setting</th><th>Model</th><th>Macro-F1</th><th>Accuracy</th><th>Macro-Recall</th><th>Macro-Precision</th></tr></thead><tbody><tr><td rowspan="3">Tabular Models</td><td>CatBoost</td><td>0.7284</td><td>0.7383</td><td>0.73</td><td>0.73</td></tr><tr><td>TabTransformer</td><td>0.7206</td><td>0.7609</td><td>0.77</td><td>0.68</td></tr><tr><td>FT-Transformer</td><td>0.7132</td><td>0.7233</td><td>0.71</td><td>0.71</td></tr><tr><td rowspan="4">ZS</td><td>LLaMA3-8B</td><td>0.6726</td><td>0.6883</td><td>0.67</td><td>0.68</td></tr><tr><td>LLaMA3-70B</td><td>0.6345</td><td>0.6355</td><td>0.67</td><td>0.67</td></tr><tr><td>GPT-4o-mini</td><td>0.6711</td><td>0.7078</td><td>0.67</td><td>0.72</td></tr><tr><td>GPT-4o</td><td>0.7067</td><td>0.7229</td><td>0.70</td><td>0.72</td></tr><tr><td rowspan="4">ZS_CoT</td><td>LLaMA3-8B</td><td>0.5071</td><td>0.5346</td><td>0.59</td><td>0.66</td></tr><tr><td>LLaMA3-70B</td><td>0.6059</td><td>0.6099</td><td>0.65</td><td>0.67</td></tr><tr><td>GPT-4o mini</td><td>0.3717</td><td>0.4413</td><td>0.52</td><td>0.55</td></tr><tr><td>GPT-4o</td><td>0.3693</td><td>0.4443</td><td>0.52</td><td>0.58</td></tr><tr><td rowspan="4">FS</td><td>LLaMA3-8B</td><td>0.6851</td><td>0.6867</td><td>0.70</td><td>0.69</td></tr><tr><td>LLaMA3-70B</td><td>0.7051</td><td>0.7184</td><td>0.70</td><td>0.71</td></tr><tr><td>GPT-4o-mini</td><td>0.6560</td><td>0.6898</td><td>0.66</td><td>0.69</td></tr><tr><td>GPT-4o</td><td>0.7062</td><td>0.7259</td><td>0.70</td><td>0.72</td></tr><tr><td>SFT</td><td>LLaMA3-8B</td><td><strong>0.7361</strong></td><td><strong>0.7395</strong></td><td><strong>0.74</strong></td><td><strong>0.74</strong></td></tr></tbody></table>

Among the tabular baselines, traditional methods demonstrate formidable performance, underscoring their continued relevance for structured data tasks. CatBoost, a tree-based model, achieves a strong Macro-F1 score of 0.7284, closely approaching our SFT model. This aligns with recent research suggesting that tree-based models possess inductive biases well-suited for the irregular, non-smooth decision boundaries often found in tabular data (). Although TabTransformer attains the highest accuracy 0.7609, its lower Macro-F1 score 0.7206 indicates an imbalanced precision-recall trade-off, a common challenge in imbalanced datasets like crash records. These findings establish a high-performance benchmark of tabular machine learning baselines.

The comparison between these specialized tabular models and zero-shot (ZS) LLM approaches reveals a notable performance gap. While GPT-4o delivers the best zero-shot performance with a Macro-F1 of 0.7067, it still falls short of all tabular baselines. This suggests that without domain-specific adaptation, powerful general-purpose LLMs under-perform the models explicitly designed for structured data. A closer analysis of prompting strategies reveals further findings: the few-shot (FS) setting generally improves performance over zero-shot, with LLaMA3-70B achieving a Macro-F1 of 0.7051. When LLaMA3-8B is given a minimal number of examples in the few-shot setting, its performance moves closer to that of GPT-4o, demonstrating the model’s capacity to incorporate contextual cues even with limited domain examples. However, the zero-shot chain-of-thought (ZS\_CoT) setting leads to a surprising and significant performance degradation across all LLMs. For instance, GPT-4o’s Macro-F1 score decreases to 0.3693. This suggests that prompting for step-by-step reasoning may encourage the model to generate speculative or extraneous text that deviates from a domain-consistent interpretation of the crash narrative.

The above analysis justifies the supervised fine-tuning of LLMs for this task. The SFT LLaMA3-8B not only achieves the best overall Macro-F1 score (0.7361) but also outperforms the much larger LLaMA3-70B model in all settings. This observation has important practical implications that domain-specific fine-tuning is more critical than model scale alone and that superior performance can be achieved with a computationally more efficient 8B-parameter model.

While the performance improvement of SFT over the best tabular baseline is modest (0.7361 vs. 0.7284 Macro-F1), the primary value of our LLM-based framework lies in its unique explainability, which provides deeper insights that raw metrics cannot capture. Unlike tree-based models that provide only aggregate feature importance scores, our gradient-based attribution method delivers word-level explanations that illuminate *how* specific influential textual elements within the crash narrative. As demonstrated in Section 6, this approach enables practitioners to identify precise phrases like “motorcycle’s rear-end collision” or “intoxication status” with quantitative attribution scores, revealing not just *what* factors matter but *how* they interact within the broad narrative context. Furthermore, the LLM with explanation techniques could uncover complex inter-dependencies among environmental, behavioral, and infrastructure factors: insights that remain opaque in traditional SHAP-based explanations ().

In conclusion, the results substantiate our initial hypothesis: transforming structured crash data into domain-specific narratives enables a fine-tuned LLM to attain state-of-the-art performance while offering deeper insights (see ). Our comparative experiments demonstrate that although specialized tabular methods remain strong, fine-tuned language models deliver versatile and practical tools with superior inference accuracy and richer explanatory power, making them highly valuable for real-world traffic safety analysis.

## 6\. CrashSage: Interpretability and attribution

In traffic safety modeling and analysis, interpretability is crucial for building trust and understanding the factors driving model predictions. Our CrashSage framework employs gradient-based attribution techniques to highlight the most influential terms in crash narratives that contribute to traffic crash severity inferences. This approach not only enhances transparency but also provides valuable insights into the complex interplay among factors affecting crash outcomes.

### 6.1. Individual incident inspection: Word-level explanations of an accident

Our word-level attribution method aggregates token-level importance scores derived from gradient-based techniques to identify which words and phrases most significantly influence the model’s severity inference. In detail, our implementation identifies token boundaries within the LLM’s tokenization scheme and combines scores of sub-word tokens into coherent words, providing more intuitive interpretations for domain experts. These importance scores quantify how much each word contributes to the final inference, enabling analysts to understand which aspects of a crash narrative were most decisive in the model’s reasoning process.

For clear and comparable visualization across cases, we use a consistent color-coded heatmap. This scheme uses a binary color mapping to differentiate between levels of attribution significance: words with high attribution values are highlighted in red, while those with moderate but still notable influence appear in green. This creates an intuitive visual hierarchy that emphasizes the most influential textual segments.

To further distill these findings for convenience, we use a semi-automated pipeline with GPT-4o to summarize each crash. The prompt used is demonstrated in the. The raw crash text, augmented with its word-level attribution scores, is processed by the model. A domain-specific prompt guides the LLM to generate a concise, JSON-based output covering environmental, vehicle/occupant, behavioral, infrastructure, and unusual factors. This approach produces precisely formatted analyses that transparently highlight each crash’s most salient risk factors. Although a formal, large-scale evaluation of the summary quality was outside the scope of this study, we conducted manual cross-checks on the summary outputs. These checks affirmed that our structured prompting approach reliably generated summaries that were faithful to the attribution scores. Nevertheless, deployment in a practical setting would require human oversight to verify the faithfulness of the summaries and mitigate the risk of hallucination.

To demonstrate how the model’s reasoning adapts to different severity level cases, we apply this process to two distinct crash examples, one with minor injuries and one with a serious/fatal outcome.

#### 6.1.1. Example 1: No apparent or minor injury crash

First, we consider a crash inferred by CrashSage as resulting in “no apparent or minor injury”. The attribution visualizations are shown in and.

![Fig. 3](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-gr3.jpg)

Download: Download high-res image (207KB)

![Fig. 4](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-gr4.jpg)

Download: Download high-res image (700KB)

The attribution visualization in reveals several key patterns in how the CrashSage evaluates crash narratives. Temporal markers (“On,” “June,” “29,” “2022,” “PM”) receive moderate to high attribution

![Image 1](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-fx1.jpg)

![Image 2](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-fx2.jpg)

scores, indicating the importance of time-related information in severity assessment. Location identifiers (“Chelan,” “Washington”) similarly show strong influence, suggesting geographical context impacts prediction.

Environmental conditions, particularly “dusk” and “two-lane” road configuration, demonstrate notable attribution weights, aligning with safety research that identifies limited visibility and road type as significant risk factors. Vehicle-specific details (“\[BRAND 1\] \[MODEL 1\] vehicle,” “2005”) receive high attribution scores, likely reflecting the model’s attention to vehicle age and model. The most substantial attributions appear for driver characteristics (“35-year-old male,” “36-year-old female”) and incident type indicators, particularly the negated “hit-and-run incident” phrase, which appears critical to the model’s classification decision.

The following summary, generated by our GPT-4o pipeline described in and, categorizes these key factors:

![Image 3](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-fx3.jpg)

![Image 4](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-fx4.jpg)

![Image 5](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-fx5.jpg)

![Image 6](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-fx6.jpg)

![Image 7](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-fx7.jpg)

#### 6.1.2. Example 2: Serious injury and fatal crash

Next, we analyze a “serious injury or fatal” crash sample, which reveals a different set of influential factors. The word-level attribution scores are shown in.

![Fig. 5](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-gr5.jpg)

Download: Download high-res image (238KB)

Similarly, the attribution visualization in reveals distinctive patterns for this serious/fatal crash. While temporal and location information remain important as in the minor injury case, this example shows particularly strong attribution to specific roadway identifiers (“542i,” “MAINLINE”) and precise geographic coordinates. The motorcycle involvement (“\[MODEL 2\],” “motorcycle’s”) receives substantial weight, consistent with traffic safety research identifying motorcycles as associated with higher crash severity outcomes. Notable also is the high attribution for “intoxication” even though it’s negated in the text, suggesting the model considers this factor critically important when assessing crash severity.

![Fig. 6](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-gr6.jpg)

Download: Download high-res image (729KB)

The attribution pattern in this serious/fatal crash example reveals notable differences compared to the minor injury case previously analyzed. While both examples show significant attribution to temporal and location information, this severe crash narrative demonstrates particularly strong influence from specific roadway identifiers (“542i,” “MAINLINE”) and precise geographic “milepost 35.42”.

The motorcycle involvement receives substantial attribution weight, with high scores for “\[MODEL 1\]\[3.00\]” and “motorcycle’s\[2.68\],” aligning with traffic safety research that consistently identifies motorcycles as associated with increased crash severity. Vehicle type information (“\[BRAND 1\] \[MODEL 1\]\[4.31\]”) shows remarkably high attribution, possibly indicating the model has learned relationships between vehicle types and crash outcomes from its training data.

![Image 8](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-fx8.jpg)

Noteworthy is the high attribution score for “intoxication\[2.68\]” despite it being negated in the text, suggesting the model places significant importance on this factor’s presence or absence when assessing crash severity. The phrase “rear-end\[2.28\]” collision type also receives substantial attribution, reflecting its relevance to severity outcomes in motorcycle-involved crashes.

This gradient-based attribution analysis demonstrates how the CrashSage identifies distinctive risk patterns when evaluating crash severity. For serious/fatal crashes, the model focuses intensely on vehicle types (particularly motorcycles), specific road identifiers, and precise location data, while utilizing different attribution patterns for minor injury incidents. The visualization provides transparent insight into the model’s decision-making process, revealing how it integrates multiple contextual elements: temporal, environmental, vehicular, and human factors, rather than focusing on isolated aspects. This comprehensive approach mirrors the multifaceted evaluation process used by human safety experts, while offering computational precision in identifying combinations of factors that contribute to different crash outcomes.

The summary of this serious/fatal crash example with word-level attribution scores to different safety aspects, is demonstrated below.

![Image 9](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-fx9.jpg)

![Image 10](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-fx10.jpg)

![Image 11](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-fx11.jpg)

![Image 12](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-fx12.jpg)

### 6.2. Co-occurrence analysis of high-score factors from different aspects

To reveal relationships between influential crash factors, we conducted analysis, focusing on high-attribution elements identified through our gradient-based attribution approach. The process begins with factor extraction, constrained to the top five factors for each of the four aspects: environmental, driver behavioral, vehicle/occupant, and infrastructure. Subsequently, co-occurring factor pairs are identified and visualized using a Sankey diagram.

Semantic grouping was applied to consolidate conceptually similar terms that appeared with varied phrasing throughout the dataset. For instance, different temporal references were unified under broader descriptors such as “time of day”. This semantic grouping process enhanced interpretability while preserving the underlying semantic relationships between factors across various crash instances.

The resulting data structure captures the co-occurrence patterns in reference to four fundamental safety aspects (i.e., environmental conditions, driver behaviors, vehicle attributes, and infrastructure features), with each node representing a distinct factor and connecting links quantifying co-occurrence frequency between factor pairs. This graphic visualization reveals how these specific aspects interact in complex crash scenarios. The structure illuminates critical inter-dependencies, such as correlations between alcohol-related behaviors and specific temporal or roadway characteristics, providing a holistic view of crash dynamics.

presents these relationships through a Sankey diagram where safety aspects are color-coded for clarity, and connection strengths are represented by flow widths proportional to co-occurrence frequency. The diagram reveals complex inter-dependencies among crash factors spanning environmental, behavioral, vehicle/occupant, and infrastructure aspects. Notably, driver behavioral factors, particularly intoxication status and alcohol-related impairment, emerge as central nodes with extensive links to both environmental and infrastructure elements, underscoring the critical role of driver condition in crash severity. Temporal factors, such as time of day, show strong associations with impairment-related behaviors, indicating diurnal patterns in high-risk driving. Additionally, geographic variability is reflected in distinct connection patterns between behavioral factors and specific locations, pointing to regional heterogeneity in crash factor distributions.

![Fig. 7](https://ars.els-cdn.com/content/image/1-s2.0-S3050860625000304-gr7.jpg)

Download: Download high-res image (583KB)

Several factor combinations stand out as particularly relevant to crash severity outcomes. The co-occurrence pathway between alcohol-related impairment and excessive speed suggests a synergistic relationship that likely amplifies crash energy and impact forces. Links between intoxication status and restraint utilization indicate a potential behavioral coupling that compounds injury risk through both increased crash likelihood and decreased protection. The visualization also reveals how certain environmental conditions interact with infrastructure characteristics, particularly evident in connections between wet weather and specific road surface attributes, which together create compounded effects on vehicle handling and control.

Vehicle and occupant factors primarily function as intermediate outcome nodes within the graph. Restraint systems and airbag status appear as downstream factors from driver behaviors, suggesting that safety equipment utilization is influenced by driver characteristics. The connection between vehicle year and restraint technologies indicates the progressive integration of advanced occupant protection systems. The position of restraint-related factors as major nodes with multiple connections across the graph underscores their persistent influence across diverse crash scenarios, confirming their fundamental role in severity mitigation regardless of initiating factors.

Infrastructure elements exhibit multifaceted interactions with both antecedent and outcome variables. Lane configuration, with its numerous cross-category connections, exemplifies the complex role of road design in shaping crash dynamics. Road surface characteristics serve as bridging factors between environmental conditions and driver behaviors, suggesting a mediating influence on crash risk. Additionally, traffic control systems display strong association with driver decision-making, reflecting their impact on behavioral responses. Collectively, these interconnections highlight how the roadway environment influences and responds to driver behavior patterns, creating feedback loops that affect crash outcomes.

This diagram analysis demonstrates that crash severity outcome arise from intricate interactions among diverse factors across different aspects. The co-occurrence patterns suggest that effective traffic safety interventions require multifaceted approaches addressing both human factors and infrastructure design. Special attention is warranted for central behavioral nodes, which act as critical links between environmental conditions and crash outcomes.

Rather than viewing risk factors in isolation, the sankey diagram highlights their interrelationships and potential synergistic effects on crash severity outcomes. This integrated perspective offer road safety researchers and practitioners with an evidence-based foundation for developing multifaceted interventions that account for interconnected dynamics of crash development, thereby supporting more effective and systematic improvements in transportation systems.

## 7\. Conclusions

This paper introduces CrashSage, a novel LLM-centered framework designed to address key challenges in traffic safety analysis. By transforming traditional crash records into coherent textual narratives, followed by context-aware data augmentation, our approach mitigates information loss inherently associated with conventional tabular formats. We then fine-tuned the LLaMA3-8B model on these enriched narratives to infer crash severity while generating interpretable insights grounded in domain-specific contexts.

Our experimental results demonstrate that the fine-tuned LLaMA3-8B model outperforms a comprehensive set of baselines, including diverse LLM prompting strategies and state-of-the-art tabular models such as CatBoost and Transformer-based approaches. These findings suggest that a well-adapted language model can effectively capture the complex patterns embedded in traffic crash narratives. Beyond performance gain, the proposed CrashSage framework advances model transparency. It goes beyond identifying isolated risk factors to uncovering their complex interplay in rich, multifaceted contexts. Its word-level, context-aware interpretations provides intuitive, linguistically grounded explanations that are accessible to safety practitioners and especially valuable for guiding targeted traffic safety interventions.

In summary, this study highlights the transformative potential of LLMs in bridging structured data and natural language to advance traffic safety research. By improving modeling accuracy, interpretability, and real-time applicability, CrashSage lays the groundwork for more insightful, transparent, and actionable crash analysis. This framework empowers transportation agencies to make informed, data-driven decisions that contribute to reducing road injuries and fatalities. Moreover, CrashSage exemplifies an agentic AI framework within the broader paradigm of Agentic Transportation Systems, paving the way toward more intelligent, adaptive, and collaborative safety management in the future of transportation.

## 8\. Limitations and future directions

This section critically reflects on the limitations of the current CrashSage framework and outlines promising avenues for future research. We first discuss key data and methodological constraints, including issues of jurisdictional generalizability, fragmented datasets, reliance on textual inputs, and the interpretive boundaries of gradient-based explanations. We then highlight potential directions to address these challenges, such as integrating multi-jurisdictional and multi-modal data, linking medical and transportation records, and developing adaptive models that remain relevant in the face of evolving transportation technologies and safety needs.

### 8.1. Data and methodological limitations

The CrashSage framework faces several constraints that contextualize its contributions. First, our analysis relies on retrospective crash records from a single jurisdiction (Washington State, USA), limiting generalizability to regions with different road networks, traffic laws, and reporting standards. The inherent variability in human reporting quality and severe class imbalance pose additional challenges for model training and validation.

Our current pipeline mainly uses roadway- and crash-level attributes (e.g., AADT, segment geometry, shoulder type) and does not explicitly consider broader geospatial context such as nearby points of interest (POIs) or land-use patterns. Prior research shows that these neighborhood-level factors can influence travel behavior and crash risk. However, adding them requires addressing challenges such as differences in spatial resolution (milepost vs. parcel), data availability across regions, and possible overlapping with sensitive socioeconomic indicators. The integration of such geospatial contexts is an important direction for future work,. Besides, since a fixed narrative template along with the data augmentation is utilized in this study, alternative prompt formats (bulleted, chronological, compressed) can be evaluated for robustness checks in future research (, ).

A fundamental data limitation reflects the field’s evolution from a transportation issue to a public health concern, which stems from data fragmentation between transportation and medical systems. Current datasets capture on-site indicators like vehicle fire or law enforcement severity classifications but lack linkage to verified medical outcomes. Critical information including specific injuries, EMS diagnoses, detailed hospital records, and long-term health consequences remains disconnected from transportation datasets. This disconnect prevents comprehensive understanding of the full injury trajectory and public health burden of traffic crashes.

CrashSage should be positioned as an analytical tool for augmenting rather than replacing transportation professionals’ knowledge and expertise. While it provides methodological advances for extracting insights from complex crash data, translating these insights into actionable safety interventions requires the critical judgment and domain expertise of traffic safety engineers. By treating crash records as rich narratives rather than isolated tabular entries, the framework uncovers semantic hidden patterns while ensuring insights remain accessible to practitioners responsible for implementing safety interventions.

At the current setting, our framework operates purely on textual data, disregarding potentially valuable visual information from vehicle and roadside camera systems. While our gradient-based explanations enhance transparency, they only provide approximations that may not fully capture the model’s internal representations. Moreover, our approach identifies statistical associations rather than causal relationships. LLMs cannot inherently perform causal inference without explicit causal chains documented in the data to verify the interpretation. The explicit causal chain of incidents, best deduced by experts at crash scenes, is seldom documented.

Besides, pre-trained LLMs possess static knowledge bases frozen at their training date, potentially missing dynamic changes in transportation ecosystems including emerging vehicle technologies, evolving legislation, and shifting travel patterns. This necessitates periodic retraining or integration with real-time knowledge sources to maintain relevance.

### 8.2. Future research directions

Looking ahead, several critical research avenues emerge from this work. Future work could expand CrashSage by incorporating richer and more diverse data sources, including multi-jurisdiction crash reports, broader geospatial context (e.g., POIs and land use) (, ), and linked medical records, to improve generalizability and capture the full public health impact of traffic crashes. Furthermore, multi-modal frameworks integrating textual narratives with visual and sensor data could provide richer contextual understanding. Continual learning capabilities would allow models to adapt to changing traffic patterns and emerging safety challenges without complete retraining. As vehicle technology evolves with advanced driver assistance systems and autonomous vehicles, analytical frameworks must incorporate new crash scenarios and risk factors through efficient, incremental knowledge updates. Future advancements should focus on intentional design of crash data collection protocols coupled with appropriate models to address analysis more rigorously. Additionally, the interpretability pipeline itself could be enhanced by implementing feedback loops where the model’s explanations are re-fed into its prompt to validate the consistency of its reasoning.

## Funding

This research received no external funding.

## CRediT authorship contribution statement

**Hao Zhen:** Visualization, Software, Methodology, Investigation, Formal analysis, Data curation, Conceptualization. **Jidong J. Yang:** Writing – review & editing, Validation, Supervision, Resources, Project administration, Methodology, Investigation, Funding acquisition, Conceptualization.

## Declaration of competing interest

The authors declare no conflicts of interest for the study.

## Appendix A. Example of Narrative Augmentation

This appendix provides a full example of a crash narrative before and after the context-aware data augmentation process. The original text is generated directly from a template, resulting in uninformative placeholders (e.g., “nan”) and disjointed phrasing. The augmented version demonstrates improved coherence and readability while preserving all factual data.

## Appendix B. Original Narrative (Template-Generated)

> On 2022-07-16 00:00:00, a Saturday at 4:00 PM, an accident involving 1.0 vehicles and 0.0 pedestrians, occurred under Daylight situation. The road surface condition was described as Dry with weather reported as Clear. The crash was categorized as Strikes OTHER OBJECT, with impact location described as nan in relation to the roadway. It occurs on 240i (MAINLINE). The crash occurred in Richland, Benton. The crash was not related to any intersections or driveways., The additional characteristics for the crash location are nan. The roadway where the crash occurred is categorized as Urban Freeways, which combines attributes like the number of lanes, urban or rural designation, median barrier type, and functional class. The road’s functional classification is noted as Urban Other Freeways / Expressways, indicating its designation within the federal functional class system, separating urban and rural areas, and the administrative class is described as State Route. Coordinates of the crash approximate latitude 1955017.35 and longitude 337469.67.The crash occurred at Milepost 34.83, which corresponds to the State Route Accumulated Route Milepost value.
> 
> The road infrastructure at the crash location featured 5 lanes with a road width of 60 feet. The road had a posted speed limit of 60 mph. The pavement surface was Portland Cement Concrete Pavement, with a lane surface described as Portland Concrete Cement. The right shoulder was 10 feet wide with a Asphalt surface, while the left shoulder was 0 feet wide with a nan surface. The road included a median of 22 feet width, with an asphalt-paved median surface, which provides a smooth, dark-colored surface commonly used for roadways. and a concrete Jersey-type barrier, which is a modular concrete barrier used to separate lanes of traffic. The road had an annual average daily traffic (AADT) of 29000 vehicles. Special use lanes were present with a Weaving/Speed Change lane, located on the right side of the road of the road, measuring 12 feet and featuring a Portland Concrete Cement surface.
> 
> The first harmful event was described as a vehicle struck or was struck by an object falling from another vehicle’s load., followed by the second harmful event: nan. Fixed objects struck during the collision included: nan and nan. The crash was not the result of an intentional action by any participant.. There was no evidence of alcohol involvement in this accident. Additionally, it was reported as a non-hit-and-run case.
> 
> The first vehicle was moving toward Southeast (Increasing milepost of major roadway), the vehicle was Moving Straight. The second vehicle was moving toward nan (Unknown or Not Applicable), the vehicle was Unknown or Not Applicable.
> 
> The sequence of events involved with Vehicle A leading to the crash included: the primary event being nan, followed by a secondary event described as nan. If applicable, a tertiary event occurred, characterized as nan, The crash occurred under traffic control conditions described as No Traffic Control, on a roadway categorized as Two Way - Divided, with Barrier. Vehicle A (MITSUBISHI ECLIPSE, manufactured in 2019.0) was involved. The vehicle was used for Vanette Under 10,000 lb and identified as a Pickup,Panel Truck or Vanette under 10,000 lb, with a gross weight rating of nan. It was Going Straight Ahead on a road with a speed limit of 60.0 km/h prior to the crash. Driver actions contributing to the crash included nan. Additionally, nan was noted as a secondary contributing factor.
> 
> The driver was 24.0 years old, identified as Female, and used Lap & Shoulder Used at the time of the crash. The airbag status was reported as Not Deployed when the crash occurred. A Drug Recognition Expert assessment was nan, and the driver’s intoxication status was noted as nan. Additional driver actions reported included nan.
> 
> A female aged 24.0, seated at motor vehicle driver in Vehicle A, was wearing lap and shoulder belts. Helmet usage was reported as not reported.

## Appendix C. Augmented Narrative (LLM-Rewritten)

> On July 16, 2022, at 4:00 PM, a traffic accident occurred on State Route 240i (MAINLINE) in Richland, Benton, involving one vehicle and no pedestrians. The road surface was dry, and the weather was clear. The crash was classified as a vehicle striking an object, with the impact location described as the right shoulder of the roadway. The crash occurred on a 60-foot-wide, five-lane urban freeway with a posted speed limit of 60 mph. The pavement surface was Portland Cement Concrete, and the right shoulder was 10 feet wide with an asphalt surface. The left shoulder was 0 feet wide with no surface. The median was 22 feet wide with an asphalt-paved surface and a concrete Jersey-type barrier. The first harmful event involved a vehicle striking an object falling from another vehicle’s load. The second harmful event was not reported. The crash was not the result of intentional action by any participant, and there was no evidence of alcohol involvement. The incident was classified as a non-hit-and-run case. Vehicle A, a 2019 Mitsubishi Eclipse, was traveling southeast on the main roadway, moving straight, when the crash occurred. The vehicle was used for vanette under 10,000 pounds and was identified as a pickup, panel truck, or vanette under 10,000 pounds. The gross weight rating was not reported. The driver, a 24-year-old female, was wearing a lap and shoulder belt at the time of the crash. The airbag did not deploy. The driver’s intoxication status was not reported, and a Drug Recognition Expert assessment was not conducted. The driver’s actions contributing to the crash were not reported. The passenger, also a 24-year-old female, was seated in the driver’s position and was not wearing a helmet. The crash occurred at milepost 34.83, which corresponds to the State Route Accumulated Route Milepost value. The coordinates of the crash are approximately latitude 39.551235 and longitude -93.747967. The road’s functional classification is Urban Other Freeways/Expressways, and its administrative class is State Route. The annual average daily traffic (AADT) on this section of the road is 29,000 vehicles.

## Appendix D. GPT-4o Summarization Prompt

The following prompt was used to generate the structured JSON analysis of crash narratives with word-level attribution scores.

Analyze the following crash text (with word-level attribution scores) to

produce a concise, structured analysis of the crash's severity. Specifically,

1\. Environmental Factors

\- Weather conditions, road surface, lighting, time of day, any location-specific

details (e.g., jurisdiction, city, county), or any relevant situational context.

\- Reference any high-scoring words or phrases that highlight environmental

risks or factors.

2\. Vehicle and Occupant Factors

\- Vehicle type(s), occupant protection details (e.g., seat belts, airbags),

occupant ages, etc.

\- Reference any high-scoring words or phrases that highlight vehicle or

occupant-related factors.

3\. Driver or Behavioral Factors

\- Speed, intoxication or drug use, distractions, vehicle movement, or other

relevant driver actions.

\- Reference any high-scoring words or phrases that highlight behavioral factors.

4\. Infrastructure Factors

\- Road surface type, lane and shoulder widths, posted speed limit, road

name/route number, annual average daily traffic (AADT), traffic control, or

intersection design.

\- Reference any high-scoring words or phrases that highlight infrastructure

elements (e.g., ''Route 20,'' ''State Highway,'' ''main roadway'').

5\. Unusual or Standout Aspects

\- Identify any words or details that have unexpectedly high attribution scores or

any unique features not covered above.

FORMAT REQUIREMENTS

\- Output must be \*\*valid JSON\*\* (no additional text or formatting outside the

JSON object).

\- Use the following structure in your JSON:

{

''environmental\_factors'': {

''summary'': ''...'',

''high\_scoring\_words'': \[ { ''word'': ''...'', ''score'':... },... \]

},

''vehicle\_and\_occupant\_factors'': {

''summary'': ''...'',

''high\_scoring\_words'': \[ { ''word'': ''...'', ''score'':... },... \]

},

''driver\_or\_behavioral\_factors'': {

''summary'': ''...'',

''high\_scoring\_words'': \[ { ''word'': ''...'', ''score'':... },... \]

},

''infrastructure\_factors'': {

''summary'': ''...'',

''high\_scoring\_words'': \[ { ''word'': ''...'', ''score'':... },... \]

},

''unusual\_or\_standout\_aspects'': {

''summary'': ''...'',

''high\_scoring\_words'': \[ { ''word'': ''...'', ''score'':... },... \]

}

}

Within each section:

\- \*\*''summary''\*\*: Provide a brief plain-text overview of key findings.

\- \*\*''high\_scoring\_words''\*\*: Include an \*\*array of objects\*\*, where each has:

\- ''word'': The high-scoring word or phrase.

\- ''score'': The numeric score attributed to that word or phrase.

GOAL: Produce an ''at-a-glance'' JSON object that shows how the model's word-level

attribution scores point to specific aspects of the crash (environmental,

vehicle/occupant, driver/behavioral, infrastructure, or unusual factors)

contributing to its severity classification.