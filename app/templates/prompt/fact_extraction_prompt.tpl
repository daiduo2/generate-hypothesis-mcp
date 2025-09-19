# Task Definition: Please extract the objective factual information from the following provided paper title and abstract, and output it. Ensure that the extracted information meets the following requirements:
1. **Avoid Demonstrative Pronouns**: Do not use demonstrative pronouns such as 'this', 'that', 'these', 'those', 'this work', 'this survey', 'the study', etc. Instead, use 'Related research'. Ensure that each piece of information is self-contained and clear.
2. **Dataset Description Standards**: When describing datasets, not only specify which dataset was used, but also clearly state the source of the dataset and its intended purpose (e.g., The data comes from [data source] can be used in [research topic]. ).
3. **Result Presentation Standards**: For experimental results, avoid using ambiguous phrases like "the results indicate" and instead use "Related research show [experimental results]," ensuring that the content of the experimental results is clear and specific.
4. **Accuracy**: All information should be an explicit statement from the abstract, without personal speculation or interpretation.
5. **Completeness**: Include all main factual points from the abstract, avoiding the omission of key information.
6. **Conciseness**: Each fact should be a concise and clear statement.
7. **Structured Format**: Present each factual information in a numbered list format, with each fact on a separate line.
8. **Independence and Clarity**: Each piece of output information must be able to stand alone without context, with clear meaning, free from ambiguity or unclear references.

# Example output format:
1.Related research have shown that [research topic].
2.Related research have used [methods], and find that [experimental results].
3.The data comes from [data source] can be used in [research topic].
4.Related research have shown that [experimental results].
5.Related research have found that [conclusion].