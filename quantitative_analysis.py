import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

# Load Data
df = pd.read_csv("cpu_utilization_asg_misconfiguration.csv")

# Convert timestamps
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Data Validation
# Check for missing values in each column
print(df.isnull().sum())
df = df.dropna() 
print()

# Validate Timestamp Conversion
if df['timestamp'].isnull().any():
    print("Invalid timestamps found!")
    df = df.dropna(subset=['timestamp'])
else: 
    print("All timestamps are valid.")
    print()

# Validate Numeric Column
if not pd.api.types.is_numeric_dtype(df['value']):
    print("Non-numeric values found in 'value' column!")
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna(subset=['value'])
else:
    print("All values are numeric.")
    print()

# Calculate Threshold
mean = df['value'].mean()
std = df['value'].std()
threshold = mean + 2 * std

# Create anomaly column
df['anomaly'] = df['value'] > threshold

# Check data
print(df.head())
print(df['anomaly'].value_counts())
print()

# Split the data
normal = df[df['anomaly'] == False]['value']
anomaly = df[df['anomaly'] == True]['value']

print("Normal count:", len(normal))
print("Anomaly count:", len(anomaly))
print()

# Calculate Median
print("Overall median:", df['value'].median())
print("Normal median:", normal.median())
print("Anomaly median:", anomaly.median())
print()

# Calculate Mean
print("Overall mean:", df['value'].mean())
print("Normal mean:", normal.mean())
print("Anomaly mean:", anomaly.mean())
print()

# Welch's t-test
t_stat, p_value = ttest_ind(normal, anomaly, equal_var=False)

print("t-statistic:", t_stat)
print("p-value: {:.20f}".format(p_value))
print()

# Scatter Plot (normal vs anomaly)
plt.figure()

plt.scatter(df[df['anomaly']==False]['timestamp'], 
            df[df['anomaly']==False]['value'], 
            alpha=0.3, label='Normal')

plt.scatter(df[df['anomaly']==True]['timestamp'], 
            df[df['anomaly']==True]['value'], 
            alpha=0.8, label='Anomaly')

plt.legend()
plt.xlabel("Time")
plt.ylabel("CPU Usage")
plt.title("CPU Usage Over Time")

plt.xticks(rotation=45)

plt.show()

# Boxplot (Normal vs Anomaly)
plt.figure()

plt.boxplot([normal, anomaly], tick_labels=['Normal', 'Anomaly'])

plt.ylabel("CPU Usage")
plt.title("CPU Usage Comparison")

plt.show()

# Histogram (normal vs anomaly)
plt.figure()

plt.hist(normal, bins=50, alpha=0.5, label='Normal')
plt.hist(anomaly, bins=50, alpha=0.5, label='Anomaly')

plt.legend()
plt.xlabel("CPU Usage")
plt.ylabel("Frequency")
plt.title("Distribution of CPU Usage: Normal vs Anomalous")

plt.show()

# Summary Table
summary = pd.DataFrame({
    'Condition': ['Overall', 'Normal', 'Anomalous'],
    'Mean': [
        df['value'].mean(),
        normal.mean(),
        anomaly.mean()
    ],
    'Median': [
        df['value'].median(),
        normal.median(),
        anomaly.median()
    ],
    'Std Dev': [
        df['value'].std(),
        normal.std(),
        anomaly.std()
    ],
    'Count': [
        len(df),
        len(normal),
        len(anomaly)
    ]
})

print(summary)

summary.to_excel("cpu_utilisation_statistics_summary.xlsx", index=False)