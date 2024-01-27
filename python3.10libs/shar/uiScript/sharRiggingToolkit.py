'''
this module is responsible for creating and configuring UI

'''

import sys

import hou
import toolutils
import importlib

# from shar import *
import shar

from PySide2 import QtCore, QtUiTools, QtWidgets

user_pref_dir = hou.text.expandString('$HOUDINI_USER_PREF_DIR')
plugpath = '/shar/python3.10libs/shar/uiScript'
ui_file = user_pref_dir + plugpath + '/' + 'shar.ui'

sys.path.append(user_pref_dir)
sViewer = toolutils.sceneViewer()

class ibraRiggingToolkit(QtWidgets.QWidget):
    def __init__(self):
        super(ibraRiggingToolkit,self).__init__()
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        
        
        # TEST
        self.customName = self.ui.BodyPartName.text()
        #self.ui.TestButton.clicked.connect(self.test)
        
        self.ui.HumanoidButton.clicked.connect(self.humanoidButtonClicked)

        self.ui.InitializeButton.clicked.connect(self.initializeButtonClicked)

        self.ui.CreateArmButton.clicked.connect(self.createArmButtonClicked)

        self.ui.CreateLegButton.clicked.connect(self.createLegButtonClicked)

        self.ui.CreateQuadLegButton.clicked.connect(self.CreateQuadLegButtonClicked)

        self.ui.CreateSpineButton.clicked.connect(self.createSpineButtonClicked)

        self.ui.CreateFingerButton.clicked.connect(self.createFingerButtonClicked)

        self.ui.CreateHipButton.clicked.connect(self.createHipButtonClicked)

        self.ui.CreatePistonButton.clicked.connect(self.createPistonButtonClicked)

        self.ui.MirrorLimbButton.clicked.connect(self.mirrorLimbButtonClicked)

        self.ui.MirrorFingersButton.clicked.connect(self.mirrorFingersButtonClicked)

        self.ui.CreateHandsFingersButton.clicked.connect(self.CreateHandsFingersButtonClicked)
        #print ("New Script is here!")

    def executeHumanoidBuild(self, rig):
        main.main(rig)

    def executeInitialize(self, rig):
        shar.build.initializeNodeGroups(rig)
        
    def humanoidButtonClicked(self):
        subnetPath = self.ui.SubnetPath.text()
        rig = hou.node(subnetPath)
        self.executeHumanoidBuild(rig)

    def initializeButtonClicked(self):
        subnetPath = self.ui.SubnetPath.text()
        rig = hou.node(subnetPath)
        self.executeInitialize(rig)

    def executeCreateArm(self, rig, parmName):
        items = sViewer.selectObjects('Select shoulder, arm, forearm, hand and twist bone, press Enter to Continue.')
        shar.build.createArm(rig, items, parmName, shar.color.red)
        # builder = build.build(rig)
        # builder.createArm(items, parmName, 0.5)

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
