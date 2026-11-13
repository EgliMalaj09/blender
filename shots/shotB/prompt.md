# Shot B: Seedance 2.5 prompts (shampoo bottle in a bubble world)

**Blockout:** `renders/blockout_grey.mp4` or `renders/blockout_colour.mp4`
(11.0 s, 720×1280 9:16, 24 fps, 4 hard cuts, built by `build.py`)
**Product photo:** `ref/product.jpg` (Indrit Gjuzi Deep Cleansing Shampoo, 300 ml)

## Generation settings (set in the UI/API, not in the prompt)

| Setting | Draft | Final |
|---|---|---|
| Mode | Reference-to-video | same |
| Duration | 11 s | 11 s |
| Aspect ratio | 9:16 | 9:16 |
| Resolution | 480p | 720p (one 1080p comparison) |
| Audio | off for the test | as needed |
| Uploads, in this order | Video 1 = blockout, Image 1 = `ref/product.jpg` | same |

If the 11 s take falls apart, split it: shots 1–2 (0–4.5 s) and shots 3–4 (4.5–11 s) as two generations.

---

## Prompt: colour variant (recommended first)

```
Asset mapping:
@Video1: use ONLY for camera position, camera movement, framing, the cut points, bubble paths and timing.
Do not copy the flat placeholder colours, the flat lighting, the plain background or the blockout shapes.
@Image1: the exact product: a matte light-blue plastic shampoo bottle with a white flip-top cap and its printed label.
Copy its shape, proportions, colours and label exactly; keep the label crisp and legible. Do not copy the white studio background.

Brief: a premium 9:16 beauty commercial for this shampoo, set in a clean, airy world of crystal-clear water bubbles,
soft blue-white light, macro lens look, four shots joined by hard cuts and one whip pan.

Proxy key (flat placeholder colours: they are NOT the colour grade, never render them):
- Light-blue cylinder with a white cap = the shampoo bottle from @Image1.
- Translucent cyan spheres = perfectly clear, glassy water bubbles with thin bright rims, soft refractions and highlights.
- Translucent pink sphere inside a bubble = a smaller clear bubble inside it, the same clear glassy material.
- Navy floor = a shallow pale-blue water surface with soft rippling caustic light patterns.
- Pale blue background = a soft bright blue-white gradient.

0–3 seconds: high angle over the water surface; the bottle stands tilted among floating bubbles. Two large bubbles in front
of the bottle drift together, then slide apart to reveal the bottle and its label as the camera pushes in.
3 seconds: a fast whip pan with strong motion blur, hard cut.
3–4.5 seconds: low-angle macro on the bottle's white cap and shoulder; small bubbles rise past the lens; slow arc around the bottle.
4.5–8 seconds: hard cut to an extreme macro of a diagonal chain of fused clear bubbles. Inside the centre bubble a small bubble
buds and gently splits off.
8–11 seconds: hard cut to a top-down view; the large bubbles drift apart, many tiny bubbles gather into a packed sphere inside
one big clear bubble that forms around them; the cluster turns slowly to the end.

Global constraints: photoreal CGI commercial finish, clean high-key blue and white palette, shallow depth of field on the macros,
bubbles stay perfectly clear and glassy, the bottle stays rigid, sharp and identical to @Image1 whenever it is visible.
No added text, no subtitles, no logos other than the bottle's own label, no hands, no people, no music.
Do not generate motion paths, axes or camera guides.
```

## Prompt: grey variant

Same as above, but replace the proxy key with:

```
Proxy key (grey placeholders, never render them as shown):
- The white cylinder with the lighter grey cap = the shampoo bottle from @Image1 (matte light-blue body, white flip-top cap).
- Translucent grey spheres = perfectly clear, glassy water bubbles with thin bright rims, soft refractions and highlights.
- Darker translucent sphere inside a bubble = a smaller clear bubble inside it, the same clear glassy material.
- Dark grey floor = a shallow pale-blue water surface with soft rippling caustic light patterns.
- Light grey background = a soft bright blue-white gradient.
```

---

## Test matrix

Run each at 480p, 3 takes each (9 drafts):

| # | Blockout | Notes |
|---|---|---|
| B1 | colour | full prompt |
| B2 | grey | grey proxy key |
| B3 | colour | split into 0–4.5 s and 4.5–11 s |

Score each take 1–5 on: camera path match · cut timing (3.0 / 4.5 / 8.25 s) · reveal at ~2.5 s ·
bubble look (clear, not cyan/pink) · label fidelity · bottle rigidity. Promote the best take to 720p.
