/* reSplit2: unpacks an Xbox disc image (XDVDFS) on the console (from reUndr-ps5's disc_image.h, MIT, bystritskiy). */
#ifndef TS2_DISC_IMAGE_H
#define TS2_DISC_IMAGE_H
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

enum {
    TS2_IMAGE_OK,
    TS2_IMAGE_NOT_A_DISC,
    TS2_IMAGE_WRONG_DISC,
    TS2_IMAGE_DAMAGED,
    TS2_IMAGE_WRITE /* the folder could not be written: most often, no room */
};

/* Copies the disc into target. accept sees default.xbe before anything else is copied and may refuse it (0);
 * progress gets 0 once the size of the game (total bytes) is known, then each new percentage. */
int ts2_image_extract(const char *image, const char *target, int (*accept)(const char *xbe),
                       void (*progress)(unsigned percent, uint64_t total));

#ifdef __cplusplus
}
#endif
#endif
