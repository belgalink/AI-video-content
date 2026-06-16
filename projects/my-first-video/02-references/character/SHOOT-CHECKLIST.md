# Character Reference Shoot — Checklist (Belgalink)

Doel: een schone, consistente set foto's + audio van jezelf, zodat Claude + Higgsfield
jouw gezicht en stem op de hoogst mogelijke kwaliteit kan reproduceren in alle video's.

> Gouden regel: **consistentie en scherpte > kwantiteit**. Liever 40 scherpe, goed
> belichte foto's dan 200 wazige.

---

## 1. Setup (eerst goed zetten, daarna pas schieten)

- [ ] **Achtergrond**: effen, neutraal (wit / lichtgrijs muur). Geen rommel, geen patroon.
- [ ] **Licht**: zacht en gelijkmatig. Daglicht bij een raam (zonder directe zon) of een softbox.
      Vermijd harde schaduwen en gemengd licht (geen half geel lamplicht + blauw daglicht).
- [ ] **Camera op statief**, ooghoogte, zelfde afstand per serie.
- [ ] **Scherpstellen op de ogen**, sluitertijd hoog genoeg zodat niets wazig is.
- [ ] **Hoogste resolutie / RAW of fijnste JPEG**. Geen filters, geen beauty-mode.
- [ ] **Grooming consistent**: zelfde kapsel/baard door de hele shoot (anders wordt de AI in de war gestuurd).

---

## 2. Foto's — per outfit dezelfde serie schieten

Schiet voor **ELKE outfit** onderstaande set. Zo blijft alles vergelijkbaar.

### A. Gezicht / hoofd (close-up, schouders in beeld) — neutrale expressie
- [ ] Recht vooraan (camera op ooghoogte)
- [ ] 3/4 links (hoofd ~45° gedraaid)
- [ ] 3/4 rechts (~45°)
- [ ] Profiel links (90°)
- [ ] Profiel rechts (90°)
- [ ] Lichtjes van boven gefotografeerd
- [ ] Lichtjes van onder gefotografeerd

### B. Gezicht — expressies (recht vooraan)
- [ ] Neutraal, mond dicht
- [ ] Glimlach (tanden)
- [ ] Pratend / mond half open (alsof je praat tegen camera)
- [ ] Wenkbrauwen omhoog / geanimeerd

### C. Medium shot (heup tot hoofd)
- [ ] Recht vooraan, armen ontspannen
- [ ] 3/4 links
- [ ] 3/4 rechts
- [ ] Met handen zichtbaar / gebaar (AI is zwak in handen → geef goede voorbeelden)

### D. Full body (hoofd tot voeten)
- [ ] Recht vooraan
- [ ] 3/4 links
- [ ] 3/4 rechts
- [ ] Achterkant (rug naar camera)
- [ ] Zittend (optioneel, als je veel "aan bureau" content wil)

➡️ Dat zijn ~20 foto's per outfit. Doe dit voor 3-5 outfits.

---

## 3. Outfits — kies bewust (denk aan Belgalink Instagram)

- [ ] **Outfit 1 — "talking head / professional"**: hoe je in je video's tegen de camera praat.
- [ ] **Outfit 2 — casual / herkenbaar**: dagelijkse brand-look.
- [ ] **Outfit 3 — neutraal basic** (effen T-shirt): makkelijkst voor de AI om mee te werken.
- [ ] (optioneel) Outfit 4-5: extra varianten / seizoen / context.

Tip: minstens één outfit met een **effen, niet te druk** kledingstuk — dat geeft de schoonste reference.

---

## 4. Audio (voor stemkloon / voice-over)

- [ ] **Stille ruimte**, geen echo (zachte materialen helpen: gordijnen, kleren).
- [ ] **Goede microfoon dichtbij** (niet de laptopmic). Zelfde mic/afstand door de hele opname.
- [ ] Spreek in je **natuurlijke video-stem** (zoals je tegen je publiek zou praten).
- [ ] Neem **2-3 minuten schone, aaneengesloten spraak** op. Variatie is goed:
  - [ ] Een paar normale, rustige zinnen
  - [ ] Een paar enthousiaste zinnen
  - [ ] Een paar zinnen met getallen / je merknaam "Belgalink"
- [ ] Eén lange take is beter dan veel kleine stukjes. Geen achtergrondmuziek.
- [ ] Lever aan als **WAV of hoge-kwaliteit MP3**.

---

## 5. Waar zet je de bestanden? (mappenstructuur)

- Ruwe foto's (alles, ongesorteerd) → `02-references/character/attempts/`
- Stem-opnames → `02-references/character/` (of een submap `audio/`)
- Zodra we samen de beste selecteren → die gaan naar `02-references/character/approved/`
- Afgekeurd / wazig → `02-references/character/disapproved/`

Volgende stap na de shoot: ik laat Claude + Higgsfield hieruit een
**character reference sheet** genereren (één beeld met al je hoeken), die we daarna
in elke video-prompt hergebruiken voor een consistent gezicht.

---

### Mini-samenvatting (als je snel wil starten)
1 effen achtergrond + zacht gelijkmatig licht.
Per outfit: 7 gezichtshoeken + 4 expressies + 4 medium + 4 full body.
3-5 outfits, waarvan 1 heel basic.
2-3 min schone audio met goede mic.
Alles in `02-references/character/attempts/`, dan kiezen we samen de beste.
