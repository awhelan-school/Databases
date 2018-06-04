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




# Problem 3D
course_dict = defaultdict(lambda:0)

# GET all course as unique
cur.execute("""
SELECT DISTINCT crse, subj
FROM course
""")

course_list = cur.fetchall()
for f in course_list:
    cur.execute("""
    SELECT count(*)
    FROM (SELECT cid, term
		FROM course
		WHERE subj = %s and crse = %s) R NATURAL JOIN enrollment
        WHERE  grade = 'A+' or grade = 'A' or grade = 'A-' or
        	   grade = 'B+' or grade = 'B' or grade = 'B-' or
        	   grade = 'C+' or grade = 'C' or grade = 'C-' or
        	   grade = 'D+' or grade = 'D' or grade = 'D-' or
        	   grade = 'F'  or grade = 'P' or grade = 'NP' or
        	   grade = 'S'  or grade = 'U' or grade = 'NS'
    """, [f[1], f[0]])
    total_students = cur.fetchone()[0]

    cur.execute("""
    SELECT count(*)
    FROM (SELECT cid, term
		FROM course
		WHERE subj = %s and crse = %s) R NATURAL JOIN enrollment
        WHERE  grade = 'A+' or grade = 'A' or grade = 'A-' or
        	   grade = 'B+' or grade = 'B' or grade = 'B-' or
        	   grade = 'C+' or grade = 'C' or grade = 'C-' or
        	   grade = 'D+' or grade = 'D' or grade = 'D-' or
               grade = 'P'  or grade = 'S'
    """, [f[1], f[0]])

    passing_students = cur.fetchone()[0]
    if(total_students > 0):

        rate = passing_students/total_students
        course_dict[(f[1], f[0])] = rate

best = max(course_dict.values())
worst = min(course_dict.values())

test = 0
for i in course_dict.items():
    print(i)
    if i[1] == 1:
        test += 1

print(len(course_dict), test)
