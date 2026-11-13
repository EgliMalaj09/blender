# Blender blockouts for Seedance 2.5: production and render guidance

Research date: 2026-11-13. Network constraint: WebFetch was unavailable. Full text was read for three primary pages (the Seedance 2.5 prompting guide on docs.seedance.tv, the CozyClay camera-control page, and the Curious Refuge Blender+Claude tutorial). Everything else comes from WebSearch result summaries, so it is snippet-level evidence; treat it as lower confidence. The GitHub MCP could not reach scenario-labs/skills (repo not configured for this session), so PR #243 and issue #275 are known only through search snippets. Code patterns under "Inferences" come from my knowledge of the Blender API. I did not check them against live docs in this session unless a citation is given.

## 1. Render engine and look: grey/clay vs colour-coded proxies; Workbench settings

### Takeaway
The evidence favours a flat grey/clay pass from Workbench, rendered from the scene camera with a plain sky. Sources disagree on colour. CozyClay says to use grey only, with at most one highlight colour on the subject. Scenario's blockout skill and Pixo use one colour per proxy so the prompt can map "the red shape is Image 2". Use colour coding when several similar subjects or material zones must be told apart. Then tell Seedance explicitly not to copy the blockout materials or colours.

### Cited Findings
- Official Seedance guidance: a blockout "can define shot order, framing, character paths, action, and lighting rhythm". The prompt must state what to inherit and fully describe any subject that lacks a visual reference. Example prompt: "Use Video 1 only for the complete shot order, camera positions, framing changes, subject paths, and timing. Do not copy the blockout materials or character appearance." — [Seedance 2.5 Prompting Guide Part 1](https://docs.seedance.tv/en/seedance-2-5-prompting-guide)
- The official guide separates a "coarse blockout" (staging and timing only, with appearance taken from 9 stage keyframe images) from a "fine blockout re-render" ("Fully re-render Video 1 while preserving its action paths, camera movement, timing, and framing exactly" plus a full text description of the new world). — [Seedance 2.5 Prompting Guide Part 1](https://docs.seedance.tv/en/seedance-2-5-prompting-guide)
- Input-recommendations table entry for Blockout: "Prefer simple geometry. Remove motion paths, axes, and camera frustums so they do not leak into the result." — [Seedance 2.5 Prompting Guide Part 1](https://docs.seedance.tv/en/seedance-2-5-prompting-guide)
- CozyClay: "Should the greybox have textures or colours? No. Grey or flat clay. Colour is a cue the model preserves, and you want it inventing the surfaces, not matching placeholders. A single highlight colour on the subject is the most you should add." It also says: "Blender works with a clay material and a workbench render", and "A flat clay pass with a plain sky is the cleanest reference Seedance can get." — [CozyClay: Seedance 2.5 camera control](https://cozyclay.org/seedance-camera-control/)
- CozyClay notes that ByteDance's own examples include clay and white-model references, and that "The reference is a pixel channel. The model matches what it sees." — [CozyClay](https://cozyclay.org/seedance-camera-control/)
- Scenario's blockout skill (scenario-labs/skills PR #243) builds "color-coded proxies at real-world scale, cameras locked to the timeline, framing and occlusion checks, a playblast, a hand-off sheet, and a motion-first prompt". — [PR #243](https://github.com/scenario-labs/skills/pull/243) (search snippet); [scenario-labs/skills](https://github.com/scenario-labs/skills)
- Pixo's blockout guide uses colour as a mapping tool: its prompt template maps "which colored shape becomes which character image". — [Pixo: Seedance 2.5 blockout to film](https://pixo.video/blog/seedance-previz-blockout) (search snippet)
- Toonkit advises stating clearly in the prompt what each important on-screen shape refers to. A small, low-quality render is "plenty" for a reference. — [Toonkit: Blender + Seedance](https://toonkit.io/en/models/seedance-blender) (search snippet)
- Curious Refuge's starter kit has a rigged human that Claude can "duplicate, color, and pose", so the characters are colour-coded. — [Curious Refuge](https://curiousrefuge.com/blog/how-to-control-ai-videos-with-blender-and-claude)
- Dreamina/CapCut offers a "Clay Renderer" plugin that renders and uploads a reference video from Blender. That supports clay as the vendor-endorsed look. — [Dreamina Seedance 2.5 Blender workflow](https://dreamina.capcut.com/seedance/seedance-2-5-blender-model-workflow) (vendor page, search snippet)
- Workbench ignores scene lights. Lighting is set in Properties > Render > Lighting: Flat ("objects are shaded in a flat color, without any highlights or shadows"), Studio (a predefined front key and back rim, which can be fixed in world space), or MatCap (colour picked from an image by surface normal). — [Blender Manual 4.5: Workbench Lighting](https://docs.blender.org/manual/en/4.5/render/workbench/lighting.html)

### Inferences
- Recommended default: Workbench engine, Studio lighting (not Flat). Flat removes all shading, so depth and form cues disappear and the model loses information about volume and camera parallax. Studio or a neutral clay MatCap keeps form readable. CozyClay's "flat" probably means "untextured and unlit-looking", not Workbench's Flat lighting mode. This is my reading; no source states it.
- Colour mode: use Single (light grey, about 0.6–0.8) for grey-only. For colour-coded proxies use Object or Material colour, with desaturated, well-separated hues. Optionally turn on Cavity (World/Screen) to sharpen edges. Turn shadows on if contact and grounding matter. Keep Outline OFF, because CozyClay lists outlines among things that "can come back in the generation as an object".
- When to colour-code: two or more similar subjects (two characters, several vehicles), or distinct material zones the prompt must address ("the blue volume is the glass tower"). When to stay grey: single-subject shots, and grades that should be invented freely. Mitigate leakage with explicit prompt text ("treat colours as identifiers only; do not copy blockout colours or materials"), which follows the official "Do not copy the blockout materials" phrasing.
- EEVEE is only worth it when the blockout must carry a lighting rhythm (the official guide says blockouts can define "lighting rhythm"), for example a light sweep or a day-to-night change. Otherwise Workbench is faster and cleaner.
- Background: set the World colour to a plain light sky-grey or pale blue. In Workbench this is World > Viewport Display colour, or Film > Transparent off with a world colour. Avoid HDRIs, which add detail the model may preserve.

### Gaps
- No controlled A/B evidence (grey vs colour-coded) was found. Both camps rely on practitioner experience.
- I could not read Scenario's skill text, so I don't know its exact palette or saturation rules.
- The Workbench Shading/Options manual pages (cavity, outline, shadow, specular) were not retrieved this session.

## 2. What to strip from the render

### Takeaway
Render from the scene camera with F12 or `-a`, not a viewport capture. Then remove every overlay: motion paths, axes/gizmos, camera frustums, grid/floor lines, selection outlines, frame counters/stamps and any text.

### Cited Findings
- Official: remove "motion paths, axes, and camera frustums so they do not leak into the result". The fine-blockout prompt also adds "Do not generate motion paths, axes, or camera guides." — [Seedance 2.5 Prompting Guide](https://docs.seedance.tv/en/seedance-2-5-prompting-guide)
- CozyClay: "Outlines, gizmos, the ground grid, a selection highlight, a frame counter: any of these can come back in the generation as an object." The checklist says "nothing drawn on top". — [CozyClay](https://cozyclay.org/seedance-camera-control/)
- Curious Refuge: avoid small text in reference images because "it can create problems during video generation". — [Curious Refuge](https://curiousrefuge.com/blog/how-to-control-ai-videos-with-blender-and-claude)

### Inferences
- A final render (Workbench via `bpy.ops.render.render(animation=True)`) has no overlays at all. Viewport playblasts ("Viewport Render Animation") need overlays and gizmos turned off: `space.overlay.show_overlays = False`, `space.show_gizmo = False`.
- Turn off Metadata burn-in: `scene.render.use_stamp = False`. Also check that no Text objects, empties shown as arrows, or visible lights and cameras are in the render. Workbench does not render empties or camera objects anyway.
- Hide helper geometry (curve paths, track-to targets) from render: `obj.hide_render = True`.

### Gaps
- No source tested whether a faint ground plane or contact shadow helps or hurts. CozyClay names only the grid as harmful.

## 3. Export: resolution, aspect, fps, length, codec, size

### Takeaway
Render H.264 MP4 at the delivery aspect ratio (16:9 or 9:16), 24 fps, 720p (1280×720) or 1080p, and keep each clip 3–5 s per shot. Multi-shot animatics can run up to 10–15 s, within Seedance's 30 s total reference budget. Stay above about 409,600 pixels (854×480) and under 200 MB.

### Cited Findings
- CozyClay checklist: "Same aspect ratio as the delivery (16:9 or 9:16), flat shading, 3 to 5 seconds." Longer references "cost more to generate against and drift more toward the end of the clip." — [CozyClay](https://cozyclay.org/seedance-camera-control/)
- Official limits: video references "Up to 10 clips, 30 seconds total". "Five to ten seconds works well for subject reference". Keep editing inputs under 20 s. Generation is up to 30 s. — [Seedance 2.5 Prompting Guide](https://docs.seedance.tv/en/seedance-2-5-prompting-guide)
- Reference aspect ratio vs output: reference tasks are "unlocked", meaning output duration and aspect ratio stay independent of the reference. Editing and extension are "locked" to the input. — [Seedance 2.5 Prompting Guide](https://docs.seedance.tv/en/seedance-2-5-prompting-guide)
- Third-party API specs: MP4/MOV; each clip 1.8–30.2 s, combined ≤30.2 s, ≤200 MB; 300–6000 px per side, aspect ratio 0.4–2.5, 24–60 fps; at least 409,600 pixels (for example 854×480). — [fal.ai Seedance 2.5 reference-to-video API](https://fal.ai/models/bytedance/seedance-2.5/reference-to-video/api); [HiAPI R2V docs](https://www.hiapi.ai/docs/models/video/seedance-2-5-r2v/); [liyue-aigc capabilities-and-limits](https://github.com/liyue-aigc/seedance-2-5-video-director/blob/main/references/capabilities-and-limits.md) (search snippets; not official ByteDance docs). One source claims reference video works only at 1080p output, which others contradict.
- Curious Refuge's starter kit "is already configured to render a 720p reference video, which is plenty". Their test used Seedance 2.5, 10 s, 16:9, audio on, 480p draft mode before upscaling to final. — [Curious Refuge](https://curiousrefuge.com/blog/how-to-control-ai-videos-with-blender-and-claude)
- Price context: on BytePlus ModelArk, Seedance 2.5 at 1080p costs about $2.84 per 5 s, so fixing the camera in a free blockout saves money. — [CozyClay](https://cozyclay.org/seedance-camera-control/)
- Blender 5.0 API change: set `render.image_settings.media_type = 'VIDEO'` before `file_format = 'FFMPEG'`. There is also a reported 5.0 regression where FFMPEG was unavailable under `--factory-startup` (4.5.5 was fine). — [Blender issue #152175](https://projects.blender.org/blender/blender/issues/152175) (search snippet)
- Switching `file_format` to an image format and back can reset FFmpeg encoding settings. — [Blender issue #110701](https://projects.blender.org/blender/blender/issues/110701)

### Inferences
- 24 fps is the safe default. It sits at the floor of the 24–60 fps range and matches cinematic output. 30 fps is also accepted. Avoid 23.976 to dodge rounding issues. (No source compared 24 and 30 for adherence.)
- At 720p, a 5 s H.264 Workbench clip with "MEDIUM" CRF is typically only a few MB, far below 200 MB.
- Use a minimum clip of 2 s, given the 1.8 s floor.

### Gaps
- No official ByteDance spec page was retrieved, so the fps, size and pixel limits come from third-party API documentation.

## 4. Scale, camera, motion, stand-in figures

### Takeaway
Build at real-world metric scale and place the camera at plausible heights with real focal lengths. Animate it with eased (Bezier) keyframes, follow-path dolly/crane rigs and track-to aim constraints. Avoid impossible moves. For characters, use legless capsules or simple stand-ins over stiff jointed mannequins, because Seedance copies the stiffness. If you do use rigged figures, tell Seedance to treat them as placeholders.

### Cited Findings
- "Block the set in grey. Boxes and a stand-in figure, at real scale." "Set the shot. Camera height, distance, lens, then the move: a dolly rail, a crane, a hold. Decide where the cut lands." "A 3-second greybox clip of a camera dollying in at 0.6 m has all of them [the numbers]". — [CozyClay](https://cozyclay.org/seedance-camera-control/)
- Character motion plus camera: send a "reference clip with the figure moving… Keep the figure grey so it invents the person instead of preserving a mannequin." For cuts, use "Two references, two generations… models do not hold a cut inside one generation reliably." — [CozyClay](https://cozyclay.org/seedance-camera-control/). This conflicts with Curious Refuge, which put three shots with cuts in one 10 s animatic and reported that Seedance "followed our Blender animation closely, giving us a good amount of control over camera angles, cuts". — [Curious Refuge](https://curiousrefuge.com/blog/how-to-control-ai-videos-with-blender-and-claude). The official guide also shows a 30 s multi-stage blockout.
- Curious Refuge: "Seedance can follow the Blender reference almost too closely, including its unnatural character movements." Their fix was this prompt line: "Use the reference video as a guide for camera positions and movements. Treat the 3D figures as placeholders rather than copying their exact poses or body mechanics." Problems seen in the Claude-built animatic included unnatural wrists, characters twisting awkwardly, a character sliding (foot-slide), and a prop interaction placed wrong. — [Curious Refuge](https://curiousrefuge.com/blog/how-to-control-ai-videos-with-blender-and-claude)
- Scenario issue #275: hero characters default to coloured capsules. "Jointed figures with rigid, stepping legs get copied stiffly by Seedance". In the Sky Islands test, five runners "came back upright, in near lockstep, with short walk-like strides". The skill offers capsule, featured capsule and mannequin stand-ins for A/B testing. Scenario's examples also recommend modelling products and props accurately "so they come back exact". — [scenario-labs/skills issue #275](https://github.com/scenario-labs/skills/issues/275) (search snippet)
- Camera focal length, path, shake and timing "transfer directly to the model as a motion reference". — [flick.art Blender AI filmmaking guide](https://flick.art/blog/blender-ai-filmmaking) (search snippet)
- If subjects ignore your volumes, "the fix is in the blockout, not the prompt"; generate at low resolution first. — [aivideosensei Seedance 2.5 previz](https://aivideosensei.com/guides/seedance-2-5-previz-workflow) (search snippet; less established site)
- Curious Refuge reported that Claude attempted the 180-degree rule but "didn't add the camera movements we'd hoped to see". — [Curious Refuge](https://curiousrefuge.com/blog/how-to-control-ai-videos-with-blender-and-claude)

### Inferences
- Practical defaults (cinematography convention, not from Seedance sources): eye-level camera about 1.5–1.7 m; low angle about 0.3–0.6 m; lenses 24–35 mm for wides and establishing shots, 35–50 mm for mediums, 85 mm or more for close-ups; sensor width 36 mm. Real dolly speeds are about 0.3–1 m/s, and real crane and drone speeds vary.
- Rigs: a dolly is an empty on a Bezier curve with a Follow Path constraint, with eval_time keyed and Bezier ease. An orbit is an empty at the subject with the camera parented, keying the empty's Z rotation. A track is a Track To / Damped Track constraint on a target empty. Keep keyframe interpolation BEZIER with auto-clamped handles. Avoid LINEAR starts and stops (unphysical snaps) and avoid camera roll unless intended.
- Add a 6–12 frame static hold or ease-in at the start, so the model reads the first composition before the move.

### Gaps
- No source quantified which lens or height mapping Seedance follows most faithfully.

## 5. Large crowds / instances

### Takeaway
Use Geometry Nodes Instance on Points (or collection instancing) with one low-poly proxy mesh. Keep the result as instances and don't realize it. Workbench renders thousands of instances cheaply.

### Cited Findings
- Instances reference shared geometry instead of copying it, so engines handle many copies efficiently. Realizing costs memory and makes downstream nodes process each copy. Realize only when per-instance unique geometry is needed. — [Blender Manual: Geometry Nodes Instances](https://docs.blender.org/manual/en/dev/modeling/geometry_nodes/instances.html); [Geometry Nodes Performance](https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/performance.html)
- Only 8 levels of nested instancing render or display. — [Blender Manual: Instances](https://docs.blender.org/manual/en/dev/modeling/geometry_nodes/instances.html)
- Third-party: Geometry Nodes work via MCP is "brittle". — [mcp.directory connector guide](https://mcp.directory/blog/claude-blender-connector-guide) (search snippet)

### Inferences
- For Claude-driven builds, building the GN tree in bpy is error-prone. A simpler path is a script that creates N linked duplicates (`obj.copy()` sharing mesh data) or collection instances, which is fine into the low thousands under Workbench. Animate crowd flow with a per-instance offset driven by noise in GN, or with a few hundred keyed hero proxies plus static fill.
- Official guidance says 1–8 subjects is most reliable for images. Read the crowd as texture or volume, and name it in the prompt ("dense crowd fills the plaza").

### Gaps
- No benchmarks were found for Seedance adherence with thousands of proxies, or for crowd-specific Blender tools (for example animated GN crowds).

## 6. Headless rendering with bpy (Claude Code path); version API changes

### Takeaway
Claude Code can write a single `build.py` that builds the scene, keys the camera, sets Workbench and FFmpeg output, and renders with `blender -b -P build.py`. This avoids MCP entirely, is reproducible and diff-able, and needs no GUI. Watch for the Blender 5.x API changes: engine `BLENDER_EEVEE` (was `BLENDER_EEVEE_NEXT` in 4.2–4.5), and `image_settings.media_type='VIDEO'` before `file_format='FFMPEG'`.

### Cited Findings
- Blender 5.0 renamed the EEVEE engine identifier from `BLENDER_EEVEE_NEXT` to `BLENDER_EEVEE`, listed as a breaking change. — [Blender 5.0 EEVEE release notes](https://developer.blender.org/docs/release_notes/5.0/eevee/)
- In 5.0, set `media_type = 'VIDEO'` first, then `file_format = 'FFMPEG'`. — [Blender issue #152175](https://projects.blender.org/blender/blender/issues/152175)
- FFmpegSettings API reference (format, codec, constant_rate_factor, ffmpeg_preset). — [bpy.types.FFmpegSettings 5.0](https://docs.blender.org/api/5.0/bpy.types.FFmpegSettings.html); 5.0 also removed some Action attributes. — [API change log](https://docs.blender.org/api/5.0/change_log.html)
- A pip `bpy` build without FFmpeg causes an enum error for FFMPEG. — [technetexperts](https://www.technetexperts.com/blender-python-ffmpeg-error/) (secondary, unverified)
- Third-party connector guidance: if MCP scripts keep failing, have Claude write the script, save it, and run it from Blender's text editor. — [mcp.directory](https://mcp.directory/blog/claude-blender-connector-guide) (search snippet)

### Inferences (code pattern, from Blender API knowledge; test on the target version)
```python
import bpy, math
scn = bpy.context.scene
# wipe
bpy.ops.wm.read_factory_settings(use_empty=True)   # beware 5.0 --factory-startup FFMPEG regression; test
scn = bpy.context.scene
scn.render.engine = 'BLENDER_WORKBENCH'
sh = scn.display.shading
sh.light = 'STUDIO'          # or 'FLAT' / 'MATCAP'
sh.color_type = 'SINGLE'     # 'OBJECT' or 'MATERIAL' for colour-coded proxies
sh.single_color = (0.7, 0.7, 0.7)
sh.show_cavity = True; sh.cavity_type = 'WORLD'
sh.show_shadows = True
sh.show_object_outline = False
sh.background_type = 'WORLD'  # world colour = plain sky
world = bpy.data.worlds.new("Sky"); scn.world = world
world.color = (0.75, 0.82, 0.9)
scn.display.render_aa = '8'   # anti-aliasing
scn.render.use_stamp = False
r = scn.render
r.resolution_x, r.resolution_y, r.resolution_percentage = 1280, 720, 100
r.fps, r.fps_base = 24, 1.0
scn.frame_start, scn.frame_end = 1, 120          # 5 s
if bpy.app.version >= (5, 0, 0):
    r.image_settings.media_type = 'VIDEO'
r.image_settings.file_format = 'FFMPEG'
r.ffmpeg.format = 'MPEG4'; r.ffmpeg.codec = 'H264'
r.ffmpeg.constant_rate_factor = 'HIGH'; r.ffmpeg.ffmpeg_preset = 'GOOD'
r.ffmpeg.audio_codec = 'NONE'
r.filepath = '//out/shot01_'   # Blender appends frame range + .mp4
# camera with eased dolly
cam_data = bpy.data.cameras.new("Cam"); cam_data.lens = 35; cam_data.sensor_width = 36
cam = bpy.data.objects.new("Cam", cam_data); scn.collection.objects.link(cam); scn.camera = cam
cam.location = (0, -8, 1.6); cam.keyframe_insert("location", frame=1)
cam.location = (0, -4, 1.6); cam.keyframe_insert("location", frame=120)
tgt = bpy.data.objects.new("Aim", None); scn.collection.objects.link(tgt); tgt.location = (0, 0, 1.2)
c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
bpy.ops.render.render(animation=True)
```
Run with `blender -b -P build.py` (or `blender -b scene.blend -P build.py -a`). Also save the .blend (`bpy.ops.wm.save_as_mainfile`) so the user can open and tweak it. Verify with `ffprobe` (duration, fps, resolution). Optionally render a few single PNG frames first to check framing; Claude can view these images to self-check composition. Note: in 5.x the keyframe interpolation default is Bezier, and fcurve access moved toward layered actions/channelbags (`action.fcurves` removal is noted in the 5.0 change log), so avoid scripting fcurves directly and prefer `keyframe_insert` plus `bpy.context.preferences.edit.keyframe_new_interpolation_type`.

### Gaps
- I could not open the 5.0/5.1 Python API release notes, so other breaking changes affecting this path (Workbench property renames, Action API) are not exhaustively checked. Run the script on the target version before relying on it.

## 7. Tooling options for having Claude build it

### Takeaway
There are four routes. (a) Claude Code plus headless bpy scripts: reproducible, no GUI, best for camera precision and batch shots. (b) The official Blender Lab MCP plus the Claude Desktop connector: interactive and live, arbitrary-Python and screenshot based, Blender 5.1+, experimental, no guardrails. (c) The community ahujasid blender-mcp: older, adds Poly Haven and Hyper3D asset tools. (d) Vendor add-ons such as Scenario (blockout skill, colour-coded proxies, Seedance hand-off), Higgsfield (in-viewport Seedance 2.5 plus an MCP Bridge), Dreamina's Clay Renderer, and Toonkit. Reports show Claude handles layout well but under-delivers on camera movement and character animation, so specify camera moves numerically or script them.

### Cited Findings
- Official connector: announced 28 Apr 2026; Claude Desktop > Customize/Settings > Connectors > Blender; Blender-side add-on installed from the Blender Lab MCP page, then start the server; runs on the same machine (Desktop only, not the browser claude.ai). — [Claude tutorial](https://claude.com/resources/tutorials/using-the-blender-connector-in-claude); [mcp.directory guide](https://mcp.directory/blog/claude-blender-connector-guide); [Claude connector listing](https://claude.com/connectors/blender) (search snippets)
- Curious Refuge setup: Edit > Preferences, drag the install link from Blender Lab, allow online access, approve the Blender Labs repository, enable the add-on, confirm the MCP server is running; then in Claude Desktop, Settings > Connectors > Blender. — [Curious Refuge](https://curiousrefuge.com/blog/how-to-control-ai-videos-with-blender-and-claude)
- Official Lab server: a Blender Foundation project, v1.0.0. An add-on talks over TCP to a standalone MCP server and exposes the Python API, blend-file checks, viewport screenshots and documentation search (about 26 tools per one reviewer). Requires Blender 5.1+. Experimental, outside the roadmap. Blender warns that it "will execute LLM generated code in Blender without any guards" and recommends a VM. — [voyager.so comparison](https://voyager.so/blog/blender-mcp); [mcp.film](https://mcp.film/mcps/blender-lab-mcp/); [projects.blender.org #152011](https://projects.blender.org/blender/blender/issues/152011) (search snippets). Version conflict: some guides say 4.2+. — [lushbinary](https://lushbinary.com/blog/claude-blender-mcp-connector-3d-modeling-guide/); [meltflexai](https://www.meltflexai.com/blog/connect-claude-to-blender)
- Connector limits (third-party): screenshots cost tokens; big scenes can time out (chunk by collection); sculpt mode is not accessible; Geometry Nodes are brittle; running the same server in Claude Desktop and Cursor collides. — [mcp.directory](https://mcp.directory/blog/claude-blender-connector-guide); [mindstudio](https://www.mindstudio.ai/blog/claude-blender-mcp-real-world-performance) (search snippets)
- Camera and animation struggles: Claude "didn't add the camera movements we'd hoped to see"; wrists were unnatural, characters twisted and slid, and a prop interaction was wrong. These were fixed by iterating with feedback. — [Curious Refuge](https://curiousrefuge.com/blog/how-to-control-ai-videos-with-blender-and-claude). Other third-party guides list camera paths and turntables as strengths but recommend hand-tuning curves in the Graph Editor. — [blendermcp.org animation](https://blendermcp.org/use-cases/animation) (search snippet). No dedicated bug reports were found.
- Curious Refuge starter-kit pattern: a .blend with a Scripting-tab prompt template, composition and camera guidelines, a rigged human to duplicate, colour and pose, procedural generators, a premade timeline, and 720p video output settings. Claude also writes the Seedance prompt with per-shot timings. — [Curious Refuge](https://curiousrefuge.com/blog/how-to-control-ai-videos-with-blender-and-claude)
- Community blender-mcp (ahujasid): `execute_blender_code` (arbitrary Python), viewport screenshot (default max 800 px), optional Poly Haven search and import, Hyper3D Rodin generation; socket on port 9876. — [glama listing](https://glama.ai/mcp/servers/@ahujasid/blender-mcp/schema); [Kapwing Astra tutorial](https://www.kapwing.com/resources/how-to-turn-gpt-6-astra-into-your-own-film-studio-blender-seedance-2-5/) (search snippets). Arbitrary code execution was raised as a security issue. — [issue #207](https://github.com/ahujasid/blender-mcp/issues/207). A mirrored addon.py was reported to contain a hardcoded API key, so use the official repo only.
- Scenario for Blender: an experimental Blender 5.0+ extension (GPL-3.0+), Blockout turns a text description into a greybox layout, it has a Render Video lane, and it includes a local MCP server for agents. Its skills (scenario-blender-blockout, plus siblings scenario-blender and scenario-seedance, which may need separate install) do colour-coded proxies, timeline-locked cameras, framing audits, a playblast and a hand-off sheet. — [scenario-labs/blender-plugin](https://github.com/scenario-labs/blender-plugin); [USER_GUIDE](https://github.com/scenario-labs/blender-plugin/blob/main/docs/USER_GUIDE.md); [blender.scenario.com](https://blender.scenario.com/); [PR #243](https://github.com/scenario-labs/skills/pull/243) (search snippets)
- Higgsfield Blender add-on (Sept 2026): a toolbar over the viewport; generates editable scenes, meshes, rigs and media; video via Seedance 2.5; shared credits; the MCP Bridge at bridge.higgsfield.ai/mcp lets Claude edit the open scene; version floor reported as 5.1+, with one guide saying 4.2–5.1. — [Higgsfield plugin page](https://higgsfield.ai/plugins/blender); [Digital Production](https://digitalproduction.com/2026/09/23/higgsfield-brings-ai-generation-into-blender-oh-goodey/); [rar.design guide](https://rar.design/posts/higgsfield-blender-plugin-guide) (search snippets)
- Toonkit has a "Blender + Seedance — design your AI video camera in 3D" page. — [toonkit.io](https://toonkit.io/en/models/seedance-blender). Separately, "seadanse" is a Blender extension plus Agent Skill that turns a grey clay pass into Seedance 2.5 video. — [SourceForge seadanse](https://sourceforge.net/projects/seadanse-blender/). Both are search snippets only.
- CozyClay is an open-source browser greybox tool (`npx cozyclay`) that exports flat clips with the delivery ratio and a camera timeline. It is an alternative to Blender. — [CozyClay](https://cozyclay.org/seedance-camera-control/)
- Mixar: no Mixar-specific Seedance 2.5 Blender guide was found in search.

### Inferences
- Hybrid recommendation: use the MCP connector (or Claude Code) for scene layout. For camera moves, have Claude generate an explicit, numeric camera script: positions in metres, lens in mm, frame ranges, interpolation. Run it headless (`blender -b`), then judge stills or contact sheets before the MP4. This addresses the reported weakness ("didn't add the camera movements") by making the move a spec, not an improvisation.
- Claude Code headless pros: version-controlled, repeatable re-renders, batch shots, no GUI, works in cloud containers. Cons: no live viewport, so the user cannot nudge things interactively. Use rendered PNG frames for visual checks. MCP pros: interactive, the user sees changes live. Cons: Desktop-only, experimental, no sandbox, timeouts on big scenes.

### Gaps
- I could not read the full Anthropic tutorial or the blender.org/lab/mcp-server page, so the exact tool list, the version floor (5.1 vs 4.2) and the plan requirements are unconfirmed.
- No Mixar guide was found. The Toonkit, Pixo and Kapwing pages were seen only as snippets.
