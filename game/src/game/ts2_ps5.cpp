// TimeSplitters 2 on a PS5: the console named as a PS5 in the game's own text, and the Xbox's soft filter as a
// setting.
#include <cstdint>
#include <cstring>
#include <string>

#include "core/input.h"
#include "core/log.h"
#include "cpu/x86_context.h"
#include "kernel/kernel.h"
#include "xdk/hle.h"

namespace ts2 {

// [graphics] soft_filter: the console's soft filter, off by default (below)
bool g_soft_filter = false;
// [input] left_trigger_aims: the left trigger and the right stick's click trade places (Pad below)
bool g_left_trigger_aims = true;

// The Xbox game fires with both triggers (the left one is Alternate Fire, or the left gun of two) and aims with a
// click of the right stick. With left_trigger_aims on, the left trigger does what the right stick's click did (Aim:
// held, or a toggle, as the game's Controls > Aim Mode says) and the click does what the left trigger did, so no
// action is lost.
void Pad(int port, input::Pad& p) {
    (void)port;
    if (!g_left_trigger_aims || !p.connected) return;
    constexpr uint16_t kRightThumb = 0x80;
    const bool trigger = p.analog[6] > 40, click = (p.buttons & kRightThumb) != 0;
    p.buttons = trigger ? uint16_t(p.buttons | kRightThumb) : uint16_t(p.buttons & ~kRightThumb);
    p.analog[6] = click ? 255 : 0;
}

namespace {

// The game's text, in every language it carries, sits in .rdata as plain strings (Latin-1). The ones that name the
// console (saving and loading, the save device, the "not enough blocks" message, the controller one) say PS5
// instead; the PS2 version's memory card text, the memory unit and dashboard messages (never shown here: there are no
// memory units) and the debug strings are left alone. Each string is rewritten in place: "PS5" is shorter than
// "Xbox", so it never grows.
constexpr uint32_t kTextFrom = 0x231000, kTextTo = 0x2A0000;

const char* const kLeave[] = {"memory card", "Memory Card", "Memory card", "memory\ncard", "Memory\ncard",
                              "memory unit", "Memory Unit", "carte m\xe9moire", "unidad de memoria", "Dashboard",
                              "Interface", "Interfaz", "interfaccia", "Liaison", "Interconexi\xf3n", "interconexi\xf3n"};

// whole strings said differently (the save device's name)
struct Whole {
    const char* from;
    const char* to;
};
const Whole kWhole[] = {{"Xbox hard disk", "PS5 storage"},
                        {"Disque dur Xbox", "Stockage PS5"},
                        {"Disco rigido Xbox", "Archiviazione PS5"}};

std::string Rewrite(const std::string& s) {
    for (const Whole& w : kWhole)
        if (s == w.from) return w.to;
    for (const char* leave : kLeave)
        if (s.find(leave) != std::string::npos) return s;
    std::string out = s;
    for (size_t at; (at = out.find("Xbox")) != std::string::npos;) out.replace(at, 4, "PS5");
    return out;
}

}  // namespace

void PlayStationButtons();  // ts2_buttons.cpp

void PatchText() {
    PlayStationButtons();
    uint8_t* p = static_cast<uint8_t*>(kernel::HostPtr(kTextFrom));
    const size_t n = kTextTo - kTextFrom;
    int changed = 0;
    for (size_t i = 0; i + 4 <= n; i++) {
        if (std::memcmp(p + i, "Xbox", 4) != 0) continue;
        size_t s = i, e = i;
        while (s > 0 && p[s - 1]) s--;
        while (e < n && p[e]) e++;
        if (e >= n) break;
        std::string old(reinterpret_cast<const char*>(p + s), e - s);
        std::string now = Rewrite(old);
        if (now != old && now.size() <= old.size()) {
            std::memcpy(p + s, now.data(), now.size());
            std::memset(p + s + now.size(), 0, old.size() - now.size());
            changed++;
        }
        i = e;
    }
    LOGI("ts2: %d of the game's strings name the PS5", changed);
}

}  // namespace ts2

// The soft filter: every frame of play the game blends the finished picture over itself shifted by one console pixel
// (down at 25%, then down and right at 20%: 0xC9F40 and 0xCA5A0), softening it for a TV of its day. Drawn at 4K that
// one pixel is four and a half, and the picture looks doubled and blurry, so these two passes are left out unless
// [graphics] soft_filter is on. Larger shifts (the game's own blur effects) still draw.
X86_EXTERN_FUNC(__imp__sub_000C9F40);
X86_FUNC(sub_000C9F40) {  // (passes, shift in pixels, alpha)
    uint32_t passes = kernel::R32(ctx.esp + 4), shift_bits = kernel::R32(ctx.esp + 8);
    float shift;
    std::memcpy(&shift, &shift_bits, 4);
    if (!ts2::g_soft_filter && passes <= 2 && shift > -1.5f && shift < 1.5f) {
        ctx.esp += 4;  // ret (cdecl: the caller drops the arguments)
        return;
    }
    __imp__sub_000C9F40(ctx, base);
}
X86_EXTERN_FUNC(__imp__sub_000CA5A0);
X86_FUNC(sub_000CA5A0) {  // (1: two one-pixel passes, 2: one diagonal pass)
    if (!ts2::g_soft_filter) {
        ctx.esp += 4;  // ret
        return;
    }
    __imp__sub_000CA5A0(ctx, base);
}
