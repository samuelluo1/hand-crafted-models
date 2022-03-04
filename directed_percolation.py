import random
import matplotlib.pyplot as plt


class Dot:
    def __init__(self, dot_number: int, percolate: bool = False):
        self.dot_number = dot_number    # the number in its layer
        self.percolate = percolate  # this dot is percolated or not
        self.parents = []    # all dot objects in upper layer that connect to it
        self.real_parents = []    # all dot objects in upper layer that real connect to it


def get_parents_number_list(layer_number: int, dot_number: int) -> list:
    output_list = []
    real_layer_number = layer_number + 1
    real_up_layer_number = layer_number
    quotient = dot_number // real_layer_number
    remainder = dot_number % real_layer_number

    if quotient != 0:  # not first row
        if remainder != 0:  # not first column
            output_list.append(real_up_layer_number * (quotient - 1) + remainder - 1)
        if remainder != real_layer_number - 1:  # not last column
            output_list.append(real_up_layer_number * (quotient - 1) + remainder)
    if quotient != real_layer_number - 1:  # not last row
        if remainder != 0:  # not first column
            output_list.append(real_up_layer_number * quotient + remainder - 1)
        if remainder != real_layer_number - 1:  # not last column
            output_list.append(real_up_layer_number * quotient + remainder)

    return output_list


def percolate_or_not(probability: float) -> bool:
    return random.random() < probability


def init_pyramid(layer: int, probability: float) -> list:
    pyramid_container = [[Dot(0, True)]]  # first layer

    for layer in range(1, layer):  # append every layer
        tmp_container = []

        for dot in range(pow(layer + 1, 2)):  # append every dot
            new_dot = Dot(dot)
            for parent_number in get_parents_number_list(layer, dot):  # check every parent
                parent = pyramid_container[layer - 1][parent_number]
                new_dot.parents.append(pyramid_container[layer - 1][parent_number])
                if parent.percolate and percolate_or_not(probability):
                    new_dot.real_parents.append(pyramid_container[layer - 1][parent_number])
                    new_dot.percolate = True

            tmp_container.append(new_dot)

        pyramid_container.append(tmp_container)

    return pyramid_container


def draw_plot(pyramid: list, title: str):
    plt.subplot(projection='3d')
    plt.title(title)
    total_gap = 0
    half_len = 0.5    # half length between adjacent dots in same layer

    for layer_number, layer in enumerate(pyramid[:0:-1]):    # every layer
        length = pow(len(layer), 0.5)

        for dot in layer:    # every dot
            for parent in dot.parents:    # draw a line between the dot and its parent
                color = "r" if parent in dot.real_parents else (0.5, 0.5, 0.5, 0.05)    # red or gray
                plt.plot([total_gap + dot.dot_number % length, total_gap + half_len + parent.dot_number % (length - 1)],
                         [total_gap + dot.dot_number // length, total_gap + half_len + parent.dot_number // (length - 1)],
                         [layer_number, layer_number + 1], color=color)
        total_gap += half_len

    plt.savefig("output.png")


def main():
    try:
        layers = int(input("Please input the number of layers(>0): "))
        if layers <= 0:
            raise ValueError
        probability = float(input("Please input the probability(0.0 ~ 1.0): "))
        pyramid = init_pyramid(layers, probability)
        lowest_layer = 1

        # print data info in text
        for layer_number, layer in enumerate(pyramid):
            print(f"{'=' * 50} layer{layer_number + 1} {'=' * 50}")
            have_percolated = False    # This layer is percolated or not
            for dot in layer:
                print(dot.dot_number + 1,
                      "parents: " + str([item.dot_number + 1 for item in dot.parents]),
                      "connected parents: " + str([item.dot_number + 1 for item in dot.real_parents]))
                if not have_percolated and dot.real_parents:
                    have_percolated = True
            if have_percolated:
                lowest_layer += 1

        draw_plot(pyramid, f"Simulation for {layers} layers (P={probability}) (lowest layer={lowest_layer})")
        print("Image for result: output.png")
    except ValueError:
        print("Please input the right format!")


if __name__ == "__main__":
    main()
