# Blender-A3DA
Project Diva A3DA stage animation importer for Blender (somewhat functional).



https://github.com/user-attachments/assets/c88a75a4-f3ec-49e7-9f21-32b25da4eac8

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
