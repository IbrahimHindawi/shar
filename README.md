# SHAR
Single Hierarchy Auto Rigger  

Synopsis:  
Auto Rigging system that takes a hip and a python file as input

Installation:  
- clone repo into your `$HOUDINI_USER_PREF_DIR`  
- create file `$HOUDINI_USER_PREF_DIR/packages/packages.json`
- configure `packages.json` to find the package:
```
{
    "package_path": [
           "$HOUDINI_USER_PREF_DIR/shar"
    ]
}
```

Workflow:
- create a hip file and add your geometry + bones to a subnet
- give the same name to your subnet and hip
- create a `rigmodule.py` file in the same directory as your hip
- create a new hip & drop a `sharnet` hda in your scene
- input your character name
- hit the 'Rig' button
- once the rig is complete, create your hda

Quickstart:  
- open shar/examples/charac.autorig.hiplc and hit the `Rig` button
- shar/examples/charac.anim.hiplc shows the animation workflow
