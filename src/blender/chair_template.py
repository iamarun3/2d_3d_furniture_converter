import bpy
import sys
import argparse

# ------------------------
# READ PARAMETERS FROM CLI
# ------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--seat_width", type=float, required=True)
parser.add_argument("--seat_depth", type=float, required=True)
parser.add_argument("--leg_height", type=float, required=True)
parser.add_argument("--back_height", type=float, required=True)

args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])

params = {
    "seat_width": args.seat_width,
    "seat_depth": args.seat_depth,
    "leg_height": args.leg_height,
    "back_height": args.back_height,
    "color": (0.6, 0.3, 0.1, 1)   # wooden color
}

# ------------------------
# CREATE CHAIR
# ------------------------

def create_chair(params):

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Material
    mat = bpy.data.materials.new(name="ChairMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = params["color"]

    seat_thickness = 0.15
    leg_thickness = 0.08
    back_thickness = 0.12

    # ------------------
    # Seat
    # ------------------
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, params["leg_height"]))
    seat = bpy.context.object
    seat.scale = (params["seat_width"], params["seat_depth"], seat_thickness)
    seat.data.materials.append(mat)

        # ------------------
    # Slatted Backrest
    # ------------------

    slat_count = 6
    slat_thickness = 0.05
    slat_gap = params["back_height"] / (slat_count + 1)

    back_y = -params["seat_depth"] + 0.05
    bottom_z = params["leg_height"] + slat_gap

    for i in range(slat_count):
        z = bottom_z + i * slat_gap

        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(0, back_y, z)
        )
        slat = bpy.context.object
        slat.scale = (params["seat_width"], slat_thickness, slat_thickness)
        slat.data.materials.append(mat)


    # ------------------
    # Legs (aligned to seat corners)
    # ------------------
    x_offset = params["seat_width"] - leg_thickness
    y_offset = params["seat_depth"] - leg_thickness

    for x in [-x_offset, x_offset]:
        for y in [-y_offset, y_offset]:
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(x, y, params["leg_height"] / 2)
            )
            leg = bpy.context.object
            leg.scale = (leg_thickness, leg_thickness, params["leg_height"])
            leg.data.materials.append(mat)

        # ------------------
    # Armrests + Supports
    # ------------------

    arm_height = params["leg_height"] + params["back_height"] * 0.35
    arm_length = params["seat_depth"] * 0.9
    arm_thickness = 0.07

    x_arm_offset = params["seat_width"] - arm_thickness
    y_arm_center = params["seat_depth"] * 0.1

    # Left armrest (horizontal)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(-x_arm_offset, y_arm_center, arm_height)
    )
    left_arm = bpy.context.object
    left_arm.scale = (arm_thickness, arm_length, arm_thickness)
    left_arm.data.materials.append(mat)

    # Right armrest (horizontal)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x_arm_offset, y_arm_center, arm_height)
    )
    right_arm = bpy.context.object
    right_arm.scale = (arm_thickness, arm_length, arm_thickness)
    right_arm.data.materials.append(mat)

    # --------
    # Arm supports (vertical bars)
    # --------
    support_height = arm_height - params["leg_height"]
    support_thickness = 0.06

    # Front left support
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(-x_arm_offset, y_arm_center + arm_length / 2, params["leg_height"] + support_height / 2)
    )
    sup_fl = bpy.context.object
    sup_fl.scale = (support_thickness, support_thickness, support_height)
    sup_fl.data.materials.append(mat)

    # Front right support
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x_arm_offset, y_arm_center + arm_length / 2, params["leg_height"] + support_height / 2)
    )
    sup_fr = bpy.context.object
    sup_fr.scale = (support_thickness, support_thickness, support_height)
    sup_fr.data.materials.append(mat)

    # Back left support
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(-x_arm_offset, y_arm_center - arm_length / 2, params["leg_height"] + support_height / 2)
    )
    sup_bl = bpy.context.object
    sup_bl.scale = (support_thickness, support_thickness, support_height)
    sup_bl.data.materials.append(mat)

    # Back right support
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x_arm_offset, y_arm_center - arm_length / 2, params["leg_height"] + support_height / 2)
    )
    sup_br = bpy.context.object
    sup_br.scale = (support_thickness, support_thickness, support_height)
    sup_br.data.materials.append(mat)


    # Export GLB
    bpy.ops.export_scene.gltf(
        filepath="C:/Users/HP/Desktop/ai_generated_chair.glb",
        export_format='GLB'
    )

    print("💾 Improved AI chair exported as GLB")



create_chair(params)
