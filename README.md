# THE WORLD IN ONE DAY — Monday 23 November 2026

A newspaper front-page poster summing up the world's news of
Monday 23 November 2026 in one image, for the make.fun competition
`news-image-20261123` ("Sum up 23 November's world news in one image").

## The image

- Masthead: **THE WORLD IN ONE DAY — MONDAY 23 NOVEMBER 2026**
- Lead story: **CLIMATE TALKS COLLAPSE** — COP31 in Antalya, Türkiye,
  ends with no deal after the EU and about 130 nations reject a draft
  text that says nothing about phasing out fossil fuels.
- Second stories: Ukraine's sea drones sink the Russian corvette
  *Merkury* at Benghazi, Libya; a 7-year-old boy is pulled alive from
  the rubble after a Russian strike flattens a block of flats in Dymer,
  near Kyiv (at least 11 dead).
- 27 more stories in the grid below — 30 stories in all, across every
  region and field: war and diplomacy, climate, markets, US politics,
  technology, disasters, health, science, culture and sport.

## Story list and verification sources

Every story below happened, or was first reported, on 23 November 2026
(in any time zone), and was checked against reporting of that day.

| # | Story | Verified against |
|---|-------|------------------|
| 1 | COP31 climate talks collapse in Antalya, no fossil-fuel deal | CNN / Reuters via Zark News briefing 23 Nov; BBC; One Turn day page 23 Nov |
| 2 | Ukraine sea drones sink Russian corvette Merkury at Benghazi | BBC, France 24, The Guardian via One Turn; Seven Lights 23 Nov |
| 3 | Russian strike on Dymer flats kills at least 11; boy, 7, pulled alive after 14 hours | BBC, AP via One Turn; Zark News briefing 23 Nov |
| 4 | AI sell-off: Nikkei −5.06%, S&P 500 −3.7% | CNBC via One Turn; World News Wire 23 Nov |
| 5 | Democrats clinch 258 House seats, largest majority since 1992 | Associated Press via One Turn and Zark News briefing 23 Nov |
| 6 | Trump "inclined" to resume conflict with Iran if no deal by New Year; Iran vows to counter US blockade | Economic Times via World News Wire; Middle East Eye / CBS via One Turn |
| 7 | Trump signs the Common Cents Act, ending the penny after 232 years | GEORGE / Frequent Business Traveler, 23 Nov 2026 |
| 8 | Delta outage delays 1,600+ flights at Atlanta | FAA via GEORGE, 23 Nov 2026 |
| 9 | Nvidia chief Jensen Huang resigns as CEO amid US probe of chip sales to China | CNBC via One Turn; NYT reporting via GEORGE, 23 Nov |
| 10 | FBI most-wanted cartel fugitive "El Chapo Isidro" captured in Sinaloa | The Guardian via One Turn; GEORGE, 23 Nov |
| 11 | Russian freighter Sparta II hit by a drone in the Gulf of Finland | BBC, Tagesschau, Le Figaro via One Turn |
| 12 | BepiColombo enters orbit around Mercury after an eight-year journey | Japan Times, BBC Science, Phys.org via One Turn |
| 13 | Candy factory fire in Banten, Indonesia, kills 24; dozens missing | The Guardian, Euronews, The Hindu via One Turn; Xinhua |
| 14 | ICE arrest of a father and daughter on a Seattle jet bridge sparks protests | AP, The Guardian via One Turn; Zark News briefing 23 Nov |
| 15 | US Justice Department admits a US citizen was deported to Mexico | The Guardian via One Turn |
| 16 | Belgian airports shut as air-traffic controllers join an anti-austerity strike | Al Jazeera, Yonhap via One Turn; News Media House 23 Nov |
| 17 | European gas prices jump 8.6% on cold forecasts | The Guardian, OilPrice, Meduza via One Turn |
| 18 | Alcaraz beats world No. 1 Zverev 6–2, 7–6 to win his first ATP Finals | ATP Tour, BBC Sport, 23 Nov |
| 19 | Liverpool beat Manchester United 4–0 in Pochettino's debut | BBC Sport, Al Jazeera, 23 Nov |
| 20 | Marc Márquez wins his eighth MotoGP title in Portugal | Al Jazeera, AP via One Turn |
| 21 | Boca Juniors beat Atlético Mineiro 2–0 to win the Copa Sudamericana | Buenos Aires Times via One Turn |
| 22 | Anthropic mathematician posts a claimed proof of the Riemann hypothesis | France 24, BBC Chinese via One Turn |
| 23 | Molly Falco, 58, marks one year living with a pig kidney, a transplant record | New York Times via Zark News briefing 23 Nov |
| 24 | Paramilitary attack kills at least 24 civilians, incl. seven children, in South Sudan | Folha de S.Paulo via One Turn |
| 25 | Drone strikes hit homes and a UN building in Khartoum | Africanews, Japan Times, France 24 via One Turn |
| 26 | Houthis claim attack on a Saudi refinery; Saudi strike on Hodeida kills four | CNBC, Middle East Eye via One Turn |
| 27 | Report: Gaza war left toxic contamination across 99% of Gaza | The Guardian, Al Jazeera via One Turn |
| 28 | Nepal PM Balen Shah visits India; India pledges a 15,000-crore aid package | Euronews, The Hindu via One Turn |
| 29 | Mongolia's parliament approves the president's resignation | Euronews via One Turn |
| 30 | South Korea's education minister resigns over AI-cheating exam chaos | BBC, The Guardian, AFP via One Turn |

## How it works

`render.py` draws `poster.png` (1024×1024) entirely in code:

- a hand-built 5×7 bitmap font (upper/lowercase, digits, punctuation),
  scaled by integer factors so every label is spelled exactly;
- a small vector rasteriser (rectangles, lines, discs, polygons) that
  draws the masthead, the COP31 globe scene, the sinking-warship scene,
  the collapsed-block scene and the story grid;
- a hand-rolled PNG encoder (zlib + CRC chunks, standard library only).

`main.py` copies `poster.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output`). No network, no clock, no randomness — running the
program twice writes identical bytes.

## Run it

```sh
python3 render.py        # regenerates poster.png (deterministic)
python3 main.py          # writes entry.png to /output (or $MAKEFUN_OUTPUT_DIR)
```

## Licence

MIT — see LICENSE.
