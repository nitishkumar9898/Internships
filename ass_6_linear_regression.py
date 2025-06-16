import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm

np.random.seed(42)

try:
    df = pd.read_csv('Salaries.csv')
except FileNotFoundError:
    print('Error: Salary_Data.csv not found. Please ensure the file is in the correct directory.')
    exit()

print('Dataset Preview:')
print(df.head())
print('\nDataset Statistics:')
print(df.describe())
print('\nMissing Values:')
print(df.isnull().sum())

try:
    X = df[['YearsExperience']]  
    y = df['Salary']  
except KeyError as e:
    print(f'Error: Column {e} not found in the dataset. Please check the column names.')
    exit()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

sk_model = LinearRegression()
sk_model.fit(X_train, y_train)
y_pred = sk_model.predict(X_test)


X_train_sm = sm.add_constant(X_train)  
X_test_sm = sm.add_constant(X_test)
sm_model = sm.OLS(y_train, X_train_sm).fit()

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print('\nModel Evaluation:')
print(f'Mean Squared Error: {mse:.2f}')
print(f'R2 Score: {r2:.2f}')
print('\nStatsmodels Summary:')
print(sm_model.summary())

plt.figure(figsize=(12, 6))
plt.scatter(X, y, color='blue', label='Data points')

X_plot = np.linspace(X['YearsExperience'].min(), X['YearsExperience'].max(), 100).reshape(-1, 1)
X_plot_sm = sm.add_constant(X_plot)
y_plot = sk_model.predict(X_plot)
plt.plot(X_plot, y_plot, color='red', label='Regression line')

predictions = sm_model.get_prediction(X_plot_sm)
conf_int = predictions.conf_int(alpha=0.05)
plt.fill_between(X_plot.flatten(), conf_int[:, 0], conf_int[:, 1], color='red', alpha=0.1, label='95% Confidence Interval')

plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.title('Salary vs Years of Experience with Confidence Interval')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))
bar_width = 0.35
index = np.arange(len(y_test))
plt.bar(index, y_test, bar_width, label='Actual Salary', color='blue')
plt.bar(index + bar_width, y_pred, bar_width, label='Predicted Salary', color='orange')
plt.xlabel('Test Sample')
plt.ylabel('Salary')
plt.title('Actual vs Predicted Salaries')
plt.xticks(index + bar_width / 2, [f'Sample {i+1}' for i in range(len(y_test))])
plt.legend()
plt.grid(True)
plt.show()

while True:
    try:
        years = float(input('Enter years of experience (or -1 to exit): '))
        if years == -1:
            break
        if years < 0:
            print('Please enter a non-negative number of years.')
            continue
        predicted_salary = sk_model.predict([[years]])[0]
        print(f'Predicted salary for {years} years of experience: ${predicted_salary:.2f}')
    except ValueError:
        print('Please enter a valid number.')