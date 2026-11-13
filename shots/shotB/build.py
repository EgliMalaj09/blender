"""Shot B — Seedance 2.5 blockout: shampoo bottle in a bubble world (11 s, 9:16, 4 cuts).

Rebuilds the camera language of a bubble-macro beauty reference with our product
(opaque matte light-blue bottle, white flip cap). Four shots live in one scene,
each on its own set 10 m apart, with timeline markers switching the active camera.
Targets Blender 5.x, Workbench engine.

Run headless:
    blender -b -P shots/shotB/build.py -- --variant grey
    blender -b -P shots/shotB/build.py -- --variant colour
Options:
    --variant grey|colour   grey = greys + white hero; colour = flat proxy colours
    --out PATH              output .mp4 (default: shots/shotB/renders/blockout_<variant>.mp4)
    --frames a,b,c          render only these frames as PNG stills (quick check, no mp4)
    --no-render             build the scene only (useful from Blender MCP / the UI)

Shot spec (24 fps, 264 frames = 11.0 s, 720x1280 9:16). Units are metres;
the bottle is real size (7 cm wide, 17 cm tall with cap).

  S1  f1-72    (0.0-3.0 s)  BUBBLE REVEAL. Set at x=0. Bottle tilted 20 deg, standing
                            on a water-floor among ~30 floating bubbles. 50 mm, camera
                            looks down ~45 deg. f1-12 hold; f12-72 eased push in and
                            down. Two big bubbles sit between lens and bottle, drift
                            together (f12-36), then slide apart (f36-60) to reveal it.
      f60-72   (2.5-3.0 s)  WHIP: target empty snaps right and down -> fast whip pan.
  S2  f73-108  (3.0-4.5 s)  MACRO SHOULDER. Same set. 85 mm low angle on the cap/shoulder.
                            f73-80 whip settles in from the left; f80-108 slow arc
                            ~30 deg around the bottle + tilt down. Small bubbles rise
                            past the lens.
  S3  f109-198 (4.5-8.25 s) BUBBLE CHAIN. Set at x=10. Diagonal chain of fused bubbles,
                            100 mm, near-locked slow push. Inside the centre bubble a
                            small inner bubble buds and splits off (f130-185).
  S4  f199-264 (8.25-11 s)  CLUSTER. Set at x=20. Top-down 50 mm. Three big bubbles drift
                            out of frame (f206-228); 37 small bubbles fly in and pack
                            into a ball (f210-238) inside one big outer bubble that
                            grows around them (f220-240). Pull back f199-240, hold,
                            cluster turns slowly to the end.
"""

import math
import os
import random
import sys

import bpy

FPS = 24
FRAMES = 264
RES = (720, 1280)

CUTS = {  # first frame of each shot -> camera name
    1: "CAM_S1_Reveal",
    73: "CAM_S2_Macro",
    109: "CAM_S3_Chain",
    199: "CAM_S4_Cluster",
}

# name: (grey-variant RGBA, colour-variant RGBA, what it stands for)
PALETTE = {
    "body":    ((1.0, 1.0, 1.0, 1.0), (0.62, 0.74, 0.95, 1.0), "HERO bottle body (matte light blue, label)"),
    "cap":     ((0.85, 0.85, 0.85, 1.0), (1.0, 1.0, 1.0, 1.0), "HERO bottle flip cap (white)"),
    "bubble":  ((0.80, 0.80, 0.80, 0.28), (0.35, 0.85, 0.95, 0.30), "clear water bubble"),
    "inner":   ((0.55, 0.55, 0.55, 0.45), (0.95, 0.55, 0.85, 0.45), "small bubble budding inside a bubble"),
    "water":   ((0.30, 0.30, 0.30, 1.0), (0.10, 0.25, 0.60, 1.0), "shallow water floor with caustic light"),
}
SKY = {"grey": (0.78, 0.80, 0.82), "colour": (0.75, 0.86, 0.96)}


# ---------------------------------------------------------------- helpers
def _reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


_MATS = {}


def _mat(key, variant):
    if key not in _MATS:
        grey, colour, _ = PALETTE[key]
        m = bpy.data.materials.new(f"MAT_{key}")
        m.diffuse_color = grey if variant == "grey" else colour
        if m.diffuse_color[3] < 1.0:
            try:
                m.surface_render_method = "BLENDED"
            except Exception:
                m.blend_method = "BLEND"
        _MATS[key] = m
    return _MATS[key]


def _assign(ob, key, variant):
    ob.data.materials.clear()
    ob.data.materials.append(_mat(key, variant))


def bubble(name, loc, r, variant, key="bubble"):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=48, ring_count=24, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = (r, r, r)
    bpy.ops.object.shade_smooth()
    _assign(ob, key, variant)
    return ob


def key_loc(ob, frames_locs):
    for f, loc in frames_locs:
        ob.location = loc
        ob.keyframe_insert("location", frame=f)


def key_scale(ob, frames_scales):
    for f, s in frames_scales:
        ob.scale = (s, s, s) if isinstance(s, (int, float)) else s
        ob.keyframe_insert("scale", frame=f)


def camera(name, lens, target_loc, frames_locs, target_keys=None):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=target_loc)
    tgt = bpy.context.active_object
    tgt.name = f"EMPTY_{name}_target"
    bpy.ops.object.camera_add(location=frames_locs[0][1])
    cam = bpy.context.active_object
    cam.name = name
    cam.data.lens = lens
    cam.data.sensor_width = 36
    cam.data.sensor_fit = "AUTO"
    cam.data.clip_start = 0.005
    cam.data.clip_end = 4.0  # never sees a neighbouring set (10 m away)
    trk = cam.constraints.new("TRACK_TO")
    trk.target = tgt
    trk.track_axis = "TRACK_NEGATIVE_Z"
    trk.up_axis = "UP_Y"
    key_loc(cam, frames_locs)
    if target_keys:
        key_loc(tgt, target_keys)
    return cam, tgt


def bottle(variant, loc=(0, 0, 0), tilt_deg=20):
    """Real size: body 7 cm x 13 cm with rounded shoulder, flip cap 6.4 cm x 4 cm."""
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=loc)
    root = bpy.context.active_object
    root.name = "HERO_Bottle"
    root.rotation_euler = (0, math.radians(tilt_deg), 0)
    parts = []
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.12, vertices=64, location=(0, 0, 0.06))
    parts.append(("HERO_Body", bpy.context.active_object, "body"))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, segments=64, ring_count=32, location=(0, 0, 0.12))
    sh = bpy.context.active_object
    sh.scale = (1, 1, 0.28)  # soft rounded shoulder
    parts.append(("HERO_Shoulder", sh, "body"))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.032, depth=0.042, vertices=64, location=(0, 0, 0.148))
    parts.append(("HERO_Cap", bpy.context.active_object, "cap"))
    for name, ob, key in parts:
        ob.name = name
        bpy.ops.object.select_all(action="DESELECT")
        ob.select_set(True)
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.shade_smooth()
        _assign(ob, key, variant)
        ob.parent = root
    return root


# ---------------------------------------------------------------- shots
def shot1_and_2(variant, rng):
    """Shared set at x=0: water floor, bottle, floating bubbles."""
    bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, -0.005))
    floor = bpy.context.active_object
    floor.name = "SET_WaterFloor"
    _assign(floor, "water", variant)

    bottle(variant, loc=(0, 0, 0), tilt_deg=20)

    # ambient floating bubbles around the bottle (never inside it)
    for i in range(30):
        while True:
            x, y = rng.uniform(-0.28, 0.28), rng.uniform(-0.25, 0.30)
            if math.hypot(x, y) > 0.07:
                break
        z = rng.uniform(0.02, 0.22)
        r = rng.choice((0.008, 0.012, 0.018, 0.025, 0.035, 0.045))
        b = bubble(f"BUB_S1_{i:02d}", (x, y, z), r, variant)
        dz = rng.uniform(0.02, 0.05)  # slow rise over the whole shot
        key_loc(b, ((1, (x, y, z)), (108, (x + rng.uniform(-0.01, 0.01), y, z + dz))))

    # two big bubbles between lens and bottle: drift together, then part to reveal
    left = bubble("BUB_S1_CurtainL", (-0.05, -0.16, 0.11), 0.06, variant)
    right = bubble("BUB_S1_CurtainR", (0.06, -0.15, 0.10), 0.055, variant)
    key_loc(left, ((1, (-0.05, -0.16, 0.11)), (12, (-0.05, -0.16, 0.11)),
                   (36, (-0.02, -0.16, 0.11)), (60, (-0.20, -0.17, 0.12))))
    key_loc(right, ((1, (0.06, -0.15, 0.10)), (12, (0.06, -0.15, 0.10)),
                    (36, (0.035, -0.15, 0.10)), (60, (0.21, -0.14, 0.11))))

    # S1 camera: hold, eased push in/down, then whip pan right (target snaps)
    t = (0.02, 0, 0.09)
    camera("CAM_S1_Reveal", 50, t,
           ((1, (0, -0.62, 0.55)), (12, (0, -0.62, 0.55)), (60, (0, -0.40, 0.33)),
            (72, (0.03, -0.38, 0.31))),
           target_keys=((1, t), (60, t), (72, (0.55, 0.05, -0.15))))

    # S2 rising foreground bubbles near the shoulder
    for i in range(8):
        x, y = rng.uniform(-0.03, 0.08), rng.uniform(-0.12, -0.06)
        r = rng.choice((0.003, 0.005, 0.008))
        z0 = rng.uniform(0.0, 0.08)
        b = bubble(f"BUB_S2_{i:02d}", (x, y, z0), r, variant)
        key_loc(b, ((73, (x, y, z0)), (108, (x, y, z0 + rng.uniform(0.05, 0.09)))))

    # S2 camera: low angle 85 mm on cap/shoulder; whip settles in from the left, slow arc
    sh_t = (0.045, 0, 0.125)  # cap/shoulder of the tilted bottle
    camera("CAM_S2_Macro", 85, sh_t,
           ((73, (-0.40, -0.30, 0.05)), (80, (-0.08, -0.40, 0.06)), (108, (0.14, -0.38, 0.10))),
           target_keys=((73, (-0.25, 0.0, 0.12)), (80, sh_t), (108, (0.04, 0, 0.10))))


def shot3(variant):
    """Set at x=10: diagonal chain of fused bubbles; inner bubble buds and splits."""
    o = (10, 0, 0)
    chain = [(-0.09, 0.0, 0.11, 0.045), (-0.035, 0.0, 0.045, 0.035),
             (0.02, 0.0, -0.01, 0.040), (0.08, 0.0, -0.075, 0.048), (0.13, 0.0, -0.14, 0.04)]
    for i, (x, y, z, r) in enumerate(chain):
        b = bubble(f"BUB_S3_Chain{i}", (o[0] + x, y, z), r, variant)
        # gentle wobble
        key_scale(b, ((109, r), (150, r * 1.03), (198, r)))
    cx, cz = o[0] + 0.02, -0.01  # centre bubble
    inner = bubble("BUB_S3_Inner", (cx - 0.008, -0.005, cz), 0.017, variant, key="inner")
    bud = bubble("BUB_S3_Bud", (cx - 0.002, -0.005, cz), 0.001, variant, key="inner")
    key_loc(inner, ((109, (cx - 0.008, -0.005, cz)), (185, (cx - 0.012, -0.005, cz + 0.002))))
    key_scale(bud, ((109, 0.001), (130, 0.002), (160, 0.008), (185, 0.009), (198, 0.009)))
    key_loc(bud, ((109, (cx - 0.002, -0.005, cz)), (130, (cx + 0.004, -0.005, cz)),
                  (160, (cx + 0.016, -0.005, cz - 0.002)), (185, (cx + 0.024, -0.005, cz - 0.004)),
                  (198, (cx + 0.025, -0.005, cz - 0.004))))
    t = (cx, 0, cz + 0.005)
    camera("CAM_S3_Chain", 100, t,
           ((109, (cx + 0.01, -0.62, cz + 0.02)), (198, (cx + 0.005, -0.50, cz + 0.015))))


def _fib_sphere(n, radius):
    pts = []
    golden = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        y = 1 - (i / (n - 1)) * 2
        rr = math.sqrt(1 - y * y)
        th = golden * i
        pts.append((math.cos(th) * rr * radius, y * radius, math.sin(th) * rr * radius))
    return pts


def shot4(variant, rng):
    """Set at x=20: top-down. Big bubbles drift out; small ones pack into a ball inside an outer bubble."""
    o = (20, 0, 0)
    for i, (x, y, r, dx, dy) in enumerate(((-0.05, 0.06, 0.06, -0.20, 0.10),
                                           (0.07, 0.03, 0.055, 0.22, 0.06),
                                           (-0.01, -0.08, 0.065, -0.02, -0.25))):
        b = bubble(f"BUB_S4_Big{i}", (o[0] + x, y, 0), r, variant)
        key_loc(b, ((199, (o[0] + x, y, 0)), (206, (o[0] + x, y, 0)), (228, (o[0] + x + dx, y + dy, 0))))

    cluster_r = 0.045
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=o)
    pivot = bpy.context.active_object
    pivot.name = "EMPTY_S4_ClusterPivot"
    for f, rot in ((199, 0), (238, 0), (264, 35)):
        pivot.rotation_euler = (0, 0, math.radians(rot))
        pivot.keyframe_insert("rotation_euler", frame=f)
    pts = _fib_sphere(30, cluster_r) + _fib_sphere(7, cluster_r * 0.45)
    for i, p in enumerate(pts):
        r = rng.uniform(0.011, 0.015)
        b = bubble(f"BUB_S4_Small{i:02d}", (0, 0, 0), r, variant)
        b.parent = pivot
        ang = rng.uniform(0, 2 * math.pi)
        far = (math.cos(ang) * 0.30, math.sin(ang) * 0.30, p[2])
        start = 210 + rng.randint(0, 8)
        key_loc(b, ((199, far), (start, far), (238, p)))
    outer = bubble("BUB_S4_Outer", o, 0.001, variant)
    key_scale(outer, ((199, 0.001), (220, 0.001), (240, 0.075)))

    camera("CAM_S4_Cluster", 50, o,
           ((199, (o[0], -0.001, 0.26)), (240, (o[0], -0.001, 0.36)), (264, (o[0], -0.001, 0.355))))


# ---------------------------------------------------------------- build
def build(variant="grey"):
    _reset()
    _MATS.clear()
    rng = random.Random(7)
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 1, FRAMES
    scene.render.resolution_x, scene.render.resolution_y = RES
    scene.render.resolution_percentage = 100

    shot1_and_2(variant, rng)
    shot3(variant)
    shot4(variant, rng)

    # hard cuts: one marker per shot bound to its camera
    for f, cam_name in CUTS.items():
        m = scene.timeline_markers.new(cam_name, frame=f)
        m.camera = bpy.data.objects[cam_name]
    scene.camera = bpy.data.objects[CUTS[1]]

    # Workbench look: flat, no overlays, plain sky
    scene.render.engine = "BLENDER_WORKBENCH"
    sh = scene.display.shading
    sh.light = "STUDIO"
    sh.color_type = "MATERIAL"
    sh.show_cavity = False
    sh.show_shadows = False
    sh.show_object_outline = False
    sh.show_specular_highlight = False
    scene.render.film_transparent = False
    world = bpy.data.worlds.new("World") if scene.world is None else scene.world
    scene.world = world
    world.color = SKY[variant]
    scene.view_settings.view_transform = "Standard"
    scene.render.use_stamp = False
    scene.render.use_motion_blur = True  # sells the whip pan; static frames stay sharp
    scene.render.motion_blur_shutter = 0.5

    scene.frame_set(1)
    print_legend(variant)
    return scene


def print_legend(variant):
    print(f"\n=== Shot B blockout legend ({variant}) — paste into the Seedance prompt ===")
    for key, (g, c, meaning) in PALETTE.items():
        rgba = g if variant == "grey" else c
        print(f"  {key:7s} rgba{tuple(round(v, 2) for v in rgba)} = {meaning}")
    print(f"  sky     rgb{SKY[variant]} = plain soft background placeholder\n")


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
