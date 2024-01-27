
# class shape(Enum):
#     null = 0
#     circles = 1
#     box = 2
#     planes = 3
#     null_and_circles = 4
#     null_and_box = 5
#     null_and_planes = 6
#     control_sop_input = 7
#     instanced_sop = 8


# null_shape = enum
# null_shape.name = "null"
# null_shape.value = 0

# circle_shape = enum
# circle_shape.name = "circle"
# circle_shape.value = 1

# box_shape = enum
# box_shape.name = "box"
# box_shape.value = 2

# planes_shape = enum
# planes_shape.name = "planes"
# planes_shape.value = 3

from Enum import Enum

null_shape = Enum("null", 0)
circle_shape = Enum("circle", 1)
box_shape = Enum("box", 2)
planes_shape = Enum("planes", 3)

allPlanes     = 0
orientationYZ = 1
orientationZX = 2
orientationXY = 3