import hou

def getNodeGroupByName( rig, name ):
    for nodeGroup in rig.nodeGroups():
        if nodeGroup.name() == name:
            return nodeGroup