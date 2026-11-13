"""Shot C — Seedance 2.5 blockout: two-person café conversation, coverage test.

15 s, 16:9, 10 cuts: 7 "real" setups + 3 quick inserts, to see how much shot
coverage Seedance 2.5 can hold in one generation. Live-action, handheld feel.
Targets Blender 5.x, Workbench engine.

Run headless:
    blender -b -P shots/shotC/build.py -- --variant colour
    blender -b -P shots/shotC/build.py -- --variant grey
Options: --variant grey|colour, --out PATH, --frames a,b,c, --no-render (as Shot A/B).

Layout (metres). Round café table at the origin. 180-degree line runs along X
between the two people; EVERY camera stays on the -Y side of it.
    Person A (woman) sits at x=-0.45, faces +X (screen-left in every shot)
    Person B (man)   sits at x=+0.45, faces -X (screen-right in every shot)
    Back wall with a big street window at y=+3; counter on the left (x=-3);
    street outside: pavement + facade at y=+8, a pedestrian passes at y=+5.

Shot list (24 fps, 360 frames = 15.0 s, 1280x720):
  #   frames    sec         setup                                   lens
  1   1-48      0.0-2.0     ESTABLISHING wide from café corner,     24 mm
                            high, slow push toward the table
  2   49-84     2.0-3.5     TWO-SHOT side-on, both in profile        35 mm
  3   85-132    3.5-5.5     OTS over B's shoulder onto A (A talks)   50 mm
  4q  133-144   5.5-6.0     QUICK insert: A's cup lifts out of frame 85 mm
  5   145-192   6.0-8.0     OTS over A's shoulder onto B (B answers) 50 mm
  6q  193-204   8.0-8.5     QUICK close-up: B reacts                 85 mm
  7   205-252   8.5-10.5    CLOSE-UP A, slow push in                 85 mm
  8q  253-264   10.5-11.0   QUICK: window, pedestrian passes outside 50 mm
  9   265-312   11.0-13.0   LOW 3/4 two-shot from table height,     35 mm
                            A's back in the foreground, slow slide
  10  313-360   13.0-15.0   HIGH WIDE pull-back, ends on the café    28 mm
"""

import math
import os
import sys

import bpy

FPS = 24
FRAMES = 360
RES = (1280, 720)

# name: (grey RGBA, colour RGBA, meaning)
PALETTE = {
    "floor":   ((0.30, 0.30, 0.30, 1), (0.45, 0.30, 0.18, 1), "café floor (dark wood)"),
    "wall":    ((0.55, 0.55, 0.55, 1), (0.85, 0.80, 0.70, 1), "café walls (warm plaster)"),
    "furn":    ((0.20, 0.20, 0.20, 1), (0.30, 0.20, 0.12, 1), "wooden table and chairs"),
    "counter": ((0.40, 0.40, 0.40, 1), (0.20, 0.35, 0.30, 1), "café counter / bar"),
    "cup":     ((1.0, 1.0, 1.0, 1), (1.0, 1.0, 1.0, 1), "white coffee cups"),
    "personA": ((0.70, 0.70, 0.70, 1), (0.95, 0.50, 0.10, 1), "Person A (woman)"),
    "personB": ((0.45, 0.45, 0.45, 1), (0.15, 0.45, 0.85, 1), "Person B (man)"),
    "street":  ((0.65, 0.65, 0.65, 1), (0.60, 0.65, 0.70, 1), "street outside: pavement + buildings"),
    "walker":  ((0.85, 0.85, 0.85, 1), (0.80, 0.20, 0.60, 1), "pedestrian outside"),
}
SKY = {"grey": (0.85, 0.86, 0.88), "colour": (0.80, 0.88, 0.95)}

_MATS = {}


def _mat(key, variant):
    if key not in _MATS:
        g, c, _ = PALETTE[key]
        m = bpy.data.materials.new(f"MAT_{key}")
        m.diffuse_color = g if variant == "grey" else c
        _MATS[key] = m
    return _MATS[key]


def _finish(ob, name, key, variant, smooth=False):
    ob.name = name
    if smooth:
        bpy.ops.object.shade_smooth()
    ob.data.materials.clear()
    ob.data.materials.append(_mat(key, variant))
    return ob


def box(name, key, variant, loc, size):
    bpy.ops.mesh.primitive_cube_add(location=loc, scale=(size[0] / 2, size[1] / 2, size[2] / 2))
    return _finish(bpy.context.active_object, name, key, variant)


def cyl(name, key, variant, loc, r, h):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=48, location=loc)
    return _finish(bpy.context.active_object, name, key, variant, smooth=True)


def sphere(name, key, variant, loc, r):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=32, ring_count=16, location=loc)
    return _finish(bpy.context.active_object, name, key, variant, smooth=True)


def key_loc(ob, fl):
    for f, loc in fl:
        ob.location = loc
        ob.keyframe_insert("location", frame=f)


def key_rot(ob, fr):
    for f, rot in fr:
        ob.rotation_euler = tuple(math.radians(a) for a in rot)
        ob.keyframe_insert("rotation_euler", frame=f)


def seated_person(name, key, variant, x, facing):
    """Legless capsule, seated: torso cylinder + head, parented to a pivot at the seat."""
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(x, 0, 0.46))
    pivot = bpy.context.active_object
    pivot.name = f"FIG_{name}"
    pivot.rotation_euler = (0, 0, math.radians(0 if facing > 0 else 180))
    torso = cyl(f"FIG_{name}_Torso", key, variant, (0, 0, 0.32), 0.19, 0.64)
    head = sphere(f"FIG_{name}_Head", key, variant, (0.02, 0, 0.80), 0.12)
    for p in (torso, head):
        p.parent = pivot
    return pivot


def chair(name, variant, x, facing):
    box(f"SET_{name}_Seat", "furn", variant, (x, 0, 0.44), (0.42, 0.42, 0.04))
    box(f"SET_{name}_Back", "furn", variant, (x - 0.21 * facing, 0, 0.68), (0.04, 0.42, 0.48))
    for dx in (-0.18, 0.18):
        for dy in (-0.18, 0.18):
            box(f"SET_{name}_Leg", "furn", variant, (x + dx, dy, 0.21), (0.03, 0.03, 0.42))


def camera(name, lens, frames_locs, target_keys):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=target_keys[0][1])
    tgt = bpy.context.active_object
    tgt.name = f"EMPTY_{name}_target"
    bpy.ops.object.camera_add(location=frames_locs[0][1])
    cam = bpy.context.active_object
    cam.name = name
    cam.data.lens = lens
    cam.data.sensor_width = 36
    cam.data.clip_start = 0.02
    cam.data.clip_end = 60
    trk = cam.constraints.new("TRACK_TO")
    trk.target = tgt
    trk.track_axis = "TRACK_NEGATIVE_Z"
    trk.up_axis = "UP_Y"
    key_loc(cam, frames_locs)
    key_loc(tgt, target_keys)
    return cam


def handheld(cam, f0, f1, amp=0.004, seed=0):
    """Tiny deterministic drift keys every 6 frames for a live-action handheld feel."""
    for i, f in enumerate(range(f0, f1 + 1, 6)):
        k = seed * 7 + i
        cam.delta_location = (amp * math.sin(k * 1.7), amp * math.cos(k * 2.3), amp * math.sin(k * 3.1))
        cam.keyframe_insert("delta_location", frame=f)


# A/B head heights for targets
A_HEAD = (-0.45, 0, 1.26)
B_HEAD = (0.45, 0, 1.26)


def build(variant="grey"):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _MATS.clear()
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 1, FRAMES
    scene.render.resolution_x, scene.render.resolution_y = RES
    scene.render.resolution_percentage = 100

    # --- room: 8 m wide, from y=-4 to y=+3, 3 m high ---
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -0.5, 0))
    fl = _finish(bpy.context.active_object, "SET_Floor", "floor", variant)
    fl.scale = (8, 7, 1)
    box("SET_WallLeft", "wall", variant, (-4, -0.5, 2.25), (0.1, 7, 4.5))
    box("SET_WallRight", "wall", variant, (4, -0.5, 2.25), (0.1, 7, 4.5))
    # back wall with a window opening x[-1.6,1.6] z[0.9,2.5]
    box("SET_BackL", "wall", variant, (-2.8, 3, 2.25), (2.4, 0.1, 4.5))
    box("SET_BackR", "wall", variant, (2.8, 3, 2.25), (2.4, 0.1, 4.5))
    box("SET_BackLow", "wall", variant, (0, 3, 0.45), (3.2, 0.1, 0.9))
    box("SET_BackHigh", "wall", variant, (0, 3, 3.5), (3.2, 0.1, 2.0))
    box("SET_Counter", "counter", variant, (-3.2, 0.5, 0.55), (0.9, 3.0, 1.1))

    # --- street outside ---
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 6, -0.01))
    st = _finish(bpy.context.active_object, "SET_Street", "street", variant)
    st.scale = (30, 6, 1)
    box("SET_Facade", "street", variant, (0, 9, 4), (30, 0.5, 8))
    wbody = cyl("FIG_Walker_Body", "walker", variant, (0, 0, 0.75), 0.22, 1.2)
    whead = sphere("FIG_Walker_Head", "walker", variant, (0, 0, 1.55), 0.15)
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(-6, 5, 0))
    walker = bpy.context.active_object
    walker.name = "FIG_Walker"
    for p in (wbody, whead):
        p.parent = walker
    key_loc(walker, ((1, (-6, 5, 0)), (250, (-2.2, 5, 0)), (268, (0.6, 5, 0)), (FRAMES, (14, 5, 0))))

    # --- table, chairs, cups ---
    cyl("SET_TableTop", "furn", variant, (0, 0, 0.74), 0.40, 0.03)
    cyl("SET_TableLeg", "furn", variant, (0, 0, 0.37), 0.04, 0.72)
    chair("ChairA", variant, -0.55, +1)
    chair("ChairB", variant, +0.55, -1)
    cup_a = cyl("PROP_CupA", "cup", variant, (-0.18, -0.06, 0.80), 0.04, 0.09)
    cyl("PROP_CupB", "cup", variant, (0.18, 0.05, 0.80), 0.04, 0.09)
    # quick insert: A lifts her cup out of frame (f133-144), it is back down by f145
    key_loc(cup_a, ((1, (-0.18, -0.06, 0.80)), (136, (-0.18, -0.06, 0.80)),
                    (144, (-0.24, -0.06, 1.05)), (145, (-0.18, -0.06, 0.80))))
    # --- people ---
    a = seated_person("PersonA", "personA", variant, -0.45, +1)
    b = seated_person("PersonB", "personB", variant, 0.45, -1)
    # talking beats: small forward lean on whoever speaks
    key_rot(a, ((85, (0, 0, 0)), (100, (0, 8, 0)), (130, (0, 6, 0)), (150, (0, 0, 0)),
                (205, (0, 0, 0)), (225, (0, 7, 0)), (252, (0, 4, 0))))
    key_rot(b, ((145, (0, 0, 180)), (160, (0, 8, 180)), (190, (0, 6, 180)), (205, (0, 2, 180))))

    # --- cameras (all on the -Y side of the A-B line) ---
    cams = {}
    cams[1] = camera("CAM_01_Establish", 24,
                     ((1, (2.8, -3.4, 2.1)), (48, (2.3, -2.8, 1.9))),
                     ((1, (0, 0.3, 0.95)), (48, (0, 0.2, 0.95))))
    cams[49] = camera("CAM_02_TwoShot", 35,
                      ((49, (0.0, -2.3, 1.15)), (84, (0.0, -2.15, 1.15))),
                      ((49, (0, 0, 1.0)), (84, (0, 0, 1.0))))
    cams[85] = camera("CAM_03_OTS_onA", 50,
                      ((85, (0.95, -0.42, 1.30)), (132, (0.92, -0.40, 1.29))),
                      ((85, (-0.45, 0.02, 1.22)), (132, (-0.45, 0.02, 1.22))))
    cams[133] = camera("CAM_04q_CupInsert", 85,
                       ((133, (0.15, -0.62, 0.93)), (144, (0.15, -0.61, 0.93))),
                       ((133, (-0.18, -0.06, 0.84)), (144, (-0.18, -0.06, 0.84))))
    cams[145] = camera("CAM_05_OTS_onB", 50,
                       ((145, (-0.95, -0.42, 1.30)), (192, (-0.92, -0.40, 1.29))),
                       ((145, (0.45, 0.02, 1.22)), (192, (0.45, 0.02, 1.22))))
    cams[193] = camera("CAM_06q_CU_B", 85,
                       ((193, (-0.40, -1.10, 1.27)), (204, (-0.39, -1.08, 1.27))),
                       ((193, B_HEAD), (204, B_HEAD)))
    cams[205] = camera("CAM_07_CU_A", 85,
                       ((205, (0.45, -1.45, 1.27)), (252, (0.30, -1.10, 1.27))),
                       ((205, A_HEAD), (252, A_HEAD)))
    cams[253] = camera("CAM_08q_Window", 50,
                       ((253, (0.9, -0.6, 1.45)), (264, (0.9, -0.6, 1.45))),
                       ((253, (0.3, 5, 1.2)), (264, (0.3, 5, 1.2))))
    cams[265] = camera("CAM_09_LowThreeQuarter", 35,
                       ((265, (-1.25, -1.45, 0.85)), (312, (-0.85, -1.70, 0.85))),
                       ((265, (0.10, 0, 1.05)), (312, (0.05, 0, 1.05))))
    cams[313] = camera("CAM_10_HighWide", 28,
                       ((313, (1.2, -2.0, 2.3)), (360, (2.2, -3.6, 2.7))),
                       ((313, (0, 0.2, 0.9)), (360, (0, 0.5, 0.9))))
    for i, (f, cam) in enumerate(sorted(cams.items())):
        end = min([k for k in cams if k > f] or [FRAMES + 1]) - 1
        if not cam.name.startswith(("CAM_04q", "CAM_08q")):
            handheld(cam, f, end, seed=i)
        m = scene.timeline_markers.new(cam.name, frame=f)
        m.camera = cam
    scene.camera = cams[1]

    # --- Workbench look ---
    scene.render.engine = "BLENDER_WORKBENCH"
    sh = scene.display.shading
    sh.light = "STUDIO"
    sh.color_type = "MATERIAL"
    sh.show_cavity = False
    sh.show_shadows = True
    sh.show_object_outline = False
    sh.show_specular_highlight = False
    scene.render.film_transparent = False
    world = bpy.data.worlds.new("World") if scene.world is None else scene.world
    scene.world = world
    world.color = SKY[variant]
    scene.view_settings.view_transform = "Standard"
    scene.render.use_stamp = False

    scene.frame_set(1)
    print_legend(variant)
    return scene


def print_legend(variant):
    print(f"\n=== Shot C blockout legend ({variant}) ===")
    for key, (g, c, meaning) in PALETTE.items():
        rgba = g if variant == "grey" else c
        print(f"  {key:8s} rgb{tuple(round(v, 2) for v in rgba[:3])} = {meaning}")
    print(f"  sky      rgb{SKY[variant]} = daylight outside\n")


def render(out_path):
    scene = bpy.context.scene
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img = scene.render.image_settings
    if hasattr(img, "media_type"):
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
    opts = {"variant": "colour", "out": None, "frames": None, "render": True}
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
    except NameError:
        return os.getcwd()


if __name__ == "__main__":
    o = _args()
    build(o["variant"])
    renders = os.path.join(_here(), "renders")
    if o["frames"]:
        render_stills(o["frames"], os.path.join(renders, f"stills_{o['variant']}"))
    elif o["render"] and bpy.app.background:
        render(o["out"] or os.path.join(renders, f"blockout_{o['variant']}.mp4"))
