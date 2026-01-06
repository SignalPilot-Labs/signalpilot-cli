# Investigate Rule

When the user asks you to investigate an issue, anomaly, or unexpected result, follow these principles:

## Approach

1. **State the Problem**: Clearly define what you're investigating
2. **Form Hypotheses**: List possible causes or explanations
3. **Gather Evidence**: Collect data systematically
4. **Test Hypotheses**: Check each possibility with data
5. **Draw Conclusions**: Identify the root cause
6. **Recommend Actions**: Suggest next steps

## Investigation Framework

### 1. Define the Problem

```markdown
## Investigation: [Clear problem statement]

**Expected**: [What should happen]
**Actual**: [What is happening]
**Impact**: [Why this matters]
```

### 2. Generate Hypotheses

List possible causes:
- Hypothesis 1: [Possible cause]
- Hypothesis 2: [Possible cause]
- Hypothesis 3: [Possible cause]

### 3. Systematic Checks

```python
# Check 1: Data quality
print("Missing values:", df.isnull().sum().sum())
print("Duplicates:", df.duplicated().sum())

# Check 2: Data distribution
print(df.describe())

# Check 3: Time-based patterns
df['date'] = pd.to_datetime(df['date'])
df.set_index('date')['metric'].plot(figsize=(12,6))
plt.title('Metric Over Time')
plt.show()

# Check 4: Segment analysis
df.groupby('segment')['metric'].describe()
```

### 4. Document Findings

```markdown
## Findings

### Hypothesis 1: [Tested hypothesis]
**Result**: ✓ Confirmed / ✗ Rejected
**Evidence**: [Data supporting this conclusion]

## Root Cause
[Clear statement of what's causing the issue]

## Evidence Summary
- [Key data point 1]
- [Key data point 2]
```

### 5. Recommendations

```markdown
## Recommended Actions

1. **Immediate**: [Quick fix or mitigation]
2. **Short-term**: [Address the root cause]
3. **Long-term**: [Prevent recurrence]
```

## Principles

- Be systematic and thorough
- Show your work and document each step
- Use data to support conclusions
- Stay objective and don't jump to conclusions
- Provide specific, actionable recommendations
