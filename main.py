import os,sys
import psycopg2
import csv
from collections import defaultdict


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
except:
    print("ERROR: Failed to Connect To Database!\n")


try:
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
        CID integer,
        TERM integer,
        INSTRUCTOR varchar(64),
        TYPE varchar(64),
        DAYS varchar(5),
        TIME varchar(20),
        BUILD varchar(16),
        ROOM varchar(8),
        PRIMARY KEY(CID, TERM, INSTRUCTOR, TYPE, DAYS, TIME, BUILD, ROOM)
    )
    """)

    # Create Students Table
    cur.execute("""
    CREATE TABLE students(
        SID integer PRIMARY KEY,
        SURNAME varchar(64),
        PREFNAME varchar(64),
        EMAIL varchar(128)
    )
    """)


    # Create Enrollment
    cur.execute("""
    CREATE TABLE enrollment(
        CID integer,
        TERM integer,
        SID integer,
        LEVEL varchar(4),
        UNITS float,
        CLASS varchar(4),
        MAJOR varchar(4),
        GRADE varchar(4),
        STATUS varchar(4),
        PRIMARY KEY(CID, TERM, SID)
    )
    """)


    # Create GPA
    cur.execute("""
    CREATE TABLE gpa(
        GRADE varchar(2) PRIMARY KEY,
        VALUE float
    )
    """)

    grades = [('A+',4.0), ('A',4.0), ('A-',3.7),
              ('B+',3.3), ('B',3.0), ('B-',2.7),
              ('C+',2.3), ('C',2.0), ('C-',1.7),
              ('D+',1.3), ('D',1.0), ('D-',0.7),
              ('F',0.0)
        ]

    SQL = "INSERT INTO gpa VALUES (%s, %s);"
    cur.executemany(SQL,grades)

    conn.commit()
except:
    print("FAILED TO CREATE TABLE\n")






start_year = 1989
end_year = 2012
quarters = ['Q1','Q2','Q3','Q4']


student_dict = defaultdict(lambda:0)

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
        batch_course = []
        batch_meeting = []
        batch_student = []
        batch_enrollment = []

        # Skip Blank Header
        next(reader)

        for row in reader:

            meeting_list = []
            student_list = []

            course_data = next(reader)

            # Skip Blank Header
            skip = next(reader)

            meeting_dict = defaultdict(lambda:0)
            meeting_list = [[course_data[0], course_data[1]]]
            meeting_header = next(reader)

            # Get all meeting locations
            while True:
                meeting_data = next(reader)
                if meeting_data == ['']:
                    break
                else:
                    if tuple(meeting_data) not in meeting_dict:
                        meeting_dict[tuple(meeting_data)]
                        meeting_list.append(meeting_data)
                    else:
                        continue


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

                capacity = len(student_list) - 1
                course_data.append(str(capacity))
                batch_course.append(tuple(course_data))

                for m in meeting_list[1:]:
                    meeting_tuple = [course_data[0], course_data[1]]
                    meeting_tuple.extend(m)
                    batch_meeting.append(tuple(meeting_tuple))

                # Add Static Student Info
                for s in student_list[1:]:
                    if tuple(s[1:4]) not in student_dict:
                        # Add student to static dictionary
                        student_dict[tuple(s[1:4])]
                        student_tuple = s[1:4]
                        student_tuple.append(s[10])
                        batch_student.append(tuple(student_tuple))
                    else:
                        continue

                # Add enrollment
                for s in student_list[1:]:
                    enrollment_tuple = [course_data[0], course_data[1]]
                    enrollment_tuple.append(s[1])
                    enrollment_tuple.extend(s[4:10])
                    batch_enrollment.append(tuple(enrollment_tuple))



        # ADD Batch to DB
        conn = psycopg2.connect("host=localhost dbname=FakeUData user=postgres")
        cur = conn.cursor()

        # Add Course Info
        SQL = "INSERT INTO course VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cur.executemany(SQL, batch_course)

        # Add Meeting Info
        SQL = "INSERT INTO meeting VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        cur.executemany(SQL, batch_meeting)

        # Add Static Student Info
        SQL = "INSERT INTO students VALUES (%s, %s, %s, %s);"
        cur.executemany(SQL, batch_student)

        # Add Class enrollment
        SQL = "INSERT INTO enrollment VALUES (%s, %s, %s, %s, NULLIF(%s,'')::float, %s, %s, %s, %s);"
        cur.executemany(SQL, batch_enrollment)

        conn.commit()
