# reSplit2

**TimeSplitters 2, the original Xbox version, statically recompiled into a native app for homebrew-enabled PS5
consoles.**

> [!IMPORTANT]
> **Bring your own game.** The app is the game's program recompiled for the PS5. It contains none of the game's
> files: the graphics, sound, music and levels come from your own disc image of the US Xbox release. Please don't ask
> for or share disc images here.

> [!CAUTION]
> **We do not support piracy.** Please don't use this project with pirated copies of the game.

> [!NOTE]
> **Early test builds.** 0.1.x builds are for testing on real consoles. Expect rough edges, and please report what
> you find.

## What it is

The Xbox game's code is translated into C++ ahead of time and compiled for the PS5, as
[reUndr](https://github.com/bystritskiy/reUndr-ps5) does for Need for Speed: Underground and
[reKing](https://github.com/coru182/reKing) for The Return of the King. It's not an emulator: a replacement runtime
handles the console's graphics (Direct3D 8 on Vulkan, through Mesa's RADV), sound, input and system services.

- Rendered at 1080p, 1620p or 4K, output at 3840x2160, at the game's own 60 fps. The game has no widescreen mode on
  the Xbox, so the picture stays 4:3 with bars at the sides.
- DualSense controllers, up to four players in split screen (sign in more users on the PS5; guests are enough).
- An in-game menu on L3 + R3: render resolution, V-Sync, frame rate counter, texture filtering, vibration, stick
  deadzone and trigger threshold.
- The first start unpacks your disc image, then the game starts straight away from then on.

## Requirements

- A PS5 that runs homebrew, with [ShadowMountPlus](https://github.com/drakmor/ShadowMountPlus) (it registers apps in
  `/data/homebrew`) and an FTP server.
- Your own disc image (`.iso`) of **TimeSplitters 2, US Xbox release**. A full or trimmed dump.

## Install

1. Download `PPSA99064-<version>.zip` from [Releases](../../releases) and unzip it on your computer. You get a folder
   named `PPSA99064`.
2. Over FTP, copy the whole `PPSA99064` folder to `/data/homebrew/` on the PS5. ShadowMountPlus adds a **reSplit2**
   tile to the home screen (give it about 30 seconds).
3. Over FTP, create `/data/ts2/` and copy your disc image into it, e.g. `/data/ts2/ts2.iso`. Or put it on a USB
   drive, in a folder named `ts2` or at the top of the drive.
4. Start the **reSplit2** tile. The first start unpacks the disc image into `/data/ts2/game/` (a screen shows how far
   it is), then the game starts. From then on it starts straight away, and you can delete the `.iso`.

Already have the disc's files (`default.xbe` and the `data` and `music` folders)? Copy them to `/data/ts2/game/`
instead. To update, copy the new `PPSA99064` folder over the old one; your saves and settings in `/data/ts2/` stay.

## Controls

| Xbox | DualSense |
| --- | --- |
| A B X Y | Cross Circle Square Triangle |
| Black / White | R1 / L1 |
| Triggers | R2 / L2 |
| Start / Back | Options / touchpad click |
| Stick clicks | L3 / R3 |
| In-game menu | L3 + R3 together |

## Your files

Everything the app writes is in `/data/ts2/`: `game/` (the unpacked disc), `hdd/` (your saves), `settings.toml` (the
menu's settings, editable over FTP) and `logs/`.

## Reporting a problem

Create an empty file `/data/ts2/logging-on`, start the game and do what goes wrong, then attach the files from
`/data/ts2/logs/` to an issue. Delete `logging-on` afterwards: without it nothing is logged, which keeps the game
smooth.

## For developers

Releases are built once, by the maintainer, from their own copy of the game; players only need their disc image.
To build it yourself (Linux, with clang 18, cmake, ninja, python3, zip; Docker the first time for the PS5
toolchain):

```sh
./setup.sh /path/to/default.xbe     # from your own TimeSplitters 2 disc (US Xbox)
./build-ps5.sh                      # build-ps5/PPSA99064-<version>.zip
```

- `game/`: the port's own files over Athelas's game template: `config/game.toml` (the recompiler's input: the
  library functions the runtime replaces, at their TimeSplitters 2 addresses) and the game's hooks.
- `patches/athelas-ps5.patch`: the PS5's changes to the SDK (from reKing). `patches/ts2-sdk.patch`: TimeSplitters 2's
  (XDK 4721's layout, the direct vertex and pixel shader programs, the music stream's status, buffer pausing,
  `XInputGetCapabilities`, Vulkan occlusion queries for the lens flares' visibility tests).
- `ps5/`: the PS5 host (from reKing): entry, first-start unpacking, DualSense input, audio, the in-game menu.

## Credits

- [Athelas](https://github.com/Shagg88/Athelas) by Shagg: the SDK, runtime and renderers this builds on (MIT).
- [XboxXBE-Recomp](https://github.com/TGP482/XboxXBE-Recomp) by TGP482: the static recompiler and runtime (MIT).
- [reUndr-ps5](https://github.com/bystritskiy/reUndr-ps5) by bystritskiy: the PS5 host's model, the first-start
  unpacking and its screen (MIT), and the PS5 toolchain recipe.
- mihawk-99's PS5_Vulkan, PS5_Mesa and PS5_PayloadSDK; Mesa's RADV; Dear ImGui; toml++; glslang; stb.
- [Cxbx-Reloaded's XbSymbolDatabase](https://github.com/Cxbx-Reloaded/XbSymbolDatabase), used to find the XDK
  library functions in the game.

## Licence

reSplit2's own code is GPL-3.0 (`LICENSE`). See `package/licenses/NOTICE.txt` for everything the app contains and
its terms.

## Legal

An unofficial fan project, not affiliated with or endorsed by Free Radical Design, Deep Silver, Plaion, Eidos,
Microsoft or Sony Interactive Entertainment. TimeSplitters is a trademark of its owner. No game files are included.
