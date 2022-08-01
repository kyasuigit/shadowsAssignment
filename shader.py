# CS3388B Assignment 4
# Kohei Yasui
# 251124530
# April 1st, 2020
# Shader implements the shader to be used in creating the images of 3D balls.
class shader:
    # This method tests to see if the object is shadowed or not.
    def __shadowed(self,object,I,S,objectList):
        M = object.getT()
        I = M * (I + S.scalarMultiply(0.001)) # use the T matrix from the object to get the I matrix

        S = M * S # convert S to world coordinates

        for i in objectList: # loop through the objects
            M = i.getT()
            M_inv = M.inverse() # get the inverse of M of the current object
            test = M_inv * I
            S = (M_inv * S).normalize() # transform to light source
            if object.intersection(test, S) != -1.0: #if there is an intersection between T and S, return True
                return True

        return False

    # This method initializes the shader object to be used in the image
    def __init__(self,intersection,direction,camera,objectList,light):
        object_init = objectList[intersection[0]] # get object at k (intersection[0])
        M_inv = object_init.getTinv()
        Ts = M_inv * light.getPosition() # initialize the light matrix, the camera matrix, and the direction using the inverse of M.
        Te = M_inv * camera.getE()
        Td = M_inv * direction

        I = Te + (Td.scalarMultiply(intersection[1])) # initialize I, S, N, R, and V matrices for use in returning colour
        S = (Ts - I).normalize()

        N = object_init.normalVector(I)

        R = N.scalarMultiply((S.dotProduct(N))*2) - S

        V = (Te - I).normalize()

        Id = 0
        Is = 0

        if N.dotProduct(S) > 0: # set Id and Is to dot products of N and S, R and V respectively
            Id = N.dotProduct(S)

        if R.dotProduct(V) > 0:
            Is = R.dotProduct(V)

        r = object_init.getReflectance() # get the reflectance, color of the object and light intensity
        c = object_init.getColor()
        Li = light.getIntensity()

        if not self.__shadowed(object_init, I, S, objectList): # check if the object is not shadowed
            f = r[0] + r[1] * Id + r[2] * (Is**r[3]) # set f to the value not shadowed

        else: # set to shadowed
            f = r[0]

        self.__color = (int(c[0] * Li[0] * f), int(c[1] * Li[1] * f), int(c[2] * Li[2] * f)) # set the color instance variable to a tuple calculated using the values that we got.

    def getShade(self):
        return self.__color