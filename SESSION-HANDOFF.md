# SESSION HANDOFF — Belgalink AI-video / Content Engine

> **Voor de nieuwe Claude Code-sessie:** dit bestand draagt de volledige context over van
> een vorige sessie. De enige reden voor de overdracht: de vorige sessie had de
> **Higgsfield MCP-connector** nog niet beschikbaar (die werd pas ná het starten gelinkt).
> Lees dit bestand volledig, voer de FIRST ACTIONS uit, en ga dan verder waar we stonden.
>
> **Taal:** antwoord de gebruiker in het **Nederlands (Vlaams)**. Hij heet **Diederick**
> (diederick@belgalink.be), zaakvoerder bij **Belgalink**.
>
> **Datum bij overdracht:** 2026-06-16.

---

## 0. TL;DR — de missie

Belgalink (Vlaams webbureau voor KMO's) bouwt een **AI-video content-engine**: marketing-
video's (Meta-ads, VSL's, short-form social, hooks) gemaakt met **Claude (creatief directeur)
+ Higgsfield (productiestudio met o.a. Seedance / Nano Banana / GPT Image)**, via de
**Storyboard Method** (kort shot per shot bouwen i.p.v. één lange prompt).

**Waar we NU staan:** we maken de **character reference set** van Diederick (de presentator
in de video's) — foto's vanuit veel hoeken/afstanden/expressies + audio voor een stemkloon.
Dit is stap 1; alle latere video-kwaliteit hangt hiervan af.

---

## 1. FIRST ACTIONS (doe dit eerst, in deze volgorde)

1. **Verifieer dat Higgsfield nu WEL beschikbaar is.** Zoek via ToolSearch naar Higgsfield /
   image generation / Seedance / Nano Banana. 
   - ✅ Als de Higgsfield-tools er zijn → top, we kunnen eindelijk genereren.
   - ❌ Als ze er NIET zijn → meld dit eerlijk aan Diederick. Dan moet de generatie in de
     **Claude.ai-chat** gebeuren (waar de connector aanstaat), niet hier. Verzin geen
     beelden en doe niet alsof.
2. **Synchroniseer met GitHub.** Alle werk staat op branch `claude/compassionate-feynman-xrn0ks`
   van repo `belgalink/AI-video-content`. Haal die binnen:
   ```bash
   git fetch origin claude/compassionate-feynman-xrn0ks
   git checkout claude/compassionate-feynman-xrn0ks   # of merge 'm in je toegewezen branch
   ```
   Werk en commit verder op deze branch (of je toegewezen feature-branch — stem af met Diederick).
3. **Lees deze repo-bestanden** (ze bevatten de diepe context, niet hier gedupliceerd):
   - `belgalink-brand/content-engine-briefing.md` ← **HEEL belangrijk**, het volledige merk- en
     marketing-kader (avatar, pijn, klanttaal, brand, waardenkader). Lees volledig.
   - `projects/my-first-video/02-references/character/SHOOT-CHECKLIST.md` ← de foto/audio-shoot.
   - `projects/my-first-video/02-references/character/character-reference-sheet-PROMPT.md`
     ← de uitgebreide master-prompt om de character sheet te genereren met Higgsfield.
   - `CLAUDE.md` en `README.md` ← hoe het storyboard-startersysteem werkt.
4. **Vat samen** wat je begrijpt en bevestig de volgende stap aan Diederick voor je genereert.

---

## 2. Git & repo-status

- **Repo:** `belgalink/AI-video-content` (was leeg; we hebben 'm gebootstrapt vanuit de
  publieke template `belgalink/ai-storyboard-video-starter`).
- **Branch:** `claude/compassionate-feynman-xrn0ks` (alles is hierheen gecommit en gepusht).
- **Commits tot nu toe (nieuwste eerst):**
  1. Add expanded character reference sheet master prompt
  2. Add Belgalink brand briefing and brand-tuned character shoot checklist
  3. Set up AI Storyboard Video Starter environment (initiële bootstrap, ~367 bestanden incl. demo-media)
- **Commit-conventie:** duidelijke Engelse commit messages, eindig met de regel
  `https://claude.ai/code/<session>` (de harness levert je eigen sessie-URL aan).
- **Push:** `git push -u origin <branch>`; bij netwerkfouten retry met backoff (2s/4s/8s/16s).
- **Géén PR aanmaken** tenzij Diederick er expliciet om vraagt.
- Er draait een **stop-hook** die klaagt over untracked files → commit & push je werk voor je afsluit.

---

## 3. Twee omgevingen (cruciaal om te begrijpen — dit veroorzaakte de verwarring)

| | **Claude.ai** (gewone chat/projects) | **Claude Code** (deze omgeving) |
|---|---|---|
| Higgsfield-connector | ✅ Aan (Diederick heeft 'm gelinkt) | ⚠️ Verifiëren (was eerder afwezig) |
| Beelden/video genereren | ✅ | alleen als Higgsfield-MCP er is |
| Repo, bestanden, git, scripts | beperkt | ✅ |

De Storyboard-tutorial gebruikte **beide**: "set up my environment" = Claude Code; het
genereren van beelden = de Higgsfield-connector. Houd dit onderscheid scherp en wees er
eerlijk over tegen Diederick.

---

## 4. Wie is Diederick / werkstijl

- Vlaamse ondernemer, zaakvoerder Belgalink. Detailgericht, wil **hoge kwaliteit**, geen
  luie/oppervlakkige output. Spreekt Nederlands, soms via spraak-naar-tekst (dus af en toe
  rommelige transcriptie — kijk naar de bedoeling, niet de letterlijke woorden).
- **Open vraag die nog niet beantwoord is:** wil hij **goedkeuring bij elke stap**, of
  **autopilot** (alleen stoppen bij risico/onduidelijkheid)? Vraag dit opnieuw als het relevant wordt.
- Hij maakt deze content voor het **Belgalink Instagram-account** (en Meta-ads breder).

---

## 5. De methode (Storyboard Method — condensed)

Het `projects/`-systeem implementeert exact dit:
`01-creative-brief` → `02-references` → `03-shot-list` → `04-image-prompts` →
`05-storyboard-frames` (eerste+laatste frame per shot) → `06-video-prompts` →
`07-transition-videos` (Seedance vult tussen de frames) → `08-stitching` → `09-final-output`.

Per stap: `attempts/` (klad), `approved/` (vergrendeld, gaat door), `disapproved/` (afgekeurd).
Elke stap gebruikt enkel bestanden uit de `approved/` van de vorige stap.
`projects/demo-walkthrough/` is een volledig afgewerkt voorbeeld (MasterChef pink cup).

---

## 6. Belgalink merk-essentials (samenvatting — lees de briefing voor het volledige beeld)

- **Positionering:** de verstandige middenweg tussen "goedkoop-onzeker" (zelf/neefje/student/Fiverr)
  en "duur-traag-vaag" (klassieke agency). Tagline: *"Jouw bedrijf? ZichtBaar."*
- **Avatar:** "Jorn, 37" — drukke Vlaamse KMO-zaakvoerder, *solution aware*, *passief* op Meta.
- **Funnel:** differentiation. **Eerste 3 seconden = alles.** Eén video = één idee = één CTA.
- **#1 regel: klink NOOIT als AI.** Authentiek (rauwe iPhone-look) verslaat gepolijst —
  letterlijke les: rauwe ads €10-15/lead, gepolijste AI-script ads €100/lead. Doel-CPL €15.
- **Klanttaal letterlijk gebruiken** (woordenbank in briefing sectie 6). Geen jargon.
- **Brand:** blauw `#2A5BF5`, navy `#0D1B4B`; fonts Montserrat + DM Sans; **geen emoji,
  geen glassmorphism, geen drukke effecten**.
- **Waardenkader (islamitisch, VERPLICHT filter):** halal-conforme niches/beeld/audio; geen
  alcohol/varkens/gokken/rente; geen vrouwen als blikvanger; **geen prominente muziek**;
  ingetogen beeld. Bij twijfel niet doen / voorleggen.

---

## 7. Wat we al gebouwd hebben (bestandsinventaris)

- `belgalink-brand/content-engine-briefing.md` — volledige content-engine context-laag (17 secties).
- `projects/my-first-video/02-references/character/SHOOT-CHECKLIST.md` — merk-afgestemde foto- +
  audio-shoot. Bevat o.a. een **audio-voorleesscript** in Belgalink-klanttaal (u/uw + je/jouw).
- `projects/my-first-video/02-references/character/character-reference-sheet-PROMPT.md` — de
  uitgebreide master-prompt (~25 shots in 4 blokken) om de character "bible" te genereren.

---

## 8. Huidige taak & plan (character reference set)

**Doel:** een uitgebreide, identity-locked character set van Diederick, zodat zijn gezicht/lichaam
consistent terugkomt in alle video's. Veel uitgebreider dan een standaard "6-foto" sheet.

**Volgorde:**
1. **Face master set** (eerst): basic effen T-shirt, neutrale achtergrond, 7 hoeken + 6 expressies.
   Dit is de hoeksteen / identity-lock.
2. **Per outfit** daarna: alleen body/medium/full-body + setting-shots (gezicht-close-ups niet
   opnieuw — dat zou ruis toevoegen). 3-5 outfits, waarvan 1 heel basic.
3. **Audio** (komt nog): 2-3 min schone spraak, nuchtere Vlaamse stem, script staat in de checklist.

**Genereren (zodra Higgsfield beschikbaar is):**
- Gebruik `character-reference-sheet-PROMPT.md`. Voer **al Diedericks echte angle-foto's** in als
  **multi-referentie** (NIET één selfie laten hallucineren — hij heeft echt vanuit veel hoeken gefotografeerd).
- **STEP 1:** bevraag de Higgsfield-modellenlijst live; kies het sterkste voor identity-preservation
  & multi-angle consistentie (vandaag wsl. Nano Banana Pro of GPT Image 2 — verifiëren).
- Genereer **blok per blok**; laat blok A (identity-lock) goedkeuren vóór B/C/D, om credits/rate-limits
  te sparen.
- Sla op in `projects/my-first-video/02-references/character/bible/` (+ contact sheets in `bible/contact-sheets/`).
- **STEP 5:** rapporteer eerlijk of de identiteit standhield; flag drift; meld ontbrekende angles.

---

## 9. Belangrijke beslissingen & inzichten die al genomen zijn (niet opnieuw uitvinden)

- Face-close-ups **één keer** doen (basic shirt), niet per outfit → schoonste identity-lock.
- **Multi-referentie i.p.v. één foto** = kernverschil met de "luie" prompt.
- De reference-bible heeft een **neutrale grijze achtergrond** (technisch); herkenbare settings
  (kantoor/bureau/natuurlijk licht) komen pas in de **video-prompts**, niet in de bible.
- **6 expressies**, met merk-prioriteit: *geconcentreerd/serieus* (vertrouwen) en *lichte glimlach*
  (warm-professioneel) zijn de kern; *pratend/mid-sentence* is #1 voor lipsync; *volle glimlach/excited*
  spaarzaam (merk is nuchter, niet hyped).
- Audio = **nuchtere, warme Vlaamse stem, géén radioreclame-stem**; u/uw voor ads, je/jouw voor social.

---

## 10. Eerstvolgende concrete acties voor jou (nieuwe sessie)

1. FIRST ACTIONS (sectie 1) afwerken: Higgsfield verifiëren + branch pullen + bestanden lezen.
2. Aan Diederick bevestigen dat je 100% mee bent en of Higgsfield nu werkt.
3. Als Higgsfield werkt: vraag zijn face-foto's, draai `character-reference-sheet-PROMPT.md`
   blok A, en laat de identity-lock goedkeuren.
4. Daarna outfits, daarna audio.
5. Alles netjes in de `bible/`-mappen, committen en pushen naar de branch.

---

### Guardrails (altijd)
- Klink nooit als AI; gebruik letterlijke klanttaal; respecteer brand + waardenkader.
- Wees eerlijk over wat wel/niet kan (bv. Higgsfield-beschikbaarheid). Verzin geen resultaten.
- Commit & push je werk; geen PR tenzij gevraagd; blijf op de afgesproken branch.
- Antwoord in het Nederlands.
