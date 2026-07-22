# Easy-Taxi Belgium — Cinematic Ad Prompt (voor Higgsfield "Cinema Studio")

Dit document is bedoeld om zelf, stap voor stap, dezelfde advertentie na te bouwen met Higgsfield's cinematische videomodel (Cinema Studio Video 3.0 / "cinematic"). De prompts zijn in het Engels geschreven (dat geeft de beste resultaten bij deze modellen); de uitleg errond staat in het Nederlands.

---

## 1. Voorbereiding: personages, wagen en locaties vastleggen (Elements)

Maak eerst 4 herbruikbare **Elements** aan in Higgsfield (Reference Elements — category "character"/"prop"/"environment"), zodat dezelfde mensen, dezelfde wagen en dezelfde nummerplaat in elke scène identiek blijven:

1. **Passagier** — man, midden dertig, kort donker haar, lichtgrijs linnen overhemd met korte mouwen, donkerblauwe broek, bruine loafers.
2. **Chauffeur** — man, eind veertig/begin vijftig, grijzend haar, kort baardje, zwart overhemd met korte mouwen, zwarte broek, zwarte schoenen, horloge.
3. **Wagen** — zwarte Škoda Superb Combi (break/station wagon), gele "TAXI"-dakbord, Belgische nummerplaat die **exact** leest als `T·XXX·XX` (geanonimiseerd formaat — nooit een echt ogende plaat, dit is bewust gekozen om juridische problemen te vermijden).
4. **Nummerplaat-detail (prop)** — los vastgelegd zodat de tekst "T·XXX·XX" in elke hoek/afstand identiek blijft: wit plaatje, blauwe EU-band met "B" links, donkerrode/bordeaux tekst, standaard Belgisch lettertype.

> Belangrijk: gebruik in elke prompt hieronder de `<<<element_id>>>`-placeholder voor deze 4 Elements zodra je ze hebt aangemaakt, zo blijven gezichten/wagen/plaat 100% consistent tussen scènes.

---

## 2. Merk & stijl (geldt voor de hele video)

- **Formaat:** 9:16 verticaal, 1080×1920, voor Facebook/Instagram Reels & Stories.
- **Logo:** klein "EASY-TAXI BELGIUM" logo (geel/zwart, taxi-dakbord icoon), permanent linksboven in beeld, ca. 300px breed, marge 44px links / 70px boven.
- **Kleurgrade:** onderkoelde, natuurlijke cinematische grade — niet overdreven contrasty, geen fel oranje-teal look. Zachte hooglichten, natuurlijke huidtinten, licht filmic contrast.
- **Camera:** overwegend statisch of zeer subtiele handheld-microbeweging. Geen zwierige drone- of gimbal-moves — dit is een realistische, ingetogen "slice of life" taxi-ad, geen actiefilm.
- **Genre-hint (indien het model dit vraagt):** `drama` of `auto` — NIET `action`, `epic` of `horror`.

---

## 3. Scène-voor-scène prompts

Elke scène = 1 losse generatie in Cinema Studio Video (duration ~4s per generatie, nadien bijgeknipt tot de gewenste lengte in de montage). Gebruik telkens een **start_image** (een eerder gegenereerde/goedgekeurde still uit dezelfde Elements) zodat personages en wagen consistent blijven.

### Scène 1 — Begroeting (luchthaven, ~2,2s in eindmontage)
```
Two men meeting calmly at a modern airport curb, next to a black Skoda Superb
station wagon taxi with a yellow "TAXI" roof sign. <<<passenger_element>>> has
just arrived with a rolling suitcase; <<<driver_element>>> is already standing
beside the parked car, waiting. Friendly, relaxed greeting -- NOT a goodbye or
a walk-away. Warm daylight, glass airport facade softly blurred in the
background, license plate <<<plate_element>>> clearly visible and unchanged.
Camera completely static, photorealistic, subtle cinematic color grade,
naturalistic, no dramatic camera movement.
```

### Scène 2 — Overdracht koffer (luchthaven, ~1,9s)
```
Close, natural moment at an airport curb: <<<passenger_element>>> lets go of
the extended suitcase handle while <<<driver_element>>> reaches out and takes
it over smoothly -- suitcase stays upright on its wheels the entire time, no
floating, no unnatural handoff. Same black Skoda Superb station wagon taxi in
the background, plate <<<plate_element>>> visible. Camera completely static,
photorealistic, cinematic, naturalistic motion.
```

### Scène 3 — Koffer inladen (luchthaven, ~1,7s)
```
Taxi driver <<<driver_element>>> loading a gray hardshell suitcase into the
open trunk of the black Skoda Superb station wagon at the airport curb.
Ordinary, realistic car trunk/boot -- not deformed, not oversized. Natural
lifting and placing motion, license plate <<<plate_element>>> visible on the
open trunk lid. Camera completely static, photorealistic, cinematic.
```

### Scène 4 — Snelweg (~1,4s)
```
The black Skoda Superb station wagon taxi driving along a highway surrounded
by green trees, seen from a three-quarter rear angle. Camera tracks alongside
the car at a constant distance and speed, smooth realistic driving motion,
license plate <<<plate_element>>> visible and legible. Understated cinematic
color grade, natural daylight, no dramatic camera movement.
```

### Scène 5 — Afscheid (gewone Belgische woonwijk, ~1,9s)
```
Two men shaking hands warmly on an ordinary upper-middle-class Belgian
residential street -- rows of normal brick terraced houses, NOT a luxury villa
neighborhood. <<<driver_element>>> and <<<passenger_element>>> next to the
black Skoda Superb station wagon taxi, suitcase standing beside them, plate
<<<plate_element>>> visible. Natural, subtle smiles -- not exaggerated
laughing. Golden-hour light. Camera completely static, photorealistic,
cinematic.
```

### Scène 6 — Aankomst / geparkeerd (~1,7s)
```
The black Skoda Superb station wagon taxi parked in front of an ordinary
Belgian brick house on a quiet residential street at golden hour, plate
<<<plate_element>>> visible. Subtle environmental motion only -- leaves
gently swaying in the breeze. Camera completely static, understated
cinematic color grade, warm light.
```

---

## 4. Audio & dialoog (Vlaams)

Gebruik voor de dialoog-scènes (1, 2 en 5) een **audio-reference** (niet enkel een tekstprompt "lips moving") -- upload de eigen ingesproken/gekloonde dialoogaudio en koppel die als audio-driving input aan de generatie. Dat is het enige wat écht werkende lipsync geeft; een prompt als "mouth moving as if talking" zonder audio-referentie geeft nooit synchrone mondbewegingen.

Dialoog (Vlaams, natuurlijk vloeiend):

- **Scène 1** — Chauffeur: *"Goede dag! Alles in orde, goede reis gehad?"* — Passagier: *"Ja, het was een rustige vlucht."*
- **Scène 5** — Passagier: *"Bedankt voor de rit."* — Chauffeur: *"Graag gedaan! Tot de volgende keer!"*

Twee duidelijk onderscheiden Vlaamse mannenstemmen. Als er geen twee natuurlijke Vlaamse stemopnames beschikbaar zijn: kloon één bevestigd goede Vlaamse stem en verschuif de tweede stem in **toonhoogte omlaag** (niet omhoog -- naar boven pitchen klinkt snel onnatuurlijk/"hoog"), met een formant-behoudende pitch-shift (bv. rubberband, niet de goedkope "speed up" truc) zodat het een geloofwaardige, andere man blijft klinken.

Achtergrondgeluid: gebruik geen geluid dat je knipt/herhaalt in een korte lus -- een kort fragment (1-2s) dat om de zoveel tijd herhaald wordt, geeft een hoorbaar "kloppend" repeterend geluid. Gebruik ofwel een langere, ononderbroken opname, of gefilterde ruis (bruine/roze ruis, laag doorgelaten) als neutrale achtergrondbedding, en meng die als ÉÉN doorlopende laag over de volledige tijdlijn heen (met één zachte overvloeiing bij de overgang luchthaven → straat) in plaats van per shot te knippen en weer te plakken.

---

## 5. Eindscherm (endcard, silent, ~3s)

Statisch beeld, donkere gradient achtergrond, logo bovenaan, tekst in 4 talen gestapeld (NL/FR/EN/TR):

> Taxi nodig voor uw vakantie of zakelijke doeleinden?
> Besoin d'un taxi pour vos vacances ou votre voyage d'affaires ?
> Need a taxi for your holiday or business trip?
> Tatiliniz veya iş seyahatiniz için bir taksiye mi ihtiyacınız var?

Gele CTA-knop "Vul het formulier in" + `easytaxibelgium.be`.

---

## 6. Technische instellingen samengevat

| Instelling | Waarde |
|---|---|
| Aspect ratio | 9:16 |
| Resolutie | 1080p (of 4K indien budget toelaat) |
| Model | Cinema Studio Video 3.0 (`cinematic_studio_3_0`) voor niet-dialoogscènes; Seedance 2.0 met audio-reference voor dialoogscènes |
| Genre-hint | `drama` of `auto` |
| Duur per generatie | 4s (minimum), nadien bijknippen per scène |
| generate_audio | `false` (audio wordt apart gemixt, niet door het model zelf gegenereerd) |
| Nummerplaat | altijd `T·XXX·XX`, nooit een echt ogende combinatie |
