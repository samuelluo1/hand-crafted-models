from typing import List

import numpy as np
from interval import Interval

from grey_model import fit


class GreyMarkovModel:
    def __init__(self, relative_err_list: List[float], count: int, used_to_predict: int):
        self.relative_err_list = relative_err_list
        self.max_relative_err = max(relative_err_list)
        self.min_relative_err = min(relative_err_list)
        self.count = count
        self.used_to_predict = used_to_predict
        self.interval_val = (self.max_relative_err - self.min_relative_err) / self.count
        self.interval_list = []

        self.expected_val_list = []
        for i in range(count):
            self.expected_val_list.append(min(relative_err_list) + (0.5 + i) * self.interval_val)

        self.trans_prob = np.zeros((self.count, self.count))
        self.__init_status_trans_prob()

    def __init_status_trans_prob(self) -> None:
        for i in range(self.count):
            if i != self.count - 1:
                self.interval_list.append(Interval(self.min_relative_err + i * self.interval_val, self.min_relative_err + (i + 1) * self.interval_val))
            else:
                self.interval_list.append(Interval(self.min_relative_err + i * self.interval_val, self.max_relative_err))

        prev = None
        for i, err_val in enumerate(self.relative_err_list):
            matrix = self.__to_vector(err_val)
            if prev:
                self.trans_prob[prev] += matrix
            prev = matrix.index(1)

        sum_list = np.sum(self.trans_prob, axis=1)
        for row_i, row in enumerate(self.trans_prob):
            if sum_list[row_i] != 0:
                for col_i, val in enumerate(row):
                    self.trans_prob[row_i, col_i] /= sum_list[row_i]

    def __to_vector(self, val: float):
        zeros = [0] * self.count
        for i, j in enumerate(self.interval_list):
            if val in j:
                zeros[i] = 1
        return zeros

    def validate_test_data(self, relative_err_list):
        prob_vector_list = np.zeros((1, self.count))
        p = self.trans_prob
        for i in range(self.used_to_predict):
            prob_dist = np.dot(self.__to_vector(relative_err_list[-i - 1]), p)
            prob_vector_list += prob_dist
            p = np.dot(p, self.trans_prob)
        return prob_vector_list / prob_vector_list.sum(axis=1) * 100


def main():
    try:
        status = int(input("Please input the number of Markov Chain status(>0): "))
        real_data = list(map(float, input("Enter the real data separated by space: ").strip().split()))
        used_to_predict = int(input("Please input how many number you want to use to predict (<data size): "))
        predict_count = int(input("Please input how many you want to predict(>0): "))
        predict_data = fit(real_data)
        relative_error_data = [(i - j) / i for i, j in zip(real_data, predict_data)]
        print("Relative error data: " + str(relative_error_data))

        interval = (max(relative_error_data) - min(relative_error_data)) / status
        interval_list = ['{:.2f}'.format((min(relative_error_data) + i * interval) * 100) + '% ~ ' +
                         '{:.2f}'.format((min(relative_error_data) + (i + 1) * interval) * 100) + '%' for i in range(status)]
        print("Slice relative error into: " + str(interval_list))
        sum = 0
        for i in range(used_to_predict + predict_count):
            model = GreyMarkovModel(relative_error_data[:-i - 1], status, used_to_predict)
            status_num = np.argmax(model.validate_test_data(relative_error_data), axis=1)[0]
            mc_pred = predict_data[-i - 1] / (1 - model.expected_val_list[status_num])
            err = (real_data[-i - 1] - mc_pred) / real_data[-i - 1] * 100
            sum += abs(err)
            if i < used_to_predict:
                print(f'adjusted real: {mc_pred}, error: {err}%')
            else:
                print(f'predict: {mc_pred}, error: {err}%')
        print('mean: ' + str(sum / 6) + '%')
        print(model.trans_prob)
    except ValueError:
        print("Please input the right format!")


if __name__ == "__main__":
    main()
