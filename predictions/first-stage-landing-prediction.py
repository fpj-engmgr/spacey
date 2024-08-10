# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np

# The data...
DATA_DIR = "/Users/fpj/Development/python/spacey/data/"
FILENAME = "dataset_part_1.csv"
# Get the previously saved data
df = pd.read_csv(DATA_DIR + FILENAME)
# Show the head of the dataframe
print(df.head(10))
#
print(df.isnull().sum()/len(df)*100)
# Calculate the number of launches on each site
print(df['LaunchSite'].value_counts())
# Calculate the number and occurrence of each orbit
print(df['Orbit'].value_counts())
# Calculate the number and occurrence of mission outcome
landing_outcomes = df['Outcome'].value_counts()
print(type(landing_outcomes))
print(landing_outcomes)
#
for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)
#
bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
print(bad_outcomes)
# Create a landing outcome label from Outcome column
landing_class = []
for outcome in df['Outcome']:
    if outcome in bad_outcomes:
        landing_class.append(0)
    else:
        landing_class.append(1)
#
df['Class']=landing_class
print(df[['Class']].head(8))
print(df.head(5))
print(df['Class'].mean())

# Export the dataframe to a csv file
df.to_csv('../data/dataset_part_2.csv', index=False)
