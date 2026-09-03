# EU-27 sovereign data center capacity - summary

Generated 2026-09-01 by `model/generate_countries.py`. All figures are scaled working assumptions derived from the Dutch reference case; see each country's `GOAL.md`.

| ISO | Country | Pop (m) | Servers | Racks | IT MW | Design MW | Sites | CAPEX (EUR m) | OPEX (EUR m/yr) | Power price | Flags |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| DE | Germany | 83.6 | 24,531 | 767 | 40.2 | 60.4 | 6 | 1,435 | 164 | 226 |  |
| FR | France | 68.6 | 18,833 | 589 | 30.6 | 45.9 | 4 | 1,086 | 100 | 153 |  |
| IT | Italy | 58.9 | 14,774 | 462 | 24.1 | 36.1 | 4 | 857 | 97 | 220 | seismic |
| ES | Spain | 49.1 | 12,517 | 391 | 20.1 | 30.2 | 4 | 711 | 61 | 132 | grid-isolated |
| PL | Poland | 36.5 | 10,231 | 320 | 16.5 | 24.7 | 4 | 578 | 61 | 192 | frontline |
| NL | Netherlands | 18.0 | 5,691 | 178 | 9.4 | 14.2 | 3 | 339 | 36 | 199 |  |
| RO | Romania | 19.0 | 4,894 | 153 | 7.9 | 11.9 | 4 | 278 | 29 | 189 | frontline, seismic |
| BE | Belgium | 11.9 | 3,528 | 110 | 5.8 | 8.7 | 3 | 207 | 21 | 187 |  |
| SE | Sweden | 10.6 | 3,212 | 100 | 5.3 | 7.9 | 3 | 189 | 14 | 97 |  |
| AT | Austria | 9.2 | 2,739 | 86 | 4.5 | 6.8 | 3 | 161 | 17 | 199 |  |
| CZ | Czechia | 10.4 | 2,692 | 84 | 4.3 | 6.5 | 3 | 152 | 15 | 182 |  |
| PT | Portugal | 10.8 | 2,685 | 84 | 4.3 | 6.4 | 3 | 150 | 13 | 133 | grid-isolated, seismic |
| EL | Greece | 10.6 | 2,573 | 80 | 4.1 | 6.1 | 3 | 142 | 14 | 174 | seismic |
| HU | Hungary | 9.5 | 2,415 | 75 | 3.8 | 5.7 | 3 | 132 | 15 | 213 |  |
| IE | Ireland | 5.4 | 2,024 | 63 | 3.5 | 5.3 | 3 | 131 | 16 | 255 | grid-isolated |
| DK | Denmark | 6.0 | 1,861 | 58 | 3.2 | 4.7 | 3 | 114 | 9 | 122 |  |
| FI | Finland | 5.6 | 1,717 | 54 | 2.9 | 4.3 | 3 | 104 | 7 | 75 | frontline |
| BG | Bulgaria | 6.4 | 1,749 | 55 | 2.8 | 4.2 | 3 | 98 | 9 | 141 | frontline, seismic |
| SK | Slovakia | 5.4 | 1,375 | 43 | 2.2 | 3.3 | 3 | 76 | 8 | 209 |  |
| HR | Croatia | 3.9 | 930 | 29 | 1.5 | 2.2 | 3 | 52 | 5 | 155 | seismic |
| LT | Lithuania | 2.9 | 836 | 26 | 1.4 | 2.1 | 3 | 49 | 5 | 159 | frontline |
| LV | Latvia | 1.9 | 608 | 19 | 1.0 | 1.5 | 3 | 36 | 3 | 136 | frontline |
| EE | Estonia | 1.4 | 574 | 18 | 1.0 | 1.4 | 3 | 35 | 3 | 141 | frontline |
| SI | Slovenia | 2.1 | 570 | 18 | 0.9 | 1.4 | 3 | 34 | 3 | 150 |  |
| LU | Luxembourg | 0.7 | 526 | 16 | 0.9 | 1.3 | 2 | 32 | 3 | 172 | micro |
| CY | Cyprus | 1.4 | 502 | 16 | 0.8 | 1.3 | 2 | 30 | 4 | 243 | grid-isolated, micro |
| MT | Malta | 0.6 | 502 | 16 | 0.8 | 1.3 | 2 | 30 | 3 | 135 | grid-isolated, micro |
| | **EU-27 total** | | **125,089** | | | **306** | **86** | **7,236** | **735** | | |

Flags: *frontline* = land border with Russia/Belarus or Black Sea war exposure (defense/security workloads scaled up, hardened site posture); *grid-isolated* = electrical island or near-island; *seismic* = high seismic risk at the capital region; *micro* = two in-country sites only.

Machine-readable: `model/eu27_results.csv`.
