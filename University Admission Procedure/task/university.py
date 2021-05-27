from typing import List


class Applicant:

    def __init__(self, raw_data: str):
        self.name = ''
        self.gpa = 0.0
        self.dep: List[int] = []
        self.assigned_dep = -1
        self.parse(raw_data)

    def parse(self, raw_data: str):
        ar_data = raw_data.split(' ')
        self.name = ' '.join(ar_data[:2])
        self.gpa = float(ar_data[2])
        self.dep = [Distribution.dep_names.index(dep_name) for dep_name in ar_data[3:]]

    def assign_dep(self, dep_ind: int):
        """
        Assigns a department to this applicant. Assigning a department means
        the applicant doesn't participate in further assignment procedures.
        """
        self.assigned_dep = dep_ind

    def __str__(self):
        return f'{self.name} {self.gpa}'


class Distribution:
    """
    Input applicant list, assign them into the departments given, according
    to an applicant's preference and GPA score
    """
    dep_names = ['Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics']
    file_name = 'applicants.txt'

    def __init__(self, dep_capacity: int):
        self.dep_capacity = dep_capacity
        self.applicants: List[Applicant] = []
        self.dep_lists: List[List[Applicant]] = [[] for _ in range(len(self.dep_names))]
        self.read_applicants()
        self.distribute()

    def read_applicants(self):
        with open(self.file_name) as file:
            self.applicants = [Applicant(line.rstrip('\n')) for line in file.readlines()]

    def distribute(self):
        for level in range(3):
            for dep_ind in range(len(self.dep_names)):
                dep_list = self.dep_lists[dep_ind]
                if len(dep_list) < self.dep_capacity:
                    app_list = [app for app in self.applicants if app.assigned_dep == -1 and app.dep[level] == dep_ind]
                    self.sort_app_list(app_list)
                    add_count = min(len(app_list), self.dep_capacity - len(dep_list))
                    for app in app_list[:add_count]:
                        app.assign_dep(dep_ind)
                        dep_list.append(app)
                    self.sort_app_list(dep_list)

    @staticmethod
    def sort_app_list(app_list: List[Applicant]):
        app_list.sort(key=lambda app: (-app.gpa, app.name))

    def dep_to_str(self, dep_ind: int):
        app_str = '\n'.join(map(str, self.dep_lists[dep_ind]))
        return f'{self.dep_names[dep_ind]}\n{app_str}'

    def __str__(self):
        return '\n\n'.join(self.dep_to_str(i) for i in range(len(self.dep_names)))


print(Distribution(int(input())))
