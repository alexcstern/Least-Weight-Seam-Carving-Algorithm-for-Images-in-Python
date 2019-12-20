# CS4102 Fall 2019 -- Homework 5
#################################
# Collaboration Policy: You are encouraged to collaborate with up to 4 other
# students, but all work submitted must be your own independently written
# solution. List the computing ids of all of your collaborators in the comment
# at the top of your java or python file. Do not seek published or online
# solutions for any assignments. If you use any published or online resources
# (which may not include solutions) when completing this assignment, be sure to
# cite them. Do not submit a solution that you are unable to explain orally to a
# member of the course staff.
#################################
# Your Computing ID: acs4wq
# Collaborators: 
# Sources: Introduction to Algorithms, Cormen, TA Office Hours
#################################
import numpy as np
import math
class SeamCarving:
    def __init__(self):
        self.n = 0
        self.m = 0
        self.min_seam = []
        self.image = 0
        self.e = 0
        return

    def setN(self, newN):
        self.n = newN

    def setM(self, newM):
        self.m = newM

    def setMinSeam(self, newMinSeam):
        self.min_seam = newMinSeam

    def setImage(self, newImage):
        self.image = newImage

    def setE(self, newE):
        self.e = newE


    # This method is the one you should implement.  It will be called to perform
    # the seam carving.  You may create any additional data structures as fields
    # in this class or write any additional methods you need.
    #
    # @return the seam's weight
    def run(self, image):

        # the pixel in image column i and row j
        # for image[j][i][pixel color]
        self.setN(len(image))
        self.setM(len(image[0]))
        self.setImage(image)
        # dynamically calculate energies
        self.e = []
        for k in range(self.n):
            y = []
            for l in range(self.m):
                y.append(0)
            self.e.append(y)

        for j in range(self.n - 1, -1, -1):
            for i in range(self.m):
                if j == (self.n - 1):
                    u = self.getEnergy(j, i)
                    self.e[j][i] = u
                else:
                    min_below1 = self.e[j + 1][i]
                    if i > 0:
                        min_below2 = self.e[j + 1][i - 1]
                    else:
                        min_below2 = float("inf")
                    if i < (self.m - 1):
                        min_below3 = self.e[j + 1][i + 1]
                    else:
                        min_below3 = float("inf")
                    self.e[j][i] = min(min_below2, min_below1, min_below3) + self.getEnergy(j, i)

        # find min seam
        k0 = np.where(self.e[0] == np.amin(self.e[0]))[0][0]
        seam = 0
        seam_route = []
        # k0 = starting column
        # i = current column, will change as you go down seam
        i = k0
        # j = current row
        j = 0
        # fill bottom to top,
        while j < (self.n - 1):
            if j == 0:
                seam = self.e[0][i]
                seam_route.append(i)
            min_below1 = self.e[j + 1][i]
            if i > 0:
                min_below2 = self.e[j + 1][i - 1]
            else:
                min_below2 = float("inf")
            if i < (self.m - 1):
                min_below3 = self.e[j + 1][i + 1]
            else:
                min_below3 = float("inf")
            min_goto = min(min_below2, min_below1, min_below3)
            if min_goto == min_below2:
                # lower left diagonal is smallest
                seam += min_below2
                seam_route.append(i - 1)
                i -= 1
            elif min_goto == min_below1:
                # directly below is the smallest
                # don't change i
                seam += min_below1
                seam_route.append(i)
            else:
                # lower right diagonal is smallest
                seam += min_below3
                seam_route.append(i + 1)
                i += 1
            j += 1

        self.setMinSeam(seam_route)
        return self.e[0][k0]

    def getEnergy(self, j, i):
        e_list = []
        if j > 0:
            # check directly above
            e_list.append(self.getDistance(j, i, j - 1, i))
        if i > 0:
            # check directly left
            e_list.append(self.getDistance(j, i, j, i - 1))
        if j > 0 and i > 0:
            # check upper left diagonal
            e_list.append(self.getDistance(j, i, j - 1, i - 1))
        if j < (self.n - 1):
            # check directly below
            e_list.append(self.getDistance(j, i, j + 1, i))
        if i < (self.m - 1):
            # check directly right
            e_list.append(self.getDistance(j, i, j, i + 1))
        if j < (self.n - 1) and i < (self.m - 1):
            # check lower right diagonal
            e_list.append(self.getDistance(j, i, j + 1, i + 1))
        if j < (self.n - 1) and i > 0:
            # check lower left diagonal
            e_list.append(self.getDistance(j, i, j + 1, i - 1))
        if j > 0 and i < (self.m - 1):
            # check lower right diagonal
            e_list.append(self.getDistance(j, i, j - 1, i + 1))
        return sum(e_list) / len(e_list)


    def getDistance(self, j1, i1, j2, i2):
        red = (self.image[j1][i1][0] - self.image[j2][i2][0])**2
        green = (self.image[j1][i1][1] - self.image[j2][i2][1])**2
        blue = (self.image[j1][i1][2] - self.image[j2][i2][2])**2
        return math.sqrt(red + blue + green)

    # Get the seam, in order from top to bottom, where the top-left corner of the
    # image is denoted (0,0).
    # 
    # Since the y-coordinate (row) is determined by the order, only return the x-coordinate
    # 
    # @return the ordered list of x-coordinates (column number) of each pixel in the seam
    #         as an array
    def getSeam(self):
        return self.min_seam

