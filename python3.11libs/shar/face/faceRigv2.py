# get the selection to find the path
#object = hou.selectedNodes()
#netparent = object[0].parent()

#selectname = kwargs['toolname']
#selectname = object[0].name()

faceBones = []

#choice = ()
#choice = hou.ui.readInput( message = "Specify a prefix", initial_contents = selectname )

#name = choice[1]

def BuildControls( target, name, netparent ):
    fkcontrolname =  name + '_ctrl'
    fkautoname = name + '_auto'
    fkoffsetname = name + '_offset'

    ctrlsize = 0.01

    ctrls = []
    # make offset
    fkoffset = netparent.createNode("null", fkoffsetname)
    fkoffset.setSelectableInViewport(False)
    fkoffset.parm("picking").set(0)
    fkoffset.setDisplayFlag(False)
    fkoffset.setFirstInput(target)
    fkoffset.moveToGoodPosition()
    fkoffset.parm('keeppos').set(True)
    fkoffset.setFirstInput(None)
    fkoffset.moveParmTransformIntoPreTransform()
    fkoffset.parm("rOrd").set("zyx")
    for child in fkoffset.children():
        child.destroy()
    ctrls.append(fkoffset)

    # make auto
    fkauto = netparent.createNode("null", fkautoname)
    fkauto.setSelectableInViewport(False)
    fkauto.parm("picking").set(0)
    fkauto.setDisplayFlag(False)
    fkauto.setFirstInput(fkoffset)
    fkauto.moveToGoodPosition()
    fkauto.parm('keeppos').set(True)
    fkauto.moveParmTransformIntoPreTransform()
    fkauto.setColor(hou.Color([1.0, 0.0, 0.5]))
    fkauto.parm("rOrd").set("zyx")
    for child in fkauto.children():
        child.destroy()
    ctrls.append(fkauto)    

    # make ctrl
    fkcontrol = netparent.createNode("null", fkcontrolname)
    fkcontrol.setFirstInput(fkauto)
    fkcontrol.moveToGoodPosition()
    fkcontrol.parm('keeppos').set(True)
    fkcontrol.moveParmTransformIntoPreTransform()
    fkcontrol.parm("rOrd").set("zyx")
    fkcontrol.setColor(hou.Color([0.145, 0.667, 0.557]))
    fkcontrol.parm('controltype').set(1)
    fkcontrol.parm('geoscale').set(ctrlsize)
    fkcontrol.moveParmTransformIntoPreTransform()
    fkcontrol.parm('orientation').set(0)
    ctrls.append(fkcontrol)
    return ctrls

def BuildConstraints( target, fkcontrol ):
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

def BuildAnimRig(target, name, netparent):
    controls = BuildControls(target, name, netparent)
    BuildConstraints( target, controls[2])
    return controls

'''
def BonesAddControls():
    #for bone in faceBones:
    for bone in hou.selectedNodes():
        BuildAnimRig(bone, name)
'''

def FacePointCloudBuildBones():
    selection = hou.selectedNodes()[0]
    parent = selection.parent().parent()
    geo = selection.geometry()
    pointcloud = geo.points()

    masterNode = parent.createNode("null", "head_master")
    #masterNode.setParms({})
    masterNode.setColor(hou.Color((0.0,0.0,0.0)) )

    for point in pointcloud:
        # get position
        pos = point.position()
        # get color
        color = point.attribValue("Cd")
        # get name
        name = point.attribValue("name")
        # create bone
        bone = parent.createNode("bone", name)
        bone.setParms({
            "length":0.01,
            "tx":pos[0],
            "ty":pos[1],
            "tz":pos[2],
            "dcolorr": color[0],
            "dcolorg": color[1],
            "dcolorb": color[2]
            })
        bone.moveParmTransformIntoPreTransform()
        bone.setInput(0, masterNode)

        faceBones.append(bone)
        #print faceBones
        controls = BuildAnimRig(bone, name, parent)
        controls[0].setInput(0, masterNode)
        controls[2].setParms({
            "dcolorr": color[0],
            "dcolorg": color[1],
            "dcolorb": color[2]
            })

def BuildCurves():
    #get curves
    sopnode = hou.selectedNodes()[0]
    parent = sopnode.parent().parent()

    #get point groups
    geo = sopnode.geometry()
    pointgroups = geo.pointGroups()

    curvesgeonodes = []

    #iterate
    for pointgroup in pointgroups:
        geonode = parent.createNode("geo", pointgroup.name() )
        obj_mrg = geonode.createNode("object_merge", pointgroup.name() + "import" )
        obj_mrg.setParms( { "objpath1" : sopnode.path() } )

        delete = geonode.createNode("delete", "isolate_" + pointgroup.name())
        delete.setParms({"group" : pointgroup.name(), "negate" : 1, "entity" : 1})
        delete.setInput(0, obj_mrg)
        delete.moveToGoodPosition()

        sort = geonode.createNode("sort")
        sort.setParms({ "ptsort": 2 })
        sort.setInput(0, delete)
        sort.moveToGoodPosition()

        add = geonode.createNode("add")
        add.setParms({"switcher1":1})
        add.setInput(0, sort)
        add.moveToGoodPosition()

        centroid = geonode.createNode("add", "centroid")
        centroid.setParms({"usept0":1})
        centroid.parm("pt0x").setExpression('centroid("../'+"OUT_" + pointgroup.name() +'/",D_X)')
        centroid.parm("pt0y").setExpression('centroid("../'+"OUT_" + pointgroup.name() +'/",D_Y)')
        centroid.parm("pt0z").setExpression('centroid("../'+"OUT_" + pointgroup.name() +'/",D_Z)')
        '''
        centroid.setExpression({
            "pt0x":'centroid("../'+"OUT_" + pointgroup.name() +'/",D_X)',
            "pt0y":'centroid("../'+"OUT_" + pointgroup.name() +'/",D_Y)',
            "pt0z":'centroid("../'+"OUT_" + pointgroup.name() +'/",D_Z)'
            })
        '''
        centroid.setInput(0, sort)
        centroid.moveToGoodPosition()        

        convert = geonode.createNode("convert")
        convert.setParms({"totype":4})
        convert.setInput(0, add)
        convert.moveToGoodPosition()

        blendshapes = geonode.createNode("blendshapes::2.0")
        blendshapes.setInput(0, convert)
        blendshapes.moveToGoodPosition()

        null = geonode.createNode("null", "OUT_" + pointgroup.name())
        null.setColor( hou.Color((1.0, 1.0, 1.0)) )
        null.setInput(0, blendshapes)
        null.moveToGoodPosition()
        null.setRenderFlag(1)
        null.setDisplayFlag(1)
        
        curvesgeonodes.append(geonode)

    return curvesgeonodes

def BuildCurveControl(numberOfBones, curve):
    #build curve
    parent = curve.parent().parent()
    #create master
    master = parent.createNode("null", "Master")
    master.setColor( hou.Color((0.0,0.0,0.0)) )
    controllers = []
    #attach null path cns @ 0, 0.5, 1    LookAt None

    for x in range(1,numberOfBones):
        controller = parent.createNode("null", "controller"+str(x))
        controllers.append(controller)

    position = 0.0
    position += (1.0/numberOfBones)
    for controller in controllers:

        controller.setParms({
            "constraints_on":1,
            "constraints_path":"constraints",
            "geoscale":0.02,
            "controltype":1,
            "orientation":3,
            "dcolorr":0.0,
            "dcolorg":0.1,
            "dcolorb":0.0
            })
        chopnet = controller.createNode("chopnet", "constraints")
        worldspace = chopnet.createNode("constraintgetworldspace", "getworldspace")
        worldspace.setParms({"obj_path":"../.."})
        constraintpath = chopnet.createNode("constraintpath", "path")
        constraintpath.setParms({
            "lookatmode":0,
            "soppath":constraintpath.relativePathTo(curve),
            "pos": position
            })
        position += (1.0/numberOfBones)
        constraintpath.setInput(0, worldspace)
        constraintpath.setAudioFlag(1)
        #child  null to master
        controller.setInput(0, master)
        #create bone
        bone = parent.createNode("bone","facebone")
        bone.setParms({"length":0.01})
        #child  bone to null
        bone.setInput(0, controller)
        #create bone controller
        animContollers = BuildAnimRig(bone, bone.name(), parent)
        #child controller to null
        animContollers[0].setInput(0, controller)

    return master

def Main():
    #BuildAnimRig()
    #FacePointCloudBuildBones()
    #BonesAddControls()

    facecurves = BuildCurves()
    for node in facecurves:
        for child in node.children():
            if child.color() == hou.Color((1.0,1.0,1.0)):
                master = BuildCurveControl(6, child)
                node.setInput(0, master)
            if child.name() == "centroid":
                geo = child.geometry()
                point = geo.points()[0] # <---- problematic LOC ! ! !
                pos = point.attribValue("P") 
                print pos
                root = child.parent().parent()
                driver = root.createNode("null", "driver")
                driver.setParms({"tx":pos[0], "ty":pos[1], "tz":pos[2]})
                driver.setColor ( hou.Color ((1.0, 0.0, 0.0)) )

                
Main()