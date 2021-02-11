import matplotlib.pyplot as plt
import Trilateration.bestFitCalcs as bestFitCalcs

from shapely.geometry import Point
from shapely.ops import cascaded_union
from itertools import combinations


def visualize_circles(radiusDict, device_positions, chosen_device_names):
    figure, axes = plt.subplots()

    color = ['red', 'blue', 'green']
    counter = 0

    axes.set_xlim((-30, 30))
    axes.set_ylim((-30, 30))
    plt.xlabel(" x-direction (ft) ")
    plt.ylabel("y-direction (ft)")
    plt.title("Beacon Intersection with Receiver")

    for ele in chosen_device_names:
        draw_circle = plt.Circle(
            device_positions[counter], radiusDict[ele], alpha=0.2, color=color[counter])
        axes.add_artist(draw_circle)

        counter += 1

    plt.show()


def get_intersection(radiusDict, device_positions, chosen_device_names):
    circles = []
    counter = 0
    for device in chosen_device_names:
        x_coor = device_positions[counter][0]
        y_coor = device_positions[counter][1]
        radius = radiusDict[device]
        circles.append(Point(x_coor, y_coor).buffer(radius))

    intersection = cascaded_union(
        [a.intersection(b)
         for a, b in combinations(circles, 2)]
    )
    print(intersection)
