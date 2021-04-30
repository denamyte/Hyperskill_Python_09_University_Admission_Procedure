def input_score() -> float:
    return sum(int(input()) for _ in range(3)) / 3


def accepted(score: float) -> bool:
    return score >= 60.0


def print_result(score: float):
    print(score)
    print('Congratulations, you are accepted!' if accepted(score)
          else 'We regret to inform you that we will not be able to offer you admission.')


print_result(input_score())
