reSplit2 0.1.6 - TimeSplitters 2 (US Xbox), recompiled for the PS5
==================================================================

A test build. An unofficial fan port: the original Xbox game's code, statically recompiled into a native PS5 app.
Not an emulator. No game files are included: it plays your own copy of the US (NTSC-U) Xbox disc.

What you need
-------------
- A PS5 that runs homebrew, with ShadowMountPlus (it registers apps in /data/homebrew) and an FTP server.
- Your own disc image (.iso) of TimeSplitters 2, US Xbox release. A full dump and a trimmed one both work.
- Room on the console for the game's files (about as much as a trimmed disc image), and for the disc image itself
  until the first start has unpacked it (or put the image on a USB drive).

Install
-------
1. Unzip PPSA99064-<version>.zip on your computer. You get a folder named PPSA99064.
2. Over FTP, copy the whole PPSA99064 folder to /data/homebrew/ on the PS5.
   ShadowMountPlus adds a "reSplit2" tile to the home screen (give it about 30 seconds).
3. Over FTP, create the folder /data/ts2/ and copy your disc image into it, e.g. /data/ts2/ts2.iso.
   Or put it on a USB drive, in a folder named ts2 or at the top of the drive.
4. Start the reSplit2 tile. The first start unpacks the disc image into /data/ts2/game/ (a screen shows how far it
   is; it takes a few minutes, longer from a USB drive), then the game starts. From then on the game starts from
   that folder straight away, and you can delete the .iso.

Already have the disc's files (default.xbe and the data and music folders)? Copy them to /data/ts2/game/ instead of
an .iso, or to ts2/game/ on a USB drive. If there isn't room to unpack the image, the game reads the .iso directly (a
notification says so) and you keep the .iso there.

If something is wrong, a screen says what (game not found, a damaged image, another game or another release of it);
press Cross to close it.

To update, copy the new PPSA99064 folder over the old one. Your saves, settings and the game's files in /data/ts2/
are kept.

Play
----
Start the reSplit2 tile. Player 1 is the user who started it. For split screen (up to four players), sign in more
users on the PS5 (guests are enough) and turn on their controllers.

  Xbox            DualSense
  A B X Y         Cross Circle Square Triangle
  Black / White   R1 / L1
  Right trigger   R2 (fire)
  Left trigger    R3 (Alternate Fire, the left gun of two)
  Right stick     L2 (aim)
    click
  Start / Back    Options / touchpad click
  Left stick      L3
    click

L2 aims and R2 fires. On the Xbox both triggers fired and a click of the right stick aimed; L2 and the click trade
places, so nothing is lost. For aiming only while L2 is held, set the game's Controls > Aim Mode to Hold. The
settings menu's "Left trigger aims" (Controls page) turns this off, for the Xbox layout.

The menus and prompts show PlayStation buttons: Cross for the Xbox's A, Circle for B, Square for X, Triangle for Y.
The Controls menu shows a PlayStation controller and names its buttons as the DualSense's (L1, R2, L3...). With
"Left trigger aims" on, the line for the Xbox's left trigger says R3 and the one for the right stick's click says L2.

The game has no widescreen mode on the Xbox, so it keeps its 4:3 picture with bars at the sides.

In-game menu
------------
Press L3 + R3 (both sticks in) at any time. The game stands still behind it. Move with the d-pad or left stick,
Cross to choose, L1 / R1 to change page, and Circle, Options or L3 + R3 to go back to the game.

  Picture   render resolution (1080p, 1620p, 4K), V-Sync, frame rate counter, texture filtering (16x by default)
            and sharpness, smooth menus and HUD, the Xbox soft filter (off by default: the game softened its picture
            for old TVs, which looks blurry at 4K)
  Controls  left trigger aims, vibration, stick deadzone, trigger threshold

Changes apply at once and are saved when you close the menu.

Your files
----------
Everything the app writes is in /data/ts2/:
  game/          the game's files, unpacked by the first start
  hdd/           your saves (the Xbox's hard disk)
  settings.toml  the menu's settings (you can edit it over FTP too)
  logs/          only when /data/ts2/logging-on exists (see below)

Reporting a problem
-------------------
Create an empty file /data/ts2/logging-on over FTP, start the game and do what goes wrong, then send the files in
/data/ts2/logs/. Delete logging-on afterwards: without it nothing is logged, which keeps the game smooth.

Credits and licences: licenses/NOTICE.txt.
