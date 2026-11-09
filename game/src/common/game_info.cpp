#include "app/app.h"

namespace ts2 {
extern bool g_soft_filter;  // ts2_ps5.cpp
extern bool g_left_trigger_aims;
void PatchText();
void Pad(int port, input::Pad& p);
}  // namespace ts2

// what the runtime asks of the game; strings must be set, hooks may stay null
const app::GameInfo app::kGame = {
    .title = L"TimeSplitters 2",               // window and splash
    .short_title = L"TimeSplitters 2",               // message boxes
    .name = L"TS2",                      // window classes, crash dumps, handover event
    .log = "ts2",                        // log file prefix
    .settings = "settings.toml",          // settings file beside the exe
    .splash = L"splash",                  // optional splash.png or splash.bmp beside the exe
    .missing = L"Put the game in the assets folder: its disc image (.iso), or default.xbe with its folders beside it.",
    .images = {{"default.xbe", "TS2"}},  // each recompiled xbe and its exe, for title launches
    // the game's own settings, in the settings file's [graphics]
    .options = {{"graphics", "soft_filter", cfg::Type::Bool, "Xbox soft filter",
                 "The game softened its picture for the TVs of its day by blending it over itself one pixel off. At "
                 "high resolutions that looks doubled and blurry, so it is off; turn it on for the console's look.",
                 &ts2::g_soft_filter},
                {"input", "left_trigger_aims", cfg::Type::Bool, "Left trigger aims",
                 "L2 aims, as clicking the right stick does, and R2 fires. Clicking the right stick then does what L2 "
                 "did (Alternate Fire, or the left gun of two). Set the game's Controls > Aim Mode to Hold to aim only "
                 "while L2 is held.",
                 &ts2::g_left_trigger_aims}},
    .load = nullptr,                      // reads more from the settings file's toml::table
    .save = nullptr,                      // writes more into it
    .init = nullptr,                      // after the settings load, before the window and boot
    .loaded = ts2::PatchText,             // image in memory, before its entry point runs: the PS5 in its text
    .window = nullptr,                    // the game window is up
    .message = nullptr,                   // window messages first; true takes one
    .ui = nullptr,                        // ImGui drawing each frame
    .pad = ts2::Pad,                      // changes a polled pad: the left trigger aims
    .rumble = nullptr,                    // changes a rumble before it is set
};
