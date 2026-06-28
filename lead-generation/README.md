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

## Niches cureren (selecteren / schrappen / bijvoegen)

De **enige plek waar je cureert** is `niches-master.csv`. Open het in Excel/Google Sheets
of laat het mij aanpassen. Kolommen die ertoe doen:

| Kolom | Wat je ermee doet |
|---|---|
| `status` | `kandidaat` (standaard), `goedgekeurd` (definitief geselecteerd) of `afgewezen` (niet benaderen) |
| `prioriteit` | vrij veld, bv. `hoog` / `midden` / `laag` — bepaalt scrape-volgorde |
| `niche`, `fit`, `upsell`, `zoektermen`, `nace` | inhoud van de niche |

- **Selecteren** → zet `status` op `goedgekeurd` (of laat op `kandidaat`).
- **Schrappen** → zet `status` op `afgewezen`, of verwijder de rij. Afgewezen niches krijgen **geen** map.
- **Bijvoegen** → voeg een rij toe met het volgende `id`.

Daarna `python3 lead-generation/build_niches.py` draaien → de mappen volgen automatisch je keuzes.
Bestaande `leads.csv`-bestanden blijven altijd staan (worden nooit overschreven).

> Standaard worden mappen aangemaakt voor status `kandidaat` én `goedgekeurd`. Wil je
> uiteindelijk enkel nog de definitief geselecteerde niches genereren? Zet `GENERATE_STATUSES`
> in `build_niches.py` op `{"goedgekeurd"}`.

De 75 huidige niches zijn een **startpunt**: er komen er nog bij, en er wordt geschrapt.

## Structuur

```text
lead-generation/
├── README.md                  ← dit bestand
├── niches-master.csv          ← BRONLIJST — hier cureer je
├── 00-niche-master-list.md    ← leesbaar overzicht (auto-gegenereerd, status per niche)
├── build_niches.py            ← reproduceerbare generator (leest de CSV)
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
