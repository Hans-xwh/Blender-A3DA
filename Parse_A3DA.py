import bpy


#### Input file path ###
inA3da = r"C:\path\to\your\a3da"

#I know the code is kind of a mess
#But it works (somewhat)

#Offset for all ids, so names won't overlap when using multiple a3da files. Add one to Max Id, and put it here.
idOffset = 0

#Offset all frames.
frameOffset = 0 #Parameter ignored in most cases



### Open A3da ###
print('')
print('Start')
a3daFile = open(inA3da, 'r')

#Dont change this
maxId = 0
maxFrame = 0
beginning = 0 

class DivaObj:
    def __init__(obj, id, name, parents):
        obj.id = int()
        obj.name = str()
        obj.meshName = str()
        obj.parents = []

class DivaLocate:
    def __init__(self):
        self.id = int()
        self.transform = str()
        self.axis = str()
        self.value = float()
        self.visible = int()


def cleanSceneNames():
    #print('[cleanSceneNames] All names to uppercase')
    for ob in bpy.data.objects:
        try: 
            ob.name = str(ob.name).upper()      #Needed so names on blender always (i hope) match a3da
        except:
            print('[cleanSceneNames] Failed to change name for', ob.name)
    print('[cleanSceneNames] Finished')
cleanSceneNames()


def parseName(line):
    global maxId

    
    line = line.strip()
    if not line.startswith('object.') or ('.name=' not in line and 'parent_name=' not in line) or '.tex_transform' in line:
        #print('[parseName] Line ignored:', line)
        return None
    
    if '.name=' in line:
        try:
            valueType, valuePart = line.split('=', 1)
            types = valueType.split('.')        #0:"Object" 1:id 2:"name"
            print(line)
            print('[parseName] Types:', types)
            DivaObj.id = int(types[1])
            print('[parseName] Id:', DivaObj.id)

            if maxId < DivaObj.id:
                maxId = DivaObj.id
            
            DivaObj.name = valuePart
            print('[parseName] Controll name:', DivaObj.name)
            
            DivaObj.meshName = valuePart.split('|')[-1]

            DivaObj.parents = DivaObj.name.strip(DivaObj.meshName)[:-1]
            print('[parseName] Parent:', DivaObj.parents)
            
            DivaObj.meshName = DivaObj.meshName.strip('OBJ_')
            print('[parseName] Mesh name:', DivaObj.meshName)
            

            print('')
            return DivaObj
        except Exception as ex:
            print('[parseName] Error while prosessing name')
            raise ex
        
        
''''
    try:
        valueType, valuePart = line.split('=', 1)
        types = valueType.split('.')
        DivaObj.id = int(types[1])
        values = valuePart.split('|')
        DivaObj.name = values[-1]
        DivaObj.name = DivaObj.name.strip('OBJ_')
        DivaObj.parents = values[:-1]
        DivaObj.parents = list(filter(None, DivaObj.parents))
                                                    #Need to separate the id and the parents block. Maybe we can first isolate the whole parents block, then extract the name.

        #print('[parseName] Id is:', DivaObj.id)
        #print('[parseName] Name is:', DivaObj.name)
        #print('[parseName] Parents line:', DivaObj.parents)    
        return DivaObj        
    except Exception as ex:
        print('[parseName] exception:', ex)
        return None
    '''
    

def parseSettle(line):
    global maxFrame
    global frameOffset
    global beginning

    if line.startswith('object.') and '.value=' in line and 'visibility' not in line:
        try: 
            configPart, valuePart = line.split('=', 1)
            config = configPart.split('.')

            settling = dict(id = int(config[1]), transform = config[2], axis = config[3], value = valuePart,) #Build a dictionary with the settling split as values.

            print('[parseSettle] settling is:', settling)
            return settling #dict
        except ValueError:
            print('[parseSettle] Exception')

    elif line.startswith('play_control'):
        if '.size' in line:
            line = line.split('=') #1: maxFrame
            maxFrame = int(line[1])

        elif 'begin' in line:
            line = line.split('=') #1: maxFrame
            beginning = int(line[1])
            frameOffset = beginning

        


    

def createObject(Name):
    try:
        #bpy.ops.object.empty_add(location=(0,0,0))
        #bpy.data.objects['Empty'].name = Name
        empty = bpy.data.objects.new(Name, None)
        bpy.context.scene.collection.objects.link(empty)

        if bpy.context.scene.objects.get(Name):
            print('[CreateObject] Empty', Name, 'succesfully created.')
            return
        else:
            print('[CreateObject] Reached end, but new object was not found.')
            raise Exception
    except Exception as ex:
        print('[createObject] Failed to create empty', Name, ex)
        return


def assignParent(parent, ctrlName, objName):  #Need to devide the crete empty into another function, and maybe call it befor this runs.
    try:
        
        print('[assignParent] Controll Name:', ctrlName)
        print('[assignParent] Object Name:', objName)
        print('[assignParent] Parent:', parent)
        
        if not bpy.context.scene.objects.get(parent): #Check if object exists in blender
            print('[assignParent] !!! Parent not on scene will be created:', parent)
            createObject(parent)
        if not bpy.context.scene.objects.get(ctrlName): #Check if object exists in blender
            print('[assignParent] !!! ctrlName not on scene will be created:', parent)
            createObject(ctrlName)
            
        childCtrl = bpy.context.scene.objects.get(ctrlName)
        print('[assignParent] childCtrl is:', childCtrl)
        childCtrl.parent = bpy.context.scene.objects.get(parent)
        print('[assignParent] Assigned: ', ctrlName, '->', parent)

        #Check if mesh exists, if it does assign it to its controller
        if bpy.context.scene.objects.get(objName):
            try:
                print('[assignParent] Matching object found', objName, '->', ctrlName)
                childMesh = bpy.context.scene.objects.get(objName)
                childMesh.parent = bpy.context.scene.objects.get(ctrlName)
            except Exception:
                print('Found a match, but failed to assign it', objName, '->', ctrlName)

                    
    except Exception as ex:
        print('[assignParent] Fuck xd', ex)
        raise ex
                            
        '''
        if type(parentList) == list():
            parents = parentList[-1]#so that only the last value of the list is taken into concideration
            print('[assignParent]', type(parents),'Parents:',parents)
        else:
            parents = parentList    #???

        for pName in parents:
            try:
                pName = str(pName.strip('OBJ_'))    #pName = Parent name
                print('[assignParent] passed args:', pName, '-', objName)

                if not bpy.context.scene.objects.get(pName): #Check if object exists in blender
                    print('[assignParent] Object not on scene will be created:', pName)
                    createObject(pName)
                    print('[assignParent] Object created')

                childObj = bpy.context.scene.objects.get(objName)
                childObj.parent = bpy.context.scene.objects.get(pName)
                #childObj.matrix_parent_inverse.identity()              #clear inverse? Not using inverse tho
                print('[assignParent] Assigned: ', objName, '->', pName)               
            except Exception as ex:
                print('[assignParent] Failed to assign ', objName, '->', pName)
                print('[assignParent] ', ex)
                raise ex
                '''


def setTransform(settling):
    global idOffset

    print('[setTransform] SetTransform start')
    #objName = 'OBJ_' + str(settling['id'])
    objName = nameDict[settling['id']].split('|')
    print(objName)
    objName = objName[-1].strip('OBJ_')

    try:                    #Need to change something here, as meshes will have friendly names, while controllers will have ugly names
        #, y, z = (0,0,0,)
        
        if not bpy.context.scene.objects.get(objName):
            print('[setTransform] Mesh not found, using id:', objName)
            objName = 'OBJ_' + str(settling['id'] + idOffset)
        else:
            print('[setTransform] Matching mesh found:', objName)
            
             
        if settling['transform'] == 'trans':
            print('[setTramsform] Location (XYZ)')
            
            match settling['axis']:
                case 'x':   #Diva X Axis -> Blender X Axis
                    x = float(settling['value'])
                    bpy.data.objects[objName].location.x = (x)
                    print('[setTransform] Transform X =', settling['value'])
                case 'z':   #Diva Z Axis -> Blender Y Axis
                    y = float(settling['value'])
                    bpy.data.objects[objName].location.y = (y*-1)
                    print('[setTransform] Transform Z =', settling['value'])
                case 'y':   #Diva Y Axis -> Blender Z Axis
                    z = float(settling['value'])
                    bpy.data.objects[objName].location.z = (z)
                    print('[setTransform] Transform Y =', settling['value'])

        elif settling['transform'] == 'rot':
            print('[setTramsform] Rotation (XYZ)')

            match settling['axis']:
                case 'x':
                    x = float(settling['value'])
                    print('[setTransform] rotation X =', x)
                    bpy.data.objects[objName].rotation_euler.x = (x)
                case 'z':
                    y = float(settling['value'])
                    print('[setTransform] rotation Y =', y)
                    bpy.data.objects[objName].rotation_euler.y = (y*-1)    #O quiza invertir este eje
                case 'y':
                    z = float(settling['value'])
                    print('[setTransform] rotation Z =', z)
                    bpy.data.objects[objName].rotation_euler.z = (z) #Probar dejar de invertir el eje z para Envy Cat Walk

        elif settling['transform'] == 'scale':
            print('[setTramsform] Scale (XYZ)')

            match settling['axis']:
                case 'x':
                    x = float(settling['value'])
                    print('[setTransform] scalen X =', x)
                    bpy.data.objects[objName].scale.x = (x)
                case 'z':
                    y = float(settling['value'])
                    print('[setTransform] scale Y =', y)
                    bpy.data.objects[objName].scale.y = (y)
                case 'y':
                    z = float(settling['value'])
                    print('[setTransform] scale Z =', z)
                    bpy.data.objects[objName].scale.z = (z)
        else:
            print('[setTransform] "Transform" didnt match any transformation:', settling['transform'])

    except Exception as ex:
        print('[setTransform] Failed to set transform:', settling['transform'])
        print('[setTransform] Object:', objName, 'Axis:', settling['axis'],':', settling['value'])
        print('[setTransform]', ex)
        raise Exception
    
def setKeyframe(line, nameDict):    #Change this later.
    global frameOffset
    global maxFrame

    #print('[setKeyFrame]',line)
    firstHalf, dataHalf = line.split('=', 1)

    firstHalf = firstHalf.split('.')    #1=id, 2=transType, 3=axis, 5=index?
    firstHalf[1] = int(firstHalf[1]) + idOffset
    print('[setKeyFrame]',firstHalf)

    dataHalf = dataHalf.strip('(').strip(')')
    dataHalf = dataHalf.split(',')      #0=frame, 1=value, 2=intrapolation(?)
    print('[setKeyFrame]',dataHalf)

    name = 'OBJ_' + str(firstHalf[1])
    #name = nameDict[int(name)]
    print('[setKeyFrame] name is:', name)

        #Time to set keyframes in blender
    try:
        obj = bpy.data.objects[name]
        frame = int(dataHalf[0]) + frameOffset

        '''if maxFrame < frame:
            maxFrame = frame'''

        if len(dataHalf) == 1:
            print('[setKeyFrame] Invalid frame data, defaulting to 0')
            dataHalf = [dataHalf, 0]
        
        if firstHalf[2] == 'trans':
            match firstHalf[3]:
                case 'x':
                    x = float(dataHalf[1])
                    obj.location.x = x
                    obj.keyframe_insert(data_path="location", index=0, frame=frame)     #Index: 0=X, 1=Y, 2=Z
                    print('[setKeyFrame] Correctly set x property')
                case 'z':
                    y = float(dataHalf[1])
                    obj.location.y = y*-1
                    obj.keyframe_insert(data_path="location", index=1, frame=frame)
                    print('[setKeyFrame] Correctly set y property')
                case 'y':
                    z = float(dataHalf[1])
                    obj.location.z = z
                    obj.keyframe_insert(data_path="location", index=2, frame=frame)
                    print('[setKeyFrame] Correctly set z property')
        elif firstHalf[2] == 'rot':
            match firstHalf[3]:
                case 'x':
                    x = float(dataHalf[1])
                    obj.rotation_euler.x = x
                    obj.keyframe_insert(data_path="rotation_euler", index=0, frame=frame)
                    print('[setKeyFrame] Correctly set x rotation')
                case 'z':
                    y = float(dataHalf[1])
                    obj.rotation_euler.y = y*-1
                    obj.keyframe_insert(data_path="rotation_euler", index=1, frame=frame)
                    print('[setKeyFrame] Correctly set y rotation')
                case 'y':
                    z = float(dataHalf[1])
                    obj.rotation_euler.z = z
                    obj.keyframe_insert(data_path="rotation_euler", index=2, frame=frame)
                    print('[setKeyFrame] Correctly set z rotation')
        elif firstHalf[2] == 'scale':
            match firstHalf[3]:
                case 'x':
                    x = float(dataHalf[1])
                    obj.scale.x = x
                    obj.keyframe_insert(data_path="scale", index=0, frame=frame)
                case 'z':
                    y = float(dataHalf[1])
                    obj.scale.y = y
                    obj.keyframe_insert(data_path="scale", index=1, frame=frame)
                case 'y':
                    z = float(dataHalf[1])
                    obj.scale.z = z
                    obj.keyframe_insert(data_path="scale", index=2, frame=frame)



    except Exception as ex:
        print('[setKeyFrame] Error:', ex)
        #if ex != IndexError:
        raise ex
        
    #print('[setKeyFrame] Finished')
    

### Start decoding names and parents, build id-name dictionary ###
nameDict = dict()
for line in a3daFile:
    divaObjTmp = parseName(line)
    if divaObjTmp != None:
        nameDict[int(divaObjTmp.id)] = divaObjTmp.name  #Dictionary containing id -> name

        newName = 'OBJ_' + str(divaObjTmp.id + idOffset)

        print('[main]', divaObjTmp.name)
        print('[main]', divaObjTmp.parents)
        print('[main]', divaObjTmp.meshName)
        print('[main]', divaObjTmp.id)
        print('')


        if not bpy.context.scene.objects.get(newName): #Check if object exists in blender
            print('[main] Object not on scene will be created:', newName)
            createObject(newName)      #commentout for testing
        
        #assignParent(divaObjTmp.parents, newName, divaObjTmp.meshName) #Shouldnt be called here
a3daFile.seek(0)
print("A3DA names analized")
#print(nameDict)

### Invert dictionary ###
idDict = {divaName: divaId for divaId, divaName in nameDict.items()}
print(idDict)

### Assign Parents & clear parent inverse###
for line in a3daFile:
    try:
        divaObjTmp = parseName(line)
        if divaObjTmp != None:
            newName = 'OBJ_' + str(divaObjTmp.id + idOffset)
            parentId = 'OBJ_' + str(idDict[divaObjTmp.parents] + idOffset)

            assignParent(parentId, newName, divaObjTmp.meshName)
    except KeyError:
        print('[main] No parent match found!')
        continue
a3daFile.seek(0)

### Start to decode settling & Set initial transformation. (may not be used on all PVs) ###
for line in a3daFile:
    divaSettleTmp = parseSettle(line)

    if divaSettleTmp != None:
        try:    #Time to match the ids to the Blender scene
            name = nameDict[divaSettleTmp['id']]        #Get name for the id referenced in a3da
            print('[main] name is:',name)
            print('[main] Id & Name:', divaSettleTmp['id'], name)

            setTransform(divaSettleTmp)
            print('')
        except ValueError as ex:
            print('[main] Value Error:', ex)
            print('')
a3daFile.seek(0)
        


### Decode & Set keyframes ###
for line in a3daFile:
    if '.key.' in line and '.type' not in line and '.length' not in line and 'tex_transform' not in line:
        line = line.strip()
        setKeyframe(line, nameDict)
        print('')

a3daFile.close()

print('Starting frame was:', beginning)
print('Max id was:', maxId + idOffset)
print('Max frame was:', maxFrame + frameOffset)
print('Excecution finished')




#### Notes on the a3da format ####
# key.x.type=2 --> intrapolation mode "Hermite curves (maybe)"
# key.x.data=(Frame, Value, Hermite)
#i dont like hermite curves. Ignoring this xd