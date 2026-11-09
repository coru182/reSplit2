# Changelog

## 0.1.0

The first test build: TimeSplitters 2 (US Xbox) statically recompiled into a native PS5 app.

- **The game on the PS5.** The Xbox game's code is recompiled to run natively, drawing through Vulkan (Mesa RADV)
  at up to 4K. Tested so far in a desktop test harness: the title screen, profiles and saves, the menus, Story's
  intro, Siberia's cutscene and gameplay, and the game over screen.
- **Install it as reKing installs.** The first start unpacks your disc image into `/data/ts2/game/` with a progress
  screen; from then on the game starts straight away and the `.iso` can go.
- **Up to four players.** DualSense controllers on every user signed in on the PS5, for split screen.
- **4:3 as on the Xbox.** The game has no widescreen mode, so its picture keeps its shape with side bars.
- **The in-game menu** (L3 + R3): render resolution, V-Sync, frame rate counter, texture filtering, vibration, stick
  deadzone, trigger threshold.

What it took to run the game, for those following along:
- The XDK library calls the game makes (XDK 4721, which the SDK didn't cover) found with Cxbx-Reloaded's
  XbSymbolDatabase and by hand.
- The game draws its 3D with vertex and pixel shader programs set directly, which the runtime now handles.
- The game waits for its music to report "playing" before a cutscene starts, and to stop music it pauses the stream
  and waits: the music stream reports both now (cutscenes no longer freeze on black; no hang after saving).
- The console's default graphics states (the depth test among them) are applied at start: the world no longer draws
  washed out.
- The lens flares are sized by visibility tests: the PS5's Vulkan renderer now counts them with occlusion queries.
- "Please reconnect the controller(s)" and "Unable to save Profile" are gone (controller capabilities, and the save
  drives set up as on a console).

## Thanks to

- Athelas by Shagg, the SDK this port builds on
- XboxXBE-Recomp by TGP482
- reUndr-ps5 by bystritskiy, the model for this port and reKing
- Cxbx-Reloaded's XbSymbolDatabase
- mihawk-99's PS5_Vulkan, PS5_Mesa and PS5_PayloadSDK
