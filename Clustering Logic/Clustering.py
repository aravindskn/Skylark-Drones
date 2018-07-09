from GetData import *
import collections
import math
import warnings
import numpy
warnings.filterwarnings('ignore', 'The iteration is not making good progress')


class Clustering:

    Sectors = collections.OrderedDict()
    GCPs = LoadGCPs()
    Images = LoadImages()
    ListOfGCPs = []
    BreadthOfRectangle = 10  # metres
    LengthOverlap = 15 # metres

    #                length
    # ......................................... b
    # .                                       . r
    # .                                       . e
    # .                                       . a
    # .                                       . d
    # .                                       . t
    # ......................................... h


    def __init__(self):


        for key, value in Clustering.GCPs.no_X_Y.items():
            Clustering.ListOfGCPs.append(value[0])
            # C1, C2, C3...


        RectanglesWithoutGPS = [Clustering.ListOfGCPs[i: i + 3] for i in range(0, len(Clustering.ListOfGCPs), 2)]
        #print(RectanglesWithoutGPS)

        def equations(x1, y1, m, d):
            if m < 0:
                x_a = x1 - math.sqrt(d ** 2 / (1 + m ** 2))
                x_b = x1 + math.sqrt(d ** 2 / (1 + m ** 2))
                y_a = y1 + m * (x_a - x1)
                y_b = y1 + m * (x_b - x1)
                return (x_b, y_b), (x_a, y_a)

            else:
                x_a = x1 + math.sqrt(d ** 2 / (1 + m ** 2))
                x_b = x1 - math.sqrt(d ** 2 / (1 + m ** 2))
                y_a = y1 + m * (x_a - x1)
                y_b = y1 + m * (x_b - x1)
                return (x_b, y_b), (x_a, y_a)

        SectorNo = 1


        for rectangle in RectanglesWithoutGPS:
            if len(rectangle) > 1:

                point1 = Clustering.GCPs.no_X_Y[rectangle[0]][0]
                x1 = Clustering.GCPs.no_X_Y[rectangle[0]][1]
                y1 = Clustering.GCPs.no_X_Y[rectangle[0]][2]
                point2 = Clustering.GCPs.no_X_Y[rectangle[1]][0]
                x2 = Clustering.GCPs.no_X_Y[rectangle[1]][1]
                y2 = Clustering.GCPs.no_X_Y[rectangle[1]][2]
                point3 = Clustering.GCPs.no_X_Y[rectangle[2]][0]
                x3 = Clustering.GCPs.no_X_Y[rectangle[2]][1]
                y3 = Clustering.GCPs.no_X_Y[rectangle[2]][2]

                #print(point1, point2, point3)
                #print(x1, y1, x2, y2, x3, y3)

                if x2 - x1 != 0:

                    slope1 = (y2 - y1) / (x2 - x1)
                    slope2 = (y3 - y2) / (x3 - x2)
                    #print(slope1)
                    #print(slope2)

                    theta1 = math.atan(slope1)
                    theta2 = math.atan(slope2)

                    slope_p1 = -1 / slope1
                    slope_p2 = -1 / slope2

                    if theta1 < 0:
                        x1_left = x1 - Clustering.LengthOverlap * math.cos(theta1)
                        y1_left = y1 - Clustering.LengthOverlap * math.sin(theta1)

                    if theta1 > 0:
                        x1_left = x1 + Clustering.LengthOverlap * math.cos(theta1)
                        y1_left = y1 + Clustering.LengthOverlap * math.sin(theta1)

                    if theta2 < 0:
                        x2_right = x2 + Clustering.LengthOverlap * math.cos(theta2)
                        y2_right = y2 + Clustering.LengthOverlap * math.sin(theta2)

                    if theta2 > 0:
                        x2_right = x2 - Clustering.LengthOverlap * math.cos(theta2)
                        y2_right = y2 - Clustering.LengthOverlap * math.sin(theta2)

                    if theta2 < 0:
                        x2_left = x2 - Clustering.LengthOverlap * math.cos(theta2)
                        y2_left = y2 - Clustering.LengthOverlap * math.sin(theta2)

                    if theta2 > 0:
                        x2_left = x2 + Clustering.LengthOverlap * math.cos(theta2)
                        y2_left = y2 + Clustering.LengthOverlap * math.sin(theta2)

                    if theta2 < 0:
                        x3_right = x3 + Clustering.LengthOverlap * math.cos(theta2)
                        y3_right = y3 + Clustering.LengthOverlap * math.sin(theta2)

                    if theta2 > 0:
                        x3_right = x3 - Clustering.LengthOverlap * math.cos(theta2)
                        y3_right = y3 - Clustering.LengthOverlap * math.sin(theta2)

                    left_points1 = equations(x1_left, y1_left, slope_p1, Clustering.BreadthOfRectangle)
                    bottom_left1 = left_points1[0]
                    top_left1 = left_points1[1]

                    right_points1 = equations(x2_right, y2_right, slope_p1, Clustering.BreadthOfRectangle)
                    bottom_right1 = right_points1[0]
                    top_right1 = right_points1[1]

                    left_points2 = equations(x2_left, y2_left, slope_p2, Clustering.BreadthOfRectangle)
                    bottom_left2 = left_points2[0]
                    top_left2 = left_points2[1]

                    right_points2 = equations(x3_right, y3_right, slope_p2, Clustering.BreadthOfRectangle)
                    bottom_right2 = right_points2[0]
                    top_right2 = right_points2[1]

                    quadrilateral1 = [bottom_left1, top_left1, top_right1, bottom_right1]
                    quadrilateral2 = [bottom_left2, top_left2, top_right2, bottom_right2]

                    regions = []
                    regions.append(quadrilateral1)
                    regions.append(quadrilateral2)

                    Clustering.Sectors[SectorNo] = regions

                    SectorNo += 1



        def is_image_in_sector(image, coordinate_array):

            area_polygon = 0.5 * abs(
                coordinate_array[0][0] * coordinate_array[1][1] + coordinate_array[1][0] * coordinate_array[2][1] +
                coordinate_array[2][0] * coordinate_array[3][1] + coordinate_array[3][0] * coordinate_array[0][1] -
                coordinate_array[1][0] * coordinate_array[0][1] - coordinate_array[2][0] * coordinate_array[1][1] -
                coordinate_array[3][0] * coordinate_array[2][1] - coordinate_array[0][0] * coordinate_array[3][1]
            )

            area_triangle1 = 0.5 * abs(
                (image[1] * (coordinate_array[0][1] - coordinate_array[1][1])) +
                (coordinate_array[0][0] * (coordinate_array[1][1] - image[2])) +
                (coordinate_array[1][0] * (image[2] - coordinate_array[0][1]))
            )
            # print("t1",area_triangle1)
            area_triangle2 = 0.5 * abs(
                (image[1] * (coordinate_array[1][1] - coordinate_array[2][1])) +
                (coordinate_array[1][0] * (coordinate_array[2][1] - image[2])) +
                (coordinate_array[2][0] * (image[2] - coordinate_array[1][1]))
            )
            # print("t2", area_triangle2)
            area_triangle3 = 0.5 * abs(
                (image[1] * (coordinate_array[2][1] - coordinate_array[3][1])) +
                (coordinate_array[2][0] * (coordinate_array[3][1] - image[2])) +
                (coordinate_array[3][0] * (image[2] - coordinate_array[2][1]))
            )
            # print("t3", area_triangle3)
            area_triangle4 = 0.5 * abs(
                (image[1] * (coordinate_array[3][1] - coordinate_array[0][1])) +
                (coordinate_array[3][0] * (coordinate_array[0][1] - image[2])) +
                (coordinate_array[0][0] * (image[2] - coordinate_array[3][1]))
            )
            area_of_polygon = numpy.around(area_polygon, 4)
            area_of_triangles = numpy.around(area_triangle1 + area_triangle2 + area_triangle3 + area_triangle4, 4)

            return area_of_polygon == area_of_triangles

        # finding sectors where the images belong
        counter = 0

        for image_name, image_x, image_y in zip(Clustering.Images.imageNames, Clustering.Images.xCoordinates,
                                                Clustering.Images.yCoordinates):
            image = [image_name, image_x, image_y]
            for sector, regions in Clustering.Sectors.items():
                if is_image_in_sector(image, regions[0]) or is_image_in_sector(image, regions[1]):
                    counter += 1
                    Clustering.Sectors[sector].append(image_name)

        #print('count', counter)

        #for key, value in Clustering.Sectors.items():
            #print(key, value)











