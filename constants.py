MAINMENU, MAINMENU_ADMIN, GET_ADMIN_STUDENTS, GET_ADD_REPLACE_ANSWER = range(4)

def load_admin_ids():
    with open('admin.txt','r') as f:
        admin_ids = []
        for line in f:
            line = line.strip()
            if line:
                admin_ids.append(int(line))
    return admin_ids

def load_students_ids():
    with open('students.txt','r') as f:
        student_ids = []
        for line in f:
            line = line.strip()
            if line:
                student_ids.append(int(line))
    return student_ids