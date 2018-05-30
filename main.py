import os,sys
import psycopg2
import csv


# Get DataPath
try:
    path = sys.argv[1]
except:
    path = './Grades/'

# Connect To DataBase
# conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
try:
    conn = psycopg2.connect("host=localhost dbname=FakeUData user=postgres")
    print("Successfully Connecte to Database!\n", conn)
    cur = conn.cursor()

    # Create Course Relation
    cur.execute("""
    CREATE TABLE course(
        CID integer,
        TERM integer,
        SUBJ char(3),
        CRSE int,
        SEC int,
        UNITS varchar(14),
        ENROLLED int,
        PRIMARY KEY(CID, TERM)
    )
    """)

    # Create Relation Meeting
    cur.execute("""
    CREATE TABLE meeting(
        CID integer PRIMARY KEY,
        INSTRUCTOR varchar(64),
        TYPE varchar(64),
        DAYS varchar(5),
        TIME varchar(20),
        BUILD varchar(16),
        ROOM int
    )
    """)

    conn.commit()
except:
    print("ERROR: Failed to Connect To Database!\n")


start_year = 1989
end_year = 2012
quarters = ['Q1','Q2','Q3','Q4']


for year in range(start_year, end_year+1):
    for quarter in quarters:

        # Open File
        try:
            file_name = str(path) + str(year) + '_' + quarter + '.csv'
            f = open(file_name, newline='')
            print("OPENED FILE: ", file_name)
        except:
            print("ERROR: Cannot open file", file_name)
            if quarter == 'Q4': break
            else: continue

        # Read Rows of Single File
        reader = csv.reader(f)

        # Initialize Batch Send Object
        batch_course = ""

        # Skip Blank Header
        next(reader)

        for row in reader:

            meeting_list = []
            student_list = []

            course_data = next(reader)

            # Skip Blank Header
            skip = next(reader)

            meeting_list = [[course_data[0], course_data[1]]]
            meeting_header = next(reader)

            # Get all meeting locations
            while True:
                meeting_data = next(reader)
                if meeting_data == ['']:
                    break
                else:
                    meeting_list.append(meeting_data)

            student_list = [[course_data[0], course_data[1]]]
            student_header = next(reader)

            # Get all students
            while True:
                try:
                    student_data = next(reader)
                except:
                    break

                if student_data == ['']:
                    break
                else:
                    student_list.append(student_data)

            if len(student_list) > 1:

                # print("\n\n***********************************************\n\n")
                # print("\n\nCourse INFO: \n\n ",course_data)
                #
                # print("\n\n***********************************************\n\n")
                # print("\n\nMEETING INFO: \n\n ",meeting_list)
                #
                # print("\n\n***********************************************\n\n")
                # print("\n\nSTUDENTS: \n\n ",student_list, len(student_list))
                capacity = len(student_list) - 1
                print(course_data, type(course_data), capacity, type(capacity))
                course_data.append(capacity)
                print(course_data)

                batch_course += str(tuple(course_data)) + ","


        conn = psycopg2.connect("host=localhost dbname=FakeUData user=postgres")
        cur = conn.cursor()

        batch_course = batch_course[:-1]
        cur.execute(
        "INSERT INTO course VALUES " + batch_course
        )
        conn.commit()
