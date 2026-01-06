---
name: data-visualization
description: Create beautiful, publication-ready visualizations with modern design principles
version: 1.0.0
author: SignalPilot
category: visualization
tags: [visualization, seaborn, matplotlib, design, accessibility]
---

# Data Visualization Skill

Create effective, accessible visualizations using modern design principles, appropriate color palettes, and proper labeling.

## Core Principles

### 1. Choose the Right Chart Type

- **Comparisons**: Bar charts, grouped bar charts
- **Distributions**: Histograms, KDE plots, violin plots, box plots
- **Relationships**: Scatter plots, line plots, heatmaps
- **Time Series**: Line plots, area charts with confidence intervals
- **Composition**: Stacked bar charts, area charts (avoid pie charts with >5 slices)

### 2. Use Modern Color Palettes

**Recommended Palettes**:
- **Categorical**: `colorblind`, `Set2`, `tab10` (for distinct categories)
- **Sequential**: `viridis`, `rocket`, `mako`, `cividis` (for continuous data)
- **Diverging**: `RdBu_r`, `coolwarm`, `PiYG` (for data with meaningful midpoint)

**Avoid**: `jet` colormap, pure red/green combinations, >8 colors

### 3. Proper Labeling

**Always Include**:
- Clear, descriptive title (14-16pt, bold)
- Axis labels with units (11-12pt)
- Legend when needed (avoid redundancy)
- Data source/date when relevant

## Best Practices Template

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Set modern style
sns.set_style("whitegrid")
sns.set_palette("colorblind")
sns.set_context("notebook", font_scale=1.2)

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Create visualization
sns.barplot(data=df, x='category', y='value', hue='segment', palette='Set2', ax=ax)

# Proper labeling
ax.set_title('Revenue by Category and Segment', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Product Category', fontsize=12)
ax.set_ylabel('Revenue ($ millions)', fontsize=12)

# Improve legend
ax.legend(title='Customer Segment', title_fontsize=11, loc='upper right', frameon=True)

# Clean styling
sns.despine()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
```

## Common Patterns

### Distribution Plot

```python
fig, ax = plt.subplots(figsize=(10, 6))

sns.histplot(data=df, x='age', hue='gender', kde=True, palette='mako', alpha=0.6, bins=30, ax=ax)

ax.set_title('Age Distribution by Gender', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Age (years)', fontsize=12)
ax.set_ylabel('Count', fontsize=12)

# Add median lines
for gender in df['gender'].unique():
    median_age = df[df['gender'] == gender]['age'].median()
    ax.axvline(median_age, linestyle='--', linewidth=2, alpha=0.7, label=f'{gender} median')

sns.despine()
plt.tight_layout()
```

### Time Series with Confidence Intervals

```python
fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(data=df, x='date', y='metric', hue='category',
             palette='Set2', linewidth=2.5, ci=95, ax=ax)

ax.set_title('Daily Active Users by Platform', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Daily Active Users (thousands)', fontsize=12)

# Format x-axis dates
import matplotlib.dates as mdates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=45, ha='right')

# Add reference line
ax.axhline(y=500, color='gray', linestyle='--', alpha=0.5, label='Target')

sns.despine()
plt.tight_layout()
```

### Heatmap with Annotations

```python
fig, ax = plt.subplots(figsize=(10, 8))

sns.heatmap(df.corr(), annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=0.5, cbar_kws={'label': 'Correlation'}, ax=ax)

ax.set_title('Feature Correlation Matrix', fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
```

### Small Multiples (Facet Grids)

```python
g = sns.FacetGrid(df, col='region', col_wrap=3, height=4, aspect=1.2, palette='Set2')
g.map_dataframe(sns.barplot, x='category', y='value')
g.set_titles('{col_name}', size=14, weight='bold')
g.set_axis_labels('Category', 'Revenue ($M)', fontsize=11)
g.set_xticklabels(rotation=45, ha='right')
plt.tight_layout()
```

## Color Palette Reference

```python
# Categorical (distinct categories)
sns.set_palette("colorblind")  # Best default
sns.set_palette("Set2")        # Pastel
custom = ['#8B5CF6', '#10B981', '#F59E0B', '#EF4444', '#3B82F6']

# Sequential (continuous)
cmap = sns.color_palette("viridis", as_cmap=True)  # Perceptually uniform
cmap = sns.color_palette("rocket", as_cmap=True)   # Dark to bright

# Diverging (with midpoint)
cmap = sns.color_palette("RdBu_r", as_cmap=True)   # Blue-white-red
cmap = sns.color_palette("coolwarm", as_cmap=True) # Cool to warm
```

## Advanced Techniques

### Annotations

```python
ax.annotate('Key insight here', xy=(x_point, y_point), xytext=(x_text, y_text),
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.5),
            fontsize=10, bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                                  edgecolor='gray', alpha=0.8))
```

### Publication Export

```python
plt.savefig('figure.png', dpi=300, bbox_inches='tight', facecolor='white')  # High-res
plt.savefig('figure.svg', bbox_inches='tight')  # Vector (publications)
```

## Visualization Checklist

- [ ] Chart type matches data and message
- [ ] Colorblind-friendly palette
- [ ] Clear, descriptive title
- [ ] Axis labels with units
- [ ] Legend is necessary and well-placed
- [ ] Font sizes are readable (title 14-16pt, labels 11-12pt, ticks 9-10pt)
- [ ] No chart junk (unnecessary elements)
- [ ] Appropriate aspect ratio and figure size
- [ ] Grid lines aid reading (if used)
- [ ] Data source/date included when relevant
- [ ] Exported at 300 DPI or as vector

## Common Mistakes to Avoid

❌ Too much data (simplify or use facets)
❌ 3D charts (harder to read)
❌ Dual y-axes (can mislead)
❌ Pie charts with >5 slices (use bar chart)
❌ Truncated y-axis on bar charts (start at zero)
❌ Poor contrast (ensure readability)
❌ Missing context (add reference lines, benchmarks)
❌ Too many colors (>8 categories)