# Workflow: Blender blockout → Seedance 2.5 video

A repeatable loop for directing an AI video shot by shot. Blender fixes the **camera, cuts,
timing and layout**; Seedance 2.5 supplies the **look**. Every new shot is a folder
`shots/<name>/` with three things: `build.py`, `renders/`, `prompt.md`.

```
 idea / reference video ─► 1 shot spec ─► 2 build.py ─► 3 check stills ─► 4 render MP4
                                                                  ▲               │
                                              fix camera here ────┘               ▼
                                   7 keep the winner ◄─ 6 score takes ◄─ 5 prompt + generate
```

---

## 0. One-time setup

- Blender 5.x installed (`/Applications/Blender.app`), ffmpeg (`brew install ffmpeg`).
- Open Claude Code in this repo. The project skill `seedance-blockout` loads automatically.
- Optional: Blender MCP add-on running in Blender, so Claude can drive the live UI.
  Without it, everything runs headless; same result.

Headless command used throughout:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b -P shots/<shot>/build.py -- --variant colour
```

---

## 1. Shot spec (say what you want)

Tell Claude one of these:

| You have | Say |
|---|---|
| A reference video | "Here's a video: `<path>`. Rebuild it as `shotX` with my product `<image>`." |
| An idea | "Make `shotX`: two people talking in a kitchen, 6–7 angles, 15 s, 16:9." |
| A finished shot to tweak | "In `shotC`, make the close-up of A longer and push in slower." |

Claude answers with a **shot table** (time · setup · lens · camera move). Fix it now.
Changing a number in Blender is free; a Seedance generation is not.

Decide up front:
- **Aspect & length:** 16:9 or 9:16; ≤15 s per generation (3–5 s for a single move).
- **Grey or colour proxies:** colour when several similar things must stay distinct
  (two people, product body vs cap); grey otherwise.
- **People:** always legless capsules in Blender.

## 2. Build (`build.py`)

Claude copies the closest existing shot and edits it:

| Template | Use it for |
|---|---|
| `shots/shotA` | one continuous camera move, one product, one walker |
| `shots/shotB` | product ad, 9:16, several **cuts** (one set per shot), translucent objects |
| `shots/shotC` | **dialogue coverage**: one set, many cameras, 180° rule, quick inserts |

Rules the scripts follow:
- Real-world metres, real lenses (24 wide · 35 two-shot · 50 OTS · 85 close-up / insert).
- One camera per shot + a `TRACK_TO` target; **timeline markers switch cameras** = hard cuts.
- Conversations: every camera on the same side of the line between the two people.
- Workbench render, no overlays, 24 fps, 1280×720 (or 720×1280), H.264, trimmed exactly.

## 3. Check stills (before any MP4)

```bash
Blender -b -P shots/<shot>/build.py -- --variant colour --frames 1,48,110,200,290,360
```

Claude tiles them into one contact sheet and checks: subject framed, nobody blocking the
other, no gaps showing sky/void, entrances on time, nothing intersecting.
Fix in `build.py`, re-render stills, repeat.

## 4. Render

```bash
Blender -b -P shots/<shot>/build.py -- --variant colour
Blender -b -P shots/<shot>/build.py -- --variant grey
```

Output: `shots/<shot>/renders/blockout_<variant>.mp4`. Claude checks duration and frame count.

## 5. Prompt + generate

`prompt.md` is always four blocks, in this order:

1. **Asset mapping**: `@Video1: use ONLY for shot order, cut points, camera, framing and timing. Do not copy colours, lighting or shapes.` (+ `@Image1` = product, if any)
2. **Brief**: one sentence: what, where, mood, how it's filmed.
3. **Proxy key + timeline**: decode every colour ("orange capsule = …"; "not the colour grade"),
   then whole-second time ranges with what happens and any dialogue.
4. **Global constraints**: look, consistency, audio, "no text / no music",
   "Do not generate motion paths, axes or camera guides."

Seedance 2.5 settings (UI, not prompt):

| Setting | Value |
|---|---|
| Mode | **Reference-to-video** |
| Upload order | blockout MP4 first (= @Video1), then images (@Image1, @Image2…) |
| Duration / aspect | set by hand to match the blockout (it does **not** inherit them) |
| Resolution | 480p for drafts → 720p for the winner |
| Audio | on only if there's dialogue / sound |

### Moderation: what we learned ("violates our policies")

- **No realistic face images** as references, including AI-generated ones. Describe people in text.
- Avoid wording that reads as "make a real person": *photoreal live-action*, *consistent faces*,
  *lip sync*. Use *cinematic and natural*, *the same two people in every shot*,
  *mouths move naturally with the spoken lines*.
- Keep dialogue mild (shotC failed with "quit … you're crazy", passed with "new job … so happy for you").
- If it still fails, bisect: (1) video + set only, no people → (2) add people, no dialogue → (3) full.
  The first step that fails is the cause.

## 6. Score takes

3 takes per variant at 480p. Score 1–5 on: camera path · cut timing · end framing ·
proxy leakage (colours/shapes showing) · natural motion · subject/product fidelity.
If a long multi-cut take falls apart, split it into two generations at a cut point.

## 7. Keep the winner

Promote the best take to 720p with the **same** files, order and prompt. Note what worked in
the shot's `prompt.md` (like the moderation note in `shots/shotC/prompt.md`) and commit.

---

## Cheat sheet: things to say to Claude

- "Analyse this video and give me a shot breakdown: `<path>`"
- "Build shotD from shotC's template: <idea>. Show me stills first."
- "Render shotD grey and colour and write the prompt."
- "Generation failed with `<error>`; here's my prompt." (Claude bisects it with you)
- "Take 2 was best but the cut at 8 s is late; fix it in Blender."
- "Commit and push."
