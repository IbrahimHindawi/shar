import hou

def getNodeGroupByName( rig, name ):
    for nodeGroup in rig.nodeGroups():
        if nodeGroup.name() == name:
            return nodeGroup
        else:
            # print("Node Group: " + name + " not found! Creating one...")
            return rig.addNodeGroup(name)
            return None
