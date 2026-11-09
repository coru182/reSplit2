// TimeSplitters 2: instruction hooks ([[hook]] entries in config/hooks.toml)
#include <cstdint>

#include "core/log.h"
#include "cpu/x86_context.h"

// XapiInitProcess asks the drive to authenticate the disc (an Xbox drive command; the host has no such drive). Its
// failure path skips setting up the T: and U: drives, so the game couldn't save: continue as on a console.
bool TS2_DiscCheckFailed(X86Context& ctx, uint8_t* base) {
    (void)ctx;
    (void)base;
    LOGI("ts2: no Xbox drive, continuing XAPI startup");
    return true;
}
