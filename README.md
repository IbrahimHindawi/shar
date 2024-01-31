# SHAR
Single Hierarchy Auto Rigger  

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

Examples:  
- shar/examples/charac.autorig.hiplc shows how to generate autorig
- shar/examples/charac.anim.hiplc shows the animation workflow
