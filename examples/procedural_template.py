import hou
import importlib
import shar
importlib.reload(shar)

character_name = "charac"

def get_node(character_name, node_name):
    return hou.node('/obj/'+character_name+'/'+node_name)

def import_model():
    path = "$" + "HIP"
    expanded = hou.expandString(path)
    hou.hipFile.merge(expanded + '/' + character_name + ".hiplc")

def execute_procedural_rigging_process():
    rig = hou.node('/obj/'+character_name)
    L_arm = [ 
        get_node(character_name, 'L_shoulder_bone0'),
        get_node(character_name, 'L_arm_bone0'),
        get_node(character_name, 'L_forearm_bone0'),
        get_node(character_name, 'L_hand_bone0'),
        get_node(character_name, 'L_twist_bone0')
    ]

    R_arm = [ 
        get_node(character_name, 'R_shoulder_bone0'),
        get_node(character_name, 'R_arm_bone0'),
        get_node(character_name, 'R_forearm_bone0'),
        get_node(character_name, 'R_hand_bone0'),
        get_node(character_name, 'R_twist_bone0')
    ]

    L_leg = [ 
        get_node(character_name, 'L_thigh_bone0'),
        get_node(character_name, 'L_shin_bone0'),
        get_node(character_name, 'L_foot_bone0'),
        get_node(character_name, 'L_toe_bone0'),
        get_node(character_name, 'L_legtwist_bone0')
    ]

    R_leg = [ 
        get_node(character_name, 'R_thigh_bone0'),
        get_node(character_name, 'R_shin_bone0'),
        get_node(character_name, 'R_foot_bone0'),
        get_node(character_name, 'R_toe_bone0'),
        get_node(character_name, 'R_legtwist_bone0')
    ]

    spines = [
        get_node(character_name, 'spine_bone0'),
        get_node(character_name, 'spine_bone1'),
        get_node(character_name, 'spine_bone2'),
        get_node(character_name, 'spine_bone3'),
        get_node(character_name, 'spine_bone4'),
    ]

    hips = [
        get_node(character_name, 'hip_bone0')
    ]

    shar.build.initialize(rig)

    shar.build.createSpine(rig, spines, "spine")
    shar.build.createHip(rig, hips, "hips")
    
    shar.build.createArm(rig, L_arm, "arm", shar.color.red)
    shar.build.createArm(rig, R_arm, "arm", shar.color.blue)
    
    shar.build.createFingers(rig, get_node(character_name, 'L_hand_bone0'), "hand", shar.color.red)
    shar.build.createFingers(rig, get_node(character_name, 'R_hand_bone0'), "hand", shar.color.blue)
    
    shar.build.createLeg(rig, L_leg, "leg", shar.color.red)
    shar.build.createLeg(rig, R_leg, "leg", shar.color.blue)
    

import_model()
execute_procedural_rigging_process()
