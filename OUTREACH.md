# Outreach map — who receives the country briefs

Companion to `countries/<ISO>/GOAL.md`. For each member state: the office that owns the
policy, the agency that would build the thing, the authority that would certify it, the
buying channel, the parliamentary committee that scrutinises it, and the press desks that
cover it. Ordered by modelled stake (largest first), matching `countries/SUMMARY.md`.

## Scope rule

**This file is institutional only.** Offices, agencies, committees and press desks — all
public record, all stable across a legislature. Named individuals, personal addresses and
direct lines go in the separate **private** repo `sovereign-data-centers-contacts`, for
exactly this reason. Do not add a person's name to this file.

## Provenance — read before sending anything

| Rows | Source | Confidence |
|---|---|---|
| Operator, certification scheme, procurement vehicle, IXP | `model/eu27_parameters.csv` | Researched in-repo against primary sources; see `DECISIONS.md` |
| Stake figures | `model/eu27_results.csv` | Model output, reproducible |
| **Ministry, committee, press** | **General knowledge, not verified in-repo** | **Check before send** |

Ministry names are the volatile field: digital portfolios get merged, split and renamed at
every cabinet reshuffle, and several below moved within the last two years (EE folded digital
into Justice in 2025; HR folded SDURDD into the justice-and-administration ministry in 2024;
DE created BMDS in 2025). Verify the current name and the current officeholder at time of
send. Committee names survive reshuffles better; press desks are the most stable rows here.

## How to use it

Four tiers, in send order. The brief is a planning model, not a proposal — it lands best with
the operator and the scrutiny layer, worst as a cold ministerial send.

1. **Operator** — the state IT agency. They have the workload inventory the model is guessing
   at, so they are the ones who can falsify it. Best first contact; also the most likely to
   engage on substance.
2. **Scrutiny** — parliamentary committee, court of audit, advisory boards. They are looking
   for exactly this kind of independent sizing and are not procurement-conflicted.
3. **Press** — trade and policy press before national dailies. The public-administration
   trade titles (Behörden Spiegel, Acteurs Publics, Binnenlands Bestuur, Altinget, Dagens
   Samhälle) reach the operator layer directly and cover procurement as a beat.
4. **Ministry** — last, and warm rather than cold. A ministerial send that arrives before the
   operator has seen it tends to get routed back to the operator as a threat.

Per-country **Hook** lines are the live policy hinge from `eu27_parameters.csv` — the thing
that makes the brief topical in that country this year. Lead with it.

---

# Tier 0 — European level

Send here in parallel with the large states, not after. The EU Cloud and AI Development Act
(CADA) is the live vehicle and makes an EU-27 comparative sizing immediately citable.

| Function | Body |
|---|---|
| Policy owner | European Commission **DG CNECT**, Cloud & Software unit; Commissioner portfolio for Tech Sovereignty, Security and Democracy |
| Commission's own estate | **DG DIGIT** — runs the Commission's data centres; an in-house counterpart to the national cases |
| Security / certification | **ENISA** (EUCS scheme), European Cybersecurity Certification Group (ECCG) |
| Defence / resilience angle | DG DEFIS, DG HOME; EU Critical Entities Resilience and NIS2 files |
| Compute infrastructure | **EuroHPC JU** — already sited in several of the modelled regions (LUMI/Kajaani, Vega/Maribor, Discoverer/Sofia) |
| Scrutiny | European Parliament **ITRE** and **IMCO**; **STOA** panel; **European Court of Auditors** (has audited Commission cloud use); **EDPS** (ruled against the Commission's own Microsoft 365 use) |
| Council | Telecom Working Party; the rotating presidency's digital file |
| Industry / multiplier | CISPE, Gaia-X, EuroCloud, ECSO, IPCEI-CIS participants |
| Think tanks | Bruegel, CEPS, ECFR, interface (ex-SNV), Clingendael, IFRI, ISPI |
| Press | **Euractiv**, **Politico Europe** (Morning Tech), **MLex**, **Contexte** (FR), **Table.Media** (DE), Science\|Business, EUobserver, Follow the Money (cross-border investigations) |

**Hook.** The model's EU-27 total — 306 MW design load, ~EUR 7.2 bn CAPEX, 86 sites — is the
number the CADA debate does not currently have. The federation finding is the sharper one:
four member states (EE, LT, LV, and the micro-states) cannot meet their own separation
requirements inside national borders, which is an argument for an EU instrument rather than
27 national programmes. See `countries/SUMMARY.md` and the deferred federation workstream in
`TODO.md`.

---

# Tier 1 — the five large states

## DE Germany
*60.4 MW design · EUR 1,435 m CAPEX · 6 sites · frontline: no*

| Function | Body |
|---|---|
| Policy owner | Bundesministerium für Digitales und Staatsmodernisierung (BMDS) |
| Federation layer | IT-Planungsrat, FITKO, govdigital, ZenDiS (openDesk) |
| Operator | **ITZBund** (Bundescloud); Deutsche Verwaltungscloud (DVC) federated |
| Security / certification | **BSI** — C5 catalogue |
| Procurement | Beschaffungsamt des BMI; Kaufhaus des Bundes |
| Scrutiny | Bundestag Ausschuss für Digitales und Staatsmodernisierung; Bundesrechnungshof |
| Press — trade | **Behörden Spiegel**, **Tagesspiegel Background Digitalisierung**, Heise online / c't, Golem.de, Netzpolitik.org |
| Press — national | FAZ, Handelsblatt, Süddeutsche Zeitung |

**Hook.** Delos Cloud (SAP/Arvato on Azure) is the contested case: a BSI-aligned "sovereign"
layer on a US hyperscaler, sitting alongside the DVC launched March 2025. The brief's Frankfurt
finding is the operational one — DE-CIX gravity pulls the primary site into the most
grid-saturated market in Europe, with multi-year connection lead times, which is why the model
puts only 36% of load there and pushes the rest to Berlin-Brandenburg, Munich, Hamburg and
Leipzig.

## FR France
*45.9 MW design · EUR 1,086 m CAPEX · 4 sites*

| Function | Body |
|---|---|
| Policy owner | **DINUM** (direction interministérielle du numérique), under the PM; minister for digital affairs |
| Operator | Nubo (Finances), Cloud Pi Native (Intérieur) |
| Security / certification | **ANSSI** — SecNumCloud, the most demanding national scheme in the EU-27 |
| Procurement | UGAP; DINUM interministerial frameworks |
| Scrutiny | Assemblée nationale commission des affaires économiques; **Sénat** — has run a commission d'enquête on public procurement and digital sovereignty; Cour des comptes |
| Industry multiplier | **Cigref** (large-enterprise CIOs; drives the sovereignty debate) |
| Press — trade | **Acteurs Publics**, next.ink (ex-NextINpact), L'Informé, La Lettre |
| Press — national | Le Monde, Les Échos, La Tribune |

**Hook.** France is the one country where the certification regime, not the capacity, is the
binding constraint — SecNumCloud qualification is what Bleu and NumSpot are still waiting on.
The brief's contribution is capacity sizing against an RTE grid that is saturated in
Île-de-France, which is why the model splits load four ways rather than concentrating it.

## IT Italy
*36.1 MW design · EUR 857 m CAPEX · 4 sites · seismic*

| Function | Body |
|---|---|
| Policy owner | Dipartimento per la trasformazione digitale (Presidenza del Consiglio); Ministro per la pubblica amministrazione |
| Operator | **PSN** — Polo Strategico Nazionale (TIM / Leonardo / CDP / Sogei), operational since 2023 |
| Security / certification | **ACN** — cloud qualification, ordinary/critical/strategic tiers |
| Procurement | Consip |
| Scrutiny | Camera IX Commissione (Trasporti e Telecomunicazioni); **COPASIR** for the security angle; Corte dei conti |
| Press — trade | **CorCom** (Corriere Comunicazioni), Wired Italia, Formiche, Decode39 |
| Press — national | Il Sole 24 Ore, Corriere della Sera, la Repubblica |

**Hook.** Italy is furthest along — PSN is running with mandatory migration deadlines — so the
brief is a check on a live programme rather than a proposal. The seismic flag is the
differentiator: base isolation is mandatory rather than optional at the primary site, which the
model prices in and which is why load is split across Milan, Rome, Turin, Bari and Bologna as
separate seismic domains.

## ES Spain
*30.2 MW design · EUR 711 m CAPEX · 4 sites · grid-isolated*

| Function | Body |
|---|---|
| Policy owner | Ministerio para la Transformación Digital y de la Función Pública; **SEDIA** |
| Operator | **SGAD** — Nube SARA; sectoral ENS-Alta clouds (AEAT, GISS) |
| Security / certification | **CCN-CERT** (CNI) — ENS at Basic/Medium/High, CCN-STIC guides |
| Procurement | Dirección General de Racionalización y Centralización de la Contratación |
| Scrutiny | Congreso Comisión para la Transformación Digital; Tribunal de Cuentas |
| Regional layer | Madrid's 2026 regional sovereign cloud — a live counterexample to central consolidation |
| Press — trade | El Confidencial (tech), Xataka, Business Insider España |
| Press — national | El País, El Mundo, Expansión, Cinco Días |

**Hook.** Spain has no single state cloud — ENS certification is the unifying layer instead,
and regional clouds are emerging underneath it. The April 2025 Iberian blackout made the
grid-isolated flag concrete rather than theoretical; the brief treats peninsular grid islanding
as a siting constraint, splitting load across Madrid, Zaragoza, Barcelona, Seville-Málaga and
Castilla y León-Galicia.

## PL Poland
*24.7 MW design · EUR 578 m CAPEX · 4 sites · **frontline***

| Function | Body |
|---|---|
| Policy owner | Ministerstwo Cyfryzacji |
| Operator | **COI** (Centralny Ośrodek Informatyki), **NASK** — RChO government cloud, ZUCH marketplace |
| Security / certification | NASK / CSIRT NASK; Government Plenipotentiary for Cybersecurity; KRI regulation |
| Procurement | COI; central framework agreements |
| Scrutiny | Sejm Komisja Cyfryzacji, Innowacyjności i Nowoczesnych Technologii; NIK (supreme audit office) |
| Press — trade | **Cyberdefence24** / Defence24 group, Niebezpiecznik, Business Insider Polska |
| Press — national | Rzeczpospolita, Gazeta Wyborcza, Dziennik Gazeta Prawna, Puls Biznesu |

**Hook.** Poland is the largest frontline state, and the frontline flag is not decorative in the
model — it scales defence and security workloads up and forces a hardened site posture. Poland
is also driving the national sovereign cloud and AI-factory argument inside the CADA debate, so
the EU-27 comparison lands directly in a position Warsaw is already arguing.

---

# Tier 2 — mid-sized states

## NL Netherlands — *the reference case*
*14.2 MW design · EUR 339 m CAPEX · 3 sites*

| Function | Body |
|---|---|
| Policy owner | Ministerie van BZK; staatssecretaris Digitalisering |
| Operator | **SSC-ICT**, **Logius**, ODC-Noord, DICTU |
| Security / certification | NCSC-NL; **BIO** is the binding baseline (no national cloud scheme) |
| Procurement | Rijksinkoop; SSC-ICT |
| Scrutiny | Tweede Kamer commissie Digitale Zaken; **Algemene Rekenkamer**; **Adviescollege ICT-toetsing (AcICT)** — reviews large government IT programmes, the single most relevant reviewer of this model |
| Press — trade | **Binnenlands Bestuur**, AG Connect, Computable, Tweakers, **Follow the Money** |
| Press — national | NRC, de Volkskrant, FD, Trouw |

**Hook.** The July 2026 cabinet decision to build a government-run sovereign cloud in the
Overheidsdatacenters, with first applications end-2026, is the live programme — and this repo's
NL case is the hand-built reference the other 26 are derived from, reproducing the Dutch xlsx
exactly (5,691 servers, 14.2 MW, EUR 339 m). Highest-credibility send in the set.

## RO Romania
*11.9 MW design · EUR 278 m CAPEX · 4 sites · **frontline**, seismic*

| Function | Body |
|---|---|
| Policy owner | Ministerul Cercetării, Inovării și Digitalizării; **ADR** |
| Operator | **STS** (Serviciul de Telecomunicații Speciale) — Cloud Privat Guvernamental |
| Security / certification | DNSC (national cyber security directorate); SRI for classified |
| Procurement | ADR; ONAC |
| Scrutiny | Camera Deputaților Comisia pentru tehnologia informației și comunicațiilor; Curtea de Conturi |
| Press | Hotnews.ro, Ziarul Financiar, Profit.ro, Economedia, Digi24 |

**Hook.** The PNRR-funded cloud (~EUR 560 m, four regional DCs) reached national operational
phase in March 2026 — and the model's own regions land on Bucharest, Timiș, Brașov and Sibiu,
which is close to the sites Romania actually chose. That agreement is worth leading with: it is
the strongest external validation the model has.

## BE Belgium
*8.7 MW design · EUR 207 m CAPEX · 3 sites*

| Function | Body |
|---|---|
| Policy owner | **FPS BOSA**; state secretary for digitalisation |
| Operator | **Smals** — federal G-Cloud, social-security IT |
| Security / certification | **CCB** (Centre for Cybersecurity Belgium) |
| Procurement | FPS BOSA federal framework; Smals |
| Scrutiny | Chambre / Kamer commission for the economy; Rekenhof / Cour des comptes |
| Industry multiplier | Beltug (CIO association) |
| Press — trade | **Data News** (Roularta) |
| Press — national | De Standaard, De Tijd, Le Soir, L'Echo |

**Hook.** Smals selected Google Cloud as its public-cloud pillar in June 2026 under federal
sovereignty and portability rules — the sharpest live test in the EU of whether contractual
sovereignty conditions on a US hyperscaler substitute for owned infrastructure. The brief prices
the alternative.

## SE Sweden
*7.9 MW design · EUR 189 m CAPEX · 3 sites*

| Function | Body |
|---|---|
| Policy owner | Finansdepartementet (digitalisation portfolio) |
| Coordination | **DIGG** (Agency for Digital Government) |
| Operator | Försäkringskassan (**SAFOS**), Skatteverket, Lantmäteriet, Trafikverket — coordinated state IT operations |
| Security | MSB; FRA; Säkerhetspolisen |
| Procurement | **Kammarkollegiet**; Adda |
| Scrutiny | Riksdag finansutskottet, konstitutionsutskottet; Riksrevisionen |
| Press — trade | **Dagens Samhälle** (public sector), Computer Sweden / IDG, Ny Teknik |
| Press — national | Dagens Nyheter, Svenska Dagbladet, Dagens Industri |

**Hook.** The May 2026 national cloud policy is guidance, not a binding doctrine — Sweden is the
largest state with no sovereignty mandate. Cheap northern power (97 EUR/MWh, second-lowest in
the set) makes the Luleå-Boden siting unusually favourable, which is the constructive angle.

## AT Austria
*6.8 MW design · EUR 161 m CAPEX · 3 sites*

| Function | Body |
|---|---|
| Policy owner | BMF (digitalisation state secretariat); Bundeskanzleramt |
| Operator | **BRZ** (Bundesrechenzentrum) |
| Security | GovCERT Austria; Cybersicherheitszentrum (BSI C5 referenced in practice) |
| Procurement | **BBG** (Bundesbeschaffung GmbH) |
| Scrutiny | Nationalrat Ausschuss für Forschung, Innovation und Digitalisierung; Rechnungshof |
| Press — trade | **futurezone**, Der Brutkasten, Trending Topics |
| Press — national | Der Standard, Die Presse, Kurier |

**Hook.** The 2026 Digital Administration Guideline names digital sovereignty a core principle
without creating a branded sovereign cloud — the gap between stated principle and built
infrastructure is the story. Danube flood zoning at the Vienna primary site is the concrete
siting constraint.

## CZ Czechia
*6.5 MW design · EUR 152 m CAPEX · 3 sites*

| Function | Body |
|---|---|
| Policy owner | **DIA** (Digitální a informační agentura); Ministerstvo vnitra |
| Operator | **SPCSS** (security level 4), **NAKIT** — eGovernment Cloud |
| Security / certification | **NÚKIB** — assesses every commercial entry to the eGC catalogue |
| Procurement | Ministry of the Interior eGC catalogue |
| Scrutiny | Poslanecká sněmovna, public administration committee and eGovernment subcommittee; NKÚ |
| Press — trade | **Lupa.cz**, Root.cz, E15 |
| Press — national | Hospodářské noviny, Deník N, Seznam Zprávy |

**Hook.** Czechia already has what most member states are still debating: a mandatory catalogue
route where hyperscalers are admitted only after a NÚKIB security assessment. It is the most
transferable governance model in the set, and worth writing up as such.

## PT Portugal
*6.4 MW design · EUR 150 m CAPEX · 3 sites · grid-isolated, seismic*

| Function | Body |
|---|---|
| Policy owner | State secretariat for digitalisation and administrative modernisation |
| Operator | **AMA** (Agência para a Modernização Administrativa), **eSPap** — Nuvem da AP |
| Security | **CNCS** (Centro Nacional de Cibersegurança) |
| Procurement | eSPap central frameworks |
| Scrutiny | Assembleia da República, economy and public works committee; Tribunal de Contas |
| Press — trade | Exame Informática, SAPO Tek, Dinheiro Vivo |
| Press — national | Público, Expresso, Jornal de Negócios, Observador |

**Hook.** The Plano Nacional de Nuvem Soberana was approved in May 2026 — data classification
and phased state infrastructure — so the brief arrives exactly at the sizing stage. Sines is the
distinctive asset: an Atlantic cable hub (EllaLink, 2Africa, Equiano, Medusa) that few EU states
can match, and the model allocates it the sovereign-secondary role accordingly.

## EL Greece
*6.1 MW design · EUR 142 m CAPEX · 3 sites · seismic*

| Function | Body |
|---|---|
| Policy owner | Ministry of Digital Governance |
| Operator | **GSIS** (ΓΓΠΣ) — G-Cloud on SYZEFXIS; **GRNET** (ΕΔΥΤΕ) — research cloud, HPC, EUDI wallet lead |
| Security | National Cybersecurity Authority |
| Procurement | Ministry of Digital Governance; GRNET |
| Scrutiny | Hellenic Parliament standing committee on public administration; Ελεγκτικό Συνέδριο |
| Press | Kathimerini, To Vima, Naftemporiki, Capital.gr, Insider.gr |

**Hook.** Greece is a genuine East-Med cable hub — Crete/Chania plus the Great Sea
Interconnector — which the model treats as a reserve/edge asset rather than a primary site,
because island siting cannot carry sovereign primary load. That trade-off is the discussion.

## HU Hungary
*5.7 MW design · EUR 132 m CAPEX · 3 sites*

| Function | Body |
|---|---|
| Policy owner | Digital Hungary Agency |
| Operator | **NISZ Zrt.** — Kormányzati Adatközpont (KAK) |
| Security | National Cyber Security Centre |
| Procurement | **DKÜ** — mandatory central IT purchasing channel |
| Scrutiny | Országgyűlés gazdasági bizottság; Állami Számvevőszék |
| Press — trade | Bitport.hu, HWSW |
| Press — national | Telex, hvg.hu, Portfolio.hu, Index |

**Hook.** Ministry IT consolidation is being done by decree, and DKÜ is a mandatory channel —
a highly centralised model that the capacity numbers can be tested against directly. Debrecen,
the model's sovereign-secondary region, sits 130 km from the Ukrainian border and gets a
hardened design in the brief.

## IE Ireland
*5.3 MW design · EUR 131 m CAPEX · 3 sites · grid-isolated*

| Function | Body |
|---|---|
| Policy owner | Department of Public Expenditure, NDP Delivery and Reform — **OGCIO** |
| Operator | Government Cloud Network; Backweston government data centres |
| Security | **NCSC Ireland** |
| Procurement | **OGP** (Office of Government Procurement) |
| Scrutiny | Oireachtas Joint Committee on Finance and Public Expenditure; **Public Accounts Committee**; C&AG |
| Grid | EirGrid, CRU — the binding constraint |
| Press — trade | Silicon Republic, The Currency |
| Press — national | The Irish Times, Irish Independent, Business Post, RTÉ |

**Hook.** Ireland is the sharpest paradox in the set: Europe's densest hyperscale data centre
market, no sovereign cloud, cloud-first with no sovereignty carve-out, and the highest power
price of any large state (255 EUR/MWh) under a CRU connection moratorium in Dublin. The Digital
Decade 2025 report already flags the grid limit. The model's answer — push capacity to Cork,
Galway-Limerick and the Midlands — is a direct policy input.

## DK Denmark
*4.7 MW design · EUR 114 m CAPEX · 3 sites*

| Function | Body |
|---|---|
| Policy owner | **Digitaliseringsministeriet** |
| Operator | **Statens It**; Digitaliseringsstyrelsen |
| Security | **CFCS** (Center for Cybersikkerhed, under FE) |
| Procurement | **SKI**; Statens Indkøb |
| Scrutiny | Folketinget Digitaliseringsudvalget; Rigsrevisionen |
| Press — trade | **Altinget** (digital vertical), Version2 / Ingeniøren, Computerworld DK |
| Press — national | Politiken, Berlingske, Jyllands-Posten, Børsen |

**Hook.** Denmark is the furthest into an actual exit: the Ministry of Digitalisation's 2025
Microsoft phase-out, plus a DKK 80 m digital-sovereignty action plan and the 2026-29 joint
strategy. It is the reference case other ministries cite, and the brief supplies the capacity
arithmetic that a phase-out implies.

## FI Finland
*4.3 MW design · EUR 104 m CAPEX · 3 sites · **frontline***

| Function | Body |
|---|---|
| Policy owner | Valtiovarainministeriö (Ministry of Finance) |
| Operator | **Valtori** (Government ICT Centre); DVV |
| Security / certification | **Traficom NCSA-FI** — Katakri and **PiTuKri** cloud criteria |
| Procurement | **Hansel Oy** |
| Scrutiny | Eduskunta hallintovaliokunta; liikenne- ja viestintävaliokunta; VTV |
| Press — trade | **Tivi**, Tekniikka&Talous |
| Press — national | Helsingin Sanomat, Kauppalehti, Yle |

**Hook.** The Digital Sovereignty Roadmap was adopted April 2026, and the C-Lion1 cable damage
of November 2024 turned subsea resilience from an abstraction into a national security file.
Finland also has the cheapest power in the EU-27 (75 EUR/MWh) and free cooling in the north —
the Oulu and Kajaani regions are the strongest siting case anywhere in the model.

## BG Bulgaria
*4.2 MW design · EUR 98 m CAPEX · 3 sites · **frontline**, seismic*

| Function | Body |
|---|---|
| Policy owner | Ministry of e-Government |
| Operator | **Information Services JSC** — State Hybrid Private Cloud (SHPC), upgraded 2024 |
| Security | National cyber security coordinator; ISO 27001 baseline |
| Procurement | Ministry of e-Government central purchasing |
| Scrutiny | National Assembly committee on electronic governance and IT; Сметна палата |
| Compute | EuroHPC **Discoverer** (Sofia) |
| Press | Capital.bg, Dnevnik, Mediapool, Investor.bg |

**Hook.** Bulgaria already mandates use of the state hybrid cloud, so the question is capacity
not policy. Varna is the interesting call: Black Sea cable landings make it attractive and
frontline exposure makes it unsuitable for primary load, so the model gives it reserve/edge
status only.

## SK Slovakia
*3.3 MW design · EUR 76 m CAPEX · 3 sites*

| Function | Body |
|---|---|
| Policy owner | **MIRRI** |
| Operator | Datacentrum Kopčianska (MV SR); DataCentrum (MoF), backup at Tajov |
| Security | **NBÚ**; SK-CERT |
| Procurement | MIRRI central catalogue |
| Scrutiny | NR SR výbor pre hospodárske záležitosti; NKÚ |
| Press — trade | Živé.sk, TREND |
| Press — national | Denník N, SME, HNonline |

**Hook.** The government cloud exists with a hybrid extension to certified providers, but the
certification layer is ISO 27001 only — no national scheme. The comparison with neighbouring
Czechia's NÚKIB-assessed catalogue is the most useful thing the EU-27 view offers Bratislava.

---

# Tier 3 — small and micro states

For these, the federation finding matters more than the national numbers. Lead with the
out-of-country reserve argument and the Estonian Data Embassy precedent.

## HR Croatia
*2.2 MW · EUR 52 m · 3 sites · seismic*

Policy owner: Ministry of Justice, Public Administration and Digital Transformation (absorbed
SDURDD in 2024). Operator: **APIS IT** — CDU shared services centre, two HA sites, NRRP-funded.
Security: ZSIS; CERT (CARNET). Scrutiny: Sabor odbor za gospodarstvo; Državni ured za reviziju.
Press: Bug.hr, Netokracija, Lider; Jutarnji list, Večernji list, Index.hr.

**Hook.** The 2020 Zagreb earthquake makes seismic isolation mandatory at the primary site — one
of only two countries in the set (with Italy) where a recent event, not a hazard map, sets the
design requirement.

## LT Lithuania
*2.1 MW · EUR 49 m · 3 sites · **frontline***

Policy owner: Ministry of Economy and Innovation; Ministry of Transport and Communications.
Operator: **KVTC**, under the **Ministry of National Defence** — the only EU state where the
government cloud sits under defence. Security: **NKSC** (under MoD). Procurement: **CPO LT**.
Scrutiny: Seimas Committee on Economics; National Security and Defence Committee; VKT.
Press: LRT, Verslo žinios, Delfi, 15min.

**Hook.** Defence ownership of the state cloud is the structural difference, and it aligns with
the model's frontline scaling. Lithuania has no subsea landing of its own — the model puts the
strategic reserve out of country.

## LV Latvia
*1.5 MW · EUR 36 m · 3 sites · **frontline***

Policy owner: Ministry of Smart Administration and Regional Development (VARAM). Operator:
**LVRTC**, **VRAA** — national federated cloud, RRF phase completed May 2026 with 64 state
systems hosted. Security: **CERT.LV**. Procurement: Electronic Procurement System (EIS).
Scrutiny: Saeima public administration and local government committee; Valsts kontrole.
Press: LSM.lv, Diena, Dienas Bizness, Delfi.lv, IR.

**Hook.** The RRF-funded phase just completed, so Latvia has fresh real numbers on what 64
migrated systems actually cost and consume — the best available calibration data for the
small-state end of the model, and worth asking for directly.

## EE Estonia
*1.4 MW · EUR 35 m · 3 sites + Data Embassy · **frontline***

Policy owner: Ministry of Justice and Digital Affairs (merged 2025). Operator: **RIT** —
Riigipilv on OCI Dedicated Region; **RIA** (Information System Authority); X-Road. Security:
RIA / CERT-EE; **E-ITS** national standard (successor to ISKE). Scrutiny: Riigikogu
constitutional and economic affairs committees; Riigikontroll. Multiplier: **e-Estonia Briefing
Centre** — a distribution channel in its own right. Press: ERR, Postimees, Äripäev, Geenius.ee.

**Hook.** Estonia already solved the problem the model surfaces elsewhere: the **Data Embassy
Act** lets state data sit under Estonian jurisdiction abroad, and the Luxembourg embassy has run
since 2018. Tartu is 60 km from the Russian border. Estonia is the natural co-author for the
federation workstream, not just a recipient.

## SI Slovenia
*1.4 MW · EUR 34 m · 3 sites*

Policy owner: **Ministrstvo za digitalno preobrazbo**. Operator: DRO state cloud, national
government DC in Ljubljana plus DR site. Security: **SI-CERT**; URSIV. Procurement: Ministry of
Public Administration. Scrutiny: DZ odbor za gospodarstvo; Računsko sodišče. Compute: EuroHPC
**Vega** (Maribor). Press: Delo, Dnevnik, Finance, RTV SLO; Monitor.

**Hook.** Vega at Maribor already proves power and cooling for large loads at the model's
proposed secondary region — the cheapest credible route to a second site.

## LU Luxembourg
*1.3 MW · EUR 32 m · 2 sites · micro*

Policy owner: **Ministère de la Digitalisation**. Operator: **CTIE** (GovCloud); **LuxConnect**
(state-owned Tier IV); **Clarence** (Proximus + LuxConnect, Google Distributed Cloud
disconnected, 2024). Security: ANSSI Luxembourg; GOVCERT.LU; ILR. Scrutiny: Chambre des Députés
commission de la digitalisation; Cour des comptes. Compute: **MeluXina**. Press: Luxemburger
Wort, Paperjam, Delano, Luxembourg Times.

**Hook.** Luxembourg is both a case and a piece of infrastructure — it **hosts Estonia's Data
Embassy under treaty**, which is the working precedent for every out-of-country reserve the
model proposes. Clarence is also the EU's clearest test of a disconnected hyperscaler stack.

## CY Cyprus
*1.3 MW · EUR 30 m · 2 sites · grid-isolated, micro*

Policy owner: **DMRID** (Deputy Ministry of Research, Innovation and Digital Policy). Operator:
Government Data Centre / G-Cloud with Cyta hosting; RRF hybrid consolidation. Security: **DSA**
(Digital Security Authority). Procurement: Public Procurement Directorate, Treasury. Scrutiny:
House committee on research, innovation and digital policy; Audit Office. Press: Phileleftheros,
Politis, Cyprus Mail, In-Business.

**Hook.** Cyprus is a major East-Med cable hub (2Africa, Cadmos, Tamares, Medusa) on an
electrical island, with the second-highest power price in the set (243 EUR/MWh). Nicosia to
Limassol is 80 km — the island maximum, and below the model's own 50-100 km separation guidance
only by a margin. The federation argument is unavoidable here.

## MT Malta
*1.3 MW · EUR 30 m · 2 sites · grid-isolated, micro*

Policy owner: ministry responsible for the digital economy (MITA's parent). Operator: **MITA** —
government hybrid cloud (MITA DC + Azure); **MDIA**. Security: MITA CIP. Procurement: Department
of Contracts. Scrutiny: House standing committee on economic and financial affairs; NAO. Press:
Times of Malta, MaltaToday, The Shift News.

**Hook.** Malta has no major IXP and transits Sicily and Milan for everything — connectivity
sovereignty fails before capacity sovereignty does. Malta-to-Gozo is the only in-country
separation available, which the model flags as insufficient.

---

## Sequencing

1. **Now** — Tier 0 (CADA is live) plus NL, RO, DK, PT: countries with a programme mid-flight
   where the brief is a calibration input rather than an unsolicited proposal.
2. **Next** — DE, FR, IT, ES, PL: larger, slower, and better approached after at least one
   operator elsewhere has engaged and can be cited.
3. **With the federation write-up** — EE, LV, LT, LU, CY, MT as a group. Do not send these
   individually; the finding is that the national-only model fails for them, and that argument
   only holds as a set. EE and LU are co-authors, not recipients.
4. **Cold, lowest priority** — SE, IE, AT: no binding sovereignty doctrine, so the brief arrives
   without a policy hook to attach to.

## Before any send

- [ ] Verify ministry names and current officeholders — see the provenance table above
- [ ] Confirm committee names against the current legislature
- [ ] Hand-edit DE, FR, IT, ES, PL briefs into full analyses first (`TODO.md`, Write-ups) —
      the generated briefs are scaled from the Dutch baseline and say so, which is fine for a
      calibration request but thin for a ministerial send
- [ ] Resolve the missing `model/export_artifacts.py` if PDFs rather than Markdown are wanted
- [ ] Named individuals and addresses → private `sovereign-data-centers-contacts` repo, never this file
