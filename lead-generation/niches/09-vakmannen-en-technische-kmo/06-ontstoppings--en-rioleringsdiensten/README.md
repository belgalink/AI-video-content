# Niche 74 — Ontstoppings- & rioleringsdiensten

**Categorie:** Vakmannen & technische KMO's (grotere teams)

## Waarom deze niche past bij BelgaLink
Urgentiegedreven; online aanvraag + 24/7-flow zetten direct aanvragen om.

> Profiel: Vlaamse KMO, team van ~3 tot 30 medewerkers, halal-conform. Zaakvoerder is
> sterk in zijn vak, minder met digitaal bezig — exact de avatar uit de briefing.

## Upsell-potentieel (naast de website)
- Website
- Online aanvraag-/interventiesysteem
- Planning backend

## Firecrawl-scraping

**Doelvelden per lead:** e-mail · volledige naam eigenaar · telefoon · website · BTW-nummer.

**Startqueries (Firecrawl `search`):**
- `ontstopping riolering bedrijf Vlaanderen`
- `rioolreiniging dienst België`

**Indicatieve NACEBEL-code(s):** 37.00 / 81.29
*(altijd verifiëren in de KBO/Kruispuntbank van Ondernemingen — codes zijn richtinggevend, niet sluitend)*

**Werkwijze:**
1. `firecrawl_search` met de startqueries → kandidaat-bedrijfswebsites verzamelen.
2. `firecrawl_extract` of `firecrawl_scrape` per website → de 5 doelvelden ophalen.
3. BTW-nummer verifiëren/aanvullen via de bedrijfswebsite (footer/contact) of KBO.
4. Resultaten in `leads.csv` zetten met bron-URL en datum. Kwaliteit > kwantiteit.

## Bestanden
- `leads.csv` — gescrapete leads (wordt nooit automatisch overschreven).

*Kwaliteitsfilter: enkel halal-conforme bedrijven (geen alcohol, varkensvlees, gokken,
interest-/woekerproducten). Bij twijfel: niet opnemen of voorleggen aan de oprichters.*
