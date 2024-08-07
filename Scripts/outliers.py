import pandas as pd

data_file = r'C:\Users\Elliot\Downloads\residuals_summeravg_vs_percent_lessthan10.csv'
df = pd.read_csv(data_file)

Q1 = df['Residual'].quantile(0.25)
Q3 = df['Residual'].quantile(0.75)
IQR = Q3 - Q1

# Define the lower and upper bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Find outliers
outliers = df[(df['Residual'] < lower_bound) | (df['Residual'] > upper_bound)]
outliers.to_csv(r'C:\Users\Elliot\Downloads\outliers_lessthan10.csv')