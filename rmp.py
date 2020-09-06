import os
import csv
import rmp_class as rmp

filename = 'data.csv'

schools = [
    # Jesuit
    # ("Creighton University", 301),
    ("Boston College", 124),
    ("Georgetown University", 355),
    ("Gonzaga Univesrity", 370),
    ("Loyola University Chicago", 540),
    ("Marquette University", 565),
    ("Xavier University", 1518),
    # Public
    ("University of California Los Angelas", 1381),
    ("University of California Berkeley", 1072),
    ("University of Michican Ann Arbor", 1258),
    ("University of Virginia", 1277),
    ("Georgia Institute of Technology", 361),
    ("University of North Carolina Chapel Hill", 1232),
    ("University of California Santa Barbara", 1077),
    ("University of Florida", 1100),
    ("University of California Irvine", 1074),
    ("University of California San Diego", 1079),
    ("University of Wisconsin Madison", 1256),
    ("University of Texas Austin", 1255),
    ("Ohio State University Columbus", 724),
    ("Purdue Univesrity", 783),
    ("University of Massachusetts Amherst", 1513),
    ("Virginia Tech", 1349),
    ("Pennsylvania State University", 758),
    # Public Midwest
    ("Truman State University", 1038),
    ("University of Northern Iowa", 1312),
    ("University of Wisconsin La Crosse", 3978),
    ("University of Illinois Springfield", 1112),
    ("University of Wisconsin Eau Claire", 3976),
    ("University of Nebraska Omaha", 1307),
    ("University of Nebraska Lincoln", 1249),
    ("University of Bellevue", 1249),
    ("University of Minnesota Duluth", 1372),
    ("Michigan State University", 601),
    ("University of Illinois Chicago", 1111),
    # Private Midwest
    ("University of Chicago", 1085),
    ("Northwestern University", 709),
    ("Washington University St. Louis", 1147),
    ("Vanderbilt University", 4002),
    ("Grinnell College", 383),
    # Non-Jesuit religious
    ("University of Notre Dame", 1576),
    ("Emory University", 340),
    ("Davidson College", 3965),
    ("Macalester College", 550),
    ("Lafayette College", 494),
    ("Southern Methodist University", 927),
    ("Brigham Young University", 135),
    ("Trinity University Texas", 1033),
    ("St. Olaf College", 862),
    ("Wheaton College", 1191),
    ("University of Tulsa", 3963),
    ("Baylor University", 90),
    ("The Catholic University of America", 189),
    ("Duke University", 1350),
    ("Islamic University of Minnesota", 15032),
    ("Islamic American University", 16849),
    ("American Jewish University", 1116),
    ("Baltimore Hebrew University", 78),
    ("Yeshiva University", 1223),
    # Ivy league
    ("Cornell University", 298),
    ("Dartmouth College", 1339),
    ("University of Pennsylvania", 1275),
    ("Columbia University", 278),
    ("Brown University", 137),
    ("Princeton University", 780),
    ("Harvard University", 399),
    ("Yale University", 1222)
]

fileexists = os.path.exists(filename)
with open(filename, 'a') as csvfile:
    columns = ['school', 'school_id', 'name', 'department', 'rating', 'difficulty', 'takeagain', 'most_common_tag', 'tags']
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    if not fileexists:
        writer.writeheader()

    def printInfo(r):
        school = r.get_school_name()
        school_id = r.get_school_id()
        name = r.get_name()
        if not name or "not available" in name:
            name = ""
        department = r.get_department()
        if not department or "not available" in department:
            department = ""
        rating = r.get_rating()
        if not rating or "not available" in rating:
            rating = ""
        difficulty = r.get_difficulty()
        if not difficulty or "not available" in difficulty:
            difficulty = ""
        common_tag = r.get_first_tag()
        if not common_tag or "not available" in common_tag:
            common_tag = ""
        tags = r.get_tags()
        if not tags or len(tags) == 0:
            tags = ""
        else:
            tags = "\"" + "\", \"".join(map(str, tags)) + "\""
        takeagain = r.get_would_take_again()
        if not takeagain or "not available" in takeagain:
            takeagain = ""

        print("Collecting: ", name)
        writer.writerow({'school': school, 'school_id': school_id, 'name': name, 'department': department, 'rating': rating, 'difficulty': difficulty, 'takeagain': takeagain, 'most_common_tag': common_tag, 'tags': tags})

    print("START")
    for school in schools:
        print("---- SCHOOL: " + school[0] + " [id: " + str(school[1]) + "] ----")
        r = rmp.RateMyProfAPI(school_id=school[1], teacher="staff", callback=printInfo)
        r.retrieve_rmp_info()
    print("DONE")
