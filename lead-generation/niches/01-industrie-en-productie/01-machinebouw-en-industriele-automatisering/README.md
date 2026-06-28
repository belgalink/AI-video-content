# Niche 01 — Machinebouw & industriële automatisering

**Categorie:** Industrie & productie

## Waarom deze niche past bij BelgaLink
Technische, kapitaalkrachtige KMO's; zaakvoerder vaak weinig digitaal-mee; sterke nood aan online geloofwaardigheid bij internationale klanten.

> Profiel: Vlaamse KMO, team van ~3 tot 30 medewerkers, halal-conform. Zaakvoerder is
> sterk in zijn vak, minder met digitaal bezig — exact de avatar uit de briefing.

## Upsell-potentieel (naast de website)
- Bedrijfswebsite + portfolio
- Backend/orderbeheer
- Klantportaal
- BI-dashboard productie

## Firecrawl-scraping

**Doelvelden per lead:** e-mail · volledige naam eigenaar · telefoon · website · BTW-nummer.

**Startqueries (Firecrawl `search`):**
- `machinebouw automatisering bedrijf Vlaanderen`
- `industriële automatisering KMO België`

**Indicatieve NACEBEL-code(s):** 28.99 / 33.20
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
