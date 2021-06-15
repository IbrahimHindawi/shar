'''
this module is responsible for building constraints

'''


import hou



def kinCheck( rig, target):
    kinExists = False
    for node in rig.children():
        #print "NODES = " + node.name()
        if node.name() == 'KIN_Chops':
            kinExists = True
            break
        else:
            kinExists = False


    if kinExists == True:
        for node in rig.children():
            if node.name() == 'KIN_Chops':
                return node
    else:
        kin = rig.createNode('chopnet', 'KIN_Chops')
        return kin


def MakeFKConstraints( rig, target, fkcontrol, parm = None):
    #Get bone
    bone = target

    #Enable Constraints
    bone.setParms({ "constraints_on" : 1 })

    #Create Chopnet in bone
    chopnet = bone.createNode("chopnet", "constraints")

    #Set Chopnet as Constraint parm
    bone.setParms({ "constraints_path" : "constraints" })

    #create constraintgetworldspace
    getworldspace = chopnet.createNode("constraintgetworldspace", "get_world")

    #set parm obj_path "../.."
    getworldspace.setParms({ "obj_path" : "../.." })

    #create constraintobject
    constraintobject = chopnet.createNode("constraintobject", fkcontrol.name() )

    #set parm obj_path relativePathTo bonectrl
    constraintobject.setParms({ "obj_path" : constraintobject.relativePathTo(fkcontrol) })

    #create constraintsimpleblend
    constraintsimpleblend = chopnet.createNode("constraintsimpleblend", "simple_blend")

    #set parm blend 1
    constraintsimpleblend.setParms({"blend":1})

    #set input 0 worldspacee
    constraintsimpleblend.setInput(0, getworldspace)

    #set input 1 constraintobject
    constraintsimpleblend.setInput(1, constraintobject)

    #create constraintoffset
    constraintoffset = chopnet.createNode("constraintoffset", "offset")

    #set input 0 simpleblend
    constraintoffset.setInput(0, constraintsimpleblend)

    #set input 1 worldspacee
    constraintoffset.setInput(1, getworldspace)

    #activate audio flag
    constraintoffset.setAudioFlag(1)

    constraintoffset.parm('update').pressButton()

    #set channel
    if parm != None:
        constraintoffset.parm('blend').setExpression('ch("' + constraintoffset.relativePathTo(rig) + '/' + parm.name() + '")')

def MakeIkConstraints( rig, target, goal, twist, parm):
    #checkKIN()
    rig = target.parent()
    kin = kinCheck(rig, target)
    ikin = kin.createNode('inversekin', 'KIN_' + target.name())
    ikin.setParms({
        'solvertype' : 2,
        'bonerootpath' : target.path(),
        'boneendpath' : target.outputs()[0].path(),
        'endaffectorpath' : goal.path(),
        'twistaffectorpath' : twist.path()
        #'blend' : ikin.relativePathTo(parm)
        })
    ikin.parm('blend').setExpression('1-ch("' + ikin.relativePathTo(rig) + '/' + parm.name() + '")')

    target.setParms({'solver' : ikin.path()})
    target.outputs()[0].setParms({'solver' : ikin.path()})

def MakeIkSelfConstraint( rig, target, goal, twist, parm):
    rig = target.parent()
    kin = kinCheck(rig, target)
    ikin = kin.createNode('inversekin', 'KIN_' + target.name())
    ikin.setParms({
        'solvertype' : 2,
        'bonerootpath' : target.path(),
        'boneendpath' : target.path(),
        'endaffectorpath' : goal.path(),
        'twistaffectorpath' : twist.path()
        #'blend' : ikin.relativePathTo(parm)
        })
    ikin.parm('blend').setExpression('1-ch("' + ikin.relativePathTo(rig) + '/' + parm.name() + '")')

    target.setParms({'solver' : ikin.path()})
    #target.outputs()[0].setParms({'solver' : ikin.path()})

def MakeComplexConstraint( rig, target, fkcontrol, ikcontrol, parm ):
    #Get bone
    bone = target

    #Enable Constraints
    bone.setParms({ "constraints_on" : 1 })

    #Create Chopnet in bone
    chopnet = bone.createNode("chopnet", "constraints")

    #Set Chopnet as Constraint parm
    bone.setParms({ "constraints_path" : "constraints" })

    #create constraintgetworldspace
    getworldspace = chopnet.createNode("constraintgetworldspace", "get_world")

    #set parm obj_path "../.."
    getworldspace.setParms({ "obj_path" : "../.." })

    #create constraintobject
    constraintobject = chopnet.createNode("constraintobject", fkcontrol.name() )

    #set parm obj_path relativePathTo bonectrl
    constraintobject.setParms({ "obj_path" : constraintobject.relativePathTo(fkcontrol) })

    #create constraintsimpleblend
    constraintsimpleblend = chopnet.createNode("constraintsimpleblend", "simple_blend")

    #set parm blend 1
    constraintsimpleblend.setParms({"blend":1})

    #set input 0 worldspacee
    constraintsimpleblend.setInput(0, getworldspace)

    #set input 1 constraintobject
    constraintsimpleblend.setInput(1, constraintobject)

    #create constraintoffset
    constraintoffset = chopnet.createNode("constraintoffset", "offset")

    #set input 0 simpleblend
    constraintoffset.setInput(0, constraintsimpleblend)

    #set input 1 worldspacee
    constraintoffset.setInput(1, getworldspace)

    #activate audio flag
    #constraintoffset.setAudioFlag(1)
    constraintoffset.parm('update').pressButton()

    #set channel
    constraintoffset.parm('blend').setExpression('ch("' + constraintoffset.relativePathTo(rig) + '/' + parm.name() + '")')

    #get parent space
    parentspace = chopnet.createNode('constraintgetparentspace', 'getparentspace')
    parentspace.parm('obj_path').set('../..')

    #object offset
    objoffset = chopnet.createNode('constraintobjectoffset', 'objectoffset')
    objoffset.parm('obj_path').set('../../../' + ikcontrol.name() )

    #simple blend
    simpleblend2 = chopnet.createNode('constraintsimpleblend', 'blendparents')
    simpleblend2.parm('blend').setExpression('1-ch("' + constraintoffset.relativePathTo(rig) + '/' + parm.name() + '")')

    #constraint parent
    constraintparentx = chopnet.createNode('constraintparentx', 'parent')
    constraintparentx.parm('writemask').set(56)

    objoffset.setInput(0, parentspace)
    simpleblend2.setInput(0, parentspace)
    simpleblend2.setInput(1, objoffset)
    constraintparentx.setInput(0, constraintoffset)
    constraintparentx.setInput(1, parentspace)
    constraintparentx.setInput(2, simpleblend2)

    constraintparentx.setAudioFlag(1)

    objoffset.parm('update').pressButton()



def MakeLookAtContraint( self, target, fkcontrol ):

    #Get bone
    bone = target

    #Enable Constraints
    bone.setParms({ "constraints_on" : 1 })

    #Create Chopnet in bone
    chopnet = bone.createNode("chopnet", "constraints")

    #Set Chopnet as Constraint parm
    bone.setParms({ "constraints_path" : "constraints" })

    #create constraintgetworldspace
    getworldspace = chopnet.createNode("constraintgetworldspace", "get_world")

    #set parm obj_path "../.."
    getworldspace.setParms({ "obj_path" : "../.." })

    #create constraintobject
    constraintobject = chopnet.createNode("constraintobject", fkcontrol.name() )

    #set parm obj_path relativePathTo bonectrl
    constraintobject.setParms({ "obj_path" : constraintobject.relativePathTo(fkcontrol) })

    #create contraintlookat
    lookat = chopnet.createNode("constraintlookat", "lookat")

    lookat.setInput(0, getworldspace)
    lookat.setInput(1, constraintobject)

    lookat.setAudioFlag(1)




