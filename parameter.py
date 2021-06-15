'''
this module is responsible for building parameter interface

'''

import hou


def initializeParmeter( rig ):
    #self.parmer.setColor( hou.Color((1.0, 1.0, 0.0)) )
    parmerptg = rig.parmTemplateGroup()
    #folder = hou.FolderParmTemplate("body", "Body")
    #parmerptg.addParmTemplate(folder)
    rig.setParmTemplateGroup(parmerptg)

def makeParameterNames( bone, postFix ):

    names = []

    parmName = bone.name() + '_' + postFix.lower()

    names.append(parmName)

    postFix = postFix.replace("_", " ")

    if bone.type().name() == 'bone':
        prettyName = bone.name()[2:-1] + ' ' + postFix
    elif bone.type().name() == 'null':
        pretty_name_prep = bone.name().replace('_ctrl', '')
        pretty_name_prep = pretty_name_prep.replace('_',' ')
        prettyName = pretty_name_prep + ' ' + postFix

    names.append(prettyName)

    return names



def makeParameter( rig, body_part_name ):
    parmgroup = rig.parmTemplateGroup()
    ikfk = hou.FloatParmTemplate(body_part_name + "_ikfk", body_part_name + "_ikfk", 1)
    ikfk.setMaxValue(1)
    parmgroup.addParmTemplate(ikfk)
    #targetfolder = ("Body",)
    #parmgroup.appendToFolder(targetfolder, parmgroup.entries()[2])
    rig.setParmTemplateGroup(parmgroup)
    return rig.parm(body_part_name + "_ikfk")

def setRotExpressions( targetController, bone):
    targetController.parm('rx').setExpression('ch("../'+bone.name()+'x")')
    targetController.parm('ry').setExpression('ch("../'+bone.name()+'y")')
    targetController.parm('rz').setExpression('ch("../'+bone.name()+'z")')

def setTransExpressions( targetController, bone):
    targetController.parm('tx').setExpression('ch("../'+bone.name()+'x")')
    targetController.parm('ty').setExpression('ch("../'+bone.name()+'y")')
    targetController.parm('tz').setExpression('ch("../'+bone.name()+'z")')

def setControllerExpressions( targetController, parameterName, channel, component):
    targetController.parm(channel+component).setExpression('ch("../' + parameterName + component + '")')






