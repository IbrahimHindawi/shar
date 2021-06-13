'''
this module is responsible for creating and configuring UI

'''


import sys

import hou
import toolutils



from PySide2 import QtCore, QtUiTools, QtWidgets

script_path = 'C:/Users/Administrator/Documents/scripts/ibra_autorig_v5/'
sys.path.append(script_path)

import utilities
reload(utilities)

import control
reload(control)

import constrain
reload(constrain)

import parameter
reload(parameter)

import analysis
reload(analysis)

import build
reload(build)

import main
reload(main)

sViewer = toolutils.sceneViewer()


def ClearMemory():
    reload(control)
    reload(constrain)
    reload(parameter)
    reload(analysis)
    reload(build)
    reload(main)

class ibraRiggingToolkit(QtWidgets.QWidget):
    def __init__(self):
        super(ibraRiggingToolkit,self).__init__()
        ui_file = script_path + 'iAutoRig.ui'
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        
        
        # TEST
        self.customName = self.ui.BodyPartName.text()
        #self.ui.TestButton.clicked.connect(self.test)
        
        # Setup HumanoidCreateButton
        self.ui.HumanoidButton.clicked.connect(self.humanoidButtonClicked)

        # Setup CreateArmButton
        self.ui.CreateArmButton.clicked.connect(self.createArmButtonClicked)

        # Setup CreateLegButton
        self.ui.CreateLegButton.clicked.connect(self.createLegButtonClicked)

        # Setup CreateQuadLegButton
        self.ui.CreateQuadLegButton.clicked.connect(self.CreateQuadLegButtonClicked)

        # Setup CreateSpineButton
        self.ui.CreateSpineButton.clicked.connect(self.createSpineButtonClicked)

        # Setup CreateFingerButton
        self.ui.CreateFingerButton.clicked.connect(self.createFingerButtonClicked)

        # Setup CreateHipButton
        self.ui.CreateHipButton.clicked.connect(self.createHipButtonClicked)

        # Setup CreatePistonButton
        self.ui.CreatePistonButton.clicked.connect(self.createPistonButtonClicked)

        # Setup MirrorLimbButton
        self.ui.MirrorLimbButton.clicked.connect(self.mirrorLimbButtonClicked)

        # Setup MirrorFingersButton
        self.ui.MirrorFingersButton.clicked.connect(self.mirrorFingersButtonClicked)

        self.ui.CreateHandsFingersButton.clicked.connect(self.CreateHandsFingersButtonClicked)
        #print ("New Script is here!")





    def executeHumanoidBuild(self, rig):
        ClearMemory()
        main.main(rig)
        
    def humanoidButtonClicked(self):
        subnetPath = self.ui.SubnetPath.text()
        rig = hou.node(subnetPath)
        self.executeHumanoidBuild(rig)
        

    def executeCreateArm(self, rig, parmName):
        items = sViewer.selectObjects('Select shoulder, arm, forearm, hand and twist bone, press Enter to Continue.')
        builder = build.build(rig)
        builder.createArm(items, parmName, 0.5)

    def createArmButtonClicked(self):
        subnetPath = self.ui.SubnetPath.text()
        rig = hou.node(subnetPath)
        parmName = self.ui.BodyPartName.text()
        self.executeCreateArm(rig, parmName)


    def executeCreateLeg(self, rig, parmName):
        items = sViewer.selectObjects('Select thigh, shin, foot and toe bones, press Enter to Continue.')
        builder = build.build(rig)
        builder.createLeg(items, parmName, 2)
        
    def createLegButtonClicked(self):
        subnetPath = self.ui.SubnetPath.text()
        rig = hou.node(subnetPath)
        parmName = self.ui.BodyPartName.text()
        self.executeCreateLeg(rig, parmName)

    def CreateQuadLegButton(self):
        subnetPath = self.ui.SubnetPath.text()
        rig = hou.node(subnetPath)
        parmName = self.ui.BodyPartName.text()
        items = sViewer.selectObjects('Select femur, knee, ankle, foot, assistA and assistB bones, press Enter to Continue.')
        builder = build.build(rig)
        builder.createQuadLeg(items, parmName, -0.5)
        
    
    def CreateQuadLegButtonClicked(self):
        self.CreateQuadLegButton()


    def executeCreateSpine(self, rig, parmName):
        items = sViewer.selectObjects('Select 5 spine bones, press Enter to Continue.')
        builder = build.build(rig)
        builder.createSpine(items, parmName)

    def createSpineButtonClicked(self):
        subnetPath = self.ui.SubnetPath.text()
        rig = hou.node(subnetPath)
        parmName = self.ui.BodyPartName.text()
        self.executeCreateSpine(rig, parmName)


    def executeCreateFinger(self, rig):
        items = sViewer.selectObjects('Select 3 finger bones, press Enter to Continue.')
        builder = build.build(rig)
        builder.createFinger(items)

    def createFingerButtonClicked(self):
        subnetPath = self.ui.SubnetPath.text()
        rig = hou.node(subnetPath)
        parmName = self.ui.BodyPartName.text()
        self.executeCreateFinger(rig)

    def executeCreateHip(self, rig, parmName):
        items = sViewer.selectObjects('Select hip bone, press Enter to Continue.')
        builder = build.build(rig)
        builder.createHip(items, parmName)

    def createHipButtonClicked(self):
        subnetPath = self.ui.SubnetPath.text()
        rig = hou.node(subnetPath)
        parmName = self.ui.BodyPartName.text()
        self.executeCreateHip(rig, parmName)

    def executeCreatePiston(self, rig):
        items = sViewer.selectObjects('Select piston nulls, press Enter to Continue.')
        builder = build.build(rig)
        builder.createPiston(items)

    def createPistonButtonClicked(self):
        subnetPath = self.ui.SubnetPath.text()
        rig = hou.node(subnetPath)
        self.executeCreatePiston(rig)

    def mirrorLimbButtonClicked(self):
        utilities.mirrorBones()

    def mirrorFingersButtonClicked(self):
        utilities.mirrorFingers()


    def CreateHandsFingersButton(self):
        subnetPath = self.ui.SubnetPath.text()
        rig = hou.node(subnetPath)
        item = sViewer.selectObjects('Select hand bone, press Enter to Continue.')
        builder = build.build(rig)
        builder.createFingers(item)


    def CreateHandsFingersButtonClicked(self):
        self.CreateHandsFingersButton()



def run():
    win = ibraRiggingToolkit()
    win.show()