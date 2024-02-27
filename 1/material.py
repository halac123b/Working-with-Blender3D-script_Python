import bpy


def InteractMaterial():
    # Get the material named "human" in Hierachy
    humanMaterial = bpy.data.materials.get(".Human")

    if humanMaterial is not None:
        # Get the node tree of the material
        nodes = humanMaterial.node_tree.nodes
        # Clear all nodes
        nodes.clear()

        # Create a new ShaderNodeTexImage node
        texture_node = nodes.new(type="ShaderNodeTexImage")

        # Load texture image
        filepath = "E:/Duy_Ha/Avatar3D/uv_images/0b2cb0bf703c.png"
        img = bpy.data.images.load(filepath)

        # Set image texture as embedded
        img.pack()
        # Assign image texture to node
        texture_node.image = img

        # In order to show ShaderNodeTexImage above, we need to create 2 more nodes
        output_node = nodes.new(type="ShaderNodeOutputMaterial")
        principled_node = nodes.new(type="ShaderNodeBsdfPrincipled")

        # Link object of node_tree to link node
        links = humanMaterial.node_tree.links
        # Link texture_node to principled_node, then link principled_node to output_node
        link = links.new(texture_node.outputs[0], principled_node.inputs[0])
        link = links.new(principled_node.outputs[0], output_node.inputs[0])
