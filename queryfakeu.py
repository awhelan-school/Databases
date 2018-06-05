import psycopg2
from collections import defaultdict
import matplotlib.pyplot as plt


unit_increments = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0,
                   11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0}

gpa_increments = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0,
                   11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0}

units_quarter = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0,
                   11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0}

conn = psycopg2.connect("host=localhost dbname=FakeUData user=postgres")
cur = conn.cursor()


# # GET ALL TERMS
# cur.execute("""
#     SELECT DISTINCT term
#     FROM enrollment
#     ORDER BY term ASC
# """)
# terms = cur.fetchall()
#
# total_students = 0
# total_terms = len(terms)
#
# for term in terms:
#     # GET units attempted
#     cur.execute("""
#         SELECT R.units_taken, count(*) AS number_students
#         FROM (SELECT DISTINCT sid, sum(units) as units_taken
#         	   FROM enrollment as c1
#                WHERE c1.term = %s and c1.grade <> 'F'
#                GROUP BY c1.sid
#                ORDER BY sid) R
#         GROUP BY R.units_taken
#         ORDER BY R.units_taken ASC
#     """ % term)
#     sample = cur.fetchall()
#
#     # Gets Grade in FORMAT
#     # {SID, TERM, UNITS_COMPLETED, UNITS_ATTEMPTED, GRADE_POINTS}
#     cur.execute("""
#
#     SELECT units_completed, avg(grade_points) / avg(units_attempted) as gpa
#     FROM(
#     	SELECT sid, term, units_completed, sum(units) as units_attempted, sum(value * units) as grade_points
#     	FROM enrollment NATURAL JOIN (
#     		SELECT DISTINCT sid, sum(units) as units_completed
#     		FROM enrollment as c1
#     		WHERE c1.term = %s
#     		GROUP BY c1.sid ) R NATURAL JOIN gpa
#     	WHERE enrollment.term = %s
#     	GROUP BY sid, term, units_completed
#     	ORDER BY sid ) S
#     WHERE units_attempted > 0
#     GROUP BY units_completed
#     ORDER BY units_completed ASC
#
#     """, [term, term])
#     student_gpas = cur.fetchall()
#
#     for g in student_gpas:
#         if g[0] in gpa_increments:
#             units_quarter[g[0]] += 1
#             gpa_increments[g[0]] += g[1]
#
#     total_students += sum(t[1] for t in sample)
#
#     for s in sample:
#         if s[0] in unit_increments:
#             unit_increments[s[0]] += s[1]
#
#
#
# for x in range(1,21):
#     unit_increments[x] /= total_students
#     gpa_increments[x] /= units_quarter[x]
#
# # plt.bar(range(len(unit_increments)), list(unit_increments.values()), align='center')
# # plt.xticks(range(len(unit_increments)), list(unit_increments.keys()))
# # plt.show()
#
#
# plt.bar(range(len(gpa_increments)), list(gpa_increments.values()), align='center')
# plt.xticks(range(len(gpa_increments)), list(gpa_increments.keys()))
# plt.show()
#
#
# print("PERCENT TOTAL ==>", sum(unit_increments.values()))
#
#
#
# grades = {'A+':4.0, 'A':4.0, 'A-':3.7,
#           'B+':3.3, 'B':3.0, 'B-':2.7,
#           'C+':2.3, 'C':2.0, 'C-':1.7,
#           'D+':1.3, 'D':1.0, 'D-':0.7,
#           'F':0.0
#     }
#
# # Select ALL Instructors
# cur.execute("""
#     SELECT DISTINCT(instructor)
#     FROM meeting
# """)
# instructors = cur.fetchall()
#
# instructors_dict = defaultdict()
# for instructor in instructors:
#     instructors_dict[instructor[0]] = None
#
#     cur.execute("""
#     	SELECT sum(S.grade_points) / sum(S.grades_count) AS avg_grade
# 	    FROM (SELECT grade, count(grade) AS grades_count, gpa.value, count(grade) * gpa.value AS grade_points
# 		FROM (SELECT cid, term
# 				FROM meeting
# 				WHERE instructor = %s)R NATURAL JOIN enrollment NATURAL JOIN gpa
# 		WHERE grade = 'A+' or grade = 'A' or grade = 'A-' or
# 			   grade = 'B+' or grade = 'B' or grade = 'B-' or
# 			   grade = 'C+' or grade = 'C' or grade = 'C-' or
# 			   grade = 'D+' or grade = 'D' or grade = 'D-' or
# 			   grade = 'F'
# 		GROUP BY grade, gpa.value
# 		ORDER BY grade ASC) S
#     """, instructor)
#
#     avg_grade = cur.fetchone()
#
#
#     if avg_grade[0] == None:
#         del instructors_dict[instructor[0]]
#     else:
#         instructors_dict[instructor[0]] = avg_grade[0]
#
# best = max(instructors_dict.values())
# worst = min(instructors_dict.values())
#
#
# best_instructors = []
# worst_instructors = []
# worst_letter = ''
# best_letter = ''
#
# for g in list(grades.items()):
#     if best < g[1] + float(0.33/2) and best >= g[1] - float(0.33/2):
#         best_letter = g[0]
#     elif worst < g[1] + float(0.33/2) and worst >= g[1] - float(0.33/2):
#         worst_letter = g[0]
#
# for i in instructors_dict.items():
#     if i[1] == best:
#         l = list(i)
#         l[1] = best_letter
#         best_instructors.append(l)
#     elif i[1] == worst:
#         l = list(i)
#         l[1] = worst_letter
#         worst_instructors.append(l)
#
# print("BEST: ", best, "GRADE: ", best_instructors, "\n")
# print("WORST: ", worst, "GRADE: ", worst_instructors, "\n")




# # Problem 3D
# course_dict = defaultdict(lambda:0)
#
# # GET all course as unique
# cur.execute("""
# SELECT DISTINCT crse, subj
# FROM course
# """)
#
# course_list = cur.fetchall()
# for f in course_list:
#     cur.execute("""
#     SELECT count(*)
#     FROM (SELECT cid, term
# 		FROM course
# 		WHERE subj = %s and crse = %s) R NATURAL JOIN enrollment
#         WHERE  grade = 'A+' or grade = 'A' or grade = 'A-' or
#         	   grade = 'B+' or grade = 'B' or grade = 'B-' or
#         	   grade = 'C+' or grade = 'C' or grade = 'C-' or
#         	   grade = 'D+' or grade = 'D' or grade = 'D-' or
#         	   grade = 'F'  or grade = 'P' or grade = 'NP' or
#         	   grade = 'S'  or grade = 'U' or grade = 'NS'
#     """, [f[1], f[0]])
#     total_students = cur.fetchone()[0]
#
#     cur.execute("""
#     SELECT count(*)
#     FROM (SELECT cid, term
# 		FROM course
# 		WHERE subj = %s and crse = %s) R NATURAL JOIN enrollment
#         WHERE  grade = 'A+' or grade = 'A' or grade = 'A-' or
#         	   grade = 'B+' or grade = 'B' or grade = 'B-' or
#         	   grade = 'C+' or grade = 'C' or grade = 'C-' or
#         	   grade = 'D+' or grade = 'D' or grade = 'D-' or
#                grade = 'P'  or grade = 'S'
#     """, [f[1], f[0]])
#
#     passing_students = cur.fetchone()[0]
#     if(total_students > 0):
#
#         rate = passing_students/total_students
#         course_dict[(f[1], f[0])] = rate
#
# best = max(course_dict.values())
# worst = min(course_dict.values())
#
# test = 0
# print("\nHIGHEST PASS RATE COURSES")
# print("((SUBJ, CRSE), PASS RATE)\n")
# for i in course_dict.items():
#     if i[1] == best:
#         print(i)
#
# print("\nLOWEST PASS RATE COURSES")
# print("((SUBJ, CRSE), PASS RATE)\n")
# for i in course_dict.items():
#     if i[1] == worst:
#         print(i)
#
#
# cur.execute("""
#     SELECT DISTINCT m1.subj, m1.crse, m2.subj, m2.crse
#     FROM
#     (
#     	SELECT cid, term, instructor, type, days, time, build, room, subj, crse
#     	FROM meeting NATURAL JOIN course
#     ) m1
#     JOIN
#     (
#     	SELECT cid, term, instructor, type, days, time, build, room, subj, crse
#     	FROM meeting NATURAL JOIN course
#     ) m2
#     ON m1.cid <> m2.cid and m1.term = m2.term and m1.term::text NOT LIKE '____06' and
#        m1.instructor = m2.instructor and m1.instructor <> '' and
#        m1.days = m2.days and m1.days <> '' and
#        m1.time = m2.time and m1.time <> '' and
#        m1.build = m2.build and m1.build <> '' and
#        m1.room = m2.room and m1.room <> '' and
#        m1.subj <> m2.subj and m1.crse <> m2.crse and
#        m1.cid < m2.cid and m1.crse < m2.crse
#     ORDER BY m1.subj, m1.crse ASC
# """)
#
# cross_list = cur.fetchall()
#
# print("\nPROBLEM 3E\n")
# for cx in cross_list:
#     print(cx)
#
#
#
# # PROBLEM 3F
#
# cur.execute("""
#     WITH R AS (SELECT major, avg(value) as gpa
#     	FROM
#     	(
#     	SELECT course.cid, course.term, subj, sid, grade, major
#     	FROM course JOIN enrollment ON course.cid = enrollment.cid and course.term = enrollment.term
#     	WHERE SUBJ = 'ABC'
#     	) R
#     	NATURAL JOIN gpa
#     	GROUP BY major
#     	ORDER BY gpa ASC
#     )
#     SELECT major, gpa as perfomance
#     FROM R
#     WHERE gpa = (SELECT max(gpa) FROM R)
#     UNION
#     SELECT major, gpa as perfomance
#     FROM R
#     WHERE gpa = (SELECT min(gpa) FROM R)
#     ORDER BY perfomance ASC
# """)
#
# abc_major_performance = cur.fetchall()
#
# cur.execute("""
#     WITH R AS (SELECT major, avg(value) as gpa
#     	FROM
#     	(
#     	SELECT course.cid, course.term, subj, sid, grade, major
#     	FROM course JOIN enrollment ON course.cid = enrollment.cid and course.term = enrollment.term
#     	WHERE SUBJ = 'DEF'
#     	) R
#     	NATURAL JOIN gpa
#     	GROUP BY major
#     	ORDER BY gpa ASC
#     )
#     SELECT major, gpa as perfomance
#     FROM R
#     WHERE gpa = (SELECT max(gpa) FROM R)
#     UNION
#     SELECT major, gpa as perfomance
#     FROM R
#     WHERE gpa = (SELECT min(gpa) FROM R)
#     ORDER BY perfomance ASC
# """)
#
# def_major_performance = cur.fetchall()
#
# print("\nPROBLEM: 3F")
# print("MAJOR PERFORMANCE ABC\n")
#
# for i in abc_major_performance:
#     print(i)
#
# print("\nMAJOR PERFORMANCE DEF\n")
#
# for i in def_major_performance:
#     print(i)


# 3G TRANSFER INTO ABC
cur.execute("""
    WITH transfers AS
    (
    SELECT e1.major as previous_major, count(*) as number_switched
    FROM enrollment as e1, enrollment as e2
    WHERE e1.sid = e2.sid and e1.major <> e2.major and e1.term < e2.term and e2.major LIKE 'ABC%' and e1.major NOT LIKE 'ABC%'
    GROUP BY e1.major
    ORDER BY number_switched DESC
    )

    SELECT previous_major, number_switched, number_switched / (SUM(number_switched) OVER ()) AS percent_switched
    FROM transfers
    ORDER BY number_switched DESC
""")

top_transfers = cur.fetchall()[0:5]
transfer_dict = defaultdict(lambda:0)

print("PROBLEM 3G: Transfers into ABC")
# Top Transfers
for t in top_transfers:
    transfer_dict[t[0]] = float(t[2])


plt.bar(range(len(transfer_dict)), list(transfer_dict.values()), align='center')
plt.xticks(range(len(transfer_dict)), list(transfer_dict.keys()))
plt.show()


# 3H TRANSFER FROM ABC
cur.execute("""
    WITH transfers AS
    (
    SELECT e2.major as new_major, count(*) as number_switched
    FROM enrollment as e1, enrollment as e2
    WHERE e1.sid = e2.sid and e1.major <> e2.major and e1.term < e2.term and e2.major NOT LIKE 'ABC%' and e1.major LIKE 'ABC%'
    GROUP BY e2.major
    ORDER BY number_switched DESC
    )

    SELECT new_major, number_switched, number_switched / (SUM(number_switched) OVER ()) AS percent_switched
    FROM transfers
    ORDER BY number_switched DESC
""")

top_transfers = cur.fetchall()[0:5]
transfer_dict = defaultdict(lambda:0)

print("PROBLEM 3H: Transfers into ABC")
# Top Transfers
for t in top_transfers:
    transfer_dict[t[0]] = float(t[2])


plt.bar(range(len(transfer_dict)), list(transfer_dict.values()), align='center')
plt.xticks(range(len(transfer_dict)), list(transfer_dict.keys()))
plt.show()


# PROBLEM 5A

# WITH student_courses AS
# (
# SELECT course.cid, course.term, sid, subj, crse
# FROM enrollment
# JOIN course on course.cid = enrollment.cid and course.term = enrollment.term
# )
#
# SELECT R.subj, R.crse, R.currently_taking, student_courses.subj, student_courses.crse, count(*) as pre_requisite, (count(*)::NUMERIC / R.currently_taking::NUMERIC) as percent_pre
# FROM
# (
# 	SELECT cid, term, sid, subj, crse, count(*) over () as currently_taking
# 	FROM student_courses
# 	WHERE subj = 'ABC' and crse = 203
# ) R JOIN student_courses ON R.sid = student_courses.sid and R.term > student_courses.term
# GROUP BY R.subj, R.crse, R.currently_taking, student_courses.subj, student_courses.crse
# ORDER BY percent_pre DESC
