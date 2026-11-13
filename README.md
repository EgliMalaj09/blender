# Blender → Seedance 2.5 previs

Direct AI video shot by shot: build a grey-box blockout with an exact camera move in Blender,
render it as a reference clip, and let Seedance 2.5 render the look.

- `reports/Blender blockouts for Seedance 2.5.md`: research playbook and fact-check of the source note
- `.claude/skills/seedance-blockout/`: project skill with the rules Claude Code follows here
- `.claude/skills/camera-cinematography/`: lens and camera-move guide (from arjun988/blender-skills, MIT)
- **`WORKFLOW.md`: the reusable step-by-step loop (start here)**
- `shots/shotA/`: one continuous dolly move (16:9, 5 s)
- `shots/shotB/`: shampoo ad in a bubble world rebuilt from a reference video (9:16, 11 s, 4 cuts)
- `shots/shotC/`: café conversation coverage test, 7 angles + 3 quick inserts (16:9, 15 s), tested prompt

Each shot folder has `build.py`, rendered `renders/*.mp4` and `prompt.md`.

## Quick start (local Claude Code + Blender MCP)

```bash
git clone -b claude/charming-mayer-kthdkq https://github.com/EgliMalaj09/blender.git
```

Open Claude Code in that folder and ask:

> Run shots/shotA/build.py in Blender through MCP with variant grey and show me the camera view at frames 1, 72 and 120.

Or render headless without MCP:

```bash
blender -b -P shots/shotA/build.py -- --variant grey
```

Then upload `shots/shotA/renders/blockout_grey.mp4` as Video 1 in Seedance 2.5
(reference-to-video) with the prompt from `shots/shotA/prompt.md`.
