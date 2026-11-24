# The World in One Day — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/abtravels/news-2026-11-24/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/abtravels/news-2026-11-24/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper front page summing up Tuesday 24 November 2026 in one image,
drawn from scratch in code for the
[news-image-20261124](https://make.fun/bounty/news-image-20261124) bounty on
[make.fun](https://make.fun).

## Stories

1. **Russian jets spark Korea air alert** — Seoul scrambles F-15K fighters as
   Russian warplanes enter the air-defence zone near Ulleung Island; the
   island's warning is lifted five minutes later.
2. **Strike on Zaporizhzhia kills 2, wounds 22** — a Russian overnight attack
   hits homes; two of the wounded are children.
3. **Iran says three tankers hit mines in Hormuz** — Tehran's Revolutionary
   Guards say three oil tankers caught fire after striking naval mines.
4. **Hasina plans return on 16 December** — the ousted Bangladeshi PM, in
   exile since 2024, says she will fly home on Victory Day.
5. **Five directors named for Musk merger talks** — SpaceX and Tesla pick five
   directors to steer talks on combining the two companies.
6. **US blacklists Megaspeed in Nvidia scandal** — Washington bars the
   Singapore chip firm, and Alibaba's Apex unit, from US technology.

Also today: NATO vows to defend space after reports Russia is ready to launch
a nuclear-armed satellite, "Sputnik-S".

## Run it

```sh
node main.ts            # writes entry.png to /output
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) runs `draw.py`, which renders the
1024×1024 front page with Pillow. No network. Two runs write identical bytes.

## License

MIT — see [LICENSE](LICENSE).
