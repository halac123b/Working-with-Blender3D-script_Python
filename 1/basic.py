import bpy

# Object đang được chọn trong Hierachy
active_object = bpy.context.active_object
print(active_object.name)
