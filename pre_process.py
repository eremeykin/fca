__author__ = 'eremeykin'
import numpy as np

black = [0, 0, 0]
purple = [128, 0, 128]
buff = [240, 220, 130]
pink = [255, 192, 203]
yellow = [255, 255, 0]
green = [0, 128, 0]
cinnamon = [123, 72, 43]
chocolate = [210, 105, 30]
red = [255, 0, 0]
white = [255, 255, 255]
gray = [128, 128, 128]
brown = [165, 42, 42]
orange = [255, 165, 0]
color_map = {
    '[0, 0, 0]': 'black',
    '[128, 0, 128]': 'purple',
    '[240, 220, 130]': 'buff',
    '[255, 192, 203]': 'pink',
    '[255, 255, 0]': 'yellow',
    '[0, 128, 0]': 'green',
    '[123, 72, 43]': 'cinnamon',
    '[210, 105, 30]': 'chocolate',
    '[255, 0, 0]': 'red',
    '[255, 255, 255]': 'white',
    '[128, 128, 128]': 'gray',
    '[165, 42, 42]': 'brown',
    '[255, 165, 0]': 'orange',
}
colors = [black, purple, buff, pink, yellow, green, cinnamon, chocolate, red, white, gray, brown, orange]

n = len(colors)
dm = [[0 for j in range(n)] for i in range(n)]
dst = lambda x, y: ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2)**0.5

for i in range(n):
    for j in range(n):
        dm[i][j] = dst(colors[i], colors[j])

da = np.array(dm)
avg = np.average(da)
for i in range(n):
    print(color_map[str(colors[i])] + ":")
    for j in range(n):
        if dm[i][j] < avg / 2.5
            print('\t' + color_map[str(colors[j])])


