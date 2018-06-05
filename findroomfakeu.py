term = input("What term? ")
cid = input("What CID? ")
num_students = input("How many students to add? ")

print(term, cid, num_students)


# SELECT meeting.build, meeting.room, max(enrolled) as enrolled
# FROM meeting JOIN course on meeting.cid = course.cid and meeting.term = course.term
# WHERE meeting.build <> '' and meeting.room <> ''
# GROUP BY meeting.build, meeting.room
# ORDER BY build, room ASC
