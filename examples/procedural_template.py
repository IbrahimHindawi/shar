import hou
import importlib
import shar
importlib.reload(shar)

character_name = "charac"

def import_model():
    path = "$" + "HIP"
    expanded = hou.expandString(path)
    hou.hipFile.merge(expanded + '/' + character_name + ".hiplc")

def execute_procedural_rigging_process():
    rig = hou.node('/obj/'+character_name)
    # bones
    L_shoulder = hou.node('/obj/'+character_name+'/L_shoulder_bone0')
    L_arm = hou.node('/obj/'+character_name+'/L_arm_bone0')
    L_forearm = hou.node('/obj/'+character_name+'/L_forearm_bone0')
    L_hand = hou.node('/obj/'+character_name+'/L_hand_bone0')
    L_twist = hou.node('/obj/'+character_name+'/L_twist_bone0')
    L_arm = [L_shoulder, L_arm, L_forearm, L_hand, L_twist]

    L_hand = hou.node('/obj/'+character_name+'/L_hand_bone0')

    R_shoulder = hou.node('/obj/'+character_name+'/R_shoulder_bone0')
    R_arm = hou.node('/obj/'+character_name+'/R_arm_bone0')
    R_forearm = hou.node('/obj/'+character_name+'/R_forearm_bone0')
    R_hand = hou.node('/obj/'+character_name+'/R_hand_bone0')
    R_twist = hou.node('/obj/'+character_name+'/R_twist_bone0')
    R_arm = [R_shoulder, R_arm, R_forearm, R_hand, R_twist]

    R_hand = hou.node('/obj/'+character_name+'/R_hand_bone0')

    L_thigh = hou.node('/obj/'+character_name+'/L_thigh_bone0')
    L_shin = hou.node('/obj/'+character_name+'/L_shin_bone0')
    L_foot = hou.node('/obj/'+character_name+'/L_foot_bone0')
    L_toe = hou.node('/obj/'+character_name+'/L_toe_bone0')
    L_legtwist = hou.node('/obj/'+character_name+'/L_legtwist_bone0')
    L_leg = [L_thigh, L_shin, L_foot, L_toe, L_legtwist]

    R_thigh = hou.node('/obj/'+character_name+'/R_thigh_bone0')
    R_shin = hou.node('/obj/'+character_name+'/R_shin_bone0')
    R_foot = hou.node('/obj/'+character_name+'/R_foot_bone0')
    R_toe = hou.node('/obj/'+character_name+'/R_toe_bone0')
    R_legtwist = hou.node('/obj/'+character_name+'/R_legtwist_bone0')
    R_leg = [R_thigh, R_shin, R_foot, R_toe, R_legtwist]

    spine0 = hou.node('/obj/'+character_name+'/spine_bone0')
    spine1 = hou.node('/obj/'+character_name+'/spine_bone1')
    spine2 = hou.node('/obj/'+character_name+'/spine_bone2')
    spine3 = hou.node('/obj/'+character_name+'/spine_bone3')
    spine4 = hou.node('/obj/'+character_name+'/spine_bone4')
    spines = [ spine0, spine1, spine2, spine3, spine4 ]

    hips = [hou.node('/obj/'+character_name+'/hip_bone0')]

    shar.build.initialize(rig)

    shar.build.createSpine(rig, spines, "spine")
    shar.build.createHip(rig, hips, "hips")
    
    shar.build.createArm(rig, L_arm, "arm", shar.color.red)
    shar.build.createArm(rig, R_arm, "arm", shar.color.blue)
    
    shar.build.createFingers(rig, L_hand, "hand", shar.color.red)
    shar.build.createFingers(rig, R_hand, "hand", shar.color.blue)
    
    shar.build.createLeg(rig, L_leg, "leg", shar.color.red)
    shar.build.createLeg(rig, R_leg, "leg", shar.color.blue)
    

import_model()
execute_procedural_rigging_process()
