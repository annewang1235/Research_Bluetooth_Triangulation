import matplotlib.pyplot as plt
import Trilateration.bestFitCalcs as bestFitCalcs


def visualize_circles(radiusDict, device_positions, chosen_device_names):
    figure, axes = plt.subplots()

    color = ['red', 'blue', 'green']
    counter = 0

    axes.set_xlim((-30, 30))
    axes.set_ylim((-30, 30))
    plt.xlabel(" x-direction (ft) ")
    plt.ylabel("y-direction (ft)")
    plt.title("Beacon Intersection with Receiver")

    print("hi 3")

    for ele in chosen_device_names:
        print("counter: ", counter)
        draw_circle = plt.Circle(
            device_positions[counter], radiusDict[ele], alpha=0.2, color=color[counter])
        axes.add_artist(draw_circle)

        counter += 1

        # draw_circle = plt.Circle((0, 0), 0, alpha=0.2, color='red')
        # draw_circle2 = plt.Circle((0, 5), 6, alpha=0.2, color='blue')
        # draw_circle3 = plt.Circle((5, 0), 5, alpha=0.2, color='green')

        # axes.add_artist(draw_circle)
        # axes.add_artist(draw_circle2)
        # axes.add_artist(draw_circle3)

    plt.show()


# visualize_circles({"HC_02": 0, "HC_04": 7}, [
#                   (0, 0), (3, 3)], ["HC_02", "HC_04"])
