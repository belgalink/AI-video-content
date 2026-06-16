# Character Reference Bible — `lead` (Belgalink presentator)

De identity-locked referentieset van de presentator, gegenereerd met Higgsfield.
Dit is de **vaste input** voor élke latere video-prompt: hergebruik de juiste hoek/expressie
zodat het gezicht consistent blijft over alle clips.

## Hoe gemaakt
- **Model:** Nano Banana Pro (Higgsfield), 2K, fotorealistisch, multi-referentie.
- **Bron:** echte foto's van de presentator vanuit veel hoeken/afstanden/expressies, ingevoerd
  als **multi-referentie** (niet één selfie). De **raw foto's staan bewust NIET in de repo**
  (afspraak met Diederick) — enkel het gegenereerde eindproduct leeft hier.
- **Identity-lock:** de canonieke frontaal `lead-A1-frontaal.png` is goedgekeurd door Diederick
  (smal/langer gezicht, gecorrigeerde wallen/oogschaduw). Die frontaal dient als anker voor de
  overige hoeken, samen met de echte profiel-/driekwartfoto's voor de geometrie.
- **Achtergrond:** neutraal grijs `#d8d8d8`, egale studiobelichting. Bewust technisch — herkenbare
  settings (kantoor/bureau/natuurlijk licht) komen pas in de **video-prompts**, niet hier.
- **Wardrobe:** effen donker navy crew-neck T-shirt (de basic-shirt face master set).

## Status
- ✅ **Blok A — angles (8):** frontaal, 3/4 links/rechts, profiel links/rechts, tilt omhoog (hero),
  tilt omlaag (contemplatief), 3/4 achter. → `contact-sheets/lead-sheet-A-angles.png`
- ✅ **Blok B — expressies (6):** neutraal, pratend/mid-sentence (lipsync), lichte glimlach,
  volle glimlach, wenkbrauwen-op, geconcentreerd. Bewust **echt-verankerd** (extra echte foto's +
  anti-idealisatie-prompt) zodat ze dicht bij Diedericks werkelijke uitstraling blijven.
  → `contact-sheets/lead-sheet-B-expressies.png`
- ✅ **Master-contactsheet (A+B, 14 shots):** `contact-sheets/lead-master-contact-sheet.png`
- ⬜ **Blok C — afstanden / full body** en **Blok D — handen/gebaar:** later, samen met de
  outfit-/lichaamsfoto's.
- ⬜ **Audio (stemkloon):** later.

## Bestanden
**Blok A — angles**
```
lead-A1-frontaal.png            lead-A5-profiel-rechts.png
lead-A2-driekwart-links.png     lead-A6-tilt-omhoog.png
lead-A3-driekwart-rechts.png    lead-A7-tilt-omlaag.png
lead-A4-profiel-links.png       lead-A8-driekwart-achter.png
```
**Blok B — expressies**
```
lead-B1-neutraal.png            lead-B4-volle-glimlach.png
lead-B2-pratend.png             lead-B5-wenkbrauwen-op.png
lead-B3-lichte-glimlach.png     lead-B6-serieus.png
```
**Contact sheets**
```
contact-sheets/lead-sheet-A-angles.png
contact-sheets/lead-sheet-B-expressies.png
contact-sheets/lead-master-contact-sheet.png
```
