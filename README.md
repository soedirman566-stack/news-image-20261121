[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/soedirman566-stack/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/soedirman566-stack/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The Daily Globe — Saturday, 21 November 2026

One image, one front page: `entry.png` is a 1024×1024 broadsheet front page that sums up the world news of Saturday 21 November 2026 at a glance. A huge date bar anchors the day; below it, a dominant lead story with a large real photograph, and three secondary stories, each with its own photograph and a short factual blurb.

**The day's stories:**

- **Lead — Russian missiles fall on Poland.** Two Russian missiles and a suspected drone came down on Polish soil in the early hours; Warsaw called it a deliberate provocation and NATO a grave violation of allied airspace, while the same barrage struck three bridges in Kyiv. Photo: the Paton Bridge over the Dnipro in Kyiv.
- **World Court: Myanmar committed genocide.** The International Court of Justice in The Hague ruled 9–6 that Myanmar's security forces committed genocide against the Rohingya in northern Rakhine. Photo: the Peace Palace.
- **Trump, Xi, Putin hold first summit.** The three leaders met in Shenzhen for a first trilateral summit, with Trump urging closer security cooperation; the talks ended with few concrete results. Photo: the Ping An Finance Centre, Shenzhen.
- **Wall Street slides into correction.** The S&P 500 and the Dow entered correction territory on Friday as plunging AI and chip shares dragged US stocks down about 3.7 percent. Photo: the New York Stock Exchange.

The page is composed by `compose.py` (Python + Pillow) from real photographs only — no AI-generated or stock-watermarked images. Text is sized with adaptive shrink-to-fit ladders, and the build is deterministic: running the composer twice yields a byte-identical `entry.png`.

## Run it

```
node main.ts
```

This copies the committed `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (the output directory defaults to `output/` when the variable is not set). To rebuild the page from its sources instead, run `python3 compose.py`.

## Photo credits

All photographs come from Wikimedia Commons under free licenses; full credits with authors, licenses and source pages are in [credits.txt](credits.txt) and in the footer of the page itself.

## Bounty

Built for the [news-image-20261121 bounty on make.fun](https://make.fun/bounty/news-image-20261121).

## License

MIT — see [LICENSE](LICENSE).
