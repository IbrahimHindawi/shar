'''
this module contains rigging utilities to ease bone manipulation

'''

import hou

def mirrorBones():
    nodes = hou.selectedNodes()

    for node in nodes:
        node.movePreTransformIntoParmTransform()

    for node in nodes:
        y = node.parm("ry").eval() * -1
        z = node.parm("rz").eval() * -1

        node.parm("ry").set(y)
        node.parm("rz").set(z)

    for node in nodes:
        node.moveParmTransformIntoPreTransform()

def mirrorFingers():
    nodes = hou.selectedNodes()

    for node in nodes:
        node.movePreTransformIntoParmTransform()

    for node in nodes:
        x = node.parm("tx").eval() * -1
        
        node.parm("tx").set(x)

    for node in nodes:
        node.moveParmTransformIntoPreTransform()

# duplicate hand
# reparent hand
# mirror bones
# mirror fingers