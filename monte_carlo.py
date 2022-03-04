import random


def equation(x: float) -> float:
    return pow(1 - x * x, 0.5)


def monte_carlo(test_times: int) -> float:
    count = 0.0
    for i in range(test_times):
        count += equation(random.uniform(0, 1))

    return count / test_times


def main():
    try:
        test_times = int(input("Please input the number of testing times(>0): "))
        if test_times <= 0:
            raise ValueError
        print(monte_carlo(test_times) * 4)
    except ValueError:
        print("Please input the right format!")


if __name__ == "__main__":
    main()
