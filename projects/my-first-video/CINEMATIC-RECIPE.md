# Cinematic recipe — consistent shots in de stijl van "variant 1"

Doel: telkens dezelfde kwaliteit/stijl als de goedgekeurde cinematic water-review shot — jij **echt geïntegreerd** in de scène (geen green-screen/compositing), je **echte gezicht**, je echte huid.

## Kernidee
Genereer de **hele scène nieuw** met je **character sheets als referentie**. Niet compositen, niet de Soul gebruiken.

## STILL (de cinematic foto)
- **Model:** Nano Banana Pro (`nano_banana_pro`), `resolution: 2k`
- **Aspect:** `16:9` (cinematic) of `9:16` (UGC verticaal)
- **Referenties** (`medias`, role `image`): 2 frames uit de gekozen outfit-sheet —
  een **chest-up frontaal** + een **close-up portret**. Die vergrendelen identiteit + outfit.
- **Prompt-template** (vul `[...]` in):

> Cinematic commercial still of this EXACT man. [SCENE: softly lit modern setting]. He [ACTION: calmly holds / presents PRODUCT] like a genuine, understated testimonial — relaxed, neutral, composed expression, NO exaggerated emotions, eyes to camera. Cinematic look: 50mm lens, shallow depth of field, creamy background bokeh, soft key light + gentle rim light, filmic colour grade, subtle film grain, professional commercial cinematography. Keep his face 100% consistent with the reference images — same reddish-brown beard and hair, same eyes, nose, mouth, jaw and proportions, and his real EVEN natural skin (low contrast, only his light freckles, no beautify, no extra red blemishes or contrast). He wears [OUTFIT] from the reference; do not invent other clothing. He must be naturally lit BY the scene and fully integrated (not pasted, not green-screen). Photoreal, realistic, not AI-looking.

## De 5 hefbomen (waarom dit werkt)
1. **Altijd je sheet-frames als referentie** meegeven → identiteit + outfit kloppen.
2. **"naturally lit BY the scene / fully integrated / not green-screen"** → geen uitgeknipte look.
3. **"even natural skin, no beautify, no extra red/contrast"** → jouw echte huid (geen rode vlekjes/te veel contrast).
4. **Ingehouden expressie** (geen brede lach) → minder gezicht-vervorming.
5. **Cinematische termen**: 50mm, shallow DOF, rim light, film grain, colour grade.

## VIDEO (beweging)
- Neem de **goedgekeurde still** → **Kling 3.0**, `mode: pro`, aspect = zelfde als de still.
- Prompt: **alleen subtiele beweging** (kleine hoofd-/handbeweging, knipperen, trage camera push-in).
  Identiteit hard vastzetten: *"keep the exact same face, no morphing, no big expression, no talking, mouth relaxed/closed."*
- ⚠️ Grote glimlach / open mond / praten → gezicht vervormt. Vermijden voor stille clips.

## PRATENDE review (jouw stem)
- In-tool lip-sync naar **jouw** stem is op Higgsfield-accountniveau vergrendeld.
- Doe de spraak + lip-sync **extern** (Hedra / HeyGen) met de cinematic still als basis + jouw audio
  (zelf ingesproken, of via een stemkloon van je opgeschoonde sample).

## Outfits — enkel deze 5 (met de bijhorende sheet, niets verzinnen)
blauw t-shirt · wit hemd · blauwe pul · zwarte pul · groene pul

---
Kort: **sheets als referentie + Nano Banana Pro + bovenstaande prompt → cinematic still**, daarna **Kling pro** voor beweging, en **extern** voor jouw stem.

---

## Upgrades uit de officiële Higgsfield skills-repo (higgsfield-ai/skills)

**Prompt-skelet (officieel):**
`subject + setting + style → lens (35/50/85mm) + hoek + camerabeweging → belichting (rim/backlight/neon) → medium (photograph/cinematic)`.
Hou het **< ~200 tokens** (te lang = vervorming). Gebruik **positieve** bewoording: *"tack sharp"* i.p.v. "no blur", *"uninhabited landscape"* i.p.v. "no people".

**Video = ALLEEN beweging beschrijven:** bij image-to-video het stilstaande beeld NIET herbeschrijven — enkel de motion. Vocab: *"slow push in, camera slowly pulls back, dolly left, sweeping pan, subtle head turn, ambient motion."*

**Modellen (echte CLI-ID's, bevestig met de catalog):**
- Cinematic still: `soul_cinematic` (film-licht, ook **21:9**) of `cinema_studio_image_2_5` (tot 4K). Onze `nano_banana_pro` + sheets blijft top voor referentie-trouw.
- Beweging/multi-shot video: `seedance_2_0` (4–15s, SOTA). Voor gezicht-trouw werkte **Kling pro** bij ons het best — beide bruikbaar.
- Hero cinematic: `cinema_studio_video_3_0` of `google_veo_3_1` (let op: enkel **4/6/8s**, **16:9 of 9:16**).

**Lip-sync (te hertesten — mogelijke unlock):** de repo stelt dat `seedance_2_0` + een **audio-rol** lip-synct naar JOUW audio (en NIET `generate-audio` gebruiken). Als dat in onze MCP echt zo werkt, kan jouw-stem-in-tool alsnog → apart valideren met je echte opname.

**UGC via Marketing Studio:** modes `ugc`, `ugc_unboxing`, `product_review`, `ugc_how_to`, `ugc_virtual_try_on` + **hooks/settings** (hook = opening, wordt vóór de prompt geplakt). Teststrategie: eerst **4 hooks × 1 mode**, dan pas modes wisselen. Default shorts: **9:16, 720p, 15s**.

**Virality Predictor (`brain_activity`):** score een afgewerkte short (piek-hook %, sustain %, aandacht-regio's) vóór posten; zwakke eerste seconde → hook + openingslijn hermaken. Lagere "Default Mode" = beter.

**Scripts voor spraak:** ~**150 woorden/min** (60s ≈ 150 woorden), korte zinnen, natuurlijke pauzes, niet opvullen om de duur te halen.

**Identiteit op schaal:** voor talking-head > 30s raadt de repo een getrainde **Soul** (`soul_cinematic`) aan, 8–12 gevarieerde foto's. Jij verkoos echter sheets-als-referentie (trouwere look) — dat houden we als standaard; Soul enkel als je lange talking-heads wil.

---

## ⭐ CRUCIAAL — Gezicht 1:1 houden (face-anchor stap)

**Probleem:** bij een scène/medium-full shot met een **klein gezicht** hertekent Nano (of elke generator) je gezicht naar een **wildvreemde lookalike**. Niet 1:1.

**Oplossing — vaste 3-staps pijplijn:**
1. **Scène/lichaam** → `nano_banana_pro` met je sheets als referentie (lichaam, outfit, stad, kader = top; gezicht mag nog afwijken).
2. **Gezicht verankeren** → `seedream_v4_5` (face-anchored edit): voer de Nano-still in als beeld 1 + je **sheet-gezicht** (chest-up of close-up) als beeld 2, prompt: *"Edit ONLY the man's face to be an EXACT match of the reference person's face; keep body, clothing, pose, background and lighting identical."* → gezicht = jouw echte gezicht, rest ongemoeid.
3. **Animeren** → `seedance_2_0` met de **gecorrigeerde still** als `start_image`. Seedance behoudt het gezicht van het startframe, dus de video houdt nu jouw echte gezicht.

**Waarom dit werkt:** Seedance dreef het gezicht niet over de frames — het hield het startframe-gezicht consistent. Het startframe-gezicht was alleen fout. Fix het startframe met `seedream_v4_5` → de hele video klopt.

⚠️ Voor een écht pixel-1:1 gezicht op bewegend beeld is de ultieme route nog steeds **externe face-swap** (per frame), net als externe lip-sync voor je stem. `seedream_v4_5` komt er in-tool het dichtst bij en is meestal voldoende.

---

## ⭐⭐ DEFINITIEVE "exact jij"-pijplijn (bevestigd)

Twee dingen samen geven het beste resultaat:

**A) Kader sheet-nabij houden.** Hoe groter + frontaler je gezicht in beeld, hoe exacter. Chest-up/medium = ✅ jij; wijd/klein gezicht = ⚠️ benadering (geen enkele methode redt een klein gezicht).

**B) Echte-foto face-swap als identiteits-lock** (lokaal, InsightFace):
- Geïnstalleerd: `pip install insightface onnxruntime opencv-python-headless`; model `inswapper_128.onnx` + `buffalo_l`.
- Bron = **gemiddelde embedding** uit meerdere **échte** frontale foto's (uit je zip), niet de AI-sheet → trouwste identiteit.
- Pas toe op de Nano-still, dan animeren met Seedance (start_image = geswapte still). Seedance behoudt het startframe-gezicht.

**Volgorde:** Nano (sheet-nabij kader) → InsightFace face-swap (echte foto's) → Seedance animeren.
**Grens:** `inswapper_128` is 128px en raakt het haar/hoofd niet → het is een sterke benadering, geen letterlijke pixel-1:1. Voor absolute 1:1: film echte beelden, of sheet-nabij kader waar het natief al klopt.
