import numpy as np


def flip(square_spins: list, temperature: float):
    square_len = len(square_spins)
    for i in range(square_len * square_len):
        rand_row = np.random.randint(0, square_len)
        rand_col = np.random.randint(0, square_len)
        s = square_spins[rand_row][rand_col]
        e = square_spins[(rand_row + 1) % square_len][rand_col] + \
            square_spins[rand_row][(rand_col + 1) % square_len] + \
            square_spins[(rand_row - 1) % square_len][rand_col] + \
            square_spins[rand_row][(rand_col - 1) % square_len]
        delta_e = 2 * s * e
        beta = 1 / temperature

        if delta_e < 0 or np.random.random() < np.exp(-beta * delta_e):
            square_spins[rand_row][rand_col] *= -1
    return square_spins


def cal_energy(square_spins: list):
    square_len = len(square_spins)
    total_energy = 0
    for i in range(square_len):
        for j in range(square_len):
            s = square_spins[i][j]
            e = square_spins[(i + 1) % square_len][j] + \
                square_spins[i][(j + 1) % square_len] + \
                square_spins[(i - 1) % square_len][j] + \
                square_spins[i][(j - 1) % square_len]
            total_energy += -e * s
    return total_energy / 4


def cal_magnetic(square_spins: list):
    return np.sum(square_spins)


def main():
    try:
        mc_steps = int(input("Please input the number of MC steps(>0): "))
        square_len = int(input("Please input the length of square(>0): "))
        temperature = float(input("Please input the temperature: "))
        if mc_steps <= 0 or square_len <= 0:
            raise ValueError
        square_spins = 2 * np.random.randint(2, size=(square_len, square_len)) - 1
        print(square_spins)
        for mc_step in range(mc_steps):
            for a_step_of_mc in range(square_len):
                square_spins = flip(square_spins, temperature)
            print(cal_magnetic(square_spins))
    except ValueError:
        print("Please input the right format!")


if __name__ == "__main__":
    main()
