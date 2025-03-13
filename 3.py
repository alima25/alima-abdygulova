import pandas as pd
import numpy as np

# 1. Handling Missing Data:
# Identifying missing values in a DataFrame using isnull().sum()
def identify_missing_values(df):
    return df.isnull().sum()

# Imputation: Filling missing values using mean, median, or mode
# It is useful to ensure data consistency and allow ML models to work correctly.
def impute_missing_values(df, column, strategy="mean"):
    if strategy == "mean":
        df[column].fillna(df[column].mean(), inplace=True)
    elif strategy == "median":
        df[column].fillna(df[column].median(), inplace=True)
    elif strategy == "mode":
        df[column].fillna(df[column].mode()[0], inplace=True)
    return df

# 2. Data Transformation:
# Encoding categorical variables using label encoding
from sklearn.preprocessing import LabelEncoder

def label_encode(df, column):
    encoder = LabelEncoder()
    df[column] = encoder.fit_transform(df[column])
    return df

# One-hot encoding: Converting categorical variables into dummy variables

def one_hot_encode(df, column):
    return pd.get_dummies(df, columns=[column])

# 3. Removing Duplicates:
# Identifying and removing duplicate rows from a DataFrame
def remove_duplicates(df):
    return df.drop_duplicates()

# Difference between duplicated() and drop_duplicates():
# - duplicated() returns a boolean Series indicating duplicate rows.
# - drop_duplicates() removes duplicate rows from the DataFrame.

def identify_duplicates(df):
    return df.duplicated()

# 4. Data Scaling and Normalization:
# Feature scaling is important in ML to ensure features are on a similar scale.
# - Min-Max Scaling: Scales data to a range of 0-1
# - Z-score Normalization: Standardizes data to have mean 0 and standard deviation 1
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def min_max_scale(df, column):
    scaler = MinMaxScaler()
    df[column] = scaler.fit_transform(df[[column]])
    return df

def z_score_normalize(df, column):
    scaler = StandardScaler()
    df[column] = scaler.fit_transform(df[[column]])
    return df

# 5. Handling Outliers:
# Outliers are extreme values that can impact ML models by skewing distributions.
# Detecting outliers using the IQR method
def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]

# Handling outliers by capping (Winsorization)
def handle_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
    df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])
    return df
