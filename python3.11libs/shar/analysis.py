'''
this module is responsible for analyzing the bones and generating
data pool and then splicing the bones into groups. . . 

'''

import hou
import re
from shar import LimbContainer

listOfBones = []    
    
leftBones = []
rightBones = []
centerBones = []    

# rig = None

# def init(input_rig):
#     print ("analysis object initialized")
#     global rig
#     rig = input_rig
    
#===================================
# Utilities
#===================================

def printBoneGroup(phrase, bonesGroup):
    print(phrase)
    for bone in bonesGroup:
        print(bone)

def printBones():
    printBoneGroup("\nLeft Bones: ", leftBones)
    printBoneGroup("\nRight Bones: ", rightBones)
    printBoneGroup("\nCenter Bones:", centerBones)
    print("\n\n")

def getNodeByName(node, name):
    if node.name() == name:
        return node

def getChildBones(node):
    bones = []
    for child in node.outputs():
        if "bone" in child.type().name():
            bones.append(child)
    return bones

def getNextBone(bone):
    try:
        for child in bone.outputs():
            if "bone" in child.type().name():
                return child
    except IndexError as error:
        return

def addBoneToList(bone, boneList):
    if bone == None:
        return
    else:
        boneList.append(bone)   

def walkBones (bone, boneList, depth):
    for itera in range(0, depth):
        bone = getNextBone(bone)
        addBoneToList(bone, boneList)

def getChildren(bone):
    # children = bone.outputs()
    children = getChildBones(bone)
    return children

def getBoneChain(startBone, iterations):
    chain = []
    for i in range (0, iterations):
        chain.append(getNextBone(startBone))
    return chain


#===================================
# Build Lists
#===================================  

def readBones(rig):
    for node in rig.children():
        if node.type().name() == "bone":
            listOfBones.append(node)

def getBones():
    return listOfBones

def populatePositionLists():
    for bone in listOfBones:
        if bone.name()[0] == "L":
            leftBones.append(bone)
        elif bone.name()[0] == "R":
            rightBones.append(bone)
        else:
            centerBones.append(bone)

    #===================================
    # Isolate Limbs
    #===================================

def isolateArm(dataPool, prefix):
    arm = []
    for bone in dataPool:
        if bone.name() == prefix + '_shoulder':
            arm.append(bone)
        if bone.name() == prefix + '_bicep':
            arm.append(bone)
        if bone.name() == prefix + '_forearm':
            arm.append(bone)
        if bone.name() == prefix + '_hand':
            arm.append(bone)
        if bone.name() == prefix + 'bicep0_twist_ctrl':
            arm.append(bone)
    return arm

def isolateLeg(dataPool, prefix):
    leg = []
    for bone in dataPool:
        if bone.name() == prefix + '_thigh':
            leg.append(bone)
        if bone.name() == prefix + '_shin':
            leg.append(bone)
        if bone.name() == prefix + '_foot':
            leg.append(bone)
        if bone.name() == prefix + '_toe':
            leg.append(bone)
    return leg

def isolateFinger(dataPool, prefix, fingerName):
    finger = []
    for bone in dataPool:
        if bone.name() == prefix +'_'+ fingerName +'_'+ str(0):
            finger.append(bone)
        if bone.name() == prefix +'_'+ fingerName +'_'+ str(1):
            finger.append(bone)
        if bone.name() == prefix +'_'+ fingerName +'_'+ str(2):
            finger.append(bone)
    return finger

def isolateSpine(dataPool):
    spine = []
    for bone in dataPool:
        if bone.name() == 'spine' + str(1):
            spine.append(bone)
        if bone.name() == 'spine' + str(2):
            spine.append(bone)
        if bone.name() == 'spine' + str(3):
            spine.append(bone)
        if bone.name() == 'spine' + str(4):
            spine.append(bone)
        if bone.name() == 'spine' + str(5):
            spine.append(bone)
    return spine

def isolateHip(dataPool):
    hip = []
    for bone in dataPool:
        if bone.name() == 'hip':
            hip.append(bone)
    return hip

def isolateHead(dataPool):
    head = []
    for bone in dataPool:
        if bone.name() == 'neck':
            head.append(bone)
        if bone.name() == 'head':
            head.append(bone)
    return head

def isolateRoot(dataPool):
    for bone in dataPool:
        if bone.name() == 'root':
            return bone

def isolateBodyParts():
    
    bodyParts = []


    shoulderList = getChain('shoulder', 3)
    bodyParts.append(shoulderList)

    legList = getChain('thigh', 3)
    bodyParts.append(legList)

    #print shoulderList

    spine = isolateSpine(centerBones)
    spine_container = LimbContainer.LimbContainer("Spine", spine)
    bodyParts.append(spine_container)

    hip = isolateHip(centerBones)
    hip_container = LimbContainer.LimbContainer("Hip", hip)
    bodyParts.append(hip_container)

    head = isolateHead(centerBones)
    head_container = LimbContainer.LimbContainer("Head", head)
    bodyParts.append(head_container)

    hands = getChain('hand', 0)
    print("HANDS: " + str(hands))
    #hand_container = LimbContainer.LimbContainer("Hand", hands)
    bodyParts.append(hands)

    # root = self.isolateRoot(self.centerBones)
    # root_container = LimbContainer.LimbContainer("Root", root)
    # bodyParts.append(root_container)

    return bodyParts

def isolateFingers():

    fingers = []
    
    left_index = isolateFinger(leftBones, 'L', 'index')
    left_index_container = LimbContainer.LimbContainer("L_Index", left_index)
    fingers.append(left_index_container)
    
    
    right_index = isolateFinger(rightBones, 'R', 'index')
    right_index_container = LimbContainer.LimbContainer("R_Index", right_index)
    fingers.append(right_index_container)
    
    
    left_thumb = isolateFinger(leftBones, 'L', 'thumb')
    left_thumb_container = LimbContainer.LimbContainer("L_thumb", left_thumb)
    fingers.append(left_thumb_container)
    
    
    right_thumb = isolateFinger(rightBones, 'R', 'thumb')
    right_thumb_container = LimbContainer.LimbContainer("R_thumb", right_thumb)
    fingers.append(right_thumb_container)
    
    
    right_ring = isolateFinger(rightBones, 'R', 'ring')
    right_ring_container = LimbContainer.LimbContainer("R_ring", right_ring)
    fingers.append(right_ring_container)
    
    left_ring = isolateFinger(leftBones, 'L', 'ring')
    left_ring_container = LimbContainer.LimbContainer("L_ring", left_ring)
    fingers.append(left_ring_container)
    
    
    right_middle = isolateFinger(rightBones, 'R', 'middle')
    right_middle_container = LimbContainer.LimbContainer("R_middle", right_middle)
    fingers.append(right_middle_container)
    
    left_middle = isolateFinger(leftBones, 'L', 'middle')
    left_middle_container = LimbContainer.LimbContainer("L_middle", left_middle)
    fingers.append(left_middle_container)
    
    
    right_pinky = isolateFinger(rightBones, 'R', 'pinky')
    right_pinky_container = LimbContainer.LimbContainer("R_pinky", right_pinky)
    fingers.append(right_pinky_container)

    left_pinky = isolateFinger(leftBones, 'L', 'pinky')
    left_pinky_container = LimbContainer.LimbContainer("L_pinky", left_pinky)
    fingers.append(left_pinky_container)
    
    return fingers


    #===================================
    # Isolate Limbs V2
    #===================================

    # def getShoulders(self, dataPool):
    #     pattern = 'shoulder'
    #     shoulders = []
    #     for bone in dataPool:
    #         if re.findall(pattern, bone.name()):
    #             shoulders.append(bone)
    #     return shoulders
    
    # def isolateArm(self, shoulders):
    #     arm = []
    #     for shoulder in shoulders:
    #         arm.append(shoulder)
    #         bicep = self.getNextBone(shoulder)
    #         forearm = self.getNextBone(bicep)
    #         hand = self.getNextBone(forearm)
    #         arm.append(bicep)
    #         arm.append(forearm)
    #         arm.append(hand)
    #     print(arm)

    #===================================
    # Isolate Limbs V3
    #===================================

def getChain(pattern, depth):

    shoulders = []
    lol = []

    # Get all shoulders
    pattern = pattern
    for bone in listOfBones:
        if re.findall(pattern, bone.name()):
            shoulders.append(bone)
    '''
    # Split shoulders into lists
    for item in shoulders:
        newList = [item]
        lol.append(newList)

    # Walk shoulders
    for listItem in lol:
        for node in listItem:
            print(node)
            walkBones(node, listItem, 3)
    '''

    for bone in shoulders:
        newList = [bone]
        walkBones(bone, newList, depth)
        lol.append(newList)

    return lol


# Usage Code
'''
import hou

import shar.analysis
reload(shar.analysis)

rig = hou.node('/obj/charac')
shar.analysis.readBones(rig)
shar.analysis.populatePositionLists()
body_parts = shar.analysis.isolateBodyParts()
shar.analysis.printBones()
print(body_parts)
'''
