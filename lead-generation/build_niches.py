#!/usr/bin/env python3
"""
BelgaLink — B2B niche-structuur generator.

Bouwt de mapstructuur voor de lead-scraping op basis van EEN centrale bronlijst:
`lead-generation/niches-master.csv`. Dat CSV-bestand is de enige plek waar je
cureert — niches selecteren, schrappen of bijvoegen.

Per niche met status "kandidaat" of "goedgekeurd" wordt een map aangemaakt met:
  - README.md   (niche-profiel + Firecrawl-scrapeplan)
  - leads.csv   (leeg, klaar voor gescrapete leads — wordt NOOIT overschreven)

Niches met status "afgewezen" krijgen GEEN map.

Run vanuit de repo-root:
    python3 lead-generation/build_niches.py

Curatie-workflow:
  - Selecteren    -> zet `status` op "goedgekeurd" (of laat op "kandidaat")
  - Schrappen     -> zet `status` op "afgewezen", of verwijder de rij
  - Bijvoegen     -> voeg een nieuwe rij toe (id = volgend nummer)
  - Prioriteren   -> vul `prioriteit` in (bv. hoog / midden / laag)
Daarna dit script opnieuw draaien.
"""

import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
MASTER_CSV = ROOT / "niches-master.csv"
NICHES_DIR = ROOT / "niches"

# Welke statussen krijgen een map? Pas aan naar {"goedgekeurd"} zodra je
# enkel nog de definitief geselecteerde niches wil genereren.
GENERATE_STATUSES = {"kandidaat", "goedgekeurd"}

# Vaste kolommen voor elke leads.csv — exact de velden die Diederick vroeg,
# plus enkele kwaliteits- en bronvelden voor de "kwaliteit boven kwantiteit"-focus.
LEAD_COLUMNS = [
    "bedrijfsnaam",
    "eigenaar_volledige_naam",
    "email",
    "telefoon",
    "website",
    "btw_nummer",
    "plaats",
    "provincie",
    "aantal_medewerkers",
    "nace_code",
    "bron_url",
    "kwaliteitsscore",   # 1-5, handmatig of via verrijking
    "status",            # nieuw / gecontacteerd / gekwalificeerd / afgewezen
    "datum_gescrapet",
    "notities",
]


def slugify(name: str, index: int) -> str:
    table = str.maketrans({
        "&": "en", "(": "", ")": "", "/": "-", ",": "", ".": "",
        "à": "a", "â": "a", "ä": "a", "é": "e", "è": "e", "ê": "e", "ë": "e",
        "ï": "i", "î": "i", "ô": "o", "ö": "o", "ù": "u", "û": "u", "ü": "u", "ç": "c",
    })
    s = name.lower().translate(table)
    s = "".join(ch if (ch.isalnum() or ch == " " or ch == "-") else "" for ch in s)
    s = "-".join(s.split())
    return f"{index:02d}-{s}"


def split_multi(value: str):
    return [p.strip() for p in (value or "").split("|") if p.strip()]


def niche_readme(row: dict) -> str:
    upsell = split_multi(row["upsell"])
    zoek = split_multi(row["zoektermen"])
    upsell_md = "\n".join(f"- {u}" for u in upsell) or "- (nog in te vullen)"
    zoek_md = "\n".join(f"- `{z}`" for z in zoek) or "- (nog in te vullen)"
    prio = row.get("prioriteit", "").strip() or "—"
    return f"""# Niche {int(row['id']):02d} — {row['niche']}

**Categorie:** {row['categorie']}
**Status:** {row['status']} · **Prioriteit:** {prio}

## Waarom deze niche past bij BelgaLink
{row['fit']}

> Profiel: Vlaamse KMO, team van ~3 tot 30 medewerkers, halal-conform. Zaakvoerder is
> sterk in zijn vak, minder met digitaal bezig — exact de avatar uit de briefing.

## Upsell-potentieel (naast de website)
{upsell_md}

## Firecrawl-scraping

**Doelvelden per lead:** e-mail · volledige naam eigenaar · telefoon · website · BTW-nummer.

**Startqueries (Firecrawl `search`):**
{zoek_md}

**Indicatieve NACEBEL-code(s):** {row['nace']}
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

---
*Gegenereerd uit `niches-master.csv` — bewerk daar, niet hier.*
"""


def write_leads_csv(path: pathlib.Path) -> None:
    if path.exists():
        return  # nooit overschrijven — hier komen de gescrapete leads in
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(LEAD_COLUMNS)


def load_rows():
    with MASTER_CSV.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = load_rows()
    NICHES_DIR.mkdir(parents=True, exist_ok=True)

    # tellers per categorie (voor stabiele nummering binnen de map)
    cat_counters = {}
    generated = 0
    by_status = {}
    index_by_cat = {}
    cat_order = []

    for row in rows:
        status = row["status"].strip().lower()
        by_status[status] = by_status.get(status, 0) + 1
        cat_slug = row["categorie_slug"].strip()
        cat_label = row["categorie"].strip()
        if cat_slug not in index_by_cat:
            index_by_cat[cat_slug] = (cat_label, [])
            cat_order.append(cat_slug)

        if status not in GENERATE_STATUSES:
            index_by_cat[cat_slug][1].append((row, None))
            continue

        cat_counters[cat_slug] = cat_counters.get(cat_slug, 0) + 1
        n_idx = cat_counters[cat_slug]
        cat_dir = NICHES_DIR / cat_slug
        cat_dir.mkdir(parents=True, exist_ok=True)
        (cat_dir / "README.md").write_text(
            f"# {cat_label}\n", encoding="utf-8")
        niche_dir = cat_dir / slugify(row["niche"], n_idx)
        niche_dir.mkdir(parents=True, exist_ok=True)
        (niche_dir / "README.md").write_text(niche_readme(row), encoding="utf-8")
        write_leads_csv(niche_dir / "leads.csv")
        generated += 1
        index_by_cat[cat_slug][1].append((row, niche_dir.relative_to(ROOT)))

    # master-lijst (status-bewust)
    lines = [
        "# BelgaLink — Master-lijst B2B niches\n",
        "Bronlijst: `niches-master.csv` (daar cureer je: selecteren / schrappen / bijvoegen).\n",
        f"**Totaal in lijst:** {len(rows)}  ·  "
        + "  ·  ".join(f"{k}: {v}" for k, v in sorted(by_status.items()))
        + f"  ·  **mappen gegenereerd:** {generated}\n",
        "Halal-conform gefilterd (geen alcohol, varkensvlees, gokken, interest-producten, "
        "horeca, beauty/cosmetica of muziek-industrie).\n",
    ]
    for cat_slug in cat_order:
        cat_label, items = index_by_cat[cat_slug]
        lines.append(f"\n### {cat_label}\n")
        for row, rel in items:
            mark = "~~" if row["status"].strip().lower() == "afgewezen" else ""
            prio = row.get("prioriteit", "").strip()
            prio_txt = f" _(prio: {prio})_" if prio else ""
            loc = f" — `{rel}/`" if rel else " — _(geen map)_"
            lines.append(
                f"- {mark}**{row['niche']}**{mark} · {row['status']}{prio_txt}{loc}")

    (ROOT / "00-niche-master-list.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Klaar. {generated} mappen gegenereerd uit {len(rows)} niches.")
    for k, v in sorted(by_status.items()):
        print(f"  status '{k}': {v}")


if __name__ == "__main__":
    main()
