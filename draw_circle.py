import matplotlib.pyplot as plt

def visualize_circles():
  figure, axes = plt.subplots()
  draw_circle = plt.Circle((0, 0),5, alpha=0.2, color='red')
  draw_circle2 = plt.Circle((0, 5),6, alpha=0.2, color='blue')
  draw_circle3 = plt.Circle((5, 0),5, alpha=0.2, color='green')

  axes.set_xlim((-10, 10))
  axes.set_ylim((-10, 10))
  axes.add_artist(draw_circle)
  axes.add_artist(draw_circle2)
  axes.add_artist(draw_circle3)
  plt.title('Circle')
  plt.show()

visualize_circles()