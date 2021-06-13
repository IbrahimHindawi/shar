'''
this module is responsible for building control objects

'''

import hou

class control:

    rig = None

    def __init__(self, rig):

        self.rig = rig

        #self.rig = hou.node('/obj/skel_hum3')


    #===================================
    # Utilities
    #===================================

    def SetupOffsetName(self, name):
        return name + '_offset'

    def SetupAutoName(self, name):
        return name + '_auto'

    def SetupControlName(self, name):
        return name + '_ctrl'

    def getBoneLength(self, bone):
        bone_length = bone.parm('length').eval()
        return bone_length


    #===================================
    # Control Core System
    #===================================

    def MakeOffset(self, target, fkOffsetName, inputTarget = None):
        targetPosition = target.position()

        # make offset
        fkoffset = self.rig.createNode("null", fkOffsetName)
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
    def MakeAuto(self, target, fkAutoName):
        targetPosition = target.position()
        # make auto
        fkauto = self.rig.createNode("null", fkAutoName)
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

    def MakeCtrl(self, target, ControllerName, ctrlSize = 0.1, parm = None, flip = False ):
        targetPosition = target.position()
        # make ctrl
        fkcontrol = self.rig.createNode("null", ControllerName )
        fkcontrol.setFirstInput(target)
        fkcontrol.move(hou.Vector2(targetPosition.x(), targetPosition.y()-1))
        #fkcontrol.moveToGoodPosition()
        fkcontrol.parm('keeppos').set(True)
        fkcontrol.moveParmTransformIntoPreTransform()
        fkcontrol.parm("rOrd").set("zyx")
        fkcontrol.setColor(hou.Color([0.145, 0.667, 0.557]))
        fkcontrol.parm('controltype').set(1)
        fkcontrol.parm('geoscale').set(ctrlSize)
        fkcontrol.moveParmTransformIntoPreTransform()
        fkcontrol.parm('orientation').set(0)
        fkcontrol.setParms({'tdisplay':1})
        fkcontrol.setParms({
            'controltype':1,
            'geosizex': 1,
            'geosizey': 1,
            'geosizez':1,
            'orientation': 3
            })
        if parm != None:
            fkcontrol.parm('display').setExpression('if ( ch("../' + parm.name() + '") > 0.5, 1, 0)' )
            if flip == True:
                fkcontrol.parm('display').setExpression('if ( ch("../' + parm.name() + '") < 0.5, 1, 0)' )
        return fkcontrol


    #===================================
    # Control System
    #===================================

    def MakeControlShape(self, target, name, ctrlSize = 0.1, parm = None):

        #self.rig = target.parent()

        fkoffsetname  = self.SetupOffsetName(name)
        fkautoname    = self.SetupAutoName(name)
        fkcontrolname = self.SetupControlName(name)

        ctrls = []

        fkoffset = self.MakeOffset(target, fkoffsetname)
        ctrls.append(fkoffset)

        fkauto = self.MakeAuto(fkoffset, fkautoname)
        ctrls.append(fkauto)    

        fkcontrol = self.MakeCtrl(fkauto, fkcontrolname, ctrlSize, parm)
        ctrls.append(fkcontrol)

        

        return ctrls

    def MakeControlFk(self, target, name, ctrlSize = 0.1, parm = None):

        fkoffsetname  = self.SetupOffsetName(name)
        fkautoname    = self.SetupAutoName(name)
        fkcontrolname = self.SetupControlName(name)

        ctrls = []

        fkoffset = self.MakeOffset(target, fkoffsetname, 'backbone')
        ctrls.append(fkoffset)

        fkauto = self.MakeAuto(fkoffset, fkautoname)
        ctrls.append(fkauto)    

        fkcontrol = self.MakeCtrl(fkauto, fkcontrolname, ctrlSize, parm)
        ctrls.append(fkcontrol)

        return ctrls

    def MakeControlIk(self, target, name, inputTarget, ctrlSize = 0.1, parm = None):
        fkoffsetname  = self.SetupOffsetName(name)
        fkautoname    = self.SetupAutoName(name)
        fkcontrolname = self.SetupControlName(name)

        ctrls = []

        fkoffset = self.MakeOffset(target, fkoffsetname, inputTarget)
        ctrls.append(fkoffset)

        fkauto = self.MakeAuto(fkoffset, fkautoname)
        ctrls.append(fkauto)    

        fkcontrol = self.MakeCtrl(fkauto, fkcontrolname, ctrlSize, parm)
        fkcontrol.parm('display').setExpression('if ( ch("../' + parm.name() + '") < 0.5, 1, 0)' )
        ctrls.append(fkcontrol)

        target.setInput(0, fkcontrol)

        return ctrls

    def SetTwistPosition(  self, twist_affector, bone1 ):
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
        
        # push_off_dir = hou.Vector3( [ -bone1_dir.x(), 0, bone1_dir.z() ] )
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

        twist_affector.setWorldTransform(forward_mtx* twist_affector_mtx )

        #local_forward


    def MakeIkObjects(self, target, parm, twist_local_offset):

        ikCtrls = []
        
        self.rig = target.parent()

        # get next bone
        targetChild = target.outputs()[0]

        # get next next bone
        targetChildChild = targetChild.outputs()[0]

        #create goal object
        goal = self.rig.createNode('null', target.name() + '_goal')
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
        twist = self.rig.createNode('null', target.name() + '_twist')
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

        twist.setParms( { 'rx' : 0, 'ry' : 0, 'rz' : 0 , 'scale' : 1} )
        twist.moveParmTransformIntoPreTransform()
        goal.setParms( { 'rx' : 0, 'ry' : 0, 'rz' : 0 , 'scale' : 1} )
        goal.moveParmTransformIntoPreTransform()

        twist.parm('display').setExpression('if ( ch("../' + parm.name() + '") > 0.5, 0, 1)' )
        twist.setParms({'tdisplay':1})
        twist.setDisplayFlag(0)
        goal.parm('display').setExpression('if ( ch("../' + parm.name() + '") > 0.5, 0, 1)' )
        goal.setParms({'tdisplay':1})
        goal.setDisplayFlag(0)

        return ikCtrls


    def MakeIkObjects2(self, target, parm, twist_object):

        ikCtrls = []

        self.rig = target.parent()

        # get next bone
        targetChild = target.outputs()[0]

        # get next next bone
        targetChildChild = targetChild.outputs()[0]

        #create goal object
        goal = self.rig.createNode('null', target.name() + '_goal')
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
        twist = twist_object
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

        twist.setParms( { 'rx' : 0, 'ry' : 0, 'rz' : 0 , 'scale' : 1} )
        twist.moveParmTransformIntoPreTransform()
        goal.setParms( { 'rx' : 0, 'ry' : 0, 'rz' : 0 , 'scale' : 1} )
        goal.moveParmTransformIntoPreTransform()

        twist.parm('display').setExpression('if ( ch("../' + parm.name() + '") > 0.5, 0, 1)' )
        twist.setParms({'tdisplay':1})
        twist.setDisplayFlag(0)
        goal.parm('display').setExpression('if ( ch("../' + parm.name() + '") > 0.5, 0, 1)' )
        goal.setParms({'tdisplay':1})
        goal.setDisplayFlag(0)

        return ikCtrls        

    def MakeIkSelfObjects(self, target, parm, twist_local_offset):

        ikCtrls = []

        self.rig = target.parent()

        # get next bone
        #targetChild = target.outputs()[0]

        # get next next bone
        #targetChildChild = targetChild.outputs()[0]

        #create goal object
        goal = self.rig.createNode('null', target.name() + '_goal')
        ikCtrls.append(goal)

        #customize shape
        goal.setParms({
            'geoscale' : 0.1,
            'controltype' : 2
            })

        #reposition
        goal.setInput(0, target)
        goal.setParms({'keeppos':1})
        goal.parm('tz').set(-self.getBoneLength(target))
        goal.setInput(0, None)


        #create twist object
        twist = self.rig.createNode('null', target.name() + '_twist')
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

        twist.setParms( { 'rx' : 0, 'ry' : 0, 'rz' : 0 , 'scale' : 1} )
        twist.moveParmTransformIntoPreTransform()
        goal.setParms( { 'rx' : 0, 'ry' : 0, 'rz' : 0 , 'scale' : 1} )

        goal.moveParmTransformIntoPreTransform()

        twist.parm('display').setExpression('if ( ch("../' + parm.name() + '") > 0.5, 0, 1)' )
        twist.setParms({'tdisplay':1})
        twist.setDisplayFlag(0)
        goal.parm('display').setExpression('if ( ch("../' + parm.name() + '") > 0.5, 0, 1)' )
        goal.setParms({'tdisplay':1})
        goal.setDisplayFlag(0)

        return ikCtrls





    # def MakeControlShape(self, target, name, ctrlSize = 0.1, parm = None, inputTarget = None):
    #     self.rig = target.parent()

    #     fkoffsetname  = self.SetupOffsetName(name)
    #     fkautoname    = self.SetupAutoName(name)
    #     fkcontrolname = self.SetupControlName(name)
        
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

