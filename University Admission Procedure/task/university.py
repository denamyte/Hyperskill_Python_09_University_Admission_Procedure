from typing import List


class Applicant:
    finals_reindex = [1, 1, 3, 2, 0]  # index - Distribution.dep_names index; value - finals' index

    def __init__(self, raw_data: str):
        self.name = ''
        self.finals: List[float] = []  # The order and number of finals fit Distribution.dep_names
        self.dep_preferences: List[int] = []  # Uses indices from Distribution.dep_names
        self.assigned_dep = -1  # Gets assigned an index from Distribution.dep_names
        self.parse(raw_data)

    def parse(self, raw_data: str):
        ar_data = raw_data.split(' ')
        self.name = ' '.join(ar_data[:2])
        self.finals = self.parse_finals(ar_data)
        self.dep_preferences = [Distribution.dep_names.index(dep_name) for dep_name in ar_data[6:]]

    @staticmethod
    def parse_finals(ar_data: List[str]):
        raw_finals = [float(x) for x in ar_data[2:6]]
        return [raw_finals[i] for i in Applicant.finals_reindex]

    def assign_dep(self, dep_ind: int):
        """
        Assigns a department to this applicant. Assigning a department means
        the applicant doesn't participate in further assignment procedures.
        """
        self.assigned_dep = dep_ind

    def __str__(self):
        return f'{self.name} {0 if self.assigned_dep == -1 else self.finals[self.assigned_dep]}'


class Distribution:
    """
    Input applicant list, assign them into the departments given, according
    to an applicant's preference and finals scores
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
        for dep_preference_level in range(3):
            for dep_ind in range(len(self.dep_names)):
                dep_list = self.dep_lists[dep_ind]
                if len(dep_list) < self.dep_capacity:
                    app_list = [app for app in self.applicants
                                if app.assigned_dep == -1 and app.dep_preferences[dep_preference_level] == dep_ind]
                    self.sort_app_list(app_list, dep_ind)
                    add_count = min(len(app_list), self.dep_capacity - len(dep_list))
                    for app in app_list[:add_count]:
                        app.assign_dep(dep_ind)
                        dep_list.append(app)
                    self.sort_app_list(dep_list, dep_ind)

    @staticmethod
    def sort_app_list(app_list: List[Applicant], dep_ind: int):
        app_list.sort(key=lambda app: (-app.finals[dep_ind], app.name))

    def dep_to_str(self, dep_ind: int):
        app_str = '\n'.join(map(str, self.dep_lists[dep_ind]))
        return f'{self.dep_names[dep_ind]}\n{app_str}'

    def __str__(self):
        return '\n\n'.join(self.dep_to_str(i) for i in range(len(self.dep_names)))


print(Distribution(int(input())))
