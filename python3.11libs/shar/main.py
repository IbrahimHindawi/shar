'''
this module is responsible for building humanoid 

'''


import hou
from shar import analysis
from shar import build

#import unicodedata

def GetBone( rig, boneName):
    for bone in rig.children():
        if bone.name() == boneName:
            return bone


def main(subnetPath):
    pass

    # Create analyzer object
    analyzer = analysis.analysis(subnetPath)

    # Collect bones
    analyzer.readBones()

    # Split bones into positional groups
    analyzer.populatePositionLists()


    # Split bone groups into limb stream
    bodyParts = analyzer.isolateBodyParts()

    shoulders = bodyParts[0]

    legs = bodyParts[1]

    spine = bodyParts[2]
    spine_nodes = spine.getArray()
    spine_nodes_name = spine.getName()

    hip = bodyParts[3]
    hip_nodes   = hip.getArray()
    hip_nodes_name = hip.getName()

    head = bodyParts[4]
    head_nodes  = head.getArray()
    head_nodes_name = head.getName()

    hands = bodyParts[5]



    #targetNode = hou.node(subnetPath)
    #print "targetNode = " + targetNode

    builder = build.build(subnetPath)

    for item in shoulders:
        builder.createArm(item, 'Arm', 0.5)

    # for hand in hands:
    #     builder.createFingers(hand)

    for item in legs:
        builder.createLeg(item, 'Leg', -0.5)


    # builder.createSpine(spine_nodes, spine_nodes_name)
    # builder.createHip(hip_nodes, hip_nodes_name)
    # builder.createHead(head_nodes, head_nodes_name)





    # root = GetBone(rig, 'root')

    # bone1 = GetBone(rig, 'bone1')

    # bone2 = GetBone(rig, 'bone2')

    # bone3 = GetBone(rig, 'bone3')



    #ctrl.MakeControlShape(bone1, bone1.name(), ctrlSize = 0.5 )
    #ctrl.MakeControlIk(bone2, bone2.name(), root, ctrlSize = 1.0)



'''
def main():
    
    # Create analyzer object
    analyzer = analysis.analysis()

    # Collect bones
    analyzer.readBones()

    # Split bones into positional groups
    analyzer.populatePositionLists()

    # Print positional groups
    #analyzer.printBones()

    #listOfLists = analyzer.getShoulder()
    #print x
    # for listItem in listOfLists:
    #   for item in listItem:
    #       print item

    # Split bone groups into limb stream
    bodyParts = analyzer.isolateBodyParts()

    L_arm = bodyParts[0]
    R_arm = bodyParts[1]
    L_leg = bodyParts[2]
    R_leg = bodyParts[3]
    spine = bodyParts[4]
    hip = bodyParts[5]
    head = bodyParts[6]

    L_arm_nodes = L_arm.getArray()
    R_arm_nodes = R_arm.getArray()
    L_leg_nodes = L_leg.getArray()
    R_leg_nodes = R_leg.getArray()
    spine_nodes = spine.getArray()
    hip_nodes   = hip.getArray()
    head_nodes  = head.getArray()


    L_arm_nodes_name = L_arm.getName()
    R_arm_nodes_name = R_arm.getName()
    L_leg_nodes_name = L_leg.getName()
    R_leg_nodes_name = R_leg.getName()
    spine_nodes_name = spine.getName()
    hip_nodes_name = hip.getName()
    head_nodes_name = head.getName()


    builder = build.build()

    builder.createSpine(spine_nodes, spine_nodes_name)
    builder.createHip(hip_nodes, hip_nodes_name)
    builder.createHead(head_nodes, head_nodes_name)

    builder.createArm(L_arm_nodes, L_arm_nodes_name, 0.5)
    builder.createArm(R_arm_nodes, R_arm_nodes_name, 0.5)

    builder.createLeg(L_leg_nodes, L_leg_nodes_name, -0.5)
    builder.createLeg(R_leg_nodes, R_leg_nodes_name, -0.5)

'''
