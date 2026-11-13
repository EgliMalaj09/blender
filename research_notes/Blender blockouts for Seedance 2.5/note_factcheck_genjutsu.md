# Fact-check: "Claude + Blender → Genjutsu: Direct AI Video Shot by Shot" (@viznfr), and Genjutsu vs Seedance 2.5 direct (as of 13 Nov 2026)

Method note: WebFetch is blocked in this environment, so most evidence below comes from WebSearch result summaries (not full-page reads) plus three pages downloaded in full (docs.seedance.tv Seedance 2.5 guide Part 1, cozyclay.org camera-control page, Curious Refuge tutorial). Where a figure only appears in a search summary, treat it as lower confidence than a full-page read. Many Genjutsu "reviews" are SEO/affiliate pages from competing tools (Kavel, Pippit, WaveSpeed, Creaa, Riffkit, imagesart); they are flagged where used.

Verdict scale: True / Mostly true / Overstated / Unverified / Wrong / Outdated.

## Claim-by-claim verdict table (summary)

| # | Claim in note | Verdict | Using Seedance 2.5 directly instead |
|---|---|---|---|
| 1 | Claude Code writes a bpy script and renders headless with `blender.exe -b -P build.py` | True (standard Blender CLI) | Unchanged |
| 2 | "Blender 4.x", path `...\Blender 4.0\blender.exe` | Outdated (Blender 5.3 current; 5.2 is LTS; 4.0 long EOL); path is Windows-only and version-specific | Unchanged; use whatever Blender is installed (`blender` on PATH on Linux/macOS) |
| 3 | Crude proxy shapes only, workbench render | True / consistent with Seedance guide and CozyClay | Unchanged |
| 4 | Flat colours, one colour per thing, so AI can tell objects apart | Mostly true, but contested (CozyClay: grey + at most one highlight; Scenario/fal: colour-coded proxies each named in prompt) | Same trade-off; must decode colours in the asset-mapping block |
| 5 | White box marks the hero | Unverified as a special rule (a reasonable convention; nothing says the model treats white specially) | Same; say "white box = hero" explicitly |
| 6 | One continuous camera move, exactly timed, no cuts | True for a single-generation shot; consistent with CozyClay "two references, two generations" for cuts | Same; Seedance 2.5 can also follow cuts inside a reference (Curious Refuge, docs blockout example) |
| 7 | 4:3, 1440x1080, 30fps, blockout.mp4 | Overstated as a recommendation: works, but resolution is overkill, 30fps gets retimed to 24fps output, and 4:3 only makes sense if you deliver 4:3 | Seedance 2.5 offers 4:3 on fal for reference-to-video; set aspect explicitly or "auto" |
| 8 | Genjutsu = "motion control"; upload blockout as Video 1, refs as Image 1, 2 | Mostly true (it is Motion Transfer mode; "motion control" is informal) | Seedance 2.5 reference-to-video: Video 1 + Images, same numbering convention in the official guide |
| 9 | ~36 credits for a 12s test at 480p, 84 at 720p | Mostly true (= 3 and 7 credits/s; matches Oct 2026 check; Sept table implies ~32/~83) | Higgsfield's own Seedance 2.5 page lists the same ~3/7 credits/s; other hosts bill in $/s |
| 10 | Three-block prompt REFERENCE MAP / GLOBAL RULES / MOMENT n | Mostly true; closely mirrors the official Seedance 2.5 four-part structure (asset mapping + brief + timeline + global constraints) but omits the one-sentence brief | Use the official four-part structure directly |
| 11 | Test at 480p first, then 720p | True (widely recommended; Curious Refuge does the same) | Same; 1080p available on some hosts |
| 12 | "Same camera, same timing, frame for frame" | Overstated (no independent blockout-fidelity test of Genjutsu found; output is retimed to 24fps so literally frame-for-frame is impossible; reviewers report drift under occlusion/fast motion) | Same caveat |
| 13 | Colour-code materials (brown palm = leather) | Plausible / consistent with "colour is a cue the model preserves"; anecdotal | Same |
| 14 | Never put timed events in GLOBAL RULES | True (consistent with official guide: global constraints = rules that apply throughout) | Same |
| 15 | Never write "already" for a reveal | Plausible anecdote; Unverified as a general rule, but consistent with "Seedance follows whole-second timestamps" | Same |
| 16 | Tell it what proxy colours are NOT | True (consistent with official guide: "Do not copy the blockout materials"; CozyClay: colour is preserved) | Same |
| 17 | Fix camera in Blender, not in the prompt | True (CozyClay, Curious Refuge, official guide all agree) | Same |
| 18 | End on a push still moving so it cuts into next shot | Reasonable editing craft; Unverified as model behaviour | Same; or use Seedance extension / last-frame tasks for continuity |
| 19 | PRO pack upsell via DM | Marketing; not a red flag by itself but the note is a lead magnet | n/a |

---

## What exactly is Higgsfield Genjutsu, which model powers it, limits and pricing; do 36/84 credits match?

### Takeaway
Genjutsu is Higgsfield's video-to-video re-render tool (Motion Transfer and Object Swap modes, plus a cheaper Genjutsu Lite and a later Restyle mode), launched around 31 Aug / 1 Sep 2026, accepting 4–30 s source clips and up to 30 reference images (Lite: 10). Higgsfield does not name the underlying model; "it is Seedance 2.5" is widespread speculation, not confirmed. The note's 36/84 credits for 12 s equal exactly 3 and 7 credits/s, which matches an October 2026 cost check and Higgsfield's "105 credits for 15 s 720p Motion Transfer" — so the pricing claim is Mostly true (Sept 2026 table implies ~32/~83).

### Cited Findings
- Genjutsu is a video-to-video tool that re-renders an existing clip while keeping the original motion and camera work; modes are Motion Transfer and Object Swap; a newer Restyle mode redraws a whole video in an animation style; accessible via web app, API and an MCP connector; Genjutsu Lite is faster/cheaper — [Higgsfield blog: Meet Higgsfield Genjutsu](https://higgsfield.ai/blog/higgsfield-genjutsu); [The Rundown tool page](https://www.therundown.ai/tools/higgsfield-genjutsu)
- Launch date cited as 31 August 2026 or 1 September 2026 depending on source (conflict) — search summary over [The Rundown](https://www.therundown.ai/tools/higgsfield-genjutsu), [Higgsfield blog](https://higgsfield.ai/blog/higgsfield-genjutsu)
- Motion Transfer "keeps the motion, camera and timing while rebuilding the scene from your references"; Object Swap "changes a selected character, outfit, product, location or object while preserving the rest of the original shot" — [Higgsfield Genjutsu product page](https://higgsfield.ai/genjutsu)
- Reference videos 4–30 seconds; up to 30 reference images — [Higgsfield product page](https://higgsfield.ai/genjutsu); [Higgsfield help center: How do I use Genjutsu](https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-genjutsu)
- Genjutsu Lite takes up to 10 reference images and applies changes automatically; standard takes up to 30 and lets you choose Motion Transfer or Object Swap — [Higgsfield blog](https://higgsfield.ai/blog/higgsfield-genjutsu)
- Note: the brief's "ref images up to 40" and "clip 3–30 s" were not found in any source; all found sources say 4–30 s and 30 images (10 for Lite). Seedance 2.5's own docs list "up to 30 images" and "up to 50 assets" total — [docs.seedance.tv guide Part 1](https://docs.seedance.tv/) (downloaded copy)
- Pricing (Higgsfield table, Sept 2026): 15 s 480p = 40 credits ($2.00); 15 s 720p = 104 credits ($5.20); 15 s 1080p = 144 credits ($7.20); "credit costs may vary by generation settings" — search summary of [Higgsfield blog](https://higgsfield.ai/blog/higgsfield-genjutsu) / [Higgsfield pricing explained](https://higgsfield.ai/blog/higgsfield-pricing-explained)
- Higgsfield blog also says Genjutsu Lite = 96 credits for 15 s at 720p vs 105 for standard Motion Transfer (105/15 = 7 credits/s) — [Higgsfield blog](https://higgsfield.ai/blog/higgsfield-genjutsu). Separately Higgsfield says Lite costs "approximately one-third" of standard — conflict with 96 vs 105 (same search). Unresolved.
- Independent cost check (26 Oct 2026): 14 s Motion Transfer 480p = 42 credits, 720p = 98, 1080p = 280; Object Swap 45 / 105 / 300; Lite 720p 30, 1080p 60, no 480p on web — [aliteq: what is Higgsfield Genjutsu](https://aliteq.com/what-is-higgsfield-genjutsu)
- API rate: Genjutsu from $0.154/s (range quoted $0.1540–$0.8346/s by resolution); Genjutsu Lite from $0.050/s; listed as its own model separate from Seedance 2.5 — [Open Higgsfield API](https://higgsfield.ai/higgsfield-api); [open.higgsfield.ai pricing](https://open.higgsfield.ai/pricing)
- Underlying model: Higgsfield does not disclose it; Kavel says Reddit users guess Seedance 2.5 (unconfirmed) — [Kavel review](https://www.kavel.ai/blog/higgsfield-genjutsu-price-guide) (competitor/affiliate site); Creative Pad Media / a YouTube video title asserts "Genjutsu AI (Seedance 2.5)" without official backing — [Creative Pad Media](https://www.creativepadmedia.com/forget-vfx-change-anything-in-a-video-genjutsu-ai-seedance-2-5/); [YouTube](https://www.youtube.com/watch?v=hkoMNkHTNjM)
- Higgsfield's own X post says Seedance 2.5 adds the cinematic pass in "3D Genjutsu" (with GPT-6 Astra building geometry) — a different product (3D Jutsu), so not proof for video Genjutsu — [Higgsfield on X](https://x.com/higgsfield_ai/status/2096109301916205380)
- WaveSpeed sells a "Genjutsu Studio" built on "Seedance 2.5 Motion Control" at $1.10/run — this is a competitor clone, not Higgsfield — [WaveSpeed Genjutsu Studio](https://wavespeed.ai/genjutsu-studio)
- Output: WaveSpeed says length, aspect ratio and camera follow the original clip, up to 1080p (480p drafts, 1080p final); Creaa (competitor) says the result keeps length and "closest supported aspect ratio" at 720p — conflict — [WaveSpeed alternative page](https://wavespeed.ai/higgsfield-genjutsu-alternative); [Creaa](https://creaa.ai/blog/higgsfield-genjutsu-alternative)

### Inferences
- 36/12 = 3.0 credits/s and 84/12 = 7.0 credits/s. These match the aliteq Oct check (42/14 = 3.0; 98/14 = 7.0) exactly and Higgsfield's "105 for 15 s 720p" (7.0/s). The Sept table (40/15 = 2.67; 104/15 = 6.93) would give ~32 and ~83 for 12 s. So the note's numbers are accurate for roughly Oct–Nov 2026 Motion Transfer pricing; Object Swap is slightly higher (~3.2/7.5 per s). Verdict: Mostly true. Dollar equivalent at ~$0.05/credit (Sept table): ~$1.80 (480p) and ~$4.20 (720p) per 12 s take, before plan discounts.
- Higgsfield's Seedance 2.5 page charges 24/56 credits for 8 s at 480p/720p = the same 3/7 credits/s as Genjutsu Motion Transfer (see next section). Identical per-second pricing is weak circumstantial evidence that Genjutsu wraps Seedance 2.5 (or is priced to match it); still unconfirmed.
- The note calls Genjutsu "motion control"; the actual mode name is Motion Transfer. Minor terminology slip.

### Gaps
- No official Higgsfield statement of the underlying model.
- Whether Genjutsu (Higgsfield) honours 4:3 output and what exact output resolutions/frame rate it uses could not be confirmed from a primary source.
- Whether Genjutsu supports user-referenced labels like "Video 1 / Image 1" in the prompt (the note implies it does) was not confirmed; Higgsfield help pages were only seen via search summary.
- "Up to 40 images" and "3–30 s" from the brief were not found anywhere.

## Seedance 2.5 directly (Dreamina, fal.ai, BytePlus, Higgsfield Seedance 2.5): same video-reference capability? What is lost/gained?

### Takeaway
Yes — Seedance 2.5 natively supports "motion and camera reference", including explicit "blockout timing" inheritance, with up to 10 video clips (30 s total) + 30 images in one request, and the official guide contains a near-identical "fully re-render Video 1 preserving action paths, camera movement, timing and framing exactly" example. Using it directly gains explicit control over aspect ratio, resolution (1080p on several hosts), duration, audio, and the full four-part prompt; it loses Genjutsu's simplified UI/mode presets. Price on Higgsfield is the same per second; API hosts bill per second in dollars.

### Cited Findings
- Official guide: Seedance 2.5 generates clips up to 30 s, accepts up to 50 image/video/audio assets per request; capability group "Motion and camera reference — inherit movement, expression, camera motion, effects timing, or blockout timing" — [docs.seedance.tv Seedance 2.5 Prompting Guide Part 1](https://docs.seedance.tv/) (downloaded)
- Input recommendations: images up to 30 (≤4K each, 1–8 subjects most reliable); video up to 10 clips, 30 s total; blockout "prefer simple geometry; remove motion paths, axes, and camera frustums so they do not leak into the result" — same source
- "Fine Blockout Re-render" example prompt: "Fully re-render Video 1 while preserving its action paths, camera movement, timing, and framing exactly... Do not generate motion paths, axes, or camera guides." Coarse-blockout example: "Use Video 1 only for the complete shot order, camera positions, framing changes, subject paths, and timing. Do not copy the blockout materials or character appearance." — same source
- Reference tasks are "unlocked": output duration and aspect ratio remain independent of the asset; locked tasks (editing, first/last frame, extension) inherit aspect ratio — same source
- Higgsfield's Seedance 2.5 page/help: up to 30 images, 10 video clips, 10 audio files per generation; available on Pro/Plus and above, not Starter/Basic; native resolution claims conflict (1080p product page vs "native 4K" landing page vs third-party 480p/720p ceiling) — [Higgsfield blog: Seedance 2.5 on Higgsfield](https://higgsfield.ai/blog/seedance-2-5-on-higgsfield-2026); [Higgsfield Seedance 2.5 page](https://higgsfield.ai/seedance/2.5); [aivideosensei settings guide](https://aivideosensei.com/guides/seedance-2-5-higgsfield-settings)
- Higgsfield Seedance 2.5 credits: 8 s clip = 24 (480p), 56 (720p), 128 (1080p), i.e. ~3/7/16 credits/s; other Higgsfield posts give conflicting figures (e.g. 72 credits for 8 s 1080p; 30/70/160 for 10 s) — [Higgsfield Seedance 2.5 pricing](https://higgsfield.ai/blog/seedance-2-5-pricing-2026); [novoads](https://novoads.ai/blog/higgsfield-vs-seedance)
- Segmind per-second: ~$0.1065 (480p), $0.2389 (720p), $0.5876 (1080p) — [Segmind pricing](https://www.segmind.com/models/seedance-2.5/pricing)
- BytePlus ModelArk 1080p about $2.84 per 5 s (≈$17 for 30 s) — [CozyClay camera control](https://cozyclay.org/) (downloaded; secondary citation)
- Runware documents Seedance 2.5 "motion control": reference video supplies motion, camera, lip-sync; reference image supplies identity — [Runware motion-control guide](https://runware.ai/docs/models/bytedance-seedance-2-5/guides/motion-control)
- fal resolution conflict: main fal guide says 480p/720p only; fal multi-angle guide says reference-to-video offers 480p–1080p (720p default) — [fal: What is Seedance 2.5](https://fal.ai/learn/tools/what-is-seedance-2-5); [fal multi-angle guide](https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5)
- Curious Refuge did exactly the note's workflow but with Seedance 2.5 directly (via Magnific): Blender animatic as video reference + Image 1–3, 10 s, 16:9, 480p draft; "Seedance followed our Blender animation closely" — [Curious Refuge tutorial](https://curiousrefuge.com/) (downloaded, 16 Oct 2026)

### Inferences
- Step translation for direct Seedance 2.5: steps 1–2 (shot list, Blender blockout) unchanged; step 3 becomes "reference-to-video" with Video 1 = blockout, Images = refs, and the four-part prompt; you must set aspect ratio/duration/resolution yourself (reference tasks do not lock them), whereas Genjutsu reportedly follows the source clip.
- Gains: explicit aspect/duration/res control, audio control, 1080p on many hosts, API automation (fal/BytePlus/Runware/Segmind), and the vendor's own prompting guidance applies verbatim. Losses: Genjutsu's one-click mode presets (Object Swap preserving the rest of the plate) and simpler UI. Price on Higgsfield is essentially identical per second.
- If Genjutsu is Seedance 2.5 underneath (unconfirmed), there is little quality reason to prefer Genjutsu for blockout-to-render; Object Swap on real footage is where Genjutsu's preset may add value.

### Gaps
- No side-by-side test of the same blockout through Genjutsu vs Seedance 2.5 reference-to-video.
- Dreamina and BytePlus UI specifics for video-reference tagging not confirmed (search returned nothing specific).

## Is 4:3 1440x1080 30fps a good choice? Does Seedance 2.5 output 4:3? Does input fps matter?

### Takeaway
It works but is not a good default. Seedance 2.5 accepts 24–60 fps reference video and outputs fixed 24 fps, so 30 fps is fine as input (timing in seconds is preserved, frames are not). 4:3 is a supported output ratio on fal reference-to-video, but you should match the blockout ratio to your delivery ratio (CozyClay advice); 1440x1080 is far above the 480p/720p generation resolution, so ~720p (Curious Refuge) is enough.

### Cited Findings
- Reference video input: MP4/MOV, 2–30 s per clip, 24–60 fps, <200 MB, ≥409,600 pixels; output fixed at 24 fps — [Sogni docs](https://docs.sogni.ai/models/seedance-2-5/); [cellcog pricing](https://cellcog.ai/blog/seedance-2-5-pricing/); [liyue-aigc capabilities file](https://github.com/liyue-aigc/seedance-2-5-video-director/blob/main/references/capabilities-and-limits.md) (third-party, aggregated)
- fal: aspect_ratio on text-to-video and reference-to-video takes auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 (default auto) — [fal Seedance 2.5 guide](https://fal.ai/learn/tools/what-is-seedance-2-5)
- CozyClay: "Export a flat clip. Same aspect ratio as the delivery (16:9 or 9:16), flat shading, 3 to 5 seconds, nothing drawn on top" — [CozyClay](https://cozyclay.org/) (downloaded)
- Curious Refuge starter kit "is already configured to render a 720p reference video, which is plenty for guiding an AI video model" — [Curious Refuge](https://curiousrefuge.com/) (downloaded)
- Genjutsu reportedly keeps source aspect ratio (WaveSpeed) or "closest supported" ratio (Creaa) — [WaveSpeed](https://wavespeed.ai/higgsfield-genjutsu-alternative); [Creaa](https://creaa.ai/blog/higgsfield-genjutsu-alternative)

### Inferences
- 1440x1080 = 1.56 MP, comfortably above the 409,600 px minimum; 960x720 (0.69 MP) would also pass and render faster. Larger is harmless but wasteful.
- 30 fps → 24 fps output means "frame for frame" cannot be literal; beats timed in seconds will hold.
- 24 fps blockout is the cleaner choice (no resampling); 30 fps is not wrong.
- 4:3 is fine for a stylistic choice or to match a 4:3 deliverable; for social/16:9 delivery, render the blockout in the delivery ratio to avoid reframing.

### Gaps
- No primary ByteDance/BytePlus doc seen directly for the 24–60 fps figure (only third-party aggregations).
- Whether Genjutsu on Higgsfield outputs 4:3 untouched could not be confirmed.

## Is "one colour per thing" supported or contradicted?

### Takeaway
Genuinely contested. CozyClay says grey/flat clay with at most one highlight colour, because colour is preserved by the model; Scenario/fal guidance favours colour-coded proxies each named in the prompt. The note sits with the colour-coding camp and mitigates the leak risk with its "tell it what the colours are NOT" rule — a reasonable, though untested, combination. Best evidence: colour-coding helps when several similar subjects must stay distinct; grey is safer for a single hero.

### Cited Findings
- "Should the greybox have textures or colours? No. Grey or flat clay. Colour is a cue the model preserves... A single highlight colour on the subject is the most you should add." — [CozyClay](https://cozyclay.org/) (downloaded; vendor of a competing tool)
- Scenario: colour-coded previs works because each prompt names every shape, so a yellow blob becomes a specific object; use legless capsules for characters — [Scenario Explorations](https://www.scenario.com/explorations); Scenario's skills repo includes a Blender blockout skill for "color-coded proxies at metric scale" — [scenario-labs/skills](https://github.com/scenario-labs/skills)
- fal: map each geometric object separately to its final subject or prop — [fal: How to use Seedance 2.5](https://fal.ai/learn/devs/how-to-use-seedance-2-5)
- Official guide: "Do not copy the blockout materials or character appearance" — [docs.seedance.tv Part 1](https://docs.seedance.tv/) (downloaded)
- Curious Refuge: Seedance can follow the reference "almost too closely", including unnatural poses; tell it to treat 3D figures as placeholders — [Curious Refuge](https://curiousrefuge.com/)

### Inferences
- The note's brown-palm = leather trick exploits exactly the "colour is preserved" behaviour CozyClay warns about — i.e. colour leakage is a feature when you want it and a bug when you don't. Both camps describe the same mechanism.

### Gaps
- Could not locate the specific Scenario PR about "5 similar runners" via search (the coordinator's claim stands unverified from my side).

## Do the prompt-structure tips align with the Seedance 2.5 guide?

### Takeaway
Yes, closely. REFERENCE MAP ≈ "asset mapping" (bind each upload, state what to inherit and what not to); MOMENT n ≈ "timeline" with continuous whole-second ranges; GLOBAL RULES ≈ "global constraints". The note omits the official "one-sentence brief" and places global rules before the timeline (order difference, not known to matter). Its decimal timings (0.0–2.3 s) go beyond the guide's "whole-second timestamps".

### Cited Findings
- "Asset mapping + one-sentence brief + timeline or shot order + global constraints"; global constraints = "rules that apply throughout, such as camera position, lighting, color, ambience, aspect ratio, no subtitles, or no BGM" — [docs.seedance.tv Part 1](https://docs.seedance.tv/)
- "Seedance 2.5 can follow whole-second timestamps. Time ranges should be continuous... without unexplained gaps"; too little content → model improvises, too much → actions omitted — same source
- "Every asset should answer two questions: Who or what does it belong to? What specifically should be referenced? If only part of an asset should be used, also state what must not be inherited." — same source
- CozyClay: with a reference clip, "Do not describe the camera again in words; the clip already did" — [CozyClay](https://cozyclay.org/); contrasted by Curious Refuge: repeating shot timings in the prompt "can help Seedance follow the sequence" — [Curious Refuge](https://curiousrefuge.com/) (conflict on redundancy)

### Inferences
- "Never put timed events in GLOBAL RULES" is a direct consequence of the guide's definition of global constraints — True.
- "Tell it what the proxy colours are NOT" matches the guide's "state what must not be inherited" — True.
- "Never write 'already'" is a specific anecdote; consistent with timeline logic but unverified as general.
- Sub-second boundaries (2.3 s) may be rounded by the model; prefer whole seconds per the guide.

### Gaps
- None major.

## Is "frame for frame" plausible? Independent fidelity tests?

### Takeaway
Overstated. Camera path and beat timing being closely followed is plausible and reported by Curious Refuge (Seedance 2.5) and shown in the official blockout examples, but no independent test of Genjutsu blockout fidelity was found, output is 24 fps (input 30 fps), and reviewers report drift under occlusion, fast motion and large perspective changes. The comparison GIF in the note is a single cherry-picked author demo.

### Cited Findings
- No review found that tests Genjutsu with a blockout/greybox; vendor-aligned reviews claim "frame-accurate camera movements"; independent-ish sources note drift with overlapping people, fast turns, partially hidden objects, occlusion and large perspective changes — search summary over [stork.ai](https://www.stork.ai/en/higgsfield-genjutsu), [litmedia](https://www.litmedia.ai/resource-ai-tips/higgsfield-genjutsu-review/), [Riffkit](https://riffkit.ai/blog/how-to-use-higgsfield-genjutsu), [imageat](https://imageat.com/blog/higgsfield-genjutsu-review-features-pricing-apis)
- Some users report Genjutsu renders "processing" for days — [Riffkit](https://riffkit.ai/blog/how-to-use-higgsfield-genjutsu) (competitor-adjacent, anecdotal)
- Curious Refuge: "Seedance followed our Blender animation closely... camera angles, cuts, character positions"; but character motion looked "video-game-like" — [Curious Refuge](https://curiousrefuge.com/)
- CozyClay demo: "The pillar, the fall and the camera all hold" (vendor demo); longer references "drift more toward the end of the clip"; recommends 3–5 s clips — [CozyClay](https://cozyclay.org/)
- Seedance 2.5 launch material acknowledges limits in complex-motion plausibility and interacting subjects — search summary over Seedance 2.5 reviews, e.g. [buildfastwithai](https://www.buildfastwithai.com/blogs/seedance-2-5-bytedance-ai-video-review-2026)

### Inferences
- "Same camera, same timing" is a fair description of best-case results; "frame for frame" is marketing language. A 12 s clip is long relative to CozyClay's 3–5 s advice; expect more end-of-clip drift (unverified for Genjutsu).
- 3,600 animated rats as tan blocks is a stress case for "Never render a block"; dense small proxies are exactly what the guide warns can leak.

### Gaps
- No quantitative (e.g. optical-flow / keypoint) fidelity measurements exist publicly for either path.

## Other technical claims (Blender)

### Takeaway
The headless CLI (`blender -b -P script.py`) is correct and timeless; "Blender 4.x / 4.0" is outdated as of Nov 2026, and the hard-coded `C:\Program Files\...\Blender 4.0\` path will fail on any other install.

### Cited Findings
- Blender 5.3 released ~9–10 Nov 2026; 5.2 LTS released 14 Jul 2026 (supported to Jul 2028); 4.5 LTS supported until Jul 2027; 4.2 LTS ended — [Phoronix](https://phoronix.com/news/Blender-5.3-Released); [endoflife.date](https://endoflife.date/blender)
- Video output is a single image type (FFMPEG) set via render image settings; standalone pip `bpy` lacks FFmpeg, so running with the full Blender binary (`blender -b -P`) is the workaround — [Blender issue #118493 / search summary](https://projects.blender.org/blender/blender/issues/118493); [technetexperts](https://www.technetexperts.com/blender-python-ffmpeg-error/)
- Blender 5.x FFmpegSettings still exposes H.264/AV1/H.265 codecs and containers — [Blender 5.2 API FFmpegSettings](https://docs.blender.org/api/5.2/bpy.types.FFmpegSettings.html)

### Inferences
- A script written for 4.0 will mostly run on 5.x, but bpy API changes across 4.x→5.x (e.g. engine identifiers, some render/output settings) may break it; ask Claude to target the installed version. (Specific 5.x breaking changes not verified here.)
- Workbench render is the right engine for flat colour proxies (fast, no lighting noise); also consistent with CozyClay's "Blender works with a clay material and a workbench render".

### Gaps
- Did not verify each specific 4.0→5.3 bpy break.

## Who is @viznfr; marketing; red flags

### Takeaway
@viznfr runs viznfr.com, self-described "AI Creative Director"; little else is publicly verifiable. The note is a lead magnet: it ends by withholding the actual build script and full prompt for a paid "PRO pack" waitlist via DM. The technique itself is legit and mirrors free sources (official Seedance guide, Curious Refuge, CozyClay).

### Cited Findings
- viznfr.com describes itself as an "AI Creative Director", lists @viznfr handle and a media contact; 2026 site; an unrelated-or-related vizn.fr ("VIZN — Visual Intelligence", music videos/commercials/reels) exists, connection unconfirmed — [viznfr.com](https://www.viznfr.com/); [vizn.fr](https://vizn.fr/)
- No affiliation disclosure with Higgsfield found; Higgsfield runs creator affiliate links (e.g. `?fpr=` referral parameters appear on many Higgsfield URLs in search results) — e.g. [Higgsfield Seedance pricing with fpr param](https://higgsfield.ai/blog/seedance-2-5-pricing-2026?fpr=gabriel-c5d7b4)

### Inferences
- Red flags (mild): (1) "frame for frame" overclaim; (2) key assets gated behind DM/waitlist; (3) tool-specific framing (Genjutsu) for a workflow that works identically with Seedance 2.5 reference-to-video; (4) hard-coded outdated Windows path suggests copy-paste from personal setup. No evidence of anything deceptive; pricing numbers are accurate.
- Whether @viznfr is a Higgsfield affiliate/partner is unknown.

### Gaps
- Could not access X/Instagram profile or follower data; no independent info on the author's track record.
