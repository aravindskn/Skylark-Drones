import matplotlib.pyplot as plt
from Clustering import *

clustering = Clustering()

class Plotter:

    gcp_x = []
    gcp_y = []
    image_x = []
    image_y = []
    rectangle_x = []
    rectangle_y = []

    def __init__(self):

        for key, values in clustering.GCPs.no_X_Y.items():
            Plotter.gcp_x.append(values[1:][0])
            Plotter.gcp_y.append(values[1:][1])

        for x, y in zip(clustering.Images.xCoordinates, clustering.Images.yCoordinates):
            Plotter.image_x.append(x)
            Plotter.image_y.append(y)

        for key, regions in Clustering.Sectors.items():
            # get coordinates of rectangle
            #

            for region in regions[:2]:
                for coordinate in region:
                    Plotter.rectangle_x.append(coordinate[0])
                    Plotter.rectangle_y.append(coordinate[1])

        #exit(0)

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.scatter(Plotter.gcp_x, Plotter.gcp_y, s=1, c='b', marker="s", label='GCPs')
        ax1.scatter(Plotter.image_x, Plotter.image_y, s=5, c='r', marker="o", label='Images')
        ax1.scatter(Plotter.rectangle_x, Plotter.rectangle_y, s=10, c='g', marker="o", label='Sectors')
        #ax1.scatter(Plotter.rectangle_x[4:8], Plotter.rectangle_y[4:8], s=10, c='b', marker="s", label='Sector1b')
        #ax1.scatter(Plotter.rectangle_x[8:12], Plotter.rectangle_y[8:12], s=15, c='g', marker="s",
        #            label='Sector2a')
        #ax1.scatter(Plotter.rectangle_x[12:16], Plotter.rectangle_y[12:16], s=25, c='r', marker="s",
        #            label='Sector2b')
        #ax1.scatter(Plotter.rectangle_x[16:20], Plotter.rectangle_y[16:20], s=15, c='y', marker="s",
        #            label='Sector2b')
        plt.legend(loc='upper left')
        plt.show()

p = Plotter()
