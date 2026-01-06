# Analyze Rule

When the user asks you to analyze data, follow these principles:

## Approach

1. **Understand the Context**: Ask clarifying questions if the goal is unclear
2. **Explore the Data**: Check shape, types, missing values, distributions
3. **Identify Patterns**: Look for trends, outliers, correlations, and anomalies
4. **Provide Insights**: Explain what the data shows and why it matters
5. **Visualize**: Create clear, labeled charts using modern design principles
6. **Document**: Add markdown cells explaining your analysis process

## Analysis Checklist

- [ ] Load and inspect the data (shape, columns, types)
- [ ] Check for missing values and data quality issues
- [ ] Calculate summary statistics (mean, median, std, quartiles)
- [ ] Identify distributions and outliers
- [ ] Look for correlations and relationships
- [ ] Create visualizations with proper labels and modern color palettes
- [ ] Provide actionable insights and recommendations

## Code Structure

```python
# 1. Load and inspect data
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv')
print(f"Shape: {df.shape}")
print(df.info())
print(df.head())

# 2. Data quality check
missing = df.isnull().sum()
print(f"Missing values:\n{missing[missing > 0]}")

# 3. Summary statistics
print(df.describe())

# 4. Visualizations
sns.set_style("whitegrid")
sns.set_palette("colorblind")

# Distribution
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=df, x='metric', kde=True, ax=ax)
ax.set_title('Distribution of Metric', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# 5. Insights and conclusions
```

## Output Format

Provide analysis in this structure:

1. **Summary**: High-level findings (2-3 sentences)
2. **Key Metrics**: Important numbers and statistics
3. **Visualizations**: Charts showing patterns and trends
4. **Insights**: What the data reveals
5. **Recommendations**: Actionable next steps

## Principles

- Be thorough but concise
- Focus on what matters most
- Use clear, non-technical language for insights
- Support claims with data and visualizations
- Highlight anomalies and interesting patterns
- Suggest next steps for further analysis
