import csv

class CourseController():

    def __init__(self, database_path):
        self.database = database_path

    def add_course(self):
        course_dept = input('Course department (four characters): ')
        if len(course_dept) != 4:
            print('Invalid course department.')
            return -1
        course_code = input('Course code (four digits): ')
        if len(course_code) != 4 or not course_code.isdigit():
            print('Invalid course code.')
            return -1
        ret = self._add_course(course_dept, course_code)
        if ret != 0:
            print('ERROR: Course {} {} already exists.'.format(course_dept, course_code))
            return 0
        print('Successfully created course {} {}'.format(course_dept, course_code))
        return 0

    def _add_course(self, dept, code):
        lines = []
        exists = False
        with open(self.database, mode='r') as f:
            reader = csv.reader(f)
            for line in reader:
                if line[0] == dept and line[1] == code:
                    exists = True
                lines.append(line)
        if exists:
            return -1
        with open(self.database, mode='w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(lines)
            writer.writerow([dept, code, '', ''])
        return 0

    def assign_instructor(self, instr_id):
        if instr_id < 0:
            return 0
        course_data = input('Course department and code to assign: ').split()
        dept = course_data[0]
        code = course_data[1]
        self._assign_instructor(dept, code, instr_id)
        return 0

    def _assign_instructor(self, dept, code, instr_id):
        lines = []
        edit_line = None
        with open(self.database, mode='r') as f:
            reader = csv.reader(f)
            for line in reader:
                if line[0] == dept and line[1] == code:
                    edit_line = line
                    continue
                lines.append(line)
        if edit_line is None:
            print('Course {} {} not found.'.format(dept, code))
            return -1
        edit_line[2] = str(instr_id).zfill(4)
        with open(self.database, mode='w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(lines)
            writer.writerow(edit_line)

class AdminController():

    def __init__(self, database_path):
        self.database = database_path

    def find_instructor(self):
        name = input('Name of instructor (Firstname Lastname): ').split()
        instr_id = self._find_instructor(name)
        if instr_id < 0:
            print('Instructor with name {} not found.'.format(name))
            return -1
        print('Successfully found instructor {} with id {}.'.format(name, str(instr_id).zfill(4)))
        return instr_id

    def _find_instructor(self, name):
        keep_line = None
        first, last = name[0], name[1]
        with open(self.database, mode='r') as f:
            reader = csv.reader(f)
            for line in reader:
                if line[2] == first and line[3] == last:
                    keep_line = line
                    break
        if keep_line is None:
            return -1
        return int(keep_line[0])

    def find_student(self, user_id: int):
        name = input('Student\'s first and last name: ')
        found_name = False
        with open(self.database, mode='r') as f:
            reader = csv.reader(f)
            for line in reader:
                student_names = line[5].split(',')
                if name in student_names:
                    found_name = True
                    break
        if not found_name:
            print('You do not manage any student with this name.')
            return ''
        return name

class StudentController():

    def __init__(self, database_path):
        self.database = database_path

    def view_student_data(self, stu_id: str):
        keep_line = None
        with open(self.database, mode='r') as f:
            reader = csv.reader(f)
            for line in reader:
                if line[0] == stu_id:
                    keep_line = line
                    break
        if keep_line is None:
            print('No matching student found in the database.')
            return 0
        print() # empty line
        first, last = keep_line[1], keep_line[2]
        courses, grades = keep_line[3].split(','), keep_line[4].split(',')
        print('Student: {} {}'.format(first, last))
        print('================================')
        for i in range(len(courses)):
            course = courses[i].strip()
            grade = grades[i].strip()
            print('Course: {}'.format(course), '\tGrade: {}'.format(grade))
        return 0
    
    def view_student_data_by_name(self, stu_name: str):
        if stu_name == '':
            return 0
        name_parts = stu_name.split()
        first, last = name_parts[0], name_parts[1]
        stu_id = None
        with open(self.database, mode='r') as f:
            reader = csv.reader(f)
            for line in reader:
                if line[1] == first and line[2] == last:
                    stu_id = line[0]
        return self.view_student_data(stu_id)