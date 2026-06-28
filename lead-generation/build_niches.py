#!/usr/bin/env python3
"""
BelgaLink — B2B niche-structuur generator.

Genereert een nette mapstructuur voor 75 B2B niche-ideeën, klaar om per niche
Firecrawl lead-scraping op los te laten (e-mail, naam eigenaar, telefoon,
website, BTW-nummer).

Run vanuit de repo-root:
    python3 lead-generation/build_niches.py

Idempotent: bestaande leads.csv-bestanden worden NOOIT overschreven
(daar komen straks de gescrapete leads in). README's worden wel ververst.
"""

import csv
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
NICHES_DIR = ROOT / "niches"

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

# ---------------------------------------------------------------------------
# De 75 niches, gegroepeerd in categorieën.
# Per niche:
#   naam        — leesbare niche-naam
#   fit         — waarom dit een goede BelgaLink-doelgroep is
#   upsell      — welke BelgaLink-producten naast een website passen
#   zoektermen  — startqueries voor Firecrawl search (Vlaamse context)
#   nace        — INDICATIEVE NACEBEL-code(s); altijd verifiëren in de KBO
# ---------------------------------------------------------------------------

CATEGORIES = [
    ("01-industrie-en-productie", "Industrie & productie", [
        ("Machinebouw & industriële automatisering",
         "Technische, kapitaalkrachtige KMO's; zaakvoerder vaak weinig digitaal-mee; sterke nood aan online geloofwaardigheid bij internationale klanten.",
         ["Bedrijfswebsite + portfolio", "Backend/orderbeheer", "Klantportaal", "BI-dashboard productie"],
         ["machinebouw automatisering bedrijf Vlaanderen", "industriële automatisering KMO België"],
         "28.99 / 33.20"),
        ("Metaalbewerking & verspaning (CNC)",
         "Onderaannemers met B2B-klanten die online betrouwbaar moeten ogen; offerteflow is vaak chaotisch.",
         ["Website", "Offerte-/aanvraagsysteem", "Backend werkbonbeheer"],
         ["CNC verspaning bedrijf Vlaanderen", "metaalbewerking onderaanneming België"],
         "25.62"),
        ("Lasbedrijven & staalconstructie",
         "Projectgedreven, groeiende ploegen; website matcht vaak niet met kwaliteit van het werk.",
         ["Website + realisaties", "Projectopvolging backend", "Lead magnet (staalcalculator)"],
         ["staalconstructie bedrijf Vlaanderen", "lasbedrijf constructiewerken België"],
         "25.11 / 25.62"),
        ("Verpakkingsbedrijven & verpakkingsmachines",
         "Industriële niche met internationale klanten; professionele uitstraling weegt zwaar.",
         ["Website meertalig", "Productcatalogus backend", "Klantportaal bestellingen"],
         ["verpakkingsbedrijf Vlaanderen", "verpakkingsmachines fabrikant België"],
         "82.92 / 28.93"),
        ("Kunststofverwerking & spuitgieten",
         "Technische maakindustrie; weinig marketingfocus, veel upsell-potentieel in systemen.",
         ["Website", "Productieplanning backend", "BI-dashboard"],
         ["kunststofverwerking spuitgieten Vlaanderen", "plastic spuitgieten bedrijf België"],
         "22.29"),
        ("Matrijzen- & gereedschapsbouw",
         "Hooggespecialiseerd, B2B-toeleverancier; sterke baat bij online vindbaarheid en cases.",
         ["Website + cases", "Offertesysteem", "Klantportaal"],
         ["matrijzenbouw bedrijf Vlaanderen", "gereedschapsbouw toolmaker België"],
         "25.73"),
        ("Industrieel onderhoud & technische diensten",
         "Service-gedreven met terugkerende klanten; planning en interventiebeheer schreeuwen om software.",
         ["Website", "Interventie-/ticketsysteem backend", "Klantportaal"],
         ["industrieel onderhoud technische diensten Vlaanderen", "industriële maintenance bedrijf België"],
         "33.12 / 33.20"),
        ("Productie bouwmaterialen (beton, prefab)",
         "Zware industrie met B2B-afnemers; vaak verouderde online aanwezigheid.",
         ["Website", "Productcatalogus", "Bestel-/offerteportaal"],
         ["prefab beton fabrikant Vlaanderen", "bouwmaterialen producent België"],
         "23.61 / 23.63"),
        ("Houtverwerking & industriële schrijnwerk",
         "Maakbedrijven met groeiende ploegen; visueel werk dat online sterk kan converteren.",
         ["Website + realisaties", "Offertesysteem op maat", "Backend projectbeheer"],
         ["industriële schrijnwerkerij Vlaanderen", "houtverwerkend bedrijf België"],
         "16.23"),
        ("Technisch textiel & non-food textielproductie",
         "Halal-conforme productieniche; B2B-leveranciers met internationale ambities.",
         ["Website meertalig", "Productcatalogus backend", "Klantportaal"],
         ["technisch textiel producent Vlaanderen", "textielbedrijf B2B België"],
         "13.96"),
    ]),
    ("02-groothandel-en-distributie", "Groothandel & distributie", [
        ("Technische groothandels (industriële toebehoren)",
         "Veel SKU's, B2B-klanten; ideale fit voor webshop + klantportaal + voorraad-BI.",
         ["B2B-webshop", "Klantportaal met prijzen", "BI-dashboard voorraad/omzet"],
         ["technische groothandel industriële toebehoren Vlaanderen", "groothandel machineonderdelen België"],
         "46.69 / 46.74"),
        ("Bouwmaterialen groothandel",
         "Grote B2B-volumes; aannemers willen online bestellen en voorraad zien.",
         ["B2B-webshop", "Offerte-/bestelportaal", "BI-dashboard"],
         ["groothandel bouwmaterialen Vlaanderen", "bouwmaterialen leverancier België"],
         "46.73"),
        ("Elektromateriaal groothandel",
         "Installateurs als vaste klanten; sterke nood aan klantportaal en snelle bestelflow.",
         ["B2B-webshop", "Klantportaal", "CRM"],
         ["groothandel elektromateriaal Vlaanderen", "elektrotechnische groothandel België"],
         "46.69"),
        ("Sanitair & verwarming groothandel",
         "Loodgieters/HVAC als afnemers; offerte- en bestelsystemen besparen veel telefoonwerk.",
         ["B2B-webshop", "Offertesysteem", "Klantportaal"],
         ["groothandel sanitair verwarming Vlaanderen", "sanitair groothandel België"],
         "46.73 / 46.74"),
        ("Groothandel in machines & gereedschap",
         "Technische verkoop; cases en specs online maken het verschil.",
         ["Website + catalogus", "Offertesysteem", "Klantportaal"],
         ["groothandel machines gereedschap Vlaanderen", "machinehandel B2B België"],
         "46.62 / 46.69"),
        ("Groothandel in verpakkingsmateriaal",
         "Herhaalaankopen; webshop + herbestel-flow verhoogt omzet direct.",
         ["B2B-webshop", "Herbestelportaal", "BI-dashboard"],
         ["groothandel verpakkingsmateriaal Vlaanderen", "verpakkingen leverancier B2B België"],
         "46.76"),
        ("Groothandel industriële chemie (non-haram)",
         "Halal-conform gefilterd; technische B2B-niche met dossier-/veiligheidsbeheer.",
         ["Website", "Documentportaal (SDS)", "Bestelsysteem"],
         ["groothandel industriële chemie Vlaanderen", "chemische producten B2B leverancier België"],
         "46.75"),
        ("Voedingsgroothandel (halal-conform)",
         "Enkel halal-conforme segmenten (geen varken/alcohol); B2B-afnemers willen online bestellen.",
         ["B2B-webshop", "Klantportaal", "Routeplanning backend"],
         ["halal voedingsgroothandel Vlaanderen", "foodservice groothandel B2B België"],
         "46.38 / 46.39"),
    ]),
    ("03-transport-en-logistiek", "Transport & logistiek", [
        ("Transportbedrijven (wegtransport goederen)",
         "Operationeel zwaar; weinig marketing, veel nood aan klantportaal en track & trace.",
         ["Website", "Klantportaal track & trace", "BI-dashboard ritten"],
         ["transportbedrijf wegtransport Vlaanderen", "goederentransport KMO België"],
         "49.41"),
        ("Logistiek, warehousing & fulfilment",
         "Schaalt snel; e-commerceklanten verwachten dashboards en API-koppelingen.",
         ["Website", "Klant-dashboard voorraad", "Fulfilment-backend"],
         ["logistiek fulfilment bedrijf Vlaanderen", "warehousing dienstverlener België"],
         "52.10"),
        ("Koeriers- & expeditiebedrijven",
         "Tijdkritisch; online boeken en opvolgen is een directe verkoophefboom.",
         ["Website", "Online boekingssysteem", "Klantportaal"],
         ["koeriersdienst expeditie Vlaanderen", "expresvervoer bedrijf België"],
         "53.20"),
        ("Containerverhuur & afvalcontainers",
         "Lokale B2B/B2C-mix; online container bestellen verlaagt telefoondruk fors.",
         ["Website", "Online bestel-/boekingssysteem", "Planning backend"],
         ["containerverhuur afvalcontainer Vlaanderen", "containerdienst bedrijf België"],
         "38.11 / 77.39"),
        ("Verhuisbedrijven (kantoor & B2B)",
         "Offerte-intensief; online intake en planning besparen veel tijd.",
         ["Website", "Online offerte-/intakeformulier", "Planning backend"],
         ["verhuisbedrijf kantoorverhuis Vlaanderen", "professionele verhuizers België"],
         "49.42"),
        ("Internationale expeditie & douane",
         "Specialistische B2B-niche; vertrouwen en meertaligheid online wegen zwaar.",
         ["Website meertalig", "Klantportaal documenten", "CRM"],
         ["douane-expediteur Vlaanderen", "internationale expeditie bedrijf België"],
         "52.29"),
    ]),
    ("04-bouw-en-technische-installatie", "Bouw & technische installatie", [
        ("Algemene aannemers (utiliteitsbouw)",
         "Grotere ploegen, B2B-projecten; portfolio en aanvraagflow zijn directe omzetdrijvers.",
         ["Website + realisaties", "Offerteaanvraag-systeem", "Projectopvolging backend"],
         ["algemene aannemer utiliteitsbouw Vlaanderen", "bouwbedrijf KMO België"],
         "41.20"),
        ("Dakwerkers",
         "Bestaande BelgaLink-asset (salespagina + cold-call offer); zaakvoerders weinig digitaal-mee.",
         ["Website + realisaties", "Lead magnet (dakcheck)", "Offertesysteem"],
         ["dakwerken bedrijf Vlaanderen", "dakwerker professioneel België"],
         "43.91"),
        ("HVAC & klimaatinstallatie",
         "Onderhoudscontracten = terugkerende omzet; planning- en servicesoftware loont.",
         ["Website", "Onderhoudscontract-portaal", "Interventieplanning backend"],
         ["HVAC klimaatinstallatie bedrijf Vlaanderen", "klimatisatie installateur België"],
         "43.22"),
        ("Koeltechniek",
         "Technische B2B-niche met servicecontracten; sterke fit voor interventiebeheer.",
         ["Website", "Interventie-/ticketsysteem", "Klantportaal"],
         ["koeltechniek bedrijf Vlaanderen", "industriële koeling installateur België"],
         "43.22 / 33.12"),
        ("Elektrotechnische installatie (industrieel)",
         "Projectgedreven met groeiende ploegen; offerte- en planningsystemen besparen tijd.",
         ["Website", "Offerte-/projectsysteem", "Backend werkbonnen"],
         ["elektrotechnische installatie industrieel Vlaanderen", "industriële elektriciteit bedrijf België"],
         "43.21"),
        ("Sanitair & loodgieterij (grotere teams)",
         "Vanaf 3-5 medewerkers; online afspraak/offerte verhoogt aanvragen meteen.",
         ["Website", "Online offerte-/afspraaksysteem", "Planning backend"],
         ["sanitair loodgieter bedrijf Vlaanderen", "loodgieterij meerdere medewerkers België"],
         "43.22"),
        ("Isolatiebedrijven",
         "Premiegedreven vraag; lead magnets (premie-/besparingscheck) werken sterk.",
         ["Website", "Lead magnet (premiecheck)", "Offertesysteem"],
         ["isolatiebedrijf Vlaanderen", "dak- en gevelisolatie bedrijf België"],
         "43.29"),
        ("Zonnepanelen-installateurs",
         "Bestaande referentie; hoge concurrentie maakt sterke site + leadflow cruciaal.",
         ["Website", "Lead magnet (besparingscalculator)", "Offerte-/planningsysteem"],
         ["zonnepanelen installateur Vlaanderen", "fotovoltaïsche installatie bedrijf België"],
         "43.21"),
        ("Liften & roltrappen (installatie/onderhoud)",
         "Door Diederick genoemd; onderhoudscontracten en B2B-vastgoedklanten, weinig marketing.",
         ["Website", "Onderhoudscontract-portaal", "Interventieplanning backend"],
         ["liften roltrappen installatie onderhoud Vlaanderen", "liftenbedrijf België"],
         "43.29 / 33.12"),
        ("Industriële poorten & toegangstechniek",
         "Technische B2B-niche met service; online configuratie en service-portaal lonen.",
         ["Website", "Product-/configuratietool", "Service-portaal"],
         ["industriële poorten toegangstechniek Vlaanderen", "sectionaalpoorten bedrijf B2B België"],
         "43.32 / 43.29"),
        ("Grondwerken & wegenis",
         "Projectaannemers; portfolio en aanvraagflow versterken B2B-positie.",
         ["Website + realisaties", "Offerteaanvraag-systeem", "Projectplanning backend"],
         ["grondwerken wegenis aannemer Vlaanderen", "grondwerker infrastructuur België"],
         "42.11 / 43.12"),
        ("Tuinaanleg & groenvoorziening (B2B)",
         "Grotere groenbedrijven met B2B-contracten; visueel werk converteert online sterk.",
         ["Website + realisaties", "Offerte-/onderhoudscontract-systeem", "Planning backend"],
         ["tuinaanleg groenvoorziening bedrijf Vlaanderen", "professioneel groenbeheer België"],
         "81.30"),
        ("Schilder- & afwerkingsbedrijven (groter)",
         "Vanaf enkele ploegen; B2B/projectwerk met nood aan offerte- en planningsysteem.",
         ["Website + realisaties", "Offertesysteem", "Planning backend"],
         ["schilderbedrijf afwerking Vlaanderen", "professionele schilderwerken B2B België"],
         "43.34"),
        ("Vloer- & tegelwerken (groter)",
         "Visueel werk; portfolio + offerteflow zijn directe conversiehefbomen.",
         ["Website + realisaties", "Offertesysteem", "Backend projectbeheer"],
         ["vloerderij tegelwerken bedrijf Vlaanderen", "professionele vloer- en tegelwerken België"],
         "43.33"),
        ("Brandbeveiliging & sprinklerinstallatie",
         "Wettelijk gedreven, contractueel; service-portaal en keuringbeheer lonen.",
         ["Website", "Service-/keuringsportaal", "CRM"],
         ["brandbeveiliging sprinklerinstallatie Vlaanderen", "brandbeveiliging bedrijf B2B België"],
         "43.29 / 80.20"),
        ("Beveiligingsinstallatie (camera & alarm)",
         "B2B-vastgoed/industrie; abonnementen en monitoring vragen om een klantportaal.",
         ["Website", "Klant-/monitoringportaal", "CRM"],
         ["camerabewaking alarmsystemen installateur Vlaanderen", "beveiligingsfirma B2B België"],
         "80.20 / 43.21"),
    ]),
    ("05-zakelijke-diensten-en-consultancy", "Zakelijke diensten & consultancy", [
        ("Boekhoud- & accountancykantoren",
         "Door Diederick genoemd; klantportalen en documentuitwisseling zijn een sterke upsell.",
         ["Website", "Klantportaal documenten", "CRM/leadbeheer"],
         ["boekhoudkantoor accountancy Vlaanderen", "accountantskantoor KMO België"],
         "69.20"),
        ("Fiscaal & bedrijfsadvies",
         "Vertrouwensberoep; autoriteit-website + lead magnets (whitepapers) werken sterk.",
         ["Website autoriteit", "Lead magnet (fiscale gids)", "CRM"],
         ["fiscaal adviseur bedrijfsadvies Vlaanderen", "fiscaal advieskantoor België"],
         "69.20 / 70.22"),
        ("Verzekeringskantoren (halal-conform)",
         "Enkel halal-conforme makelaars; CRM + lead magnets voor offerteaanvragen.",
         ["Website", "Offerte-/leadformulieren", "CRM"],
         ["verzekeringsmakelaar kantoor Vlaanderen", "verzekeringskantoor KMO België"],
         "66.22"),
        ("Sociale secretariaten & payroll",
         "B2B-dienstverlening met portalen; sterke fit voor klant- en documentportaal.",
         ["Website", "Klantportaal", "CRM"],
         ["sociaal secretariaat payroll Vlaanderen", "loonadministratie dienstverlener België"],
         "69.20 / 78.30"),
        ("HR- & rekruteringsbureaus",
         "Lead- en kandidaatstromen; vacatureportaal + CRM zijn kernsystemen.",
         ["Website + vacatureportaal", "Kandidaat-/klant-CRM", "Lead magnet"],
         ["rekruteringsbureau HR Vlaanderen", "wervingsbureau B2B België"],
         "78.10 / 78.30"),
        ("Vertaalbureaus",
         "Door Diederick genoemd; online offerte/upload-flow verkort de salescyclus sterk.",
         ["Website meertalig", "Online offerte-/uploadsysteem", "Klantportaal"],
         ["vertaalbureau Vlaanderen", "professionele vertaaldiensten B2B België"],
         "74.30"),
        ("Advocaten- & notariskantoren",
         "Vertrouwensberoep; professionele site + beveiligd documentportaal verhogen autoriteit.",
         ["Website autoriteit", "Beveiligd documentportaal", "Afspraaksysteem"],
         ["advocatenkantoor Vlaanderen", "notariskantoor KMO België"],
         "69.10"),
        ("Bedrijfsrevisoren & audit",
         "Hoogwaardige B2B-niche; autoriteit-website + portaal voor dossiers.",
         ["Website autoriteit", "Klantportaal dossiers", "CRM"],
         ["bedrijfsrevisor audit kantoor Vlaanderen", "revisorenkantoor B2B België"],
         "69.20"),
        ("Managementconsultancy (kleine, toegankelijke firms)",
         "Door Diederick genoemd; thought-leadership site + lead magnets = leadmotor.",
         ["Website autoriteit", "Lead magnet (assessment)", "CRM"],
         ["managementconsultancy adviesbureau Vlaanderen", "bedrijfsconsultant KMO België"],
         "70.22"),
        ("Marketing- & communicatiebureaus (non-haram)",
         "Digitaal-mature partners voor co-creatie; nood aan eigen sterke site + portaal.",
         ["Website portfolio", "Klantportaal/projectopvolging", "CRM"],
         ["communicatiebureau marketingbureau Vlaanderen", "B2B marketing agency België"],
         "73.11 / 70.21"),
    ]),
    ("06-engineering-en-studie", "Engineering & studiebureaus", [
        ("Ingenieurs- & studiebureaus (bouw/stabiliteit)",
         "Door Diederick genoemd; technisch sterk maar online zwak — grote upsell in systemen.",
         ["Website + projecten", "Projectportaal", "Documentbeheer backend"],
         ["studiebureau stabiliteit ingenieursbureau Vlaanderen", "engineering bouw KMO België"],
         "71.12"),
        ("Architectenbureaus",
         "Visueel werk dat online sterk converteert; portfolio + klantportaal lonen.",
         ["Website portfolio", "Klantportaal plannen", "Offerte-/intakesysteem"],
         ["architectenbureau Vlaanderen", "architect KMO B2B België"],
         "71.11"),
        ("Landmeters & geodeten",
         "Technische B2B-niche; online aanvraag + dossierportaal versnellen de flow.",
         ["Website", "Online aanvraagsysteem", "Dossierportaal"],
         ["landmeter geodeet bureau Vlaanderen", "landmeetkundig bureau België"],
         "71.12"),
        ("EPB- & energieadviesbureaus",
         "Premie-/regelgevingsgedreven; lead magnets (energiescan) werken sterk.",
         ["Website", "Lead magnet (energiescan)", "Dossier-/klantportaal"],
         ["EPB-verslaggever energieadvies Vlaanderen", "energieadviesbureau België"],
         "71.20 / 74.90"),
        ("Veiligheidscoördinatie & preventie",
         "Wettelijk gedreven B2B-dienst; dossier- en planningsoftware loont sterk.",
         ["Website", "Dossier-/planningportaal", "CRM"],
         ["veiligheidscoördinatie preventieadviseur Vlaanderen", "veiligheidscoördinator bouw België"],
         "74.90 / 71.20"),
        ("Industriële ontwerp- & engineeringbureaus",
         "Hoogwaardige B2B-niche; cases en meertalige site versterken internationale positie.",
         ["Website meertalig + cases", "Projectportaal", "Documentbeheer"],
         ["industrieel ontwerp engineering bureau Vlaanderen", "product engineering B2B België"],
         "71.12 / 74.10"),
    ]),
    ("07-it-en-tech", "IT & tech", [
        ("IT-diensten & systeembeheer (MSP)",
         "Door Diederick genoemd; digitaal-mature klant, maar eigen site/portaal vaak verwaarloosd.",
         ["Website", "Ticket-/klantportaal", "CRM"],
         ["IT-diensten systeembeheer MSP Vlaanderen", "managed services provider KMO België"],
         "62.02 / 62.09"),
        ("Softwarebedrijven (kleine B2B SaaS)",
         "Co-creatie- en doorverwijspartners; sterke fit voor marketingsite + leadflow.",
         ["Website/marketingsite", "Lead magnet (demo/trial)", "CRM"],
         ["softwarebedrijf B2B SaaS Vlaanderen", "software ontwikkelaar KMO België"],
         "62.01"),
        ("Telecom- & netwerkinstallatie",
         "B2B-installateurs met contracten; service-portaal en CRM lonen.",
         ["Website", "Service-/klantportaal", "CRM"],
         ["telecom netwerkinstallatie bedrijf Vlaanderen", "netwerkbekabeling installateur België"],
         "61.10 / 43.21"),
        ("Cybersecurity-bedrijven",
         "Vertrouwen + autoriteit cruciaal; lead magnets (security scan) werken sterk.",
         ["Website autoriteit", "Lead magnet (security scan)", "CRM"],
         ["cybersecurity bedrijf Vlaanderen", "IT-beveiliging dienstverlener B2B België"],
         "62.02 / 62.09"),
        ("Datacenters & hosting (kleinere spelers)",
         "Technisch B2B; klantportaal + statusdashboards zijn kernsystemen.",
         ["Website", "Klant-/statusportaal", "BI-dashboard"],
         ["datacenter hosting provider Vlaanderen", "hostingbedrijf B2B België"],
         "63.11"),
    ]),
    ("08-medisch-en-paramedisch", "Medisch & paramedisch (non-cosmetisch)", [
        ("Tandartspraktijken (groepspraktijk)",
         "Vanaf meerdere behandelaars; online afspraak + patiëntportaal verhogen instroom.",
         ["Website", "Online afspraaksysteem", "Patiëntportaal"],
         ["tandarts groepspraktijk Vlaanderen", "tandartsenpraktijk meerdere artsen België"],
         "86.23"),
        ("Kinesitherapie-groepspraktijken",
         "Teampraktijken; online boeken en patiëntopvolging zijn directe verbeteringen.",
         ["Website", "Online boekingssysteem", "Patiëntportaal"],
         ["kinesitherapie groepspraktijk Vlaanderen", "kine praktijk meerdere therapeuten België"],
         "86.90"),
        ("Podologie & orthopedie (praktijken)",
         "Paramedische niche met afspraakflow; online boeken verhoogt instroom.",
         ["Website", "Online afspraaksysteem", "Patiëntportaal"],
         ["podologie praktijk Vlaanderen", "orthopedie podoloog praktijk België"],
         "86.90"),
        ("Medische labo's & beeldvorming",
         "B2B/B2C-mix met verwijzers; resultaten- en afspraakportaal lonen.",
         ["Website", "Afspraak-/resultatenportaal", "Verwijzersportaal"],
         ["medisch labo beeldvorming Vlaanderen", "klinisch laboratorium B2B België"],
         "86.90"),
        ("Dierenartsenpraktijken",
         "Door Diederick genoemd; online afspraak + klantportaal verhogen klantbinding.",
         ["Website", "Online afspraaksysteem", "Klant-/dierportaal"],
         ["dierenartsenpraktijk Vlaanderen", "dierenkliniek meerdere artsen België"],
         "75.00"),
        ("Thuisverpleging-organisaties",
         "Operationeel zwaar; planning- en patiëntopvolging schreeuwen om software.",
         ["Website", "Planning-/rooster backend", "Patiënt-/familieportaal"],
         ["thuisverpleging organisatie Vlaanderen", "thuisverpleegkundigen team België"],
         "86.90 / 88.10"),
        ("Medische hulpmiddelen & orthopedische technologie",
         "B2B-leveranciers met voorschriftflow; bestel- en dossierportaal lonen.",
         ["Website", "Bestel-/dossierportaal", "CRM"],
         ["medische hulpmiddelen orthopedische technologie Vlaanderen", "bandagist orthopedie B2B België"],
         "32.50 / 47.74"),
    ]),
    ("09-vakmannen-en-technische-kmo", "Vakmannen & technische KMO's (grotere teams)", [
        ("Schrijnwerkerijen & interieurbouw (maatwerk)",
         "Visueel maatwerk; portfolio + offerteconfigurator zijn sterke conversiehefbomen.",
         ["Website + realisaties", "Offerte-/configuratietool", "Projectopvolging backend"],
         ["schrijnwerkerij interieurbouw maatwerk Vlaanderen", "maatmeubel interieurbouwer België"],
         "16.23 / 43.32"),
        ("Bandencentrales & autotechniek (B2B/vloot)",
         "Vlootcontracten = terugkerende B2B-omzet; online afspraak en vlootbeheer lonen.",
         ["Website", "Online afspraaksysteem", "Vloot-/klantportaal"],
         ["bandencentrale autotechniek vloot Vlaanderen", "bandenservice B2B fleet België"],
         "45.20"),
        ("Garages & carrosserie (vlootonderhoud)",
         "BelgaLink heeft al een garage-backend gebouwd; bewezen fit voor beheersystemen.",
         ["Website", "Online afspraak-/intakesysteem", "Wagenpark-/werkplaats backend"],
         ["garage carrosserie vlootonderhoud Vlaanderen", "autogarage fleet B2B België"],
         "45.20"),
        ("Schoonmaakbedrijven (industrieel/kantoor)",
         "Contractgedreven B2B; offerte- en planningsystemen besparen veel administratie.",
         ["Website", "Offerte-/contractsysteem", "Planning-/rooster backend"],
         ["industriële schoonmaak kantoorschoonmaak Vlaanderen", "schoonmaakbedrijf B2B contract België"],
         "81.21 / 81.22"),
        ("Gevel-, ruiten- & industriële reiniging",
         "Gespecialiseerde B2B-reiniging met contracten; online offerte en planning lonen.",
         ["Website", "Offertesysteem", "Planning backend"],
         ["gevelreiniging ruitenwasserij industrieel Vlaanderen", "industriële reiniging bedrijf België"],
         "81.22 / 81.29"),
        ("Ontstoppings- & rioleringsdiensten",
         "Urgentiegedreven; online aanvraag + 24/7-flow zetten direct aanvragen om.",
         ["Website", "Online aanvraag-/interventiesysteem", "Planning backend"],
         ["ontstopping riolering bedrijf Vlaanderen", "rioolreiniging dienst België"],
         "37.00 / 81.29"),
        ("Drukkerijen & grafische bedrijven",
         "Door Diederick genoemd; online bestel-/offerteportaal verkort de salescyclus sterk.",
         ["Website", "Online bestel-/offerteportaal", "Klant-/orderbeheer backend"],
         ["drukkerij grafisch bedrijf Vlaanderen", "professionele drukkerij B2B België"],
         "18.12 / 18.13"),
    ]),
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


def niche_readme(num: int, cat_label: str, name: str, fit: str,
                 upsell, zoektermen, nace: str) -> str:
    upsell_md = "\n".join(f"- {u}" for u in upsell)
    zoek_md = "\n".join(f"- `{z}`" for z in zoektermen)
    return f"""# Niche {num:02d} — {name}

**Categorie:** {cat_label}

## Waarom deze niche past bij BelgaLink
{fit}

> Profiel: Vlaamse KMO, team van ~3 tot 30 medewerkers, halal-conform. Zaakvoerder is
> sterk in zijn vak, minder met digitaal bezig — exact de avatar uit de briefing.

## Upsell-potentieel (naast de website)
{upsell_md}

## Firecrawl-scraping

**Doelvelden per lead:** e-mail · volledige naam eigenaar · telefoon · website · BTW-nummer.

**Startqueries (Firecrawl `search`):**
{zoek_md}

**Indicatieve NACEBEL-code(s):** {nace}
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
"""


def write_leads_csv(path: pathlib.Path) -> None:
    if path.exists():
        return  # nooit overschrijven — hier komen de gescrapete leads in
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(LEAD_COLUMNS)


def main() -> None:
    NICHES_DIR.mkdir(parents=True, exist_ok=True)
    counter = 0
    index_lines = []

    for cat_idx, (cat_slug, cat_label, niches) in enumerate(CATEGORIES, start=1):
        cat_dir = NICHES_DIR / cat_slug
        cat_dir.mkdir(parents=True, exist_ok=True)
        index_lines.append(f"\n### {cat_idx:02d}. {cat_label}\n")
        # categorie-README
        (cat_dir / "README.md").write_text(
            f"# {cat_label}\n\n{len(niches)} niches in deze categorie.\n", encoding="utf-8")

        for n_idx, (name, fit, upsell, zoek, nace) in enumerate(niches, start=1):
            counter += 1
            niche_dir = cat_dir / slugify(name, n_idx)
            niche_dir.mkdir(parents=True, exist_ok=True)
            (niche_dir / "README.md").write_text(
                niche_readme(counter, cat_label, name, fit, upsell, zoek, nace),
                encoding="utf-8")
            write_leads_csv(niche_dir / "leads.csv")
            rel = niche_dir.relative_to(ROOT)
            index_lines.append(f"{counter}. **{name}** — `{rel}/`")

    total = counter
    master = (
        "# BelgaLink — Master-lijst 75 B2B niches\n\n"
        f"In totaal **{total} niches**, gegroepeerd in {len(CATEGORIES)} categorieën.\n\n"
        "Elke niche heeft een eigen map met `README.md` (niche-profiel + scraping-plan) "
        "en `leads.csv` (klaar voor Firecrawl-resultaten).\n\n"
        "Halal-conform gefilterd (geen alcohol, varkensvlees, gokken, interest-producten, "
        "horeca, beauty/cosmetica of muziek-industrie).\n"
        + "".join(l + "\n" for l in index_lines)
    )
    (ROOT / "00-niche-master-list.md").write_text(master, encoding="utf-8")
    print(f"Klaar: {total} niches gegenereerd in {NICHES_DIR}")


if __name__ == "__main__":
    main()
