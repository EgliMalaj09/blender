# Shot A — Seedance 2.5 prompts

**Blockout:** `renders/blockout_grey.mp4` or `renders/blockout_colour.mp4`
(5.0 s, 1280×720, 24 fps, built by `build.py`)

## Generation settings (set in the UI/API, not in the prompt)

| Setting | Draft | Final |
|---|---|---|
| Mode | Reference-to-video | same |
| Duration | 5 s | 5 s |
| Aspect ratio | 16:9 | 16:9 |
| Resolution | 480p | 720p (one 1080p comparison) |
| Audio | off for the test | as needed |
| Uploads, in this order | Video 1 = blockout, Image 1 = product photo | same |

Swap `<PRODUCT>` for your real product and attach its photo as Image 1.
**No realistic human faces in reference images** (the official API blocks them).

---

## Prompt — grey variant

```
Asset mapping:
@Video1: use ONLY for camera position, camera movement, framing, subject paths and timing.
Do not copy the grey materials, the flat lighting, the plain background or the blockout shapes.
@Image1: the exact look of the product — shape, label, material, colour.

Brief: a premium live-action product shot of <PRODUCT> on a wooden table in a sunlit
Scandinavian apartment, shallow depth of field, slow cinematic dolly-in.

Proxy key (placeholders, never render them as shown):
- The white cylinder on the table = <PRODUCT> from @Image1.
- The dark box = a solid oak table.
- The grey capsule with a sphere head = an adult woman in casual linen clothes walking past.
  Treat the 3D figure as a placeholder; do not copy its pose or body mechanics, give her a natural walk.
- The grey wall and floor = a bright apartment interior with a window off-frame left.

0–2 seconds: wide shot, the camera holds, then begins a slow push toward the product.
2–4 seconds: the woman walks from left to right behind the table, out of focus, never touching the product.
4–5 seconds: the push continues, the product fills the centre of frame; the camera is still moving at the end.

Global constraints: photoreal, soft warm morning light, natural colour grade, 35mm lens look,
the product stays sharp and unchanged throughout. No text, no subtitles, no logos other than
the product's own label, no music. Do not generate motion paths, axes or camera guides.
```

## Prompt — colour variant

Same as above, but replace the proxy key with the colour legend printed by `build.py`:

```
Proxy key (flat placeholder colours — they are NOT the colour grade, never render them):
- White cylinder = <PRODUCT> from @Image1.
- Brown box = a solid oak table.
- Orange capsule with a sphere head = an adult woman in casual linen clothes walking past.
  Treat the figure as a placeholder; do not copy its pose or body mechanics.
- Tan wall = a bright off-white apartment wall. Navy floor = light oak floorboards.
```

---

## Test matrix (from the playbook)

Run each at 480p, 3 takes each (12 drafts):

| # | Blockout | Placeholder line ("Treat the 3D figure as a placeholder…") |
|---|---|---|
| A1 | grey | on |
| A2 | grey | off |
| A3 | colour | on |
| A4 | colour | off |

Score each take 1–5 on: camera path match · timing of the walk (2–4 s) · framing at the end ·
proxy/colour leakage · figure looks natural · product fidelity. Promote the best take to 720p.
