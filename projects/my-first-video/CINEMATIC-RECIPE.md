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
