// TimeSplitters 2 on a PS5: the game's Xbox buttons drawn as PlayStation ones. Its menus and prompts draw them from a
// few small textures, the same in every level's file and the front end's: the A, B, X and Y buttons (32x32 each) and
// a sheet with B Y X A, Start, Back and two arrows (128x64). Each is replaced, by the hash the renderer gives its
// contents, with reSplit2's own drawing four times larger (tools/mkbuttons.py, game/art): A Cross, B Circle,
// X Square, Y Triangle, as the DualSense's buttons are mapped; Start is Options and Back the touch pad.
// The Controls menu's picture of the Xbox controller (textures/misc/xbcontroller, 128x128) and the glow behind it
// (xbcontrollerglow, 64x64) are replaced the same way, with reSplit2's own controller.
#include <cstddef>
#include <cstdint>

#include "core/log.h"
#include "gpu/texture_pack.h"

namespace ts2 {

namespace art {  // ts2_button_art.cpp
extern const unsigned char kCross[], kCircle[], kSquare[], kTriangle[], kSheet[], kPad[], kGlow[];
extern const size_t kCrossSize, kCircleSize, kSquareSize, kTriangleSize, kSheetSize, kPadSize, kGlowSize;
}  // namespace art

namespace {

struct Replacement {
    uint64_t hash;  // the renderer's texture pack hash of the game's picture
    uint32_t width, height;
    const unsigned char* png;
    const size_t* size;
    const char* what;
};

const Replacement kButtons[] = {
    {0x2f7b22f67b9c7cf1ull, 32, 32, art::kCross, &art::kCrossSize, "A button (as Cross)"},
    {0xafbc42fefa2fe6ffull, 32, 32, art::kCircle, &art::kCircleSize, "B button (as Circle)"},
    {0x85921cd4ed5dd12dull, 32, 32, art::kSquare, &art::kSquareSize, "X button (as Square)"},
    {0x9211a939afc09ff1ull, 32, 32, art::kTriangle, &art::kTriangleSize, "Y button (as Triangle)"},
    {0x210f1687fc0f7194ull, 128, 64, art::kSheet, &art::kSheetSize, "button sheet"},
    {0x732626c1a3b1308bull, 128, 128, art::kPad, &art::kPadSize, "controller picture"},
    {0x4e824d663a467894ull, 64, 64, art::kGlow, &art::kGlowSize, "controller picture's glow"},
};

bool Buttons(uint64_t hash, uint32_t width, uint32_t height, gpu::pack::Image& out) {
    for (const Replacement& r : kButtons) {
        if (r.hash != hash || r.width != width || r.height != height) continue;
        bool ok = gpu::pack::DecodePng(r.png, *r.size, out);
        LOGI("ts2: the Xbox %s %s", r.what, ok ? "drawn as reSplit2's PlayStation one" : "could not be replaced (PNG)");
        return ok;
    }
    return false;
}

}  // namespace

void PlayStationButtons() { gpu::pack::g_builtin = Buttons; }

}  // namespace ts2
