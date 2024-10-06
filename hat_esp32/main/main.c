/*
 * SPDX-FileCopyrightText: 2010-2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: CC0-1.0
 */

#include <stdio.h>
#include <inttypes.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_chip_info.h"
#include "esp_flash.h"
#include "esp_system.h"
#include "hat_defines.h"
#include "driver/gpio.h"

// static rgbVal rgbs[HAT_RGB_HEIGHT * HAT_RGB_WIDTH];

static gpio_config_t gpio5_config = {
    .intr_type = GPIO_INTR_DISABLE,
    .mode = GPIO_MODE_OUTPUT,
    .pin_bit_mask = (1 << 5),
    .pull_down_en = true,
    .pull_up_en = false
};

static gpio_config_t gpio6_config = {
    .intr_type = GPIO_INTR_DISABLE,
    .mode = GPIO_MODE_OUTPUT,
    .pin_bit_mask = (1 << 6),
    .pull_down_en = true,
    .pull_up_en = false
};

static gpio_config_t gpio7_config = {
    .intr_type = GPIO_INTR_DISABLE,
    .mode = GPIO_MODE_OUTPUT,
    .pin_bit_mask = (1 << 7),
    .pull_down_en = true,
    .pull_up_en = false
};

static gpio_config_t gpio8_config = {
    .intr_type = GPIO_INTR_DISABLE,
    .mode = GPIO_MODE_OUTPUT,
    .pin_bit_mask = (1 << 8),
    .pull_down_en = true,
    .pull_up_en = false
};

static gpio_config_t gpio9_config = {
    .intr_type = GPIO_INTR_DISABLE,
    .mode = GPIO_MODE_OUTPUT,
    .pin_bit_mask = (1 << 9),
    .pull_down_en = true,
    .pull_up_en = false
};

static gpio_config_t gpio10_config = {
    .intr_type = GPIO_INTR_DISABLE,
    .mode = GPIO_MODE_OUTPUT,
    .pin_bit_mask = (1 << 10),
    .pull_down_en = true,
    .pull_up_en = false
};

static uint32_t gpio_order[] = {5, 6, 7, 8, 10, 9};

/**
 * Takes 1.2s
 */
void spin(void)
{
    for (uint32_t i = 0; i < 6; i++)
    {
        gpio_set_level(gpio_order[i], 1);
        gpio_set_level(gpio_order[(i + 1)%6], 1);
        gpio_set_level(gpio_order[(i + 2)%6], 1);
        
        vTaskDelay(200 / portTICK_PERIOD_MS);
        
        gpio_set_level(gpio_order[i], 0);
        gpio_set_level(gpio_order[(i + 1)%6], 0);
        gpio_set_level(gpio_order[(i + 2)%6], 0);
    }
}

/**
 * Takes 1.2s
 */
void rotate(void)
{
    for (uint32_t i = 0; i < 6; i++)
    {
        gpio_set_level(gpio_order[i], 1);
        gpio_set_level(gpio_order[(i+3)%6], 1);
        vTaskDelay(200 / portTICK_PERIOD_MS);
        gpio_set_level(gpio_order[i], 0);
        gpio_set_level(gpio_order[(i+3)%6], 0);
    }
}

/**
 * Takes 0.4s
 */
void flash(void)
{
    for (uint32_t i = 0; i < 6; i++)
    {
        gpio_set_level(gpio_order[i], 1);
    }
    
    vTaskDelay(200 / portTICK_PERIOD_MS);

    for (uint32_t i = 0; i < 6; i++)
    {
        gpio_set_level(gpio_order[i], 0);
    }

    vTaskDelay(200 / portTICK_PERIOD_MS);
}

/**
 * Takes 0.2s
 */
void flicker(void)
{
    gpio_set_level(gpio_order[0], 1);
    gpio_set_level(gpio_order[1], 0);
    gpio_set_level(gpio_order[2], 1);
    gpio_set_level(gpio_order[3], 0);
    gpio_set_level(gpio_order[4], 1);
    gpio_set_level(gpio_order[5], 0);

    vTaskDelay(100 / portTICK_PERIOD_MS);
    
    gpio_set_level(gpio_order[0], 0);
    gpio_set_level(gpio_order[1], 1);
    gpio_set_level(gpio_order[2], 0);
    gpio_set_level(gpio_order[3], 1);
    gpio_set_level(gpio_order[4], 0);
    gpio_set_level(gpio_order[5], 1);

    vTaskDelay(100 / portTICK_PERIOD_MS);
    
    gpio_set_level(gpio_order[1], 0);
    gpio_set_level(gpio_order[3], 0);
    gpio_set_level(gpio_order[5], 0);
}

void app_main(void)
{
    printf("Hello world!\n");
    fflush(stdout);

    gpio_config(&gpio5_config);
    gpio_config(&gpio6_config);
    gpio_config(&gpio7_config);
    gpio_config(&gpio8_config);
    gpio_config(&gpio9_config);
    gpio_config(&gpio10_config);

    uint32_t level = 0;

    while (true)
    {
        // 3.6s
        for (uint32_t i = 0; i < 3; i++)
            rotate();

        for (uint32_t i = 0; i < 9; i++)
            flash();

        for (uint32_t i = 0; i < 18; i++)
            flicker();

        for (uint32_t i = 0; i < 3; i++)
            spin();
            
        /*
        vTaskDelay(1000 / portTICK_PERIOD_MS);

        level += 1;

        for (uint32_t i = 5; i <= 10; i++)
            gpio_set_level(i, level % 2);*/
    }
}
