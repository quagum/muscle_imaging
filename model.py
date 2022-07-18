from mpl_toolkits import mplot3d
from mri import multi_point

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
fig = plt.figure()


ax = fig.add_subplot(projection="3d")
ax.set_xlabel('x')
ax.set_ylabel('z')
ax.set_zlabel('y')
ax.set_xlim(-200, 700)
ax.set_ylim(0, 500)
ax.set_zlim(0, 500)

print("Collecting points")
all_points = multi_point() 
print("Drawing points")


ypoints = []
for index in range(0, 20, 2):
    for pair in all_points[index]:
        point1, point2 = pair[0], pair[1]
        x, y, z = [[point1[0], point2[0]], [300-point1[1], 300-point2[1]], [point1[2], point2[2]]]
        ypoints.append(y[0])
        ax.scatter(x, z, y, c='red', s=1)
        ax.plot(x, z, y, color='black')
plt.show()


fig, (ax1) = plt.subplots(nrows=1)
ax1.hist(ypoints)
plt.show()
#fig.savefig("test", dpi=None, facecolor='w', edgecolor='w', orientation='portrait', format=None,transparent=False, bbox_inches=None, pad_inches=0.1,metadata=None)