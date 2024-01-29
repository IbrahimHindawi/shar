'''
this module is responsible for building control objects

'''

import hou
from shar import *

#===================================
# Utilities
#===================================

def setupOffsetName(name):
    return name + '_offset'

def setupAutoName(name):
    return name + '_auto'

def setupControlName(name):
    return name + '_ctrl'

def getBoneLength(bone):
    bone_length = bone.parm('length').eval()
    return bone_length

def setupNodeDisplayColor(node, color):
    node.parm('dcolorr').set(color.rgb()[0])
    node.parm('dcolorg').set(color.rgb()[1])
    node.parm('dcolorb').set(color.rgb()[2])

#===================================
# Control Core System
#===================================

def MakeOffset(rig, target, fkOffsetName, inputTarget = None):
    targetPosition = target.position()

    # make offset
    fkoffset = rig.createNode("null", fkOffsetName)
    nodeGroup = shar.nodegroups.getNodeGroupByName(rig, "help")
    nodeGroup.addNode(fkoffset)

    fkoffset.setSelectableInViewport(False)
    fkoffset.parm("picking").set(0)
    fkoffset.setDisplayFlag(False)
    fkoffset.setFirstInput(target)
    fkoffset.move(hou.Vector2(targetPosition.x()+2, targetPosition.y()))
    #fkoffset.moveToGoodPosition()
    fkoffset.parm('keeppos').set(True)
    fkoffset.setFirstInput(None)
    fkoffset.moveParmTransformIntoPreTransform()
    fkoffset.parm("rOrd").set("zyx")
    for child in fkoffset.children():
        child.destroy()

    if inputTarget == None:
        fkoffset.setInput(0, None)

    elif inputTarget == 'backbone':
        offsetInput = target.inputs()[0]
        fkoffset.setInput(0, offsetInput)
        
    else:
        fkoffset.setInput(0, inputTarget)

    return fkoffset

#fkoffsetPosition = fkoffset.position()
def MakeAuto(rig, target, fkAutoName):
    targetPosition = target.position()
    # make auto
    fkauto = rig.createNode("null", fkAutoName)
    nodeGroup = shar.nodegroups.getNodeGroupByName(rig, "help")
    nodeGroup.addNode(fkauto)

    fkauto.setSelectableInViewport(False)
    fkauto.parm("picking").set(0)
    fkauto.setDisplayFlag(False)
    fkauto.setFirstInput(target)
    fkauto.move(hou.Vector2(targetPosition.x(), targetPosition.y()-1))
    #fkauto.moveToGoodPosition()
    fkauto.parm('keeppos').set(True)
    fkauto.moveParmTransformIntoPreTransform()
    fkauto.setColor(hou.Color([1.0, 0.0, 0.5]))
    fkauto.parm("rOrd").set("zyx")
    for child in fkauto.children():
        child.destroy()
    return fkauto

def MakeCtrl(rig, target, controllerName, ctrlColor = shar.color.green, ctrlSize = 0.1, parm = None, flip = False):
    targetPosition = target.position()
    # make ctrl
    fkcontrol = rig.createNode("null", controllerName)
    nodeGroup = shar.nodegroups.getNodeGroupByName(rig, "ctrl")
    nodeGroup.addNode(fkcontrol)
    fkcontrol.setFirstInput(target)
    fkcontrol.move(hou.Vector2(targetPosition.x(), targetPosition.y()-1))
    #fkcontrol.moveToGoodPosition()
    setupNodeDisplayColor(fkcontrol, ctrlColor)
    fkcontrol.parm('keeppos').set(True)
    fkcontrol.moveParmTransformIntoPreTransform()
    fkcontrol.parm("rOrd").set("zyx")
    fkcontrol.setColor(hou.Color([0.145, 0.667, 0.557]))
    fkcontrol.parm('controltype').set(1)
    fkcontrol.parm('geoscale').set(ctrlSize)
    fkcontrol.moveParmTransformIntoPreTransform()
    fkcontrol.parm('orientation').set(0)
    fkcontrol.setParms({'tdisplay':1})
    shar.parameter.setupDisplay(fkcontrol, 'c')
    fkcontrol.setParms({
        'controltype':1,
        'geosizex': 1,
        'geosizey': 1,
        'geosizez':1,
        'orientation': 3
        })
    if parm != None:
        fkcontrol.parm('display').setExpression('if (ch("../' + parm.name() + '") > 0.5, 1, 0) && ch("../cdisplay") == 1')
        if flip == True:
            fkcontrol.parm('display').setExpression('if (ch("../' + parm.name() + '") < 0.5, 1, 0) && ch("../cdisplay") == 1')
    return fkcontrol


#===================================
# Control System
#===================================

def MakeControlShape(rig, target, name, ctrlColor = shar.color.green, ctrlSize = 0.1, parm = None):

    fkoffsetname  = setupOffsetName(name)
    fkautoname    = setupAutoName(name)
    fkcontrolname = setupControlName(name)

    ctrls = []

    fkoffset = MakeOffset(rig, target, fkoffsetname)
    ctrls.append(fkoffset)

    fkauto = MakeAuto(rig, fkoffset, fkautoname)
    ctrls.append(fkauto)    

    fkcontrol = MakeCtrl(rig, fkauto, fkcontrolname, ctrlColor, ctrlSize, parm)
    ctrls.append(fkcontrol)

    return ctrls

def MakeControlFk(rig, target, name, ctrlColor = shar.color.green, ctrlSize = 0.1, parm = None):

    fkoffsetname  = setupOffsetName(name)
    fkautoname    = setupAutoName(name)
    fkcontrolname = setupControlName(name)

    ctrls = []

    fkoffset = MakeOffset(rig, target, fkoffsetname, 'backbone')
    ctrls.append(fkoffset)

    fkauto = MakeAuto(rig, fkoffset, fkautoname)
    ctrls.append(fkauto)    

    fkcontrol = MakeCtrl(rig, fkauto, fkcontrolname, ctrlColor, ctrlSize, parm)
    ctrls.append(fkcontrol)

    return ctrls

def MakeControlIk(rig, target, name, inputTarget, ctrlColor = shar.color.green, ctrlSize = 0.1, parm = None):
    fkoffsetname  = setupOffsetName(name)
    fkautoname    = setupAutoName(name)
    fkcontrolname = setupControlName(name)

    ctrls = []

    fkoffset = MakeOffset(rig, target, fkoffsetname, inputTarget)
    ctrls.append(fkoffset)

    fkauto = MakeAuto(rig, fkoffset, fkautoname)
    ctrls.append(fkauto)    

    fkcontrol = MakeCtrl(rig, fkauto, fkcontrolname, ctrlColor, ctrlSize, parm)
    fkcontrol.parm('display').setExpression('if (ch("../' + parm.name() + '") < 0.5, 1, 0) && ch("../cdisplay") == 1')
    ctrls.append(fkcontrol)

    target.setInput(0, fkcontrol)

    return ctrls

def SetTwistPosition(twist_affector, bone1):
    # OLD IMPLEMENTATION START #
    # bone2 = bone1.outputs()[0]
    
    # twist_affector_matrix = twist_affector.worldTransform()
    # bone1_matrix = bone1.worldTransform()
    # bone2_matrix = bone2.worldTransform()
    
    # bone1_position = bone1_matrix.extractTranslates()
    # bone2_position = bone2_matrix.extractTranslates()
    
    # bone1_dir = bone2_position - bone1_position
    # twist_affector.setWorldTransform(bone1_matrix)
    
    # bone1_translation_dir = bone1_position + bone1_dir
    # twist_affector.setParms({'tx':bone1_translation_dir.x() ,'ty':bone1_translation_dir.y() ,'tz':bone1_translation_dir.z()})
    
    # push_off_dir = hou.Vector3([ -bone1_dir.x(), 0, bone1_dir.z() ])
    # push_off_dir = push_off_dir.normalized()
    # twist_affector.setParms({'tx':push_off_dir.x()  ,'tz':push_off_dir.z()})
    # OLD IMPLEMENTATION END #

    #box = hou.node('/obj/boxer')
    #bone1 = hou.node('/obj/chain_bone1/')
    #bone2 = hou.node('/obj/chain_bone2/')
    bone2 = bone1.outputs()[0]

    # get box world transform
    box_mtx = twist_affector.worldTransform()

    # get bone1 world transform
    bone1_mtx = bone1.worldTransform()

    # get bone2 world transform
    bone2_mtx = bone2.worldTransform()

    # set twist_affector transform to bone transform
    twist_affector.setWorldTransform(bone1_mtx)

    # create forward vector
    forward = hou.Vector3([ 0.0, 0.0, -1.0 ])

    # extract bone positions
    bone1_position = bone1_mtx.extractTranslates()
    bone2_position = bone2_mtx.extractTranslates()

    # move along bone1
    bone1_dir = bone2_position - bone1_position

    bone1_dir += bone1_position

    twist_affector.setParms({'tx':bone1_dir.x() ,'ty':bone1_dir.y() ,'tz':bone1_dir.z()})
    twist_affector.setParms({'rx':0})

    # new twist_affector world transform
    twist_affector_mtx = twist_affector.worldTransform()

    # transform forward vector to twist_affector local space
    local_forward = forward * twist_affector_mtx

    forward_mtx = hou.hmath.buildTranslate(forward)

    twist_affector.setWorldTransform(forward_mtx* twist_affector_mtx)

    #local_forward


def MakeIkObjects(rig, target, parm, twist_local_offset):

    ikCtrls = []
    
    rig = target.parent()

    # get next bone
    targetChild = target.outputs()[0]

    # get next next bone
    targetChildChild = targetChild.outputs()[0]

    targetPosition = target.position()
    #create goal object
    goal = rig.createNode('null', target.name() + '_goal')
    goal.move(hou.Vector2(targetPosition.x()+4, targetPosition.y()))
    ikCtrls.append(goal)

    #customize shape
    goal.setParms({
        'geoscale' : 0.1,
        'controltype' : 2
        })

    #reposition
    goal.setInput(0, targetChildChild)
    goal.setParms({'keeppos':1})
    goal.setInput(0, None)


    #create twist object
    twist = rig.createNode('null', target.name() + '_twist')
    twist.move(hou.Vector2(targetPosition.x()+4, targetPosition.y()))
    ikCtrls.append(twist)

    #customize shape
    twist.setParms({
        'geoscale' : 0.1,
        'controltype' : 2
        })

    #reposition
    twist.setInput(0, targetChild)
    twist.parm('ty').set(twist_local_offset)
    twist.setParms({'keeppos':1})
    twist.setInput(0, None)
    #self.SetTwistPosition(twist, target)
    twist.moveParmTransformIntoPreTransform()
    
    twist.movePreTransformIntoParmTransform()

    twist.setParms({ 'rx' : 0, 'ry' : 0, 'rz' : 0 , 'scale' : 1})
    twist.moveParmTransformIntoPreTransform()
    goal.setParms({ 'rx' : 0, 'ry' : 0, 'rz' : 0 , 'scale' : 1})
    goal.moveParmTransformIntoPreTransform()

    twist.parm('display').setExpression('if (ch("../' + parm.name() + '") > 0.5, 0, 1) && ch("../cdisplay") == 1')
    twist.setParms({'tdisplay':1})
    twist.setDisplayFlag(0)
    goal.parm('display').setExpression('if (ch("../' + parm.name() + '") > 0.5, 0, 1) && ch("../cdisplay") == 1')
    goal.setParms({'tdisplay':1})
    goal.setDisplayFlag(0)

    return ikCtrls


def MakeIkObjects2(rig, target, parm, twistObject):

    nodeGroup = shar.nodegroups.getNodeGroupByName(rig, "help")

    ikCtrls = []

    rig = target.parent()

    # get next bone
    targetChild = target.outputs()[0]

    # get next next bone
    targetChildChild = targetChild.outputs()[0]

    #create goal object
    goal = rig.createNode('null', target.name() + '_goal')
    nodeGroup.addNode(goal)
    targetPosition = target.position()
    goal.move(hou.Vector2(targetPosition.x()+4, targetPosition.y()))
    ikCtrls.append(goal)

    #customize shape
    goal.setParms({
        'geoscale' : 0.1,
        'controltype' : 2
        })

    #reposition
    goal.setInput(0, targetChildChild)
    goal.setParms({'keeppos':1})
    goal.setInput(0, None)

    #get twist object
    #twist = self.rig.createNode('null', target.name() + '_twist')
    twist = twistObject
    nodeGroup.addNode(twist)
    ikCtrls.append(twist)

    #customize shape
    twist.setParms({
        'geoscale' : 0.1,
        'controltype' : 2
        })

    #reposition
    twist.setInput(0, targetChild)
    #twist.parm('ty').set(twist_local_offset)
    twist.setParms({'keeppos':1})
    twist.setInput(0, None)
    #self.SetTwistPosition(twist, target)
    twist.moveParmTransformIntoPreTransform()
    
    twist.movePreTransformIntoParmTransform()

    twist.setParms({ 'rx' : 0, 'ry' : 0, 'rz' : 0 , 'scale' : 1})
    twist.moveParmTransformIntoPreTransform()
    goal.setParms({ 'rx' : 0, 'ry' : 0, 'rz' : 0 , 'scale' : 1})
    goal.moveParmTransformIntoPreTransform()

    twist.parm('display').setExpression('if (ch("../' + parm.name() + '") > 0.5, 0, 1) && ch("../cdisplay") == 1')
    twist.setParms({'tdisplay':1})
    twist.setDisplayFlag(0)
    goal.parm('display').setExpression('if (ch("../' + parm.name() + '") > 0.5, 0, 1) && ch("../cdisplay") == 1')
    goal.setParms({'tdisplay':1})
    goal.setDisplayFlag(0)

    return ikCtrls        

def MakeIkSelfObjects(rig, target, parm, twist_local_offset):

    ikCtrls = []

    rig = target.parent()

    # get next bone
    #targetChild = target.outputs()[0]

    # get next next bone
    #targetChildChild = targetChild.outputs()[0]

    #create goal object
    targetPosition = target.position()
    goal = rig.createNode('null', target.name() + '_goal')
    goal.move(hou.Vector2(targetPosition.x()+4, targetPosition.y()))
    ikCtrls.append(goal)

    #customize shape
    goal.setParms({
        'geoscale' : 0.1,
        'controltype' : 2
        })

    #reposition
    goal.setInput(0, target)
    goal.setParms({'keeppos':1})
    goal.parm('tz').set(-getBoneLength(target))
    goal.setInput(0, None)


    #create twist object
    twist = rig.createNode('null', target.name() + '_twist')
    twist.move(hou.Vector2(targetPosition.x()+4, targetPosition.y()))
    ikCtrls.append(twist)

    #customize shape
    twist.setParms({
        'geoscale' : 0.1,
        'controltype' : 2
        })

    #reposition
    twist.setInput(0, target)
    twist.setParms({'keeppos':1})
    twist.setInput(0, None)
    twist.moveParmTransformIntoPreTransform()
    twist.parm('ty').set(-twist_local_offset)
    twist.movePreTransformIntoParmTransform()

    twist.setParms({ 'rx' : 0, 'ry' : 0, 'rz' : 0 , 'scale' : 1})
    twist.moveParmTransformIntoPreTransform()
    goal.setParms({ 'rx' : 0, 'ry' : 0, 'rz' : 0 , 'scale' : 1})

    goal.moveParmTransformIntoPreTransform()

    twist.parm('display').setExpression('if (ch("../' + parm.name() + '") > 0.5, 0, 1) && ch("../cdisplay") == 1')
    twist.setParms({'tdisplay':1})
    twist.setDisplayFlag(0)
    goal.parm('display').setExpression('if (ch("../' + parm.name() + '") > 0.5, 0, 1) && ch("../cdisplay") == 1')
    goal.setParms({'tdisplay':1})
    goal.setDisplayFlag(0)

    return ikCtrls





    # def MakeControlShape(self, target, name, ctrlSize = 0.1, parm = None, inputTarget = None):
    #     self.rig = target.parent()

    #     fkoffsetname  = self.setupOffsetName(name)
    #     fkautoname    = self.setupAutoName(name)
    #     fkcontrolname = self.setupControlName(name)
        
    #     ctrlsize = 0.1

    #     ctrls = []

    #     if inputTarget == None:
    #         fkoffset = self.MakeOffset(target, fkoffsetname)

    #     elif inputTarget == 'free':
    #         fkoffset = self.MakeOffset(target, fkoffsetname, inputTarget = 'free')

    #     else:
    #         fkoffset = self.MakeOffset(target, fkoffsetname, inputTarget)

    #     ctrls.append(fkoffset)

    #     # make auto
    #     fkauto = self.MakeAuto(fkoffset, fkautoname)
    #     ctrls.append(fkauto)    

    #     # make ctrl
    #     if parm == None:
    #         fkcontrol = self.MakeCtrl(fkauto, fkcontrolname)
    #     else:
    #         fkcontrol = self.MakeCtrl(fkauto, fkcontrolname, parm)
    #     ctrls.append(fkcontrol)

    #     return ctrls

