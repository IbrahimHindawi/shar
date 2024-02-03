import hou
import importlib
import sys
import shar
importlib.reload(shar)

character_name = 'charac'

def import_character(character_name):
    hou.hipFile.merge(hou.expandString('$' + 'HIP')+ '/' + character_name + '.hiplc')

def get_node(rig, node_name):
    return hou.node(rig.path()+'/'+node_name)

def rigging(rig):
    L_arm = [ 
        get_node(rig, 'L_shoulder_bone0'),
        get_node(rig, 'L_arm_bone0'),
        get_node(rig, 'L_forearm_bone0'),
        get_node(rig, 'L_hand_bone0'),
        get_node(rig, 'L_twist_bone0')
    ]

    R_arm = [ 
        get_node(rig, 'R_shoulder_bone0'),
        get_node(rig, 'R_arm_bone0'),
        get_node(rig, 'R_forearm_bone0'),
        get_node(rig, 'R_hand_bone0'),
        get_node(rig, 'R_twist_bone0')
    ]

    L_leg = [ 
        get_node(rig, 'L_thigh_bone0'),
        get_node(rig, 'L_shin_bone0'),
        get_node(rig, 'L_foot_bone0'),
        get_node(rig, 'L_toe_bone0'),
        get_node(rig, 'L_legtwist_bone0')
    ]

    R_leg = [ 
        get_node(rig, 'R_thigh_bone0'),
        get_node(rig, 'R_shin_bone0'),
        get_node(rig, 'R_foot_bone0'),
        get_node(rig, 'R_toe_bone0'),
        get_node(rig, 'R_legtwist_bone0')
    ]

    head = [ 
        get_node(rig, 'neck_bone0'),
        get_node(rig, 'head_bone0'),
    ]

    spines = [
        get_node(rig, 'spine_bone0'),
        get_node(rig, 'spine_bone1'),
        get_node(rig, 'spine_bone2'),
        get_node(rig, 'spine_bone3'),
        get_node(rig, 'spine_bone4'),
        # get_node(rig, 'hip_bone0'),
    ]

    shar.build.initialize(rig)

    shar.build.createHeadAndNeck(rig, head, "head")

    shar.build.createSpine(rig, spines)
    
    shar.build.createArm(rig, L_arm, 'arm', shar.color.red)
    shar.build.createFingers(rig, get_node(rig, 'L_hand_bone0'), 'hand', shar.color.red)

    shar.build.createArm(rig, R_arm, 'arm', shar.color.blue)
    shar.build.createFingers(rig, get_node(rig, 'R_hand_bone0'), 'hand', shar.color.blue)
    
    shar.build.createLeg(rig, L_leg, 'leg', shar.color.red)
    shar.build.createLeg(rig, R_leg, 'leg', shar.color.blue)
    
def procedural_rig_execute():
    print('x')
    import_character(character_name)
    rigging(hou.node('/obj/'+character_name))
