**TimeSplitters 2 (US Xbox), statically recompiled into a native PS5 app.** A test build.

You need a PS5 that runs homebrew, with ShadowMountPlus and an FTP server, and your own disc image (.iso) of the US
Xbox release.

1. Unzip `PPSA99064-<version>.zip` and copy the `PPSA99064` folder to `/data/homebrew/` over FTP. A "reSplit2" tile
   appears on the home screen after about 30 seconds.
2. Copy your disc image to `/data/ts2/` (for example `/data/ts2/ts2.iso`), or to a `ts2` folder on a USB drive.
3. Start the tile. The first start unpacks the image into `/data/ts2/game/` (a screen shows the progress), then the
   game starts. After that it starts straight away, and you can delete the `.iso`.

Press L3 + R3 at any time for the settings menu. For split screen, sign in more users on the PS5 (guests are enough)
and turn on their controllers. To update, copy the new `PPSA99064` folder over the old one: your saves, settings and
the game's files in `/data/ts2/` are kept.

`README.txt` in the app has the details. No game files are included.

What changed in each version is in [CHANGELOG.md](https://github.com/coru182/reSplit2/blob/main/CHANGELOG.md).
