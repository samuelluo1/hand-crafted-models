from typing import Tuple, List

import numpy as np


def fit(real_data: List[float]) -> List[float]:
    a, b = _get_coefficient(real_data)

    output_list = []
    for i in range(len(real_data)):  # X(1)(k) = (X(0)(1) - b/a) * e^(-a(k-1)) + (b/a)
        output_list.append((real_data[0] - b / a) * np.exp(-a * i) + b / a)

    output_list = [el - output_list[i - 1] if i > 0 else el for i, el in enumerate(output_list)]  # inverse of cumulative sum
    return output_list


def _get_coefficient(real_data: List[float]) -> Tuple[float, float]:
    """
    Get coefficient a, b for the function of the model.
    """
    y_cum_sum = np.cumsum(real_data)
    b = []
    for i in range(len(real_data) - 1):  # (-1/2)(X(1)(n-1) + X(1)(n))
        b.append([-0.5 * (y_cum_sum[i] + y_cum_sum[i + 1]), 1])

    # ((B^T)B)^(-1) * (B^T) * y
    b = np.array(b)
    b_t = np.transpose(b)
    output = np.linalg.inv(np.dot(b_t, b))
    output = np.dot(output, b_t)
    y = np.transpose(real_data[1:])
    output = np.dot(output, y)
    output = np.transpose(output)

    return output[0], output[1]


def get_precision(real_data: List[float], pred_data: List[float]) -> float:
    real_corr = 0
    for i in range(1, len(real_data) - 1):
        real_corr += real_data[i] - real_data[0]
    real_corr += (real_data[-1] - real_data[0]) / 2
    real_corr = np.abs(real_corr)

    pred_corr = 0
    for i in range(1, len(pred_data) - 1, 1):
        pred_corr += pred_data[i] - pred_data[0]
    pred_corr += (pred_data[-1] - pred_data[0]) / 2
    pred_corr = np.abs(pred_corr)

    sub_corr = 0
    for i in range(1, len(pred_data) - 1, 1):
        sub_corr += (real_data[i] - real_data[0]) - (pred_data[i] - pred_data[0])
    sub_corr += ((real_data[-1] - real_data[0]) - (pred_data[-1] - pred_data[0])) / 2
    sub_corr = np.abs(sub_corr)

    return (1 + real_corr + pred_corr) / (1 + real_corr + pred_corr + sub_corr)


def main():
    try:
        real_data = list(map(float, input("Enter the real data separated by space: ").strip().split()))
        predict_data = fit(real_data)
        print("Predict data: " + str(predict_data))
        print("Precision: " + str(get_precision(real_data, predict_data)))
    except ValueError:
        print("Please input the right format!")


if __name__ == "__main__":
    main()
