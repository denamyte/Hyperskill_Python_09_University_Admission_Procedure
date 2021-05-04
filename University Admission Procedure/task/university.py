from typing import Tuple, List


class AdmissionScores:
    """Input student and their grades, sort them by the grades and print the admitted ones"""
    def __init__(self):
        self.student_count = 0
        self.admitted_count = 0
        self.students: List[Tuple[str, float]] = []

    def input_data(self):
        self.student_count = int(input())
        self.admitted_count = int(input())
        self.students = [self.input_student() for _ in range(self.student_count)]

    @staticmethod
    def input_student() -> Tuple[str, float]:
        raw_str = input()
        last_space_ind = raw_str.rindex(' ')
        return raw_str[:last_space_ind], float(raw_str[last_space_ind + 1:])

    def sort(self):
        self.students.sort(key=lambda t: (-t[1], t[0]))

    def __str__(self):
        res = ['Successful applicants:']
        for t in self.students[:self.admitted_count]:
            res.append(t[0])
        return '\n'.join(res)


ad_score = AdmissionScores()
ad_score.input_data()
ad_score.sort()
print(ad_score)
