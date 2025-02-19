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


def mirrorRotations():
    nodes = hou.selectedNodes()

    for node in nodes:
        if '_twist_' not in node.name() and '_legtwist_' not in node.name():
            node.movePreTransformIntoParmTransform()

    for node in nodes:
        y = node.parm("ry").eval() * -1
        z = node.parm("rz").eval() * -1

        node.parm("ry").set(y)
        node.parm("rz").set(z)

    for node in nodes:
        if '_twist_' not in node.name() and '_legtwist_' not in node.name():
            node.moveParmTransformIntoPreTransform()

def mirrorRoots():
    nodes = hou.selectedNodes()

    for node in nodes:
        if '_twist_' not in node.name() and '_legtwist_' not in node.name():
            node.movePreTransformIntoParmTransform()

    for node in nodes:
        x = node.parm("tx").eval() * -1
        
        node.parm("tx").set(x)

    for node in nodes:
        if '_twist_' not in node.name() and '_legtwist_' not in node.name():
            node.moveParmTransformIntoPreTransform()

def unlockTranslates():
    nodes = hou.selectedNodes()
    for node in nodes:
        if '_twist_' not in node.name() and '_legtwist_' not in node.name():
            for p in node.parms():
                if 'tx' == p.name() or 'ty' == p.name() or 'tz' == p.name():
                    p.lock(False)

def lockTranslates():
    nodes = hou.selectedNodes()
    for node in nodes:
        if '_twist_' not in node.name() and '_legtwist_' not in node.name():
            for p in node.parms():
                if 'tx' == p.name() or 'ty' == p.name() or 'tz' == p.name():
                    p.lock(True)

# duplicate hand
# reparent hand
# mirror bones
# mirror fingers
