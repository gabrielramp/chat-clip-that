#ifndef HAT_DEFINES_H
#define HAT_DEFINES_H

#define HAT_RGB_GPIO    16  
#define HAT_RGB_WIDTH   16
#define HAT_RGB_HEIGHT  16
#define HAT_RGB_SIZE    3
#define HAT_RMT_BUF_SIZE HAT_RGB_WIDTH * HAT_RGB_HEIGHT * HAT_RGB_SIZE

#define HAT_DIVIDER 1

#define T0H_ns 400
#define T0L_ns 850
#define T1H_ns 800
#define T1L_ns 450

#define T0H_duration ((uint16_t) (T0H_ns / 12))
#define T0L_duration ((uint16_t) (T0L_ns / 12))
#define T1H_duration ((uint16_t) (T1H_ns / 12))
#define T1L_duration ((uint16_t) (T1L_ns / 12))

#endif