// TimeSplitters 2: instruction hooks ([[hook]] entries in config/hooks.toml)
#include <cstdint>
#include <cstdlib>

#include "core/log.h"
#include "cpu/x86_context.h"
#include "kernel/kernel.h"
#include "xdk/d3d8.h"

// XapiInitProcess asks the drive to authenticate the disc (an Xbox drive command; the host has no such drive). Its
// failure path skips setting up the T: and U: drives, so the game couldn't save: continue as on a console.
bool TS2_DiscCheckFailed(X86Context& ctx, uint8_t* base) {
    (void)ctx;
    (void)base;
    LOGI("ts2: no Xbox drive, continuing XAPI startup");
    return true;
}

// Each frame the game steps its world by the vertical blanks counted since the last frame (0x47C5E8, which its blank
// callback 0x1C89D2 counts), at least once and at most three times. On the Xbox, Swap kept frames to the 60 Hz blanks;
// here a frame drawn sooner (a 120 Hz TV, V-Sync off) still stepped once, so the game ran too fast. At the frame
// timer's read of the count (0x1AE009) the frame waits for the next blank when none has passed since the last one.
// TS2_UNPACED in the environment (the test harness) lets frames run as fast as they come.
void TS2_FramePace(X86Context& ctx, uint8_t* base) {
    (void)ctx;
    (void)base;
    static const bool unpaced = std::getenv("TS2_UNPACED") != nullptr;
    if (unpaced) return;
    constexpr uint32_t kBlankCount = 0x47C5E8;
    static uint32_t last = 0;
    for (int i = 0; i < 5 && kernel::R32(kBlankCount) == last; i++) d3d::WaitVBlank(20);
    last = kernel::R32(kBlankCount);
}
