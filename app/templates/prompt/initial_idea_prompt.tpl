# Task Definition
You are going to generate a research draft that should be original, clear, feasible, relevant, and significant. This will be based on {{ hypotheses_index }} related hypotheses, the title and abstract of those of {{ index + 1 }} related papers in the existing literature, and {{ keynum }} entities potentially connected to the research area.
Understanding of the related hypotheses, papers, and entities is essential:
- The related hypotheses should serve as a foundation or starting point for your research problem, acknowledging that they may contain flaws or inaccuracies that can be refined. They might offer insights, reveal gaps, or present contradictions that you can build upon, address, or improve upon in your problem statement.
- The related papers indicate their direct relevance and connection to the primary research topic you are focusing on, and providing additional context and insights that are essential for understanding and expanding upon the paper.
- The entities can include topics, keywords, individuals, events, or any subjects with possible direct or indirect connections to the related studies, serving as auxiliary sources of inspiration or information that may be instrumental in formulating the research problem.

I will provide the related hypotheses, papers, and entities, as follows:
# Hypotheses
{{ hypotheses_prompt }}
{{ title_abstract_prompt }}
# Entities:
'''{{ keyword_str }}'''

# Output Requirements
With the provided related hypotheses, papers, and entities, your objective now is to formulate a research draft that not only builds upon these existing studies but also strives to be original, clear, feasible, relevant, and significant. In addition, you also need to provide a detailed Rationale, Necessary technical details, possible datasets and Reference to ultimately form the paper title,abstract,methods and experiments. Note: The final title should be appealing, and the experimental content should include relevant baselines as much as possible.

# Respond in the following format:
### Problem:
### Rationale:
### Necessary technical details:
### Datasets:
### Paper Title:
### Paper Abstract:
### Methods:
### Experiments:
### Reference: 1.[Title 1], 2.[Title 2], ..., n.[Title n]