import os,sys
import psycopg2
import csv


# Get DataPath
try:
    path = sys.argv[1]
except:
    path = '.'


# Connect To DataBase
# conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
try:
    conn = psycopg2.connect("host=localhost dbname=FakeUData user=postgres")
    print("Successfully Connecte to Database!\n")
    cur = conn.cursor()

except:
    print("ERROR: Failed to Connect To Database!\n")

i = 0

with open('./Grades/2012_Q3.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print("\nLINE: " + str(i) + " --> " + str(row))
        i += 1
