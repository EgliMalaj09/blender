"""Shot A — Seedance 2.5 blockout test (5 s product dolly-in + figure cross).

Builds a clean grey-box scene, animates the camera, and renders a reference
clip for Seedance 2.5 reference-to-video. Targets Blender 5.x.

Run headless:
    blender -b -P shots/shotA/build.py -- --variant grey
    blender -b -P shots/shotA/build.py -- --variant colour
Options:
    --variant grey|colour   grey = greys + white hero; colour = one flat colour per thing
    --out PATH              output .mp4 (default: shots/shotA/renders/blockout_<variant>.mp4)
    --frames a,b,c          render only these frames as PNG stills (quick check, no mp4)
    --no-render             build the scene only (useful from Blender MCP / the UI)

From Blender MCP / the Text Editor: exec this file, then call
    build(variant="grey") and optionally render(out_path)

Shot spec (all numbers are the contract — change them here, not in the prompt):
    5.0 s @ 24 fps = 120 frames, 1280x720 (16:9), 35 mm lens
    f1-10    hold on wide: camera 4.0 m from product, 1.25 m high
    f10-120  ease-in/ease-out dolly to 1.9 m from product, 1.10 m high
    f36-108  (1.5-4.5 s) capsule figure crosses left->right behind the table,
             entering and leaving frame (off-screen at f1 and f120)
    Hero product (white) on a table at frame centre the whole time.
"""

import math
import os
import sys

import bpy

FPS = 24
FRAMES = 120
RES = (1280, 720)
LENS_MM = 35

# name: (grey-variant RGB, colour-variant RGB, what it stands for)
PALETTE = {
    "floor":   ((0.22, 0.22, 0.22), (0.10, 0.14, 0.30), "floor"),
    "wall":    ((0.34, 0.34, 0.34), (0.80, 0.55, 0.30), "back wall"),
    "table":   ((0.14, 0.14, 0.14), (0.40, 0.22, 0.10), "wooden table"),
    "product": ((1.0, 1.0, 1.0), (1.0, 1.0, 1.0), "HERO product (bottle)"),
    "figure":  ((0.55, 0.55, 0.55), (0.90, 0.35, 0.05), "person walking (placeholder)"),
}
SKY = (0.78, 0.80, 0.82)


def _color(name, variant):
    grey, colour, _ = PALETTE[name]
    return (*(grey if variant == "grey" else colour), 1.0)


def _reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def _obj(op, name, variant, key, **kw):
    op(**kw)
    ob = bpy.context.active_object
    ob.name = name
    ob.color = _color(key, variant)
    return ob


def build(variant="grey"):
    _reset()
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 1, FRAMES
    scene.render.resolution_x, scene.render.resolution_y = RES
    scene.render.resolution_percentage = 100

    # --- set (real-world metres) ---
    floor = _obj(bpy.ops.mesh.primitive_plane_add, "SET_Floor", variant, "floor", size=30)
    wall = _obj(bpy.ops.mesh.primitive_cube_add, "SET_BackWall", variant, "wall",
                location=(0, 6, 2), scale=(15, 0.1, 2))
    table = _obj(bpy.ops.mesh.primitive_cube_add, "SET_Table", variant, "table",
                 location=(0, 0, 0.375), scale=(0.6, 0.45, 0.375))
    product = _obj(bpy.ops.mesh.primitive_cylinder_add, "HERO_Product", variant, "product",
                   radius=0.07, depth=0.30, location=(0, 0, 0.90))

    # --- legless capsule figure (avoids copied stiff limb motion) ---
    _obj(bpy.ops.mesh.primitive_cylinder_add, "FIG_Body", variant, "figure",
         radius=0.22, depth=1.2, location=(0, 0, 0.75))
    body = bpy.context.active_object
    _obj(bpy.ops.mesh.primitive_uv_sphere_add, "FIG_Head", variant, "figure",
         radius=0.16, location=(0, 0, 1.55))
    head = bpy.context.active_object
    bpy.ops.object.select_all(action="DESELECT")
    body.select_set(True)
    head.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    figure = body
    figure.name = "FIG_Walker"
    walk_y = 1.3
    # off-screen left until f36, crosses at constant speed, off-screen right from f108
    for frame, x in ((1, -3.2), (36, -3.2), (108, 3.2), (FRAMES, 3.2)):
        figure.location = (x, walk_y, 0.75)  # origin is at body centre
        figure.keyframe_insert("location", frame=frame)
    _set_linear(figure, (36, 108))

    # --- camera + target empty ---
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0.92))
    target = bpy.context.active_object
    target.name = "EMPTY_CamTarget_ShotA"
    bpy.ops.object.camera_add(location=(0, -4.0, 1.25))
    cam = bpy.context.active_object
    cam.name = "CAM_ShotA_Dolly"
    cam.data.lens = LENS_MM
    cam.data.sensor_width = 36
    trk = cam.constraints.new("TRACK_TO")
    trk.target = target
    trk.track_axis = "TRACK_NEGATIVE_Z"
    trk.up_axis = "UP_Y"
    scene.camera = cam
    for frame, loc in ((1, (0, -4.0, 1.25)), (10, (0, -4.0, 1.25)), (FRAMES, (0, -1.9, 1.10))):
        cam.location = loc
        cam.keyframe_insert("location", frame=frame)
    # Bezier (Blender default) gives the ease-in/ease-out on the 10->120 dolly.

    # --- Workbench look: flat, no overlays, plain sky ---
    scene.render.engine = "BLENDER_WORKBENCH"
    sh = scene.display.shading
    sh.light = "STUDIO"
    sh.color_type = "OBJECT"
    sh.show_cavity = False
    sh.show_shadows = True
    sh.show_object_outline = False
    sh.show_specular_highlight = False
    scene.render.film_transparent = False
    world = bpy.data.worlds.new("World") if scene.world is None else scene.world
    scene.world = world
    world.color = SKY
    scene.view_settings.view_transform = "Standard"
    scene.render.use_stamp = False

    scene.frame_set(1)
    print_legend(variant)
    return scene


def _set_linear(ob, frames):
    """Set LINEAR interpolation on keys at the given frames (Blender 4.4+/5.x slotted actions)."""
    ad = ob.animation_data
    if not ad or not ad.action:
        return
    fcurves = []
    try:  # Blender 5.x layered actions
        from bpy_extras import anim_utils
        cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
        fcurves = list(cb.fcurves) if cb else []
    except Exception:
        fcurves = list(getattr(ad.action, "fcurves", []))
    for fc in fcurves:
        for kp in fc.keyframe_points:
            if int(round(kp.co.x)) in frames:
                kp.interpolation = "LINEAR"


def print_legend(variant):
    print(f"\n=== Shot A blockout legend ({variant}) — paste into the Seedance prompt ===")
    for key, (g, c, meaning) in PALETTE.items():
        rgb = g if variant == "grey" else c
        print(f"  {key:8s} rgb{tuple(round(v, 2) for v in rgb)} = {meaning}")
    print(f"  sky      rgb{SKY} = plain background placeholder\n")


def render(out_path):
    scene = bpy.context.scene
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img = scene.render.image_settings
    if hasattr(img, "media_type"):  # Blender 5.x: must be set before file_format
        img.media_type = "VIDEO"
    img.file_format = "FFMPEG"
    ff = scene.render.ffmpeg
    ff.format = "MPEG4"
    ff.codec = "H264"
    ff.constant_rate_factor = "HIGH"
    ff.audio_codec = "NONE"
    scene.render.filepath = out_path
    bpy.ops.render.render(animation=True)
    print(f"Rendered {out_path}")


def render_stills(frames, out_dir):
    scene = bpy.context.scene
    os.makedirs(out_dir, exist_ok=True)
    img = scene.render.image_settings
    if hasattr(img, "media_type"):
        img.media_type = "IMAGE"
    img.file_format = "PNG"
    for f in frames:
        scene.frame_set(f)
        scene.render.filepath = os.path.join(out_dir, f"frame_{f:03d}.png")
        bpy.ops.render.render(write_still=True)
    print(f"Stills written to {out_dir}")


def _args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    opts = {"variant": "grey", "out": None, "frames": None, "render": True}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--variant":
            opts["variant"] = argv[i + 1]; i += 1
        elif a == "--out":
            opts["out"] = argv[i + 1]; i += 1
        elif a == "--frames":
            opts["frames"] = [int(x) for x in argv[i + 1].split(",")]; i += 1
        elif a == "--no-render":
            opts["render"] = False
        i += 1
    if opts["variant"] not in ("grey", "colour"):
        raise SystemExit("--variant must be grey or colour")
    return opts


def _here():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:  # exec'd from MCP / Text Editor
        return os.getcwd()


if __name__ == "__main__":
    o = _args()
    build(o["variant"])
    renders = os.path.join(_here(), "renders")
    if o["frames"]:
        render_stills(o["frames"], os.path.join(renders, f"stills_{o['variant']}"))
    elif o["render"] and bpy.app.background:
        render(o["out"] or os.path.join(renders, f"blockout_{o['variant']}.mp4"))
