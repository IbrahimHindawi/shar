import hou
import importlib

import shar.build
importlib.reload(shar.build)

import shar.constrain
importlib.reload(shar.constrain)

import shar.control
importlib.reload(shar.control)

import shar.color
importlib.reload(shar.color)

################################
# LOAD MESH & RIG FROM DISK
################################

def import_model():
    path = "$" + "HIP"
    expanded = hou.expandString(path)
    hou.hipFile.merge(expanded + '/' + "charac.hiplc")


################################
# PROCEDURAL RIGGING BEGIN EXEC
################################

def execute_procedural_rigging_process():
    rig = hou.node('/obj/charac')

    L_shoulder = hou.node('/obj/charac/L_shoulder_bone0')
    L_arm = hou.node('/obj/charac/L_arm_bone0')
    L_forearm = hou.node('/obj/charac/L_forearm_bone0')
    L_hand = hou.node('/obj/charac/L_hand_bone0')
    L_twist = hou.node('/obj/charac/L_twist_bone0')
    L_arm = [L_shoulder, L_arm, L_forearm, L_hand, L_twist]

    L_hand = hou.node('/obj/charac/L_hand_bone0')

    R_shoulder = hou.node('/obj/charac/R_shoulder_bone0')
    R_arm = hou.node('/obj/charac/R_arm_bone0')
    R_forearm = hou.node('/obj/charac/R_forearm_bone0')
    R_hand = hou.node('/obj/charac/R_hand_bone0')
    R_twist = hou.node('/obj/charac/R_twist_bone0')
    R_arm = [R_shoulder, R_arm, R_forearm, R_hand, R_twist]

    R_hand = hou.node('/obj/charac/R_hand_bone0')

    L_thigh = hou.node('/obj/charac/L_thigh_bone0')
    L_shin = hou.node('/obj/charac/L_shin_bone0')
    L_foot = hou.node('/obj/charac/L_foot_bone0')
    L_toe = hou.node('/obj/charac/L_toe_bone0')
    L_legtwist = hou.node('/obj/charac/L_legtwist_bone0')
    L_leg = [L_thigh, L_shin, L_foot, L_toe, L_legtwist]

    R_thigh = hou.node('/obj/charac/R_thigh_bone0')
    R_shin = hou.node('/obj/charac/R_shin_bone0')
    R_foot = hou.node('/obj/charac/R_foot_bone0')
    R_toe = hou.node('/obj/charac/R_toe_bone0')
    R_legtwist = hou.node('/obj/charac/R_legtwist_bone0')
    R_leg = [R_thigh, R_shin, R_foot, R_toe, R_legtwist]

    first_spine = hou.node('/obj/charac/spine_bone0')
    second_spine = hou.node('/obj/charac/spine_bone1')
    third_spine = hou.node('/obj/charac/spine_bone2')
    fourth_spine = hou.node('/obj/charac/spine_bone3')
    fifth_spine = hou.node('/obj/charac/spine_bone4')
    spines = [first_spine, second_spine, third_spine, fourth_spine, fifth_spine]

    hip = hou.node('/obj/charac/hip_bone0')
    hips = [hip]

    shar.build.initialize(rig)
    
    shar.build.createArm(rig, L_arm, "arm", shar.color.red)
    shar.build.createArm(rig, R_arm, "arm", shar.color.blue)
    
    shar.build.createFingers(rig, L_hand, "hand", shar.color.red)
    shar.build.createFingers(rig, R_hand, "hand", shar.color.blue)
    
    shar.build.createLeg(rig, L_leg, "leg", shar.color.red)
    shar.build.createLeg(rig, R_leg, "leg", shar.color.blue)
    
    shar.build.createSpine(rig, spines, "spine")
    shar.build.createHip(rig, hips, "hips")

import_model()
execute_procedural_rigging_process()
