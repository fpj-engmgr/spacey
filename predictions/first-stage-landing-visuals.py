# pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns

#from js import fetch
import io

DATA_DIR = "/Users/fpj/Development/python/spacey/data/"
DATA_FILE = "dataset_part_2.csv"
#
# Load the data

df = pd.read_csv(DATA_DIR + DATA_FILE)
print(df.head())
#
sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()
# Plot a scatter point chart with x axis to be Flight Number and y axis to be the launch site, and hue to be the class value
sns.scatterplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Launch Site", fontsize=20)
plt.show()

# Visualize the relationship between Payload Mass and Launch Site
sns.scatterplot(x="PayloadMass", y="LaunchSite", hue="Class", data=df)
plt.xlabel("Launch Site", fontsize=20)
plt.ylabel("Pay load Mass (kg)", fontsize=20)
plt.show()

# Create a bar chart to visualize the relationship between success rate of each orbit type
# Use groupby orbit column and get the mean of the class column
orbit_success_rate = df.groupby("Orbit")["Class"].mean()
# Display the bar chart
orbit_success_rate.plot(kind='bar')
plt.xlabel("Orbit", fontsize=20)
plt.ylabel("Success Rate", fontsize=20)
plt.show()

# Visualize the relationship between Flight Number and Orbit type
sns.scatterplot(x="FlightNumber", y="Orbit", hue="Class", data=df)
plt.xlabel("Flight Number", fontsize=20)
plt.ylabel("Orbit", fontsize=20)
plt.show()

# Visualize the relationship between Payload and Orbit type
sns.scatterplot(x="PayloadMass", y="Orbit", hue="Class", data=df)
plt.xlabel("Payload Mass (kg)", fontsize=20)
plt.ylabel("Orbit", fontsize=20)
plt.show()

# A function to Extract years from the date 
year=[]
def Extract_year():
    for i in df["Date"]:
        year.append(i.split("-")[0])
    return year
Extract_year()
df['Date'] = year
df.head()

# Plot a line chart with x axis to be the extracted year and y axis to be the success rate
df.groupby("Date")["Class"].mean().plot(kind="line")
plt.xlabel("Launch Year", fontsize=20)
plt.ylabel("Success Rate", fontsize=20)
plt.show()

# Features Engineering
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()
# Use the get_dummies function and features dataframe to apply OneHotEncoder to column Orbit, LauchSite, LandingPad and Serial
features_one_hot = pd.get_dummies(features)
features_one_hot.head()
# Cast all numeric columns to `float64`
features_one_hot = features_one_hot.astype('float64')

# Export the data to a new CSV file
features_one_hot.to_csv(DATA_DIR + 'dataset_part_3.csv')
