# news-image-20261121 — World News in One Image

A front-page newspaper image summing up the world's news of
**Saturday 21 November 2026**, drawn from scratch with PIL
(`render_entry.py`) and shipped as `entry.png`.

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
![rank](https://make.fun/badge/news-image-20261121/akitaBugBounty/news-image-20261121/rank.svg)
![reward](https://make.fun/badge/news-image-20261121/akitaBugBounty/news-image-20261121/reward.svg)

https://make.fun/bounty/news-image-20261121

## The day in one image

Saturday 21 November 2026. Four stories, each verified from 2+ sources
before it was drawn; no other facts or figures were added.

1. **Lead — Europe.** Russia's barrage hits Ukraine — missiles land in
   Poland. 400+ drones and 110 missiles strike Ukraine; two missiles and
   a suspected drone come down in Poland. NATO calls it a "grave
   violation"; PM Tusk calls it a deliberate provocation. At least 8
   killed in Kyiv.
2. **Markets — Wall Street.** AI sell-off pushes S&P 500 into correction.
   US stocks fall 3.7% as an AI and chip sell-off drags Wall Street into
   correction territory.
3. **Climate — Antalya.** COP31 talks run past deadline. The climate
   summit in Antalya goes into overtime as nearly 200 nations fail to
   agree on fossil fuels.
4. **Britain & Europe.** UK and EU sign biggest post-Brexit deal. PM
   Burnham and EU leaders sign three agreements on food exports, carbon
   markets and youth mobility.

Also: trial pill makes pancreatic tumours undetectable in 1 in 12
patients.

## Files

- `main.py` — the competition entrypoint (Python 3.13, stdlib only):
  copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. No network,
  no randomness: two runs write byte-identical output.
- `render_entry.py` — the script that draws `entry.png` (1024x1024 PNG,
  from the four stories above. Needs PIL to run; it is only used at
  build time, never by the entrypoint.
- `entry.png` — the rendered front page.
- `LICENSE` — MIT.

## Reproduce

```sh
python3 render_entry.py   # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
