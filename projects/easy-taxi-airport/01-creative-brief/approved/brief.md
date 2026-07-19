# Creative Brief — Easy-Taxi Belgium (Airport → Thuis)

## Klant
Easy-Taxi Belgium (easytaxibelgium.be) — taxidienst, o.a. luchthaventransfers.

## Doel
Facebook-advertentie die de kern-service toont: zorgeloze luchthaven-transfer.
Een man wordt vlot opgehaald aan de luchthaven en tot aan zijn deur in Leuven gebracht.
Gevoel: premium, betrouwbaar, moeiteloos, verzorgd (mooie Mercedes).

## Verhaal (in 1 zin)
Een reiziger geeft zijn valies af aan een vriendelijke Mercedes-taxichauffeur aan de
luchthaven en wordt comfortabel tot aan zijn voordeur in een mooie Leuvense wijk gebracht.

## Vaste continuïteit-locks (MOETEN identiek blijven over alle shots)
- **De reiziger (man):** zelfde gezicht, vakantiekledij met lange broek (smart-casual: polo/overhemd + chino), zelfde tas/valies.
- **De taxichauffeur (man):** zelfde gezicht, verzorgd, nette donkere kledij (chauffeurslook).
- **De taxi:** zelfde zwarte Mercedes (E-Klasse look), zelfde taxi-daklicht.
- **De valies:** zelfde hardshell koffer (kleur/vorm identiek in elk shot).

## Cast-regels (klantvereiste)
- Zowel de reiziger als de chauffeur zijn **mannen**.

## Tone & look
- Fotorealistisch, cinematisch, warm daglicht, zachte natuurlijke belichting.
- Rustige, premium reclame-vibe. Geen overdreven camera-effecten.

## Formaat
- Facebook-ad. Aspect ratio nog te bevestigen (zie shotlist / vraag).

## Einde / CTA
- Eindkaart met **Easy-Taxi Belgium logo** (echte PNG, overlay — niet AI-hergenereerd).
- CTA-tekst: **"Taxi nodig voor uw vakantie? Vul het formulier in"**

## Techniek (meest efficiënt & realistisch met Higgsfield MCP)
1. **Prop sheets = Higgsfield Elements.** Voor reiziger, chauffeur, Mercedes en valies maken we
   elk één schone referentie-afbeelding (Nano Banana Pro) en slaan die op als Element.
2. Elk Element wordt in élke prompt geïnjecteerd via `<<<element_id>>>` → identiteit blijft locked.
3. Per shot genereren we de start- (en waar nodig eind-) frame met de Elements erin.
4. Video per shot met een Elements-compatibel model (Kling 3.0 / Seedance 2.0).
5. Stitchen tot één ad, logo + CTA als overlay op de eindkaart.
