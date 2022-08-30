from mpl_toolkits import mplot3d
from mri import multi_point
import pickle 

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
fig = plt.figure()


ax = fig.add_subplot(projection="3d")
ax.set_xlabel('x')
#ax.set_ylabel('z')
ax.set_zlabel('y')
ax.set_xlim(-200, 700)
ax.set_ylim(-200, 400)
ax.set_zlim(0, 400)

def model(starting_slice, number_of_slices, interval):
    print("Collecting points")
    collected_points = multi_point(starting_slice, number_of_slices, interval) 
    print("Drawing points")

    #ypoints = []
    for index in range(len(collected_points)):
        slice = collected_points[index]
        for pair in slice:
            point1, point2 = pair[0], pair[1]
            X, Y, Z = [[point1[0], point2[0]], [300-point1[1], 300-point2[1]], [point1[2], point2[2]]]
            #ypoints.append(Y[0])

            ax.scatter(X, Z, Y, c='black', s=0.2)
            ax.plot(X, Z, Y, color='pink')
    ax.set_title(str(starting_slice) + " to " + str(number_of_slices) + " with interval of " + str(interval))
    plt.show()

model(400, 500, 20)
#fig, (ax1) = plt.subplots(nrows=1)
#ax1.hist(ypoints)
#plt.show()