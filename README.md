# Blender-A3DA
Project Diva A3DA stage animation importer for Blender (somewhat functional).

Im working on this, but I'll take some time to polish it before uploading it.
This version is realy old... I wouldn't recommend using it. This doesn't reflect my current version!




https://github.com/user-attachments/assets/d781be2a-18ee-444f-9dd8-1af4e50a5f9b




Another example, Common World Domination
https://youtu.be/QDQPE-ZaXfo

Gaikotsu Gakudan To Riria https://youtu.be/t4o9OkwPAO4

Object instances & Change Field commands - [Ghost Rule](https://youtu.be/YU3VF_tHu4g)

## Usage
- Import the stage model, and apply all rotations. The script will change all object names to uppercase, so make sure no conflicts will occur. If needed, rename the meshes.
- Load the script in the blender scripting tab, set the path to your A3DA file, and hit run.
- Controllers will be created for each object declared in the A3DA, and the script will try to match the controllers to existing objects on the scene.
- The framerate for every (i think) PV is 60fps.
- Its possible to import multiply A3DA files, just load them one after the other.

## Limits
Some transformations are weird after importing, and i dont know why. Some objects will be fixed by inverting their Z rotation, I'm still not sure why this happens.

Right now supports only stage object animation.
It does not support camera anim, morphs, lights, instance animation, and HRC bone anim.

This is my first time trying to write a Blender script, so don't expect this to work perfectly.
Im open to any feedback!

## Next Steps
I'll fix whatever is causing the weird rotations. 
I plant to keep working on this to support at least: 
DivaScript _change field_ commands, instance animation, and camera animation. 

A3DA animations are meant to be cyclic, it also stores interpolation data, and some kind of visibility animation. Handling this is my top priority right now. 
