# Changelog

## 0.1.5

- **A PlayStation controller in the Controls menu.** The picture of the Xbox controller beside the button layout,
  and the glow behind it, are a PlayStation-style controller: reSplit2's own drawing, eight times sharper, in the
  menus' dark blue.
- **The DualSense's names.** The layout names the buttons as the DualSense's, with the PS2 version's names: L1 and R1
  for White and Black, R2 for the right trigger, L3 and R3 for the stick clicks, "Left stick" and "Right stick". With
  **Left trigger aims** on, the left trigger's line says R3 and the right stick click's says L2, as they are swapped;
  turning the setting off names them back at once. MapMaker's help says the same.

## 0.1.4

- **PlayStation buttons.** The menus' and prompts' Xbox buttons are drawn as PlayStation ones, four times sharper:
  A is Cross, B Circle, X Square and Y Triangle, as the DualSense's buttons are mapped ("Select", "Back", "Add",
  "Cancel"...). The game's button sheet gets Options and the touch pad for Start and Back. They are reSplit2's own
  drawings (`game/art`, `tools/mkbuttons.py`).

## 0.1.3

- **L2 aims, R2 fires.** The Xbox game fired with both triggers (the left one is Alternate Fire, or the left gun of
  two) and aimed with a click of the right stick. Now L2 aims and R2 fires; clicking the right stick does what L2
  did, so nothing is lost. Set the game's own **Controls > Aim Mode** to **Hold** to aim only while L2 is held. The
  settings menu's **Left trigger aims** (Controls page) turns it off, for the Xbox layout.

## 0.1.2

- **The right speed.** The game steps its world once for each of the console's 60 Hz vertical blanks since its last
  frame, and at least once a frame. On a 120 Hz TV (or with V-Sync off) the PS5 drew more than 60 frames a second, so
  everything moved too fast. Each frame now waits for the next blank, as the Xbox's display kept it: 60 fps at the
  game's own speed on any TV.

## 0.1.1

- **A sharp picture.** Every frame of play, the game blended its finished picture over itself one console pixel
  off, softening it for the TVs of its day. At 4K that pixel is four and a half, so edges looked doubled and blurry.
  Those two passes are now left out; the menu's new **Xbox soft filter** brings them back for the console's look.
  The game's own effects (motion blur when turning, damage and stun effects) are unchanged.
- **16x texture filtering by default.** Floors and walls seen at an angle, like the tunnel at the start of Siberia,
  stay sharp. Settings files from 0.1.0 are turned up once; after that the menu's choice stands.
- **PS5 in the game's text.** "Please don't turn off your Xbox console" and the save device's "Xbox hard disk" now say
  PS5 ("PS5 storage"), in every language the game carries.

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
