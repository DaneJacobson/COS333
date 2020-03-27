# COS333

<!-- 
# To find - courseid, days, stanrttime, endgame, bldg, roomnum:
SELECT courseid, days, starttime, endtime, bldg, roomnum
FROM classes
WHERE classid = ?;

# To find - dept, coursenum:
SELECT dept, coursenum
FROM classes, crosslistings
WHERE classes.courseid = crosslistings.courseid
AND classid = ?
ORDER BY dept, coursenum ASC;


# To find - area, title, descrip, prereqs:
SELECT area, title, descrip, prereqs
FROM classes, courses
WHERE classes.courseid = courses.courseid
AND classid = ?;

# To find - profname:
SELECT profname
FROM classes, coursesprofs, profs
WHERE classes.courseid = coursesprofs.courseid
AND coursesprofs.profid = profs.profid
AND classid = ?
ORDER BY profname ASC; 
-->
