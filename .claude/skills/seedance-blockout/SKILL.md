---
name: seedance-blockout
description: Build Blender grey-box / colour-proxy blockouts with an exact animated camera and render them as reference clips for Seedance 2.5 reference-to-video, then write the matching Seedance prompt. Use whenever the user wants to previs, block out, or direct the camera of an AI video shot in Blender, mentions Seedance + Blender, Genjutsu, "white model", "clay render", or asks to build/revise a shot like shots/shotA.
---

# Seedance blockout

Blender controls camera, timing and layout; Seedance 2.5 supplies the look.
Full research: `reports/Blender blockouts for Seedance 2.5.md`. Worked example: `shots/shotA/`.

## Workflow

1. **Shot spec first.** Write the take second by second with numbers: camera start/end
   position (metres), height, lens (mm), frame ranges, what enters/exits when. Ask the user
   for anything missing; do not improvise camera moves (Claude is weakest there).
2. **Script it.** Copy `shots/shotA/build.py` to `shots/<shot>/build.py` and edit the
   constants/geometry. One file builds, animates and renders — reproducible and diff-able.
   - With Blender MCP connected: exec the file in Blender, call `build(variant=...)`,
     take a viewport screenshot from the camera at start/mid/end, iterate with the user.
   - Headless: `blender -b -P shots/<shot>/build.py -- --variant grey`
     (`--frames 1,60,120` renders PNG stills for a quick check).
3. **Check stills before the MP4**: subject framed at start/mid/end, entrances/exits on time,
   nothing sinking into the floor, no overlays.
4. **Render** the MP4 and write `shots/<shot>/prompt.md` from the template in shotA.
5. **Iterate camera in Blender, never in the prompt.** Re-render is free; generations cost.

## Blender rules

- Real-world scale (metres), real lens values (18–28 mm establishing, 35–50 mm product/story,
  85 mm+ hero). Camera + `TRACK_TO` target empty. Eased Bezier moves, short holds at the start.
- Workbench engine, Studio light, object colours, cavity/outline off, plain world colour.
  Render from the scene camera (never a viewport capture), stamps off.
- **Strip everything that can leak**: motion paths, axes, gizmos, grid, camera frustum,
  selection outline, frame counter, text.
- **People = legless capsules** (cylinder + sphere head). Jointed mannequins get their stiff
  motion copied.
- **Grey vs colour**: default grey set + one white hero. Use one flat colour per object only
  when several similar subjects must stay distinct or to mark material zones — then every
  colour must be decoded in the prompt and declared "not the colour grade".
- Export: delivery aspect ratio, 1280×720 (never below 854×480), 24 fps, H.264 MP4,
  trimmed to the exact shot length (input seconds are billed). Keep single-move shots 3–5 s;
  ≤15 s for multi-beat shots.
- Blender 5.x: set `image_settings.media_type = "VIDEO"` before `file_format = "FFMPEG"`;
  joined objects keep the active object's origin (key the right Z).

## Prompt rules (Seedance 2.5)

Four parts, in order: **asset mapping → one-sentence brief → whole-second timeline → global constraints.**

- Tags are positional: `@Video1`, `@Image1` … in upload order.
- Every asset gets "use ONLY for X; do not copy Y".
- Blockout line: "Use @Video1 only for camera position, camera movement, framing, subject
  paths and timing. Do not copy the blockout materials, lighting or shapes."
- Figures: "Treat the 3D figures as placeholders rather than copying their exact poses or
  body mechanics."
- Decode every proxy ("orange capsule = …"); say what the colours are NOT.
- Restate timing and what happens per time range; don't re-describe the camera move.
- Timed events go only in the timeline, never in global constraints. Avoid "already" for reveals.
- End with: "Do not generate motion paths, axes or camera guides." No text/subtitles/music
  unless wanted.
- Duration, aspect ratio and resolution are settings, not prompt text.
- No realistic human faces in reference images (blocked on the official API).

## Iteration

Draft at 480p, 3 takes per variant, score (camera path · timing · end framing · leakage ·
natural motion · subject fidelity), promote the best to 720p. Budget 2–3× list price for misses.
