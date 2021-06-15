import hou

import ibra_shar.build
reload(ibra_shar.build)

import ibra_shar.constrain
reload(ibra_shar.constrain)

import ibra_shar.control
reload(ibra_shar.control)

################################
# LOAD MESH & RIG FROM DISK
################################

path = hou.expandString("C:/Users/Administrator/devel-hou")
hou.hipFile.merge(path + "/" + "charac.hiplc")

################################
# PROCEDURAL RIGGING BEGIN EXEC
################################

rig = hou.node('/obj/charac')

L_shoulder = hou.node('/obj/charac/L_shoulder_bone0')
L_arm = hou.node('/obj/charac/L_arm_bone0')
L_forearm = hou.node('/obj/charac/L_forearm_bone0')
L_hand = hou.node('/obj/charac/L_hand_bone0')
L_twist = hou.node('/obj/charac/L_twist_bone0')
L_arm = [L_shoulder, L_arm, L_forearm, L_hand, L_twist]

R_shoulder = hou.node('/obj/charac/R_shoulder_bone0')
R_arm = hou.node('/obj/charac/R_arm_bone0')
R_forearm = hou.node('/obj/charac/R_forearm_bone0')
R_hand = hou.node('/obj/charac/R_hand_bone0')
R_twist = hou.node('/obj/charac/R_twist_bone0')
R_arm = [R_shoulder, R_arm, R_forearm, R_hand, R_twist]

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

ibra_shar.build.createArm(rig, L_arm, "arm", 0.5)
ibra_shar.build.createArm(rig, R_arm, "arm", 0.5)
ibra_shar.build.createLeg(rig, L_leg, "leg", 0.5)
ibra_shar.build.createLeg(rig, R_leg, "leg", 0.5)
ibra_shar.build.createSpine(rig, spines, "spine")
ibra_shar.build.createHip(rig, hips, "hips")
