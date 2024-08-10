import csv, sqlite3
import pandas as pd

#####################
# Constants
FILEPATH = "/Users/fpj/Development/python/spacey/data/"
FILESPACEX = "Spacex.csv"

# Connect to the database
con = sqlite3.connect("my_data1.db")
cur = con.cursor()


df = pd.read_csv(FILEPATH + FILESPACEX)
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")

# Drop the table if exists
cur.execute("DROP TABLE IF EXISTS SPACEXTABLE")
# Create a new table with the same columns
cur.execute("create table SPACEXTABLE as select * FROM SPACEXTBL WHERE Date is not null")
#
# Display the names of the unique launch sites
cur.execute("SELECT DISTINCT Launch_Site FROM SPACEXTABLE")
launch_sites = cur.fetchall()
print("Launch Sites\n", launch_sites)
# Get 5 records where launch sites begin with CCA 
cur.execute("SELECT * FROM SPACEXTABLE WHERE Launch_Site LIKE 'CCA%' LIMIT 5")
# Fetch 5 records where launch sites begin with CCA
first_records = cur.fetchmany(5)
for record in first_records:
    print(record)
# Get the total payload mass carried by boosters launched by NASA (CRS)
cur.execute("SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTABLE WHERE Customer = 'NASA (CRS)'")
total_payload_mass = cur.fetchall()
print("Total Payload Mass carried by NASA (CRS): ", total_payload_mass[0][0])
# Get the average payload mass carried by booster version F9 v1.1
cur.execute("SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTABLE WHERE Booster_Version = 'F9 v1.1'")
avg_payload_mass = cur.fetchall()
print("Average Payload Mass carried by F9 v1.1: ", avg_payload_mass[0][0])
# Find the date of the first successful landing outcome in ground pad
cur.execute("SELECT Date FROM SPACEXTABLE WHERE Landing_Outcome = 'Success (ground pad)' ORDER BY Date ASC LIMIT 1")
first_success_date = cur.fetchall()
print("First Successful Landing Date: ", first_success_date[0][0])
# List the names of the boosters which have success in drone ship and payload mass greater than 4000 but less than 6000
cur.execute("SELECT Booster_Version FROM SPACEXTABLE WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000")
success_boosters = cur.fetchall()
print("Boosters with Success in Drone Ship and Payload Mass between 4000 and 6000: ", success_boosters)
# List the total number of successful and failure mission outcomes
cur.execute("SELECT Mission_Outcome, COUNT(*) FROM SPACEXTABLE GROUP BY Mission_Outcome")
mission_outcomes = cur.fetchall()
print("Total Number of Successful and Failure Mission Outcomes: ", mission_outcomes)
# List the names of the booster versions which have carried the maximum payload mass
cur.execute("SELECT Booster_Version FROM SPACEXTABLE WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTABLE)")
max_payload_boosters = cur.fetchall()
print("Booster Versions with Maximum Payload Mass: ", max_payload_boosters)
# List the records which will display the month names, failure landing outcomes in drone ship, booster versions, and launch sites for the months in year 2015
cur.execute("SELECT strftime('%m', Date) AS Month, Landing_Outcome, Booster_Version, Launch_Site FROM SPACEXTABLE WHERE Landing_Outcome = 'Failure (drone ship)' AND strftime('%Y', Date) = '2015'")
failure_records = cur.fetchall()
print("Failure Landing Outcomes in Drone Ship for 2015: ", failure_records)
#
# Rank the count of landing outcomes (such as Failure (drone ship), Success (ground pad), etc.) in descending order between the date 2010-06-04 and 2017-03-20
cur.execute("SELECT Landing_Outcome, COUNT(*) FROM SPACEXTABLE WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY COUNT(*) DESC")
landing_outcomes = cur.fetchall()
print("Landing Outcomes Between 2010-06-04 and 2017-03-20: ", landing_outcomes)
# Select the minimum payload mass from the table
cur.execute("SELECT MIN(PAYLOAD_MASS__KG_) FROM SPACEXTABLE")
min_payload_mass = cur.fetchall()
print("Minimum Payload Mass: ", min_payload_mass[0][0])
# Close the database connection
con.close()
