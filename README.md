# Introduction
This repo is a demo to retrieve topic notes (background knowledge) for AP calculus question.

# Run this demo
Fill your own OPENAI API KEY in streamlitDemo.py

`pip install -q streamlit langchain llama_index openai qdrant_client lxml`

`streamlit run streamlitDemo.py`

# Potential Questions
1. "Prove that $\lim _{x \rightarrow 0} x^{10} \cos \frac{3 \pi}{x}=0$"

2. "Find the points on the graph of $f(x)=2x^3-3x^2-12x+8$ where the tangent is horizontal."

3. "Find the average value of the function $f(x)=4+x-x^3$ on the interval [-2,3]."

4. "Find the length of the curve $r=4sin\theta$ from 0≤θ≤π."

5. "Show that the following series are convergent and find its sum: $\sum_{n=0}^\infty \frac{1}{3^n}$"

6. "Use the Comparison Test to determine if the series converge or diverge. $\sum_{n=1}^\infty \frac{1}{2^n+5}$"

7. "Differentiate: Polynomial Functions $\frac{d}{dx}(2x-1)^3$"

8. "Determine if the series is absolutely convergent, conditionally convergent, or divergent. \sum_{n=2}^\infty \frac{(-1)^n}{n-1}$"

# Additional Info
Note that crawler.py needs modifying because it only output [URL,Topic Notes]

The csv file still needs Summary column

demo.csv in this folder is created manually