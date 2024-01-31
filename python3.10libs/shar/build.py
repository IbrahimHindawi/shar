'''
this module is responsible for building limbs

'''

import hou
from shar import *
# from shar import shape

def searchForNodeByName(rig, name):
    for item in rig.children():
        if item.name() == name:
            return item
    print("ERROR::" + name + " not found!!!")

def getBoneLength(bone):
    bone_length = bone.parm('length').eval()
    return bone_length

def initializeNodeGroups(rig):
    ngGeom = rig.addNodeGroup("geom")
    ngHelp = rig.addNodeGroup("help")
    ngCtrl = rig.addNodeGroup("ctrl")
    ngBone = rig.addNodeGroup("bone")
    return [ngGeom, ngHelp, ngCtrl, ngBone]

def initialize(rig):
    nodegroups = initializeNodeGroups(rig)
    ngGeom = nodegroups[0]
    ngHelp = nodegroups[1]
    ngCtrl = nodegroups[2]
    ngBone = nodegroups[3]

    shar.parameter.lockAndHideOldParameters(rig)
    shar.parameter.initializeParameterInterface(rig)

    for node in rig.children():
        if node.type().name() == "bone":
            ngBone.addNode(node)
            shar.parameter.setupDisplay(node, 'b')
        elif node.type().name() == "geo":
            ngGeom.addNode(node)
            shar.parameter.setupDisplay(node, 'g')
        elif node.name() == "root":
            ngBone.addNode(node)
            shar.parameter.setupDisplay(node, 'b')
    createRoot(rig)

def createRoot(rig):
    ptg = rig.parmTemplateGroup()
    folder = hou.FolderParmTemplate('folder', 'root')        

    folder.addParmTemplate(hou.FloatParmTemplate('roott', 'Root Trans', 3))
    folder.addParmTemplate(hou.FloatParmTemplate('rootr', 'Root Rot', 3))
    folder.addParmTemplate(hou.FloatParmTemplate('roots', 'Root Scale', 3, default_value=(1.0, 1.0, 1.0)))

    rootnode = None
    for node in rig.children():
        if node.name() == "root":
            rootnode = node
    if rootnode == None:
        print('Root node not found! Halting execution.')
        exit()

    rootnode.parm('tx').setExpression('ch("../' + "roott" + 'x' + '")')
    rootnode.parm('ty').setExpression('ch("../' + "roott" + 'y' + '")')
    rootnode.parm('tz').setExpression('ch("../' + "roott" + 'z' + '")')
    rootnode.parm('rx').setExpression('ch("../' + "rootr" + 'x' + '")')
    rootnode.parm('ry').setExpression('ch("../' + "rootr" + 'y' + '")')
    rootnode.parm('rz').setExpression('ch("../' + "rootr" + 'z' + '")')
    rootnode.parm('sx').setExpression('ch("../' + "roots" + 'x' + '")')
    rootnode.parm('sy').setExpression('ch("../' + "roots" + 'y' + '")')
    rootnode.parm('sz').setExpression('ch("../' + "roots" + 'z' + '")')

    shar.parameter.addFolderToAnim(ptg, folder)
    rig.setParmTemplateGroup(ptg)

def createSpine(rig, spine_nodes):

    nodeGroupCtrl = shar.nodegroups.getNodeGroupByName(rig, "ctrl")
    nodeGroupHelp = shar.nodegroups.getNodeGroupByName(rig, "help")

    first_spine = spine_nodes[0]
    second_spine = spine_nodes[1]
    third_spine = spine_nodes[2]
    fourth_spine = spine_nodes[3]
    fifth_spine = spine_nodes[4]
    root = searchForNodeByName( rig, "root")
        
    body_part_name = 'Spine'

    # Get rig's PTG
    ptg = rig.parmTemplateGroup()

    # create a folder template
    folder = hou.FolderParmTemplate('folder', body_part_name)        

    # Create cog
    cog = rig.createNode('null', 'cog_ctrl')
    nodeGroupCtrl.addNode(cog)
    targetPosition = second_spine.position()
    cog.move(hou.Vector2(targetPosition.x()+2, targetPosition.y()))
    cog.setParms({'controltype':1, 'orientation': 2})
    shar.control.setupNodeDisplayColor(cog, shar.color.red)
    shar.parameter.setupDisplay(cog, 'c')
    #cog.setParms({'tx':})
    cog.setInput(0, second_spine)
    second_spine_length = getBoneLength(second_spine)
    cog.setParms({'tz':second_spine_length/2})
    cog.parm('keeppos').set(True)
    cog.setInput(0, None)
    cog.setParms({'rx':0, 'ry':0, 'rz':0})
    cog.moveParmTransformIntoPreTransform()
    
    # Build CVs
    spine_hip_cv = rig.createNode('pathcv', 'spine_hip_cv')
    nodeGroupHelp.addNode(spine_hip_cv)
    spine_hip_cv.move(hou.Vector2(cog.position().x()+2, cog.position().y()-6))
    spine_hip_cv.setParms({'sz':0.06})
    spine_hip_cv.setInput(0, first_spine)
    spine_hip_cv.parm('keeppos').set(True)
    spine_hip_cv.setInput(0, None)
    spine_hip_cv.moveParmTransformIntoPreTransform()
    shar.parameter.setupDisplay(spine_hip_cv, 'c')

    spine_mid_cv = rig.createNode('pathcv', 'spine_mid_cv')
    nodeGroupHelp.addNode(spine_mid_cv)
    spine_mid_cv.move(hou.Vector2(cog.position().x()+4, cog.position().y()-8))
    spine_mid_cv.setParms({'sz':0.06})
    spine_mid_cv.setInput(0, fourth_spine)
    spine_mid_cv.parm('keeppos').set(True)
    spine_mid_cv.setInput(0, None)
    spine_mid_cv.moveParmTransformIntoPreTransform()
    shar.parameter.setupDisplay(spine_mid_cv, 'c')


    spine_chest_cv = rig.createNode('pathcv', 'spine_chest_cv')
    nodeGroupHelp.addNode(spine_chest_cv)
    spine_chest_cv.move(hou.Vector2(cog.position().x()+6, cog.position().y()-10))
    spine_chest_cv.setParms({'sz':0.06})
    spine_chest_cv.setInput(0, fifth_spine)
    fifth_spine_length = getBoneLength(fifth_spine)
    spine_chest_cv.setParms({'tz':-fifth_spine_length})
    spine_chest_cv.parm('keeppos').set(True)
    spine_chest_cv.setInput(0, None)
    spine_chest_cv.moveParmTransformIntoPreTransform()
    shar.parameter.setupDisplay(spine_mid_cv, 'c')

    # Build Path
    spine_path = rig.createNode('path', 'spine_path')
    spine_path.parm("tdisplay").set(True)
    spine_path.parm("display").setExpression('0')
    nodeGroupHelp.addNode(spine_path)
    for node in spine_path.children():
        if node.name() == 'points_merge':
            node.parm('numobj').set(3)
            node.setParms({
                'objpath1' : node.relativePathTo(spine_hip_cv) + '/points/',
                'objpath2' : node.relativePathTo(spine_mid_cv) + '/points/',
                'objpath3' : node.relativePathTo(spine_chest_cv) + '/points/'
                })
        if node.name() == "delete_endpoints":
            delete_mid = spine_path.createNode('delete', 'delete_mid_points')
            points_merge = node.inputs()[0]
            connect_points = node.outputs()[0]
            delete_mid.setParms({
                'group': '4 2',
                'entity' : 1
                })
            delete_mid.setInput(0, node)
            connect_points.setInput(0, delete_mid)
        if node.name() == 'output_curve':
            node.setParms({'totype':4})

    # Build IK shar.controls
    BaseIk = rig.createNode('null', 'Base_Ik_ctrl')
    nodeGroupCtrl.addNode(BaseIk)
    BaseIk.move(hou.Vector2(cog.position().x()+2, cog.position().y()-4))
    shar.parameter.setupDisplay(BaseIk, 'c')

    midIk = rig.createNode('null', 'Mid_Ik_ctrl')
    nodeGroupCtrl.addNode(midIk)
    midIk.move(hou.Vector2(cog.position().x()+4, cog.position().y()-6))
    shar.parameter.setupDisplay(midIk, 'c')

    chestIk = rig.createNode('null', 'Chest_Ik_ctrl')
    nodeGroupCtrl.addNode(chestIk)
    chestIk.move(hou.Vector2(cog.position().x()+6, cog.position().y()-8))
    shar.parameter.setupDisplay(chestIk, 'c')

    BaseIk.setInput(0, first_spine)
    BaseIk.parm('keeppos').set(True)
    BaseIk.setInput(0, None)
    BaseIk.setParms({'rx':0, 'ry':0, 'rz':0})
    BaseIk.setParms({
        'controltype':2,
        'geosizex': 0.5,
        'geosizey': 0.1,
        'geosizez':0.5
        })
    #BaseIk.setParms
    BaseIk.moveParmTransformIntoPreTransform()

    midIk.setInput(0, fourth_spine)
    midIk.parm('keeppos').set(True)
    midIk.setInput(0, None)
    midIk.setParms({'rx':0, 'ry':0, 'rz':0})
    midIk.setParms({
        'controltype':2,
        'geosizex': 0.5,
        'geosizey': 0.1,
        'geosizez':0.5
        })
    midIk.moveParmTransformIntoPreTransform()

    chestIk.setInput(0, fifth_spine)
    chestIk.parm('keeppos').set(True)
    chestIk.setParms({'tz':-fifth_spine_length})
    chestIk.setInput(0, None)
    chestIk.setParms({'rx':0, 'ry':0, 'rz':0})
    chestIk.setParms({
        'controltype':2,
        'geosizex': 0.5,
        'geosizey': 0.1,
        'geosizez':0.5
        })
    chestIk.moveParmTransformIntoPreTransform()

    spine_hip_cv.setInput(0, BaseIk)
    spine_hip_cv.setDisplayFlag(0)

    spine_mid_cv.setInput(0, midIk)
    spine_mid_cv.setDisplayFlag(0)

    spine_chest_cv.setInput(0, chestIk)
    spine_chest_cv.setDisplayFlag(0)

    kin = shar.constrain.kinCheck( rig, first_spine)
    spine_kin = kin.createNode('inversekin', 'spinekin')
    spine_kin.setParms({
        'solvertype': 4,
        'bonerootpath':spine_kin.relativePathTo(first_spine),
        'boneendpath':spine_kin.relativePathTo(fifth_spine),
        'curvepath':spine_kin.relativePathTo(spine_path)
        })

    for spine in spine_nodes:
        spine.setParms({'solver': spine.relativePathTo(spine_kin)})

    # Build FK shar.controls
    targetPosition = cog.position()
    spine_A_Fk = rig.createNode('null', 'spine_A_Fk_ctrl')
    nodeGroupCtrl.addNode(spine_A_Fk)
    spine_A_Fk.move(hou.Vector2(targetPosition.x()+2, targetPosition.y()-2))
    shar.parameter.setupDisplay(spine_A_Fk, 'c')

    spine_B_Fk = rig.createNode('null', 'spine_B_Fk_ctrl')
    nodeGroupCtrl.addNode(spine_B_Fk)
    spine_B_Fk.move(hou.Vector2(targetPosition.x()+4, targetPosition.y()-4))
    shar.parameter.setupDisplay(spine_B_Fk, 'c')

    spine_C_Fk = rig.createNode('null', 'spine_C_Fk_ctrl')
    nodeGroupCtrl.addNode(spine_C_Fk)
    spine_C_Fk.move(hou.Vector2(targetPosition.x()+6, targetPosition.y()-6))
    shar.parameter.setupDisplay(spine_C_Fk, 'c')

    spine_A_Fk.setInput(0, first_spine)
    spine_A_Fk.parm('keeppos').set(True)
    spine_A_Fk.setInput(0, None)
    spine_A_Fk.setParms({'rx':0, 'ry':0, 'rz':0})
    spine_A_Fk.setParms({
        'controltype':1,
        'geosizex': 1,
        'geosizey': 1,
        'geosizez':1,
        'orientation': 2
        })
    #spine_A_Fk.setParms
    spine_A_Fk.moveParmTransformIntoPreTransform()

    spine_B_Fk.setInput(0, third_spine)
    spine_B_Fk.parm('keeppos').set(True)
    spine_B_Fk.setInput(0, None)
    spine_B_Fk.setParms({'rx':0, 'ry':0, 'rz':0})
    spine_B_Fk.setParms({
        'controltype':1,
        'geosizex': 1,
        'geosizey': 1,
        'geosizez':1,
        'orientation': 2
        })
    spine_B_Fk.moveParmTransformIntoPreTransform()

    spine_C_Fk.setInput(0, fourth_spine)
    spine_C_Fk.parm('keeppos').set(True)
    spine_C_Fk.setParms({'tz':-fifth_spine_length})
    spine_C_Fk.setInput(0, None)
    spine_C_Fk.setParms({'rx':0, 'ry':0, 'rz':0})
    spine_C_Fk.setParms({
        'controltype':1,
        'geosizex': 1,
        'geosizey': 1,
        'geosizez':1,
        'orientation': 2
        })
    spine_C_Fk.moveParmTransformIntoPreTransform()


    # Parent hierarchy
    cog.setInput(0, root)
    spine_A_Fk.setInput(0, cog)
    spine_B_Fk.setInput(0, spine_A_Fk)
    spine_C_Fk.setInput(0, spine_B_Fk)

    BaseIk.setInput(0, spine_A_Fk)
    midIk.setInput(0, spine_B_Fk)
    chestIk.setInput(0, spine_C_Fk)

    cog.moveParmTransformIntoPreTransform()
    spine_A_Fk.moveParmTransformIntoPreTransform()
    spine_B_Fk.moveParmTransformIntoPreTransform()
    spine_C_Fk.moveParmTransformIntoPreTransform()
    BaseIk.moveParmTransformIntoPreTransform()
    midIk.moveParmTransformIntoPreTransform()
    chestIk.moveParmTransformIntoPreTransform()

    paramNames = shar.parameter.makeParameterNames(cog, 'Rot')
    shar.parameter.setControllerExpressions(cog, paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(cog, paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(cog, paramNames[0], 'r', 'z')
    cogrparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(cogrparm)
    paramNames = shar.parameter.makeParameterNames(cog, 'Trans')
    shar.parameter.setControllerExpressions(cog, paramNames[0], 't', 'x')
    shar.parameter.setControllerExpressions(cog, paramNames[0], 't', 'y')
    shar.parameter.setControllerExpressions(cog, paramNames[0], 't', 'z')
    cogtparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(cogtparm)

    paramNames = shar.parameter.makeParameterNames(spine_A_Fk, 'Rot')
    shar.parameter.setControllerExpressions(spine_A_Fk, paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(spine_A_Fk, paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(spine_A_Fk, paramNames[0], 'r', 'z')
    spineAparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(spineAparm)

    paramNames = shar.parameter.makeParameterNames(spine_B_Fk, 'Rot')
    shar.parameter.setControllerExpressions(spine_B_Fk, paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(spine_B_Fk, paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(spine_B_Fk, paramNames[0], 'r', 'z')
    spineBparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(spineBparm)

    paramNames = shar.parameter.makeParameterNames(spine_C_Fk, 'Rot')
    shar.parameter.setControllerExpressions(spine_C_Fk, paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(spine_C_Fk, paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(spine_C_Fk, paramNames[0], 'r', 'z')
    spineCparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(spineCparm)

    paramNames = shar.parameter.makeParameterNames(BaseIk, 'Rot')
    shar.parameter.setControllerExpressions(BaseIk, paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(BaseIk, paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(BaseIk, paramNames[0], 'r', 'z')
    hipIkrparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(hipIkrparm)
    paramNames = shar.parameter.makeParameterNames(BaseIk, 'Trans')
    shar.parameter.setControllerExpressions(BaseIk, paramNames[0], 't', 'x')
    shar.parameter.setControllerExpressions(BaseIk, paramNames[0], 't', 'y')
    shar.parameter.setControllerExpressions(BaseIk, paramNames[0], 't', 'z')
    hipIktparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(hipIktparm)

    paramNames = shar.parameter.makeParameterNames(midIk, 'Rot')
    shar.parameter.setControllerExpressions(midIk, paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(midIk, paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(midIk, paramNames[0], 'r', 'z')
    midIkrparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(midIkrparm)
    paramNames = shar.parameter.makeParameterNames(midIk, 'Trans')
    shar.parameter.setControllerExpressions(midIk, paramNames[0], 't', 'x')
    shar.parameter.setControllerExpressions(midIk, paramNames[0], 't', 'y')
    shar.parameter.setControllerExpressions(midIk, paramNames[0], 't', 'z')
    midIktparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(midIktparm)

    paramNames = shar.parameter.makeParameterNames(chestIk, 'Rot')
    shar.parameter.setControllerExpressions(chestIk, paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(chestIk, paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(chestIk, paramNames[0], 'r', 'z')
    chestIkrparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(chestIkrparm)
    paramNames = shar.parameter.makeParameterNames(chestIk, 'Trans')
    shar.parameter.setControllerExpressions(chestIk, paramNames[0], 't', 'x')
    shar.parameter.setControllerExpressions(chestIk, paramNames[0], 't', 'y')
    shar.parameter.setControllerExpressions(chestIk, paramNames[0], 't', 'z')
    chestIktparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(chestIktparm)        

    hipCtrls = createHip(rig, [searchForNodeByName(rig, "hip_bone0")])
    paramNames = shar.parameter.makeParameterNames(hipCtrls[2], 'Rot')
    shar.parameter.setControllerExpressions(hipCtrls[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(hipCtrls[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(hipCtrls[2], paramNames[0], 'r', 'z')
    Hiprparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(Hiprparm)        

#    mainfolder = ptg.findFolder('Main')
#    # print(mainfolder)
#    mpt = mainfolder.parmTemplates()
#    animfolder = None
#    for pt in mpt:
#        if "Anim" in pt.label():
#            animfolder = pt
#    if animfolder == None:
#        print("animfolder not found!")
#        exit()
#    # ptg.appendToFolder(folder, mainfolder)
#    ptg.appendToFolder(animfolder, folder)

    shar.parameter.addFolderToAnim(ptg, folder)
    rig.setParmTemplateGroup(ptg)

def createHip(rig, hip_nodes):
    hip = hip_nodes[0]
    shar.parameter.setupDisplay(hip, 'b')

    #hipCtrls = self.CreateFkControlsWithConstraintsSimple( hip, hip.name() )
    hipCtrls = shar.control.MakeControlFk(rig, hip, hip.name(), ctrlSize = 0.5)
    # shar.parameter.setupDisplay(hipCtrls, 'c')
    shar.constrain.MakeFKConstraints(rig, hip, hipCtrls[2])

    cog =  searchForNodeByName(rig, "cog_ctrl")

    hipCtrls[0].setInput(0, cog )

    return hipCtrls

def createArm( rig, arm_nodes, body_part_name, ctrlColor):
    shoulder = arm_nodes[0]
    bicep    = arm_nodes[1]
    forearm  = arm_nodes[2]
    hand     = arm_nodes[3]
    twist    = arm_nodes[4]

    if shoulder.name()[0] == 'L':
        body_part_name = 'L_' + body_part_name
    elif shoulder.name()[0] == 'R':
        body_part_name = 'R_' + body_part_name

    body_part_name += shoulder.name()[-1]        


    # Get rig's PTG
    ptg = rig.parmTemplateGroup()

    # create a folder template
    folder = hou.FolderParmTemplate('folder', body_part_name)
    #paramNames = self.parmt.makeParameterNames(body_part_name, 'IkFk')
    parm = hou.FloatParmTemplate(body_part_name + "_ikfk", body_part_name[2:-1] + " IkFk", 1)

    parm.setMaxValue(1)

    # add a shar.parameter template to the folder template
    folder.addParmTemplate(parm)

    #parm = self.parmt.MakeParameter(body_part_name)


    shoulderCtrl = shar.control.MakeControlFk(rig, shoulder, shoulder.name(), ctrlColor = ctrlColor, ctrlSize = 0.5, parm = parm)
    shar.constrain.MakeFKConstraints(rig, shoulder, shoulderCtrl[2], parm = parm)
    paramNames = shar.parameter.makeParameterNames(shoulder, 'Rot')
    shar.parameter.setControllerExpressions(shoulderCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(shoulderCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(shoulderCtrl[2], paramNames[0], 'r', 'z')
    sparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(sparm)


    bicepCtrl = shar.control.MakeControlFk(rig, bicep, bicep.name(), ctrlColor = ctrlColor, ctrlSize = 0.5, parm = parm)
    shar.constrain.MakeFKConstraints(rig, bicep, bicepCtrl[2], parm = parm)
    paramNames = shar.parameter.makeParameterNames(bicep, 'Rot')
    shar.parameter.setControllerExpressions(bicepCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(bicepCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(bicepCtrl[2], paramNames[0], 'r', 'z')
    bparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(bparm)

    forearmCtrl = shar.control.MakeControlFk(rig, forearm, forearm.name(), ctrlColor = ctrlColor, ctrlSize = 0.5, parm = parm)
    shar.constrain.MakeFKConstraints(rig, forearm, forearmCtrl[2], parm = parm)
    paramNames = shar.parameter.makeParameterNames(forearm, 'Rot')
    shar.parameter.setControllerExpressions(forearmCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(forearmCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(forearmCtrl[2], paramNames[0], 'r', 'z')
    fparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(fparm)

    handCtrl = shar.control.MakeControlFk(rig, hand, hand.name(), ctrlColor = ctrlColor, ctrlSize = 0.5, parm = parm)
    shar.parameter.setRotExpressions(handCtrl[2], hand)
    paramNames = shar.parameter.makeParameterNames(hand, 'Rot')
    shar.parameter.setControllerExpressions(handCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(handCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(handCtrl[2], paramNames[0], 'r', 'z')
    hparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(hparm)
    
    ik = shar.control.MakeIkObjects2(rig, bicep, parm, twist)
    shar.constrain.MakeIkConstraints(rig, bicep, ik[0], ik[1], parm)

    goalCtrl = shar.control.MakeControlIk(rig, ik[0], ik[0].name(), searchForNodeByName(rig, "root"),  ctrlColor = ctrlColor, ctrlSize = 0.5, parm = parm)

    twistCtrl = shar.control.MakeControlIk(rig, ik[1], ik[1].name(), searchForNodeByName(rig, "root"), ctrlColor = ctrlColor, ctrlSize = 0.5, parm = parm)

    shar.constrain.MakeComplexConstraint(rig, hand, handCtrl[2], ik[0], parm)

    paramNames = shar.parameter.makeParameterNames(hand, 'goal_Trans')
    shar.parameter.setControllerExpressions(goalCtrl[2], paramNames[0], 't', 'x')
    shar.parameter.setControllerExpressions(goalCtrl[2], paramNames[0], 't', 'y')
    shar.parameter.setControllerExpressions(goalCtrl[2], paramNames[0], 't', 'z')
    gtparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(gtparm)

    paramNames = shar.parameter.makeParameterNames(hand, 'goal_Rot')
    shar.parameter.setControllerExpressions(goalCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(goalCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(goalCtrl[2], paramNames[0], 'r', 'z')
    grparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(grparm)

    paramNames = shar.parameter.makeParameterNames(hand, 'twist_Trans')
    shar.parameter.setControllerExpressions(twistCtrl[2], paramNames[0], 't', 'x')
    shar.parameter.setControllerExpressions(twistCtrl[2], paramNames[0], 't', 'y')
    shar.parameter.setControllerExpressions(twistCtrl[2], paramNames[0], 't', 'z')
    tparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(tparm)


    # append folder to node's parm template group
    # ptg.append(folder)
    shar.parameter.addFolderToAnim(ptg, folder)

    # set templates to node
    rig.setParmTemplateGroup(ptg)


    # fingerRoots = self.ana.getChildren(hand)
    # for root in fingerRoots:
    #     chain = [root]
    #     self.ana.walkBones(root, chain, 3)
    #     self.createFinger(chain)

def createFingers( rig, hand, parmName, ctrlColor ):
    ptg = rig.parmTemplateGroup()
    handName = hand.name().replace("_bone", "")
    folder = hou.FolderParmTemplate('folder', handName)
    # ptg.append(folder)
    # rig.setParmTemplateGroup(ptg)

    fingerRoots = shar.analysis.getChildren( hand )
    fingerChains = []
    for fingerRoot in fingerRoots:
        # ptg = rig.parmTemplateGroup()
        # fingerFolder = hou.FolderParmTemplate('folder', fingerRoot.name())
        # handFolder = ptg.findFolder(handName)

        # ptg.appendToFolder(handFolder, fingerFolder)
        # rig.setParmTemplateGroup( ptg )

        boneChain = [fingerRoot]
        shar.analysis.walkBones(fingerRoot, boneChain, 3)
        fingerChains.append(boneChain)

    for fingerChain in fingerChains:
        for fingerBone in fingerChain:
            fk = shar.control.MakeControlFk(rig, fingerBone, fingerBone.name(), ctrlColor = ctrlColor, ctrlSize = 0.1, parm = None)
            # shar.parameter.setupDisplay(fk, 'c')
            shar.constrain.MakeFKConstraints(rig, fingerBone, fk[2], parm = None)

            paramNames = shar.parameter.makeParameterNames(fingerBone, 'Rot')
            shar.parameter.setControllerExpressions(fk[2], paramNames[0], 'r', 'x')
            shar.parameter.setControllerExpressions(fk[2], paramNames[0], 'r', 'y')
            shar.parameter.setControllerExpressions(fk[2], paramNames[0], 'r', 'z')
            # print(paramNames[0])
            # print(paramNames[1])
            fparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
            folder.addParmTemplate(fparm)

            # rig.setParmTemplateGroup(ptg)
    # ptg.append(folder)
    shar.parameter.addFolderToAnim(ptg, folder)
    rig.setParmTemplateGroup(ptg)

            # ptg = rig.parmTemplateGroup()
            # handFolder = ptg.findFolder(handName)
            # handFolderPT = handFolder.parmTemplates()

            # for folder in handFolderPT:
            #     if fingerBone.name()[0:-1] in folder.label():
            #         # print(fingerBone.name() + ":" + folder.label())
            #         handFolder = ptg.findFolder(handName)
            #         folder.addParmTemplate(fparm)
            #         #ptg.appendToFolder(handFolder, folder)
            #         rig.setParmTemplateGroup(ptg)

def createFinger( rig, finger_nodes ):
    for finger_bone in finger_nodes:
        fk = shar.control.MakeControlFk(rig, finger_bone, finger_bone.name(), ctrlSize = 0.1, parm = None)
        shar.constrain.MakeFKConstraints(rig, finger_bone, fk[2], parm = None)
    
def createLeg( rig, leg_nodes, body_part_name, ctrlColor):

    nodeGroupHelp = shar.nodegroups.getNodeGroupByName(rig, "help")

    thigh = leg_nodes[0]
    shin = leg_nodes[1]
    foot = leg_nodes[2]
    toe = leg_nodes[3]
    twist = leg_nodes[4]


    if thigh.name()[0] == 'L':
        body_part_name = 'L_' + body_part_name
    elif thigh.name()[0] == 'R':
        body_part_name = 'R_' + body_part_name

    body_part_name += thigh.name()[-1]        

    # Get rig's PTG
    ptg = rig.parmTemplateGroup()

    # create a folder template
    folder = hou.FolderParmTemplate('folder', body_part_name)

    parm = hou.FloatParmTemplate(body_part_name + "_ikfk", body_part_name[2:-1] + " IkFk", 1)

    parm.setMaxValue(1)

    # add a shar.parameter template to the folder template
    folder.addParmTemplate(parm)

    # FK

    thighCtrl = shar.control.MakeControlFk(rig, thigh, thigh.name(), ctrlColor = ctrlColor, ctrlSize = 0.5, parm = parm)
    shar.constrain.MakeFKConstraints(rig, thigh, thighCtrl[2], parm = parm)
    paramNames = shar.parameter.makeParameterNames(thigh, 'Rot')
    shar.parameter.setControllerExpressions(thighCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(thighCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(thighCtrl[2], paramNames[0], 'r', 'z')
    tparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(tparm)
    
    shinCtrl = shar.control.MakeControlFk(rig, shin, shin.name(), ctrlColor = ctrlColor, ctrlSize = 0.5, parm = parm)
    shar.constrain.MakeFKConstraints(rig, shin, shinCtrl[2], parm = parm)
    paramNames = shar.parameter.makeParameterNames(shin, 'Rot')
    shar.parameter.setControllerExpressions(shinCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(shinCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(shinCtrl[2], paramNames[0], 'r', 'z')
    sparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(sparm)
    
    footCtrl = shar.control.MakeControlFk(rig, foot, foot.name(), ctrlColor = ctrlColor, ctrlSize = 0.5, parm = parm)
    shar.constrain.MakeFKConstraints(rig, foot, footCtrl[2], parm = parm)
    paramNames = shar.parameter.makeParameterNames(foot, 'Rot')
    shar.parameter.setControllerExpressions(footCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(footCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(footCtrl[2], paramNames[0], 'r', 'z')
    fparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(fparm)
    
    toeCtrl = shar.control.MakeControlFk(rig, toe, toe.name(), ctrlColor = ctrlColor, ctrlSize = 0.5, parm = parm)
    shar.constrain.MakeFKConstraints(rig, toe, toeCtrl[2], parm = parm)
    paramNames = shar.parameter.makeParameterNames(toe, 'Rot')
    shar.parameter.setControllerExpressions(toeCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(toeCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(toeCtrl[2], paramNames[0], 'r', 'z')
    toparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(toparm)

    # IK

    #ik = shar.control.MakeIkObjects(thigh, parm, -twist_local_offset)
    ik = shar.control.MakeIkObjects2(rig, thigh, parm, twist)
    shar.constrain.MakeIkConstraints(rig, thigh, ik[0], ik[1], parm)

    ikGoalCtrl = shar.control.MakeControlIk(rig, ik[0], ik[0].name(), searchForNodeByName(rig, "root"), ctrlColor = ctrlColor, ctrlSize = 0.5, parm = parm)
    paramNames = shar.parameter.makeParameterNames(thigh, 'Goal_Trans')
    shar.parameter.setControllerExpressions(ikGoalCtrl[2], paramNames[0], 't', 'x')
    shar.parameter.setControllerExpressions(ikGoalCtrl[2], paramNames[0], 't', 'y')
    shar.parameter.setControllerExpressions(ikGoalCtrl[2], paramNames[0], 't', 'z')
    gtparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(gtparm)
    paramNames = shar.parameter.makeParameterNames(thigh, 'Goal_Rot')
    shar.parameter.setControllerExpressions(ikGoalCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(ikGoalCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(ikGoalCtrl[2], paramNames[0], 'r', 'z')
    grparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(grparm)

    ikTwistCtrl = shar.control.MakeControlIk(rig, ik[1], ik[1].name(), searchForNodeByName(rig, "root"), ctrlColor = ctrlColor, ctrlSize = 0.5, parm = parm)
    paramNames = shar.parameter.makeParameterNames(thigh, 'Twist_Trans')
    shar.parameter.setControllerExpressions(ikTwistCtrl[2], paramNames[0], 't', 'x')
    shar.parameter.setControllerExpressions(ikTwistCtrl[2], paramNames[0], 't', 'y')
    shar.parameter.setControllerExpressions(ikTwistCtrl[2], paramNames[0], 't', 'z')
    ttparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(ttparm)        

    #shar.constrain.MakeComplexConstraint(foot, footCtrl[2], ik[0], parm)
    twist_local_offset = 0.5
    footIkCtrl = shar.control.MakeIkSelfObjects(rig, foot, parm, -twist_local_offset)
    shar.constrain.MakeIkSelfConstraint(rig, foot, footIkCtrl[0], footIkCtrl[1], parm)
    
    toeIkCtrl = shar.control.MakeIkSelfObjects(rig, toe, parm, -twist_local_offset)
    shar.constrain.MakeIkSelfConstraint(rig, toe, toeIkCtrl[0], toeIkCtrl[1], parm)
    
    thighGoal = ik[0]
    thighGoalCtrl = ikGoalCtrl[2]
    footGoal = footIkCtrl[0]
    footTwist = footIkCtrl[1]
    toeGoal = toeIkCtrl[0]
    toeTwist = toeIkCtrl[1]

    nodeGroupHelp.addNode(footGoal)
    nodeGroupHelp.addNode(footTwist)
    nodeGroupHelp.addNode(toeGoal)
    nodeGroupHelp.addNode(toeTwist)

    thighGoal.setInput(0, None)
    toeGoal.setInput(0, thighGoalCtrl)
    footGoal.setInput(0, toeGoal)
    thighGoal.setInput(0, footGoal)
    toeTwist.setInput(0, footGoal)
    footTwist.setInput(0, thighGoal)

    heelRotCtrl = shar.control.MakeCtrl(rig, thighGoal, body_part_name + '_heelRot_ctrl' , ctrlColor = ctrlColor, ctrlSize = 0.1, parm = parm, flip = True)  
    heelRotCtrl.setInput(0, None)
    heelRotCtrl.setParms({'ty':0, 'tz': -0.2})
    toeGoal.setInput(0, None)
    toeGoal.setInput(0, heelRotCtrl)
    heelRotCtrl.setInput(0, thighGoalCtrl)
    heelRotCtrl.moveParmTransformIntoPreTransform()
    paramNames = shar.parameter.makeParameterNames(foot, 'Foot_Rot')
    shar.parameter.setControllerExpressions(heelRotCtrl, paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(heelRotCtrl, paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(heelRotCtrl, paramNames[0], 'r', 'z')
    hrparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(hrparm)   

    toeRotCtrl = shar.control.MakeCtrl(rig, toeGoal, body_part_name + '_toeRot_ctrl', ctrlColor = ctrlColor, ctrlSize = 0.1, parm = parm, flip = True)
    toeRotCtrl.setInput(0, None)
    toeGoal.setInput(0, toeRotCtrl)
    toeRotCtrl.setInput(0, heelRotCtrl)
    toeRotCtrl.moveParmTransformIntoPreTransform()
    paramNames = shar.parameter.makeParameterNames(toe, 'Toe_Rot')
    shar.parameter.setControllerExpressions(toeRotCtrl, paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(toeRotCtrl, paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(toeRotCtrl, paramNames[0], 'r', 'z')
    toerparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(toerparm)

    footRotCtrl = shar.control.MakeCtrl(rig, footGoal, body_part_name + '_footRot_ctrl', ctrlColor = ctrlColor, ctrlSize = 0.1, parm = parm, flip = True)
    footRotCtrl.setInput(0, None)
    footRotCtrl.setInput(0, toeRotCtrl)
    footRotCtrl.moveParmTransformIntoPreTransform()
    footGoal.parm('rx').setExpression("ch('"+footGoal.relativePathTo(footRotCtrl) + "/rx')")
    paramNames = shar.parameter.makeParameterNames(foot, 'Ball_Rot')
    shar.parameter.setControllerExpressions(footRotCtrl, paramNames[0], 'r', 'x')
    #self.parmt.setControllerExpressions(toeRotCtrl[2], paramNames[0], 'r', 'y')
    #self.parmt.setControllerExpressions(toeRotCtrl[2], paramNames[0], 'r', 'z')
    footrparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(footrparm)
    
    # append folder to node's parm template group
    # ptg.append(folder)
    shar.parameter.addFolderToAnim(ptg, folder)

    # set templates to node
    rig.setParmTemplateGroup(ptg)

def createQuadLeg( rig, leg_nodes, body_part_name, twist_local_offset):
    femur = leg_nodes[0]
    knee = leg_nodes[1]
    ankle = leg_nodes[2]
    foot = leg_nodes[3]
    assist_A = leg_nodes[4]
    assist_B = leg_nodes[5]


    if femur.name()[0] == 'L':
        body_part_name = 'L_' + body_part_name
    elif femur.name()[0] == 'R':
        body_part_name = 'R_' + body_part_name

    body_part_name += femur.name()[-1]        

    ptg = rig.parmTemplateGroup()

    folder = hou.FolderParmTemplate('folder', body_part_name)

    parm = hou.FloatParmTemplate(body_part_name + "_ikfk", body_part_name[2:-1] + " IkFk", 1)

    parm.setMaxValue(1)

    # add a shar.parameter template to the folder template
    folder.addParmTemplate(parm)

    femurCtrl = shar.control.MakeControlFk(rig, femur, femur.name(), ctrlSize = 0.5, parm = parm)
    shar.constrain.MakeFKConstraints(rig, femur, femurCtrl[2], parm = parm)
    paramNames = shar.parameter.makeParameterNames(femur, 'Rot')
    shar.parameter.setControllerExpressions(femurCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(femurCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(femurCtrl[2], paramNames[0], 'r', 'z')
    fparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(fparm)
    
    kneeCtrl = shar.control.MakeControlFk(rig, knee, knee.name(), ctrlSize = 0.5, parm = parm)
    shar.constrain.MakeFKConstraints(rig, knee, kneeCtrl[2], parm = parm)
    paramNames = shar.parameter.makeParameterNames(knee, 'Rot')
    shar.parameter.setControllerExpressions(kneeCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(kneeCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(kneeCtrl[2], paramNames[0], 'r', 'z')
    kparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(kparm)
    
    ankleCtrl = shar.control.MakeControlFk(rig, ankle, ankle.name(), ctrlSize = 0.5, parm = parm)
    shar.constrain.MakeFKConstraints(rig, ankle, ankleCtrl[2], parm = parm)
    paramNames = shar.parameter.makeParameterNames(ankle, 'Rot')
    shar.parameter.setControllerExpressions(ankleCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(ankleCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(ankleCtrl[2], paramNames[0], 'r', 'z')
    aparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(aparm)
    
    footCtrl = shar.control.MakeControlFk(rig, foot, foot.name(), ctrlSize = 0.5, parm = parm)
    shar.constrain.MakeFKConstraints(rig, foot, footCtrl[2], parm = parm)
    paramNames = shar.parameter.makeParameterNames(foot, 'Rot')
    shar.parameter.setControllerExpressions(footCtrl[2], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(footCtrl[2], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(footCtrl[2], paramNames[0], 'r', 'z')
    ftparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(ftparm)

    # toeCtrl = shar.control.MakeControlFk(rig, toe, toe.name(), ctrlSize = 0.5, parm = parm)
    # shar.constrain.MakeFKConstraints(rig, toe, toeCtrl[2], parm = parm)
    # paramNames = shar.parameter.makeParameterNames(toe, 'Rot')
    # shar.parameter.setControllerExpressions(toeCtrl[2], paramNames[0], 'r', 'x')
    # shar.parameter.setControllerExpressions(toeCtrl[2], paramNames[0], 'r', 'y')
    # shar.parameter.setControllerExpressions(toeCtrl[2], paramNames[0], 'r', 'z')
    # toparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    # folder.addParmTemplate(toparm)


    ik = shar.control.MakeIkObjects(rig, femur, parm, -twist_local_offset)
    shar.constrain.MakeIkConstraints(rig, femur, ik[0], ik[1], parm)

    ikGoalCtrl = shar.control.MakeControlIk(rig, ik[0], ik[0].name(), searchForNodeByName(rig, "root"), ctrlSize = 0.5, parm = parm)
    paramNames = shar.parameter.makeParameterNames(femur, 'Goal_Trans')
    shar.parameter.setControllerExpressions(ikGoalCtrl[2], paramNames[0], 't', 'x')
    shar.parameter.setControllerExpressions(ikGoalCtrl[2], paramNames[0], 't', 'y')
    shar.parameter.setControllerExpressions(ikGoalCtrl[2], paramNames[0], 't', 'z')
    gtparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(gtparm)
    # paramNames = shar.parameter.makeParameterNames(femur, 'Goal_Rot')
    # shar.parameter.setControllerExpressions(ikGoalCtrl[2], paramNames[0], 'r', 'x')
    # shar.parameter.setControllerExpressions(ikGoalCtrl[2], paramNames[0], 'r', 'y')
    # shar.parameter.setControllerExpressions(ikGoalCtrl[2], paramNames[0], 'r', 'z')
    # grparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    # folder.addParmTemplate(grparm)

    ikTwistCtrl = shar.control.MakeControlIk(rig, ik[1], ik[1].name(), searchForNodeByName(rig, "root"), ctrlSize = 0.5, parm = parm)
    paramNames = shar.parameter.makeParameterNames(femur, 'Twist_Trans')
    shar.parameter.setControllerExpressions(ikTwistCtrl[2], paramNames[0], 't', 'x')
    shar.parameter.setControllerExpressions(ikTwistCtrl[2], paramNames[0], 't', 'y')
    shar.parameter.setControllerExpressions(ikTwistCtrl[2], paramNames[0], 't', 'z')
    ttparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(ttparm)        

    #shar.constrain.MakeComplexConstraint(foot, footCtrl[2], ik[0], parm)

    ankleIkCtrl = shar.control.MakeIkSelfObjects(rig, ankle, parm, twist_local_offset)
    shar.constrain.MakeIkSelfConstraint(rig, ankle, ankleIkCtrl[0], ankleIkCtrl[1], parm)
    ankleIkCtrl[0].setDisplayFlag(1)
    ankleIkCtrl[0].parm('geoscale').set(0.3)
    paramNames = shar.parameter.makeParameterNames(ankle, 'Goal_Trans')
    shar.parameter.setControllerExpressions(ankleIkCtrl[0], paramNames[0], 't', 'x')
    shar.parameter.setControllerExpressions(ankleIkCtrl[0], paramNames[0], 't', 'y')
    shar.parameter.setControllerExpressions(ankleIkCtrl[0], paramNames[0], 't', 'z')
    anktparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(anktparm)
    paramNames = shar.parameter.makeParameterNames(ankle, 'Goal_Rot')
    shar.parameter.setControllerExpressions(ankleIkCtrl[0], paramNames[0], 'r', 'x')
    shar.parameter.setControllerExpressions(ankleIkCtrl[0], paramNames[0], 'r', 'y')
    shar.parameter.setControllerExpressions(ankleIkCtrl[0], paramNames[0], 'r', 'z')
    ankrparm = hou.FloatParmTemplate(paramNames[0], paramNames[1], 3)
    folder.addParmTemplate(ankrparm)        

    
    footIkCtrl = shar.control.MakeIkSelfObjects(rig, foot, parm, twist_local_offset)
    shar.constrain.MakeIkSelfConstraint(rig, foot, footIkCtrl[0], footIkCtrl[1], parm)

    assist_Ik = shar.control.MakeIkObjects(rig, assist_A, parm, -twist_local_offset)
#import shar.nodegroups
    shar.constrain.MakeIkConstraints(rig, assist_A, assist_Ik[0], assist_Ik[1], parm)
    #assist_Ik[1].setDisplayFlag(1)
    #assist_Ik[1].parm('geoscale').set(0.3)


    # ankle goal child of root
    root = femur.inputs()[0]
    ankleIkCtrl[0].setInput(0, root)
    ankleIkCtrl[1].setInput(0, root)

    # assist A goal child of ankle goal
    assist_Ik[0].setInput(0, ankleIkCtrl[0])
    assist_Ik[1].setInput(0, root)
    # foot goal child of ankle goal
    footIkCtrl[0].setInput(0, ankleIkCtrl[0])
    footIkCtrl[1].setInput(0, root)
    #femur goal offset child of foot goal
    ikGoalCtrl[0].setInput(0, footIkCtrl[0])


    # append folder to node's parm template group
    # ptg.append(folder)
    shar.parameter.addFolderToAnim(ptg, folder)

    # set templates to node
    rig.setParmTemplateGroup(ptg)

def createHeadAndNeck(rig, head_nodes, body_part_name):

    ptg = rig.parmTemplateGroup()

    folder = hou.FolderParmTemplate('folder', body_part_name)
    folder.addParmTemplate(hou.FloatParmTemplate('headr', 'Head Rot', 3))
    folder.addParmTemplate(hou.FloatParmTemplate('neckr', 'Neck Rot', 3))

    neck = head_nodes[0]
    head = head_nodes[1]

    neckCtrl = shar.control.MakeControlFk(rig, neck, neck.name(), ctrlSize = 0.5)
    shar.parameter.setRotExpressions(neckCtrl[2], neck)
    neckCtrl[2].parm('rx').setExpression('ch("../'+'neckr'+'x")')
    neckCtrl[2].parm('ry').setExpression('ch("../'+'neckr'+'y")')
    neckCtrl[2].parm('rz').setExpression('ch("../'+'neckr'+'z")')
    shar.constrain.MakeFKConstraints(rig, neck, neckCtrl[2])

    headCtrl = shar.control.MakeControlFk(rig, head, head.name(), ctrlSize = 0.5)
    headCtrl[2].parm('rx').setExpression('ch("../'+'headr'+'x")')
    headCtrl[2].parm('ry').setExpression('ch("../'+'headr'+'y")')
    headCtrl[2].parm('rz').setExpression('ch("../'+'headr'+'z")')
    shar.constrain.MakeFKConstraints(rig, head, headCtrl[2])

    shar.parameter.addFolderToAnim(ptg, folder)

    rig.setParmTemplateGroup(ptg)

def createPiston(rig, piston_nodes):

    piston1 = piston_nodes[0]
    piston2 = piston_nodes[1]

    piston1_bone = piston1.outputs()[0]
    piston2_bone = piston2.outputs()[0]

    shar.constrain.MakeLookAtContraint(piston1_bone, piston2)
    shar.constrain.MakeLookAtContraint(piston2_bone, piston1)

    # base = finger_nodes[0]
    # mid = finger_nodes[1]
    # end = finger_nodes[2]

    # fk_base = self.ctrl.MakeControlFk(base, base.name())
    # self.cnst.MakeFKConstraints(rig, base, fk_base[2])

    # fk_mid = self.ctrl.MakeControlFk(mid, mid.name())
    # self.cnst.MakeFKConstraints(rig, mid, fk_mid[2])

    # fk_end = self.ctrl.MakeControlFk(end, end.name())
    # self.cnst.MakeFKConstraints(rig, end, fk_end[2])

    # print base
    # print mid
    # print end

