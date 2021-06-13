# Auto Face Setup
# Ibrahim Hindawi
# H17.5.425
# https://www.ibrahimhindawi.com

# How to use:
# Create point groups for face curves in sops
# Select sop output and execute script
# Script builds control curves and assigns bone controls to them
# Tweak curves manually to make shapes
# Curves with Autos to rig face
#
# TODO:
# Automate skinning process:
# 1_parent masters to bone(s)
# 2_skin using root
# 3_detach master/controller connections, keep master/geonode connections
#
# Automate curve blendshape generation
# Automate autos generation
# Implement node layout 

import hou
faceBones = []

#choice = ()
#choice = hou.ui.readInput( message = "Specify a prefix", initial_contents = selectname )

#name = choice[1]

# Build parm holder
#root = facecurves[0].parent()
root = hou.selectedNodes()[0].parent().parent()
parmer = root.createNode("null", "Parmer")
parmer.setColor( hou.Color((1.0, 1.0, 0.0)) )
parmer.move((0,3))
parmerptg = parmer.parmTemplateGroup()
folder = hou.FolderParmTemplate("face", "Face")
parmerptg.addParmTemplate(folder)
#folder = hou.FolderParmTemplate("face", "Face")
parmer.setParmTemplateGroup(parmerptg)

def BuildFKControls( target, name, netparent ):
    fkcontrolname =  name + '_ctrl'
    fkautoname = name + '_auto'
    fkoffsetname = name + '_offset'

    ctrlsize = 0.01

    ctrls = []

    targetpos = target.position()
    # make offset
    fkoffset = netparent.createNode("null", fkoffsetname)
    fkoffset.setSelectableInViewport(False)
    fkoffset.parm("picking").set(0)
    fkoffset.setDisplayFlag(False)
    fkoffset.setFirstInput(target)
    fkoffset.setPosition(targetpos)
    fkoffset.move((0, -1))
    #fkoffset.moveToGoodPosition()
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
    fkauto.setPosition(targetpos)
    fkauto.move((0, -2))
    #fkauto.moveToGoodPosition()
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
    fkcontrol.setPosition(targetpos)
    fkcontrol.move((0, -3))
    #fkcontrol.moveToGoodPosition()
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
    controls = BuildFKControls(target, name, netparent)
    BuildConstraints( target, controls[2])
    return controls


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
    
    #get curves parent
    parent = sopnode.parent().parent()

    #get geometry
    geo = sopnode.geometry()

    #get point groups
    pointgroups = geo.pointGroups()

    #list to collect curves
    curvesgeonodes = []

    #iterate
    for pointgroup in pointgroups:
        # 
        geonode = parent.createNode("geo", pointgroup.name() )

        #create Folder parms
        parmgroup = geonode.parmTemplateGroup()
        parmfolder = hou.FolderParmTemplate("folder", pointgroup.name() + "Blends", folder_type = hou.folderType.Simple)

        #create parm templates
        blendparm1 = hou.FloatParmTemplate(pointgroup.name() + "_up", pointgroup.name() + "_up", 1)      
        blendparm1.setMaxValue(1)
        parmfolder.addParmTemplate(blendparm1)

        blendparm2 = hou.FloatParmTemplate(pointgroup.name() + "_down", pointgroup.name() + "_down", 1)      
        blendparm2.setMaxValue(1)
        parmfolder.addParmTemplate(blendparm2)

        blendparm3 = hou.FloatParmTemplate(pointgroup.name() + "_in", pointgroup.name() + "_in", 1)      
        blendparm3.setMaxValue(1)
        parmfolder.addParmTemplate(blendparm3)

        blendparm4 = hou.FloatParmTemplate(pointgroup.name() + "_out", pointgroup.name() + "_out", 1)      
        blendparm4.setMaxValue(1)
        parmfolder.addParmTemplate(blendparm4)

        targetfolder = ("Face",)
        
        parmgroup.append(parmfolder)
        geonode.setParmTemplateGroup(parmgroup)

        parmerptg.appendToFolder(targetfolder, parmgroup.entries()[0])
        #parmer.setParmTemplateGroup(parmerptg)


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

        destroypoints = geonode.createNode("delete", "destroy_points")
        destroypoints.setParms({"group":"*", "entity": 1})
        destroypoints.setInput(0, sort)

        centroid = geonode.createNode("add", "centroid")
        centroid.setParms({"usept0":1})
        centroid.parm("pt0x").setExpression('centroid("../'+"OUT_" + pointgroup.name() +'/",D_X)')
        centroid.parm("pt0y").setExpression('centroid("../'+"OUT_" + pointgroup.name() +'/",D_Y)')
        centroid.parm("pt0z").setExpression('centroid("../'+"OUT_" + pointgroup.name() +'/",D_Z)')
        centroid.setInput(0, destroypoints)
        centroid.moveToGoodPosition()        

        convert = geonode.createNode("convert")
        convert.setParms({"totype":4})
        convert.setInput(0, add)
        convert.moveToGoodPosition()

        edit1 = geonode.createNode("edit", pointgroup.name() + "_up")
        edit1.setInput(0, convert)

        edit2 = geonode.createNode("edit", pointgroup.name() + "_down")
        edit2.setInput(0, convert)

        edit3 = geonode.createNode("edit", pointgroup.name() + "_in")
        edit3.setInput(0, convert)

        edit4 = geonode.createNode("edit", pointgroup.name() + "_out")
        edit4.setInput(0, convert)

        blendshapes = geonode.createNode("blendshapes::2.0")
        blendshapes.setInput(0, convert)
        blendshapes.setInput(1, edit1)
        blendshapes.setInput(2, edit2)
        blendshapes.setInput(3, edit3)
        blendshapes.setInput(4, edit4)
        blendshapes.moveToGoodPosition()

        blendshapes.parm("updatechannels").pressButton()
        #blendshapes.parm("blend1").setExpression('ch("../'+ pointgroup.name() + "_up"+'")')
        blendshapes.parm("blend1").setExpression('ch("../../Parmer/'+ pointgroup.name() + "_up"+'")')
        blendshapes.parm("blend2").setExpression('ch("../../Parmer/'+ pointgroup.name() + "_down"+'")')
        blendshapes.parm("blend3").setExpression('ch("../../Parmer/'+ pointgroup.name() + "_in"+'")')
        blendshapes.parm("blend4").setExpression('ch("../../Parmer/'+ pointgroup.name() + "_out"+'")')

        null = geonode.createNode("null", "OUT_" + pointgroup.name())
        null.setColor( hou.Color((1.0, 1.0, 1.0)) )
        null.setInput(0, blendshapes)
        null.moveToGoodPosition()
        null.setRenderFlag(1)
        null.setDisplayFlag(1)
        
        curvesgeonodes.append(geonode)

    return curvesgeonodes

def BuildCurveControl(numberOfBones, curve, name, iterator):

    #build curve
    parent = curve.parent().parent()
    #create master
    master = parent.createNode("null", name + "_Master")
    master.setColor( hou.Color((0.0,0.0,0.0)) )
    master.setParms({ "keeppos" : 1 })
    master.move((0, iterator))
    controllers = []

    #curve.setPosition(master.position())
    #curve.move((2, 0))

    #attach null path cns @ 0, 0.5, 1    LookAt None
    xoffset = 0
    for x in range(1,numberOfBones):
        controller = parent.createNode("null", name + "_controller_"+ str(0))
        controller.setPosition(master.position())
        controller.move((xoffset,-1))
        controllers.append(controller)
        xoffset += 3

    position = 0.0
    position += (1.0/numberOfBones)

    xoffset = 0
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

        constraintparent = chopnet.createNode("constraintgetparentspace")
        constraintparent.setParms({"obj_path":"../.."})

        constraintobject = chopnet.createNode("constraintobjectoffset")
        constraintobject.setParms({"obj_path":constraintobject.relativePathTo(curve.parent()) })
        constraintobject.setInput(0, constraintparent)

        simpleblend = chopnet.createNode("constraintsimpleblend")
        simpleblend.setParms({"blend":1 })
        simpleblend.setInput(0, constraintparent)
        simpleblend.setInput(1, constraintobject)

        constraintparentx = chopnet.createNode("constraintparentx")
        constraintparentx.setInput(0, constraintpath)
        constraintparentx.setInput(1, constraintparent)
        constraintparentx.setInput(2, simpleblend)

        constraintparentx.setAudioFlag(1)

        #child  null to master
        #controller.setInput(0, master)

        #create bone
        bone = parent.createNode("bone", name + "_bone_" + str(0) )
        bone.setParms({"length":0.01})
        bone.setPosition(controller.position())
        bone.move((xoffset,-1))

        #child  bone to null
        bone.setInput(0, controller)

        #create bone controller
        animContollers = BuildAnimRig(bone, bone.name(), parent)

        #child controller to null
        animContollers[0].setInput(0, controller)

    return master

def Main():
    # select point cloud to begin building rig . . . 

    #FacePointCloudBuildBones()


    
    facecurves = BuildCurves()
    #print facecurves

    iterator = 0

    for facecurve in facecurves:
        for child in facecurve.children():
            if child.color() == hou.Color((1.0,1.0,1.0)):
                master = BuildCurveControl( 6, child, facecurve.name(), iterator )
                facecurve.setInput(0, master)
                facecurve.setPosition(master.position())
                facecurve.move((3,0))
                iterator -= 7
            # if child.name() == "centroid":

            #     geo = child.geometry()
            #     point = geo.points()[0]
            #     pos = point.attribValue("P")

            #     root = child.parent().parent()
            #     driver = root.createNode("null", "driver")
            #     driver.setParms({"tx":pos[0], "ty":pos[1], "tz":pos[2]})
            #     driver.setColor ( hou.Color ((1.0, 0.0, 0.0)) )
            #     driver.setParms({
            #         "keeppos": 1,
            #         "dcolorr": 1,
            #         "dcolorg": 0,
            #         "dcolorb": 0,
            #         "geoscale": 0.02,
            #         "geocenterz":0.01,
            #         "controltype":1,
            #         "orientation":3
            #     })
            #     driver.setInput(0, node)
            #     driver.moveParmTransformIntoPreTransform()

    # for facecurve in facecurves:
    #     print facecurve.name()


    # # Build parm holder
    # root = facecurves[0].parent()
    # parmer = root.createNode("null", "Parmer")
    # parmer.setColor( hou.Color((1.0, 1.0, 0.0)) )
    # parmerptg = parmer.parmTemplateGroup()
    # folder = hou.FolderParmTemplate("face", "Face")
    # parmerptg.addParmTemplate(folder)
    # parmer.setParmTemplateGroup(parmerptg)

    # targetfolder = ("Face",)
    # for node in facecurves:
    #     ptg = node.parmTemplateGroup()
    #     parmerptg.appendToFolder(targetfolder, ptg.entries()[4])
    #     parmer.setParmTemplateGroup(parmerptg)


    
    #parmer = hou.node('/obj/subnet5/Parmer')
    #pptg = parmer.parmTemplateGroup()
    #pptg.appendToFolder(targetFolder, ptg.entries()[4])
    #parmer.setParmTemplateGroup(pptg)

    #parmer.setParms({ "" :  })



Main()