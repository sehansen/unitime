import glob


def loadTestData(testNumber):
    alldata = [open(f) for f in
            glob.glob("./TestData/Test%02d/*.utt" % (testNumber))]
    names = [i.name.strip('/.utt').split("/")[2] for i in alldata]
    files = dict(zip(names, alldata))

    #sets = alldata[0].readline().split(sep)
    #cards = map(int,alldata[0].readline().split(sep))
    #card = dict(zip(sets,cards))

    basicinfo = dict(zip(files['basic'].readline().split(" "), map(int,
                                files['basic'].readline().split(" "))))

    files['courses'].readline()
    L = {}  # A dict with key = course, and value = number of lectures
    S = {}  # A dict with key = course, and value = number of students
    M = {}  # A dict with key = course, and value = minimum number of
            # days that it should be spread across
    lecturer = {}
    for line in files['courses']:
        Course, Lecturer, Number_of_lectures, Minimum_working_days,\
                        Number_of_students = tuple(line.split(" "))
        L[Course] = int(Number_of_lectures)
        S[Course] = int(Number_of_students)
        M[Course] = int(Minimum_working_days)
        lecturer[Course] = Lecturer

    C = {}  # A dict with key = room, and value = number of students
            # that can be in the room
    files['rooms'].readline()
    for line in files['rooms']:
        Room, Capacity = tuple(line.split(" "))
        C[Room] = int(Capacity)

    curric = {}  # A dict with key = couse, and value = list of
                 # curriculae it belongs to
    files['relation'].readline()
    for line in files['relation']:
        Curriculum, Course = tuple(line.strip('\r\n').split(" "))
        if Course not in curric.keys():
            curric[Course] = []
        curric[Course].append(Curriculum)

    def lists_overlap(a, b):
        sb = set(b)
        return any(el in sb for el in a)

    chi = {}
    for c1 in L.keys():
        for c2 in L.keys():
            if c1 == c2 or lecturer[c1] == lecturer[c2] or \
                            lists_overlap(curric[c1], curric[c2]):
                chi[(c1, c2)] = 1  # if some key isn't there,
                                  # there is no conflict

    # T = [(day, period) for day in range(1,basicinfo['Days']+1)
    # for period in range(1,basicinfo['Periods_per_day']+1)]
    #weirdgreekletter = {}

    for f in files.values():
        f.close()

    return (basicinfo, L, M, S, lecturer, C, curric)


if __name__ == "__main__":
    (basicinfo, L, M, S, lecturer, C, curric) = loadTestData(5)

    print L
    print
    print S
    print
    print M
