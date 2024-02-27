import bpy
from HumGen3D.common import is_part_of_human
from HumGen3D import Human

active_object = bpy.context.active_object

# Use HumanGen3D to check if this object is a part of HumanGen plugin body
if is_part_of_human(active_object):
    print("Current object is a part of HumanGen plugin body")

human = Human.from_existing(active_object)

fileName = "filepath.txt"
myfile = open(fileName, mode="r")
data = myfile.readlines()
myfile.close()

data = list(map(lambda x: float(x), data))

# List component Body of HumanGen3D
for i in range(len(human.body.keys)):
    bodyname = human.body.keys[i].name
    if bodyname == "muscular" or bodyname == "overweight":
        if bodyname == "muscular":
            human.body.keys[i].set_without_update(data[0])
        else:
            human.body.keys[i].set_without_update(data[0])

index = 2
# Next with component Face
for i in range(len(human.face.keys)):
    facename = human.face.keys[i].name
    if (not facename.find("ear")) or (not facename.find("Eye Scale")):
        continue
    human.face.keys[i].set_without_update(data[index])
    index += 1
# Update above changes
human.keys.update_human_from_key_change()

# Convert hair to haircards, with inclue Mesh, after that we can render hair on 3D model
human.hair.regular_hair.convert_to_haircards(quality="high", context=bpy.context)

# Select all object in Hierachy
bpy.ops.object.select_all(action="SELECT")
