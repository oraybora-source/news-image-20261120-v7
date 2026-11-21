# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/oraybora-source/news-image-20261120-v6/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/oraybora-source/news-image-20261120-v6/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday 20 November 2026: a giant date masthead, three big illustrated heroes (Cyclone Akvan's landfall in India, missiles over Kyiv, COP31's final day), 10 illustrated story cards and 18 more briefs across seven regions — 31 stories in all. A numbered world map sits beside the heroes; every story on the page happened, or was first reported, on Friday 20 November 2026, and the DATE CHECK band names 12 stories from 17–19 November that were left out on purpose, plus two things that had not happened yet.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## How the image was made

`compose_v4.py` composes `entry.png` (1024×1024) from text rendered from verified news strings (see `STORIES.md`, research cutoff 21 Nov 2026) plus flat vector-style illustrations drawn in code — no copied artwork, no photos, no text inside the illustrations except the labels the design itself draws; every word on the page is drawn by `compose_v4.py`. The frame is sketch 7 "newspaper" (Kevin's pick): serif masthead, five-item deck, six-number strip, seven-segment region bar, three heroes with a tall numbered world map beside them, 10 cards in two rows of five, 18 briefs, DATE CHECK and sources. `main.py` (Python 3.13, standard library only) copies `entry.png` to the output directory; it runs twice in grading and writes identical bytes both times.

---

<sub>Entered on [make.fun](https://make.fun/?ref=s4486c7v&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
