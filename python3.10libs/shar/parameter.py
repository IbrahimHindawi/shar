'''
this module is responsible for building the parameter interface

'''

import hou

def initializeParmeter(rig):
    #self.parmer.setColor(hou.Color((1.0, 1.0, 0.0)))
    parmerptg = rig.parmTemplateGroup()
    #folder = hou.FolderParmTemplate("body", "Body")
    #parmerptg.addParmTemplate(folder)
    rig.setParmTemplateGroup(parmerptg)

def hideParameter(node, parmname):
    ptg = node.parmTemplateGroup()
    p = ptg.findFolder(parmname)
    p.hide(True)
    ptg.replace(p.name(), p)
    node.setParmTemplateGroup(ptg) 

def lockAndHideOldParameters(node):
    parms = node.parms()
    for p in parms:
        if 'stdswitcher' not in p.name():
            p.lock(True)

    topfoldersnames = ['Transform', 'Subnet']

    for name in topfoldersnames:
        hideParameter(node, name)

def addFolderToAnim(ptg, targetfolder):
    mainfolder = ptg.findFolder('Main')
    # print(mainfolder)
    mpt = mainfolder.parmTemplates()
    animfolder = None
    for pt in mpt:
        if "Anim" in pt.label():
            animfolder = pt
    if animfolder == None:
        print("animfolder not found!")
        exit()
    # ptg.appendToFolder(folder, mainfolder)
    ptg.appendToFolder(animfolder, targetfolder)


def initializeParameterInterface(rig):
    ptg = rig.parmTemplateGroup()

    mainfolder = hou.FolderParmTemplate('folder', 'Main')

    cparm = hou.IntParmTemplate('cdisplay', 'Ctrl', 1, menu_items=('0', '1'), menu_labels=('OFF', 'ON'), default_value=(1,))
    mainfolder.addParmTemplate(cparm)
    gparm = hou.IntParmTemplate('gdisplay', 'Geo', 1, menu_items=('0', '1'), menu_labels=('OFF', 'ON'), default_value=(1,))
    mainfolder.addParmTemplate(gparm)
    bparm = hou.IntParmTemplate('bdisplay', 'Bone', 1, menu_items=('0', '1'), menu_labels=('OFF', 'ON'), default_value=(1,))
    mainfolder.addParmTemplate(bparm)

    ptg.append(mainfolder)

    # mainfolderf = ptg.findFolder('Main')
    animfolder = hou.FolderParmTemplate('folder', 'Anim')
    ptg.appendToFolder(mainfolder, animfolder)

    rig.setParmTemplateGroup(ptg)

def makeParameterNames(bone, postFix):
    names = []
    parmName = bone.name() + '_' + postFix.lower()
    names.append(parmName)
    postFix = postFix.replace("_", " ")
    prettyName = ''

    if bone.type().name() == 'bone':
        prettyName = bone.name()[2:] + ' ' + postFix
        prettyName = prettyName.replace("_bone", " ")
        prettyNameList = [char for char in prettyName]
        prettyNameList[0] = prettyNameList[0].upper()
        prettyName = ''.join(prettyNameList)
    elif bone.type().name() == 'null':
        prettyName = bone.name().replace('_ctrl', '')
        prettyName = prettyName.replace('_',' ')
        prettyName = prettyName.replace("_bone", "")
        prettyName = prettyName + ' ' + postFix
        prettyNameList = [char for char in prettyName]
        prettyNameList[0] = prettyNameList[0].upper()
        prettyName = ''.join(prettyNameList)
    else:
        print("Error: Unknown Type")

    names.append(prettyName)

    return names

def makeParameter(rig, body_part_name):
    parmgroup = rig.parmTemplateGroup()
    ikfk = hou.FloatParmTemplate(body_part_name + "_ikfk", body_part_name + "_ikfk", 1)
    ikfk.setMaxValue(1)
    parmgroup.addParmTemplate(ikfk)
    #targetfolder = ("Body",)
    #parmgroup.appendToFolder(targetfolder, parmgroup.entries()[2])
    rig.setParmTemplateGroup(parmgroup)
    return rig.parm(body_part_name + "_ikfk")

def setRotExpressions(targetController, bone):
    targetController.parm('rx').setExpression('ch("../'+bone.name()+'x")')
    targetController.parm('ry').setExpression('ch("../'+bone.name()+'y")')
    targetController.parm('rz').setExpression('ch("../'+bone.name()+'z")')

def setTransExpressions(targetController, bone):
    targetController.parm('tx').setExpression('ch("../'+bone.name()+'x")')
    targetController.parm('ty').setExpression('ch("../'+bone.name()+'y")')
    targetController.parm('tz').setExpression('ch("../'+bone.name()+'z")')

def setControllerExpressions(targetController, parameterName, channel, component):
    targetController.parm(channel+component).setExpression('ch("../' + parameterName + component + '")')

def setControllerExpressionsSimple(targetController, parameterName):
    targetController.parm(parameterName).setExpression('ch("../' + parameterName + '")')

def setupDisplay(node, display_category):
    node.parm("tdisplay").set(True)
    node.parm("display").setExpression('ch("../'+display_category+'display")')
