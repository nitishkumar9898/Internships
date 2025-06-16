import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('Titanic-Dataset.csv')

df['Age'].fillna(df['Age'].median(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
df.drop('Cabin', axis=1, inplace=True)  
df['Survived'] = df['Survived'].astype('category')

df.drop_duplicates(inplace=True)

print("Dataset Info:")
print(df.info())
print("\nSummary Statistics:")
print(df.describe())
print("\nValue Counts for Categorical Variables:")
print(df['Survived'].value_counts())
print(df['Pclass'].value_counts())

plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
sns.histplot(df['Age'], bins=30)
plt.title('Age Distribution')

plt.subplot(2, 2, 2)
sns.boxplot(x='Pclass', y='Fare', data=df)
plt.title('Fare Distribution by Passenger Class')

plt.subplot(2, 2, 3)
sns.countplot(x='Survived', data=df)
plt.title('Survival Count')

plt.subplot(2, 2, 4)
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')

plt.tight_layout()
plt.show()

print("\nSurvival Rate by Passenger Class:")
print(df.groupby('Pclass')['Survived'].mean())

df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
print("\nSurvival Rate by Family Size:")
print(df.groupby('FamilySize')['Survived'].mean())

plt.figure(figsize=(8, 6))
sns.violinplot(x='Pclass', y='Age', hue='Survived', split=True, data=df)
plt.title('Age Distribution by Class and Survival')
plt.show()

# Top 5 Insights
print("""
Top 5 Insights:
1. Age distribution is right-skewed with most passengers between 20-40 years.
2. Higher passenger class (Pclass=1) had better survival rates.
3. Larger families (FamilySize > 4) had lower survival rates.
4. Fare and Pclass show strong negative correlation.
5. Younger passengers in higher classes had better survival chances.
""")