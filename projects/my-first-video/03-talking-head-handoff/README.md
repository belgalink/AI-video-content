# Talking-head handoff — externe lip-sync met je échte stem

Doel: pratende video's die er **exact** zoals jij uitzien én klinken — met je **echte huid** (egaal, laag contrast) en je **echte stem**.

## Waarom extern (kort)
- De in-tool video-modellen (Seedance/Kling/Veo3) **her-renderen je huid** en overdrijven rode vlekjes + contrast (zie de diagnose-vergelijking in de chat). Niet bruikbaar voor getrouwe talking-heads.
- De lip-sync-modellen die **jouw eigen audio** als stem gebruiken, zitten op Higgsfield-**accountniveau vergrendeld** (kon ik niet ontgrendelen).
- Daarom: lip-sync **extern**, met als bron je **echte foto** (niet de AI-templates) → huid klopt 100%.

## Wat zit in deze map
- `avatar/avatar-real-frontal-1_white.jpg` & `-2_white.jpg`
  Je **echte foto's**, enkel achtergrond → wit (via background-removal). **Geen** huidbewerking, geen contrast-boost, geen "beautify". Dit zijn je avatar-basisbeelden voor lip-sync.
- `audio/voice-master_clean.wav` (+ `.mp3`)
  Je opname, opgeschoond: high-pass (rommel weg), lichte ruisreductie, genormaliseerd op −16 LUFS. **Master** voor een stemkloon.
- `audio/voice-sample-15s_clean.wav` — kort fragment.

## Stap 1 — (aanbevolen) Schaalbare stemkloon
Tool: **ElevenLabs** (of gelijkaardig).
- **Instant clone**: 1–3 min audio (de master volstaat) → snel + goed.
- **Professional clone**: ~30 min schone audio → beste kwaliteit. Wil je dit: neem ~20–30 min rustig in, zelfde stille kamer, Razer Seiren V3 Mini (vraag me gerust een leesscript).
- Daarna genereer je **elk** script in **jouw** stem (NL en/of EN) — schaalbaar, zonder telkens opnieuw in te spreken.

## Stap 2 — Lip-sync (foto + audio → pratende video)
Gebruik een tool die een **foto animeert op basis van audio** (behoudt je echte huid):
- **Hedra (Character-3)** — upload `avatar-real-frontal-1_white.jpg` + je audio → pratende clip. Zeer natuurlijk, goed huidbehoud.
- **HeyGen (Talking Photo / Photo Avatar)** — idem.
- **Sync.so / Sync Labs** — vooral om lip-sync op een bestaande video te zetten.

Instellingen:
- Formaat: **9:16** (TikTok/Reels/Shorts) of **16:9** (YouTube).
- Hoogste resolutie; **géén** "beautify"/"smooth skin"/"enhance" filters (die brengen net de nep-huid terug).
- "Preserve identity/skin" aanzetten indien beschikbaar.

## Huid-fidelity — vaste regels
1. Bron = **altijd je echte foto** (deze avatars). **Nooit** de AI-outfit-templates voor video: die voegen al sproeten/contrast toe.
2. **Geen** in-tool Seedance/Kling voor pratende koppen (her-rendert + overdrijft huid).
3. **Geen** beautify/enhance in de lip-sync tool.

## Wat ik (Higgsfield-kant) blijf leveren
- **Identiteit/visuals**: de getrainde **Soul** (digital twin, `soul_id 8bbfffbc…`) staat klaar → consistente beelden/scènes van jou (cinematic & UGC b-roll, looks, locaties).
- **Audio**: opschonen, normaliseren, knippen.
- **Afwerking**: upscalen, monteren, ondertitelen.

## Workflow per video
1. **Stem** — genereer audio in je kloon, óf neem in.
2. **Beeld** — avatar uit deze map (of een nieuw beeld dat ik genereer).
3. **Lip-sync** — Hedra/HeyGen: foto + audio → clip.
4. **Afwerking** — stuur de clip terug; ik upscale/monteer/ondertitel.

---
Avatars = echte foto's, enkel achtergrond vervangen. Skin = ongewijzigd. Stem = jouw opname (master voor kloon).
