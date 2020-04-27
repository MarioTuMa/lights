import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    ambientcol = calculate_ambient(ambient, areflect)
    diffusecol = calculate_diffuse(light, dreflect, normal)
    specularcol = calculate_specular(light, sreflect, view, normal)
    #print(ambientcol)
    #print(diffusecol)
    #print(specularcol)
    #print(limit_color(ambientcol,diffusecol,specularcol))
    return limit_color(ambientcol,diffusecol,specularcol)

def calculate_ambient(alight, areflect):
    return [alight[0]*areflect[0],alight[1]*areflect[1],alight[2]*areflect[2]]

def calculate_diffuse(light, dreflect, normal):
    location = light[0]
    lcol = light[1]
    normalize(normal)
    normalize(location)
    ans = []
    for i in range(3):
        ans.append(lcol[i] * dreflect[i] * dot_product(normal, location))
    return ans

def calculate_specular(light, sreflect, view, normal):
    location = light[0]
    lcol = light[1]
    normalize(normal)
    normalize(location)
    normalize(view)

    bounceVector = []
    for i in range(3):
        bounceVector.append((2 * normal[i] * dot_product(normal, location) - location[i]))
    normalize(bounceVector)

    cosalpha = dot_product(bounceVector, view)
    modifiedscale = cosalpha ** SPECULAR_EXP

    specular = []
    for i in range(3):
        specular.append(lcol[i] * sreflect[i] * modifiedscale)

    return specular


def limit_color(ambientcol,diffusecol,specularcol):
    col = []
    for i in range(3):
        #print(min(255,int(ambientcol[i]+diffusecol[i]+specularcol[i])))
        col.append(min(255,int(ambientcol[i]+diffusecol[i]+specularcol[i])))
        if(col[i]<0):
            col[i]=0
    return col
#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
