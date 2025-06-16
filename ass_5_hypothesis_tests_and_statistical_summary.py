import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('Shopping Trends And Customer Behaviour Dataset.csv')


print("Descriptive Statistics for Purchase Amount:")
print(df['Purchase Amount (USD)'].describe())
print("\nDescriptive Statistics for Age:")
print(df['Age'].describe())


t_stat, p_value_t = stats.ttest_1samp(df['Purchase Amount (USD)'], 60)
print("\nOne-sample t-test (Mean Purchase Amount = 60 USD):")
print(f"t-statistic: {t_stat:.4f}, p-value: {p_value_t:.4f}")
print("Reject H0" if p_value_t < 0.05 else "Fail to reject H0")

df['Purchase_Category'] = pd.qcut(df['Purchase Amount (USD)'], 3, labels=['Low', 'Medium', 'High'])
contingency_table = pd.crosstab(df['Purchase_Category'], df['Category'])
chi2, p_value_chi, dof, expected = stats.chi2_contingency(contingency_table)
print("\nChi-square Test (Purchase Category vs Item Category):")
print(f"Chi2: {chi2:.4f}, p-value: {p_value_chi:.4f}")
print("Reject H0" if p_value_chi < 0.05 else "Fail to reject H0")

correlation = df[['Age', 'Purchase Amount (USD)']].corr()
print("\nCorrelation Matrix (Age vs Purchase Amount):")
print(correlation)

pivot_table = df.pivot_table(values='Purchase Amount (USD)', index='Purchase_Category', 
                            columns='Category', aggfunc='mean')
print("\nPivot Table (Mean Purchase Amount by Category):")
print(pivot_table)

plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
sns.histplot(df['Purchase Amount (USD)'], kde=True, color='skyblue')
plt.title('Purchase Amount Distribution')

plt.subplot(2, 2, 2)
sns.boxplot(x='Category', y='Purchase Amount (USD)', data=df, palette='Set2')
plt.title('Purchase Amount by Category')
plt.xticks(rotation=45)

plt.subplot(2, 2, 3)
sns.heatmap(correlation, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Heatmap (Age vs Purchase Amount)')

plt.subplot(2, 2, 4)
sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='.2f')
plt.title('Mean Purchase Amount by Category')

plt.tight_layout()
plt.show()

print("\n# Summary of Findings\n")
print("- **Descriptive Statistics**: The average purchase amount is around ${:.2f} with a standard deviation of ${:.2f}. The age of customers ranges from {} to {} years.".format(
    df['Purchase Amount (USD)'].mean(), df['Purchase Amount (USD)'].std(), df['Age'].min(), df['Age'].max()))
print("- **t-test**: The p-value ({:.4f}) suggests {} the null hypothesis that the mean purchase amount is $60.".format(
    p_value_t, "rejecting" if p_value_t < 0.05 else "failing to reject"))
print("- **Chi-square Test**: The p-value ({:.4f}) indicates {} the null hypothesis of independence between purchase amount categories and item categories.".format(
    p_value_chi, "rejecting" if p_value_chi < 0.05 else "failing to reject"))
print("- **Correlation**: The correlation between age and purchase amount is {:.4f}, suggesting {} relationship.".format(
    correlation.loc['Age', 'Purchase Amount (USD)'], 
    "a weak" if abs(correlation.loc['Age', 'Purchase Amount (USD)']) < 0.3 else "a moderate/strong"))
print("- **Pivot Table & Visualizations**: The heatmap and boxplots highlight variations in purchase amounts across categories, with {} showing the highest average spend.".format(
    pivot_table.mean().idxmax()))