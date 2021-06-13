'''
this module is responsible for analyzing the bones and generating
data pool and then splicing the bones into groups. . . 

'''


import hou
import re
import LimbContainer

class analysis:

    listOfBones = []    
    
    leftBones = []
    rightBones = []
    centerBones = []    

    rig = None

    #selection = hou.selectedNodes()[0]


    def __init__(self, rig):
        print ("analysis object initialized")

        self.rig = rig

        #self.rig = hou.node('/obj/skel_hum3')


    
    #===================================
    # Utilities
    #===================================

    def printBoneGroup(self, phrase, bonesGroup):
        print phrase
        for bone in bonesGroup:
            print bone

    def printBones(self):
        #print self.listOfBones
        #print self.leftBones
        self.printBoneGroup("\nLeft Bones: ", self.leftBones)
        #print self.rightBones
        self.printBoneGroup("\nRight Bones: ", self.rightBones)
        #print self.centerBones
        self.printBoneGroup("\nCenter Bones:", self.centerBones)
        print "\n\n"

    def getNodeByName( self, node, name ):
        if node.name() == name:
            return node

    def getNextBone( self, bone ):
        try:
            return bone.outputs()[0]
        except IndexError as error:
            return

    def addBoneToList( self, bone, boneList ):
        if bone == None:
            return
        else:
            boneList.append(bone)   

    def walkBones ( self, bone, boneList, depth):
        for itera in range(0, depth):
            bone = self.getNextBone(bone)
            self.addBoneToList(bone, boneList)

    def getChildren( self, bone ):
        children = bone.outputs()
        return children

    def getBoneChain(self, startBone, iterations):
        chain = []
        for i in range (0, iterations):
            chain.append(self.getNextBone(startBone))
        return chain


    #===================================
    # Build Lists
    #===================================  

    def readBones(self):
        #selection = hou.selectedNodes()[0]
        for node in self.rig.children():
            if node.type().name() == "bone":
                self.listOfBones.append(node)
        #print self.listOfBones

    def getBones(self):
        return self.listOfBones

    def populatePositionLists(self):
        for bone in self.listOfBones:
            if bone.name()[0] == "L":
                self.leftBones.append(bone)
            elif bone.name()[0] == "R":
                self.rightBones.append(bone)
            else:
                self.centerBones.append(bone)

    # def getNextBone(self, startBone):
    #     return startBone.outputs()[0]

    #def getNextBone(self, startBone):
    #    return startBone.outputs()[0]



    #===================================
    # Isolate Limbs
    #===================================

    def isolateArm(self, dataPool, prefix):
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

    def isolateLeg(self, dataPool, prefix):
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

    def isolateFinger(self, dataPool, prefix, fingerName):
        finger = []
        for bone in dataPool:
            if bone.name() == prefix +'_'+ fingerName +'_'+ str(0):
                finger.append(bone)
            if bone.name() == prefix +'_'+ fingerName +'_'+ str(1):
                finger.append(bone)
            if bone.name() == prefix +'_'+ fingerName +'_'+ str(2):
                finger.append(bone)
        return finger

    def isolateSpine(self, dataPool):
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

    def isolateHip(self, dataPool):
        hip = []
        for bone in dataPool:
            if bone.name() == 'hip':
                hip.append(bone)
        return hip

    def isolateHead(self, dataPool):
        head = []
        for bone in dataPool:
            if bone.name() == 'neck':
                head.append(bone)
            if bone.name() == 'head':
                head.append(bone)
        return head

    def isolateRoot(self, dataPool):
        for bone in dataPool:
            if bone.name() == 'root':
                return bone

    def isolateBodyParts(self):
        
        bodyParts = []


        shoulderList = self.getChain('shoulder', 3)
        bodyParts.append(shoulderList)

        legList = self.getChain('thigh', 3)
        bodyParts.append(legList)

        #print shoulderList

        spine = self.isolateSpine(self.centerBones)
        spine_container = LimbContainer.LimbContainer("Spine", spine)
        bodyParts.append(spine_container)

        hip = self.isolateHip(self.centerBones)
        hip_container = LimbContainer.LimbContainer("Hip", hip)
        bodyParts.append(hip_container)

        head = self.isolateHead(self.centerBones)
        head_container = LimbContainer.LimbContainer("Head", head)
        bodyParts.append(head_container)

        hands = self.getChain('hand', 0)
        print "HANDS: " + str(hands)
        #hand_container = LimbContainer.LimbContainer("Hand", hands)
        bodyParts.append(hands)

        # root = self.isolateRoot(self.centerBones)
        # root_container = LimbContainer.LimbContainer("Root", root)
        # bodyParts.append(root_container)

        return bodyParts

    def isolateFingers(self):

        fingers = []
        
        left_index = self.isolateFinger(self.leftBones, 'L', 'index')
        left_index_container = LimbContainer.LimbContainer("L_Index", left_index)
        fingers.append(left_index_container)
        
        
        right_index = self.isolateFinger(self.rightBones, 'R', 'index')
        right_index_container = LimbContainer.LimbContainer("R_Index", right_index)
        fingers.append(right_index_container)
        
        
        left_thumb = self.isolateFinger(self.leftBones, 'L', 'thumb')
        left_thumb_container = LimbContainer.LimbContainer("L_thumb", left_thumb)
        fingers.append(left_thumb_container)
        
        
        right_thumb = self.isolateFinger(self.rightBones, 'R', 'thumb')
        right_thumb_container = LimbContainer.LimbContainer("R_thumb", right_thumb)
        fingers.append(right_thumb_container)
        
        
        right_ring = self.isolateFinger(self.rightBones, 'R', 'ring')
        right_ring_container = LimbContainer.LimbContainer("R_ring", right_ring)
        fingers.append(right_ring_container)
        
        left_ring = self.isolateFinger(self.leftBones, 'L', 'ring')
        left_ring_container = LimbContainer.LimbContainer("L_ring", left_ring)
        fingers.append(left_ring_container)
        
        
        right_middle = self.isolateFinger(self.rightBones, 'R', 'middle')
        right_middle_container = LimbContainer.LimbContainer("R_middle", right_middle)
        fingers.append(right_middle_container)
        
        left_middle = self.isolateFinger(self.leftBones, 'L', 'middle')
        left_middle_container = LimbContainer.LimbContainer("L_middle", left_middle)
        fingers.append(left_middle_container)
        
        
        right_pinky = self.isolateFinger(self.rightBones, 'R', 'pinky')
        right_pinky_container = LimbContainer.LimbContainer("R_pinky", right_pinky)
        fingers.append(right_pinky_container)

        left_pinky = self.isolateFinger(self.leftBones, 'L', 'pinky')
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
    #     print arm

    #===================================
    # Isolate Limbs V3
    #===================================

    def getChain( self, pattern, depth ):

        shoulders = []
        lol = []

        # Get all shoulders
        pattern = pattern
        for bone in self.listOfBones:
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
                print node
                self.walkBones(node, listItem, 3)
        '''

        for bone in shoulders:
            newList = [bone]
            self.walkBones(bone, newList, depth)
            lol.append(newList)

        return lol



