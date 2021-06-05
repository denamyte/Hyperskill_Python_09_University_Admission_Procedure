from typing import List


class Applicant:
    exams_reindex = [1, 1, 3, 2, 0]  # index - Distribution.dep_names index; value - exams' index

    def __init__(self, raw_data: str):
        self.name = ''
        self.exams: List[float] = []  # The order and number of exams fit Distribution.dep_names
        self.dep_preferences: List[int] = []  # Uses indices from Distribution.dep_names
        # self.assigned_dep = -1  # Gets assigned an index from Distribution.dep_names
        self.score = 0.0
        self.parse(raw_data)

    def parse(self, raw_data: str):
        ar_data = raw_data.split(' ')
        self.name = ' '.join(ar_data[:2])
        self.exams = self.parse_finals(ar_data)
        self.dep_preferences = [Distribution.dep_names.index(dep_name) for dep_name in ar_data[6:]]

    @staticmethod
    def parse_finals(ar_data: List[str]):
        raw_finals = [float(x) for x in ar_data[2:6]]
        return [raw_finals[i] for i in Applicant.exams_reindex]

    def assign_dep(self, dep_ind: int, dep_score: float):
        """
        Assigns a department to this applicant. Assigning a department means
        the applicant doesn't participate in further assignment procedures.
        """
        # self.assigned_dep = dep_ind
        self.score = dep_score

    def __str__(self):
        return f'{self.name} {self.score}'


class Distribution:
    """
    Input applicant list, assign them into the departments given, according
    to an applicant's preference and finals scores
    """
    dep_names = ['Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics']
    required_exams_indices = [(1, 4), (1,), (2, 3), (3,), (3, 4)]
    app_file_name = 'applicants.txt'

    def __init__(self, dep_capacity: int):
        self.dep_capacity = dep_capacity
        self.applicants: List[Applicant] = []
        self.dep_lists: List[List[Applicant]] = [[] for _ in range(len(self.dep_names))]
        self.read_applicants()
        self.distribute()
        self.save_to_files()

    def read_applicants(self):
        with open(self.app_file_name) as file:
            self.applicants = [Applicant(line.rstrip('\n')) for line in file.readlines()]

    def distribute(self):
        for dep_preference_level in range(3):
            for dep_ind in range(len(self.dep_names)):
                dep_list = self.dep_lists[dep_ind]
                if len(dep_list) < self.dep_capacity:
                    app_list = [app for app in self.applicants
                                if app.score == 0.0 and app.dep_preferences[dep_preference_level] == dep_ind]
                    self.sort_app_list(app_list, dep_ind)
                    add_count = min(len(app_list), self.dep_capacity - len(dep_list))
                    for app in app_list[:add_count]:
                        app.assign_dep(dep_ind, self.calc_sort_score(app, dep_ind))
                        dep_list.append(app)
                    self.sort_app_list(dep_list, dep_ind)

    def sort_app_list(self, app_list: List[Applicant], dep_ind: int):
        app_list.sort(key=lambda app: (-self.calc_sort_score(app, dep_ind), app.name))

    def calc_sort_score(self, app: Applicant, dep_ind: int) -> float:
        req_ind = self.required_exams_indices[dep_ind]
        return sum(app.exams[i] for i in req_ind) / len(req_ind)

    # def dep_to_str(self, dep_ind: int):
    #     app_str = '\n'.join(map(str, self.dep_lists[dep_ind]))
    #     return f'{self.dep_names[dep_ind]}\n{app_str}'

    def save_to_files(self):
        for dep_ind in range(len(self.dep_names)):
            file_name = self.dep_names[dep_ind].lower() + '.txt'
            with open(file_name, 'w') as file:
                file.write('\n'.join(str(app) for app in self.dep_lists[dep_ind]))

    # def __str__(self):
    #     return '\n\n'.join(self.dep_to_str(i) for i in range(len(self.dep_names)))


Distribution(int(input()))
