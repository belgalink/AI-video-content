# Character Reference Sheet — Master Generation Prompt (Belgalink lead)

> **Waar voer je dit uit?** In de **Claude Desktop app** (of Claude.ai) waar de
> **Higgsfield-connector (MCP)** aan staat — NIET in Claude Code op het web (daar is
> Higgsfield niet gekoppeld). Open je Desktop app in deze repo-map en zeg:
> *"Lees en voer de prompt in `02-references/character/character-reference-sheet-PROMPT.md` uit."*
>
> **Belangrijk principe:** dit is GEEN "één-selfie" prompt. Voer **al je echte foto's**
> (verschillende angles, afstanden, expressies) in als multi-referentie. Hoe meer echte
> hoeken je geeft, hoe sterker de identity-lock. Het model normaliseert achtergrond,
> licht en kadrering — het verzint je gezicht niet, het reproduceert het.

---

## INPUT

- **Subject:** de presentator van Belgalink (label: `lead`) — de persoon op de foto's.
- **Bronmateriaal:** ALLE echte foto's uit de shoot van de *face master set* (sectie 2A/B
  van de SHOOT-CHECKLIST): frontaal, 3/4 links/rechts, profielen, tilt op/neer, plus de
  expressies. Sleep ze allemaal mee als referentie. Begin met de **basic effen T-shirt**-set
  (schoonste reference).
- **Wardrobe:** lees de kledij van de bronfoto's af en reproduceer die exact en identiek in
  élke output (één outfit per sheet).
- **Identiteit:** dit is de "lock". Gezichtsgeometrie, kapsel, baardlijn, huidtint en -textuur
  moeten exact overeenkomen met de bronfoto's. **Niet driften.** Bij twijfel: match de bron.

## GLOBALE CONSTRAINTS (gelden voor ELKE afbeelding)

- Fotorealistisch, scherpe focus, studiokwaliteit.
- Neutrale naadloze achtergrond, lichtgrijs `#d8d8d8`.
- Egale, zachte three-point-belichting, geen harde schaduwen.
- Zelfde persoon, zelfde wardrobe, zelfde haar/baard, zelfde licht — alleen verandert wat
  per shot is aangegeven (hoek / expressie / afstand / handen).
- Ingetogen, halal-conform (waardenkader). Casual-professioneel, geen pak.

---

## STEP 1 — Kies het sterkste model

Bevraag de **Higgsfield MCP modellenlijst (live)** en kies het model dat vandaag het sterkst is in:
- fotorealistische identity-preservation over meerdere generaties,
- multi-angle consistentie vanuit referentiebeelden,
- vasthouden van wardrobe, belichting en huiddetail.

Vandaag waarschijnlijk **Nano Banana Pro** of **GPT Image 2** — maar **verifieer eerst** tegen de
actuele lijst. Kies er één. Vertel mij in één zin welk model en waarom, en ga dan verder.

---

## STEP 2 — Genereer, in 4 blokken (review blok A vóór je verdergaat!)

> Genereer **blok per blok** en laat mij blok A (de identity-lock) goedkeuren vóór B/C/D.
> Zo verbranden we geen credits als de gelijkenis afwijkt. Let op rate limits.

### BLOK A — Angles / identity-lock (hoofd + schouders, neutrale expressie, oogcontact)
1. **A1 frontaal** — recht in de camera, schouders vierkant.
2. **A2 driekwart links** — hoofd+schouders ~30° naar camera-links.
3. **A3 driekwart rechts** — ~30° naar camera-rechts.
4. **A4 profiel links** — volledige zijaanzicht, camera op ooghoogte.
5. **A5 profiel rechts** — volledige zijaanzicht, ooghoogte.
6. **A6 tilt omhoog** — frontaal, kin licht omlaag ~15° zodat de ogen omhoog kijken (hero-shots).
7. **A7 tilt omlaag** — frontaal, kin licht omhoog ~15° zodat de ogen omlaag kijken (contemplatief).
8. **A8 driekwart achter** — ~135° gedraaid, achterhoofd/schouder zichtbaar (continuïteit).

### BLOK B — Expressie-range (frontaal, borst-omhoog, oogcontact)
1. **B1 neutraal / rust** — ontspannen, lichte aandacht in de blik.
2. **B2 pratend / mid-sentence** ⭐ — mond mid-woord open, tanden licht zichtbaar (cruciaal voor lipsync).
3. **B3 lichte glimlach** — mond dicht, warm-professioneel.
4. **B4 volle glimlach** — tanden zichtbaar, ogen lachen mee.
5. **B5 wenkbrauwen omhoog / "aha"** — geïnteresseerd-verrast (hooks).
6. **B6 geconcentreerd / serieus** — vertrouwen/autoriteit, geen frons.

### BLOK C — Afstand / kadrering (neutrale expressie, frontaal + driekwart)
1. **C1 extreme close-up** — gezicht vult het beeld, huid-/oogdetail (identity-detail).
2. **C2 close-up** — hoofd + schouders.
3. **C3 medium frontaal** — middel-omhoog.
4. **C4 medium driekwart** — middel-omhoog, ~30°.
5. **C5 full body frontaal** — staand, hoofd tot voeten.
6. **C6 full body driekwart** — staand, ~30°.
7. **C7 full body profiel** — staand, zijaanzicht.

### BLOK D — Handen & gebaar (medium, middel-omhoog)
1. **D1 handen ontspannen, zichtbaar.**
2. **D2 open handgebaar** — alsof je iets uitlegt.
3. **D3 telefoon vasthoudend** — "talking-to-camera"-pose.
4. **D4 gebaar naar een product-placeholder** (voor toekomstige product-shots).

---

## STEP 3 — Opslaan

Map: `projects/my-first-video/02-references/character/bible/`

```
lead-A1-frontaal.png            lead-B1-neutraal.png         lead-C1-extreme-closeup.png   lead-D1-handen-rust.png
lead-A2-driekwart-links.png     lead-B2-pratend.png          lead-C2-closeup.png           lead-D2-handgebaar.png
lead-A3-driekwart-rechts.png    lead-B3-lichte-glimlach.png  lead-C3-medium-frontaal.png   lead-D3-telefoon.png
lead-A4-profiel-links.png       lead-B4-volle-glimlach.png   lead-C4-medium-driekwart.png  lead-D4-product.png
lead-A5-profiel-rechts.png      lead-B5-wenkbrauwen-op.png   lead-C5-fullbody-frontaal.png
lead-A6-tilt-omhoog.png         lead-B6-serieus.png          lead-C6-fullbody-driekwart.png
lead-A7-tilt-omlaag.png                                      lead-C7-fullbody-profiel.png
lead-A8-driekwart-achter.png
```

## STEP 4 — Bouw de contact sheets

Na elk blok één contact-sheet (panelen in een net raster, elk paneel onderaan gelabeld met
de shotnaam in een strakke sans-serif). Daarna één **master contact sheet** met alles.

Map: `projects/my-first-video/02-references/character/bible/contact-sheets/`
- `lead-sheet-A-angles.png` (4×2)
- `lead-sheet-B-expressies.png` (3×2)
- `lead-sheet-C-afstanden.png` (4×2, laatste cel leeg)
- `lead-sheet-D-handen.png` (2×2)
- `lead-master-contact-sheet.png`

## STEP 5 — Rapporteer terug

Toon de contact sheets en bevestig:
- Welk model je gebruikte (en waarom, één zin).
- Of de identiteit standhield over alle shots (jouw eerlijke inschatting per blok).
- Welke shots zijn gedrift en heropgenomen moeten worden.
- Of er angles/expressies ontbraken in mijn bronfoto's (zodat ik die nog kan bijschieten).

---

### Productienoot
- De neutrale grijze achtergrond is bewust: dit is de **technische reference-bible**, geen
  finale content. Herkenbare settings (kantoor, bureau, natuurlijk licht) doen we later in de
  vídeo-prompts, niet hier — consistentie is hier koning.
- Zodra deze bible is goedgekeurd, is dit de **vaste input** voor élke video-prompt: we
  hergebruiken de juiste angle/expressie zodat je gezicht consistent blijft over alle clips.
