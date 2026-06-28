# BelgaLink — B2B Lead-generatie (75 niches)

Mapstructuur voor **75 B2B niche-ideeën** voor BelgaLink (belgalink.be), klaar om er per
niche **Firecrawl lead-scraping** op los te laten.

BelgaLink is een digitaal bureau dat websites, web-applicaties, CRM's, back-end systemen en
BI-dashboards bouwt voor Vlaamse KMO's (teams van 3–30 medewerkers, halal-conform bedrijf).
Deze niches zijn gekozen omdat ze **upsell-potentieel** hebben: niet enkel een website, maar
ook lead magnets, klantportalen, offerte-/boekingssystemen, operationele back-ends en
BI-dashboards.

## Wat we scrapen (per lead)

De gevraagde doelvelden, kwaliteit boven kwantiteit:

1. **E-mail**
2. **Volledige naam van de eigenaar/zaakvoerder**
3. **Telefoonnummer**
4. **Website**
5. **BTW-nummer**

Elke `leads.csv` heeft daarnaast bron- en kwaliteitsvelden (`bron_url`, `kwaliteitsscore`,
`status`, `datum_gescrapet`, `notities`, `plaats`, `provincie`, `aantal_medewerkers`,
`nace_code`).

## Structuur

```text
lead-generation/
├── README.md                  ← dit bestand
├── 00-niche-master-list.md    ← genummerde lijst van alle 75 niches
├── build_niches.py            ← reproduceerbare generator
└── niches/
    ├── 01-industrie-en-productie/
    │   ├── 01-machinebouw-en-automatisering/
    │   │   ├── README.md       ← niche-profiel + Firecrawl-scrapeplan
    │   │   └── leads.csv        ← hier komen de gescrapete leads in
    │   └── ...
    └── 09-vakmannen-en-technische-kmo/
```

9 categorieën, samen 75 niches. Zie `00-niche-master-list.md` voor de volledige index.

## Workflow per niche (Firecrawl)

1. Open de niche-map en lees de `README.md` (bevat startqueries + indicatieve NACEBEL-codes).
2. `firecrawl_search` met de startqueries → kandidaat-bedrijfswebsites verzamelen.
3. `firecrawl_extract` / `firecrawl_scrape` per website → de 5 doelvelden ophalen.
4. BTW-nummer verifiëren via de website (footer/contactpagina) of de KBO.
5. Leads wegschrijven in `leads.csv` met `bron_url` en `datum_gescrapet`.

> De generator overschrijft bestaande `leads.csv`-bestanden **nooit** — gescrapete data
> blijft veilig. README's worden wel ververst bij een nieuwe run.

## Kwaliteits- & waardenfilter (verplicht)

Halal-conform: **geen** alcohol, varkensvlees, gokken, interest-/woekerproducten, horeca,
beauty/cosmetica of muziek-industrie als kernactiviteit. Focus op Vlaamse KMO's met
**teams** (geen pure zelfstandigen) en duidelijk upsell-potentieel. Bij twijfel: niet
opnemen of voorleggen aan de oprichters.

## Generator opnieuw draaien

```bash
python3 lead-generation/build_niches.py
```

---

> **Repo-noot:** de oorspronkelijke opdracht noemde de repo `belgalink/Leadscoldcalls`.
> Deze sessie heeft echter enkel toegang tot `belgalink/ai-video-content` (en de toegewezen
> branch `claude/belgalink-niche-folders-878lhq`), dus de structuur staat hier. Wil je ze in
> een aparte `Leadscoldcalls`-repo? Geef die repo dan toegang aan een sessie en we
> verplaatsen `lead-generation/` daarheen.
