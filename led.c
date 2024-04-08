#include <linux/init.h>
#include <linux/module.h>
#include <linux/gpio.h>
#include <linux/delay.h>
#define PIN 23

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Robbie Sangster");

static int __init led_on(void) {
    int result = 0;

    // Request GPIO pin
    result = gpio_request(PIN, "LED_PIN");
    if (result < 0) {
        pr_err("LED Module: Failed to request GPIO %d, error %d\n", PIN, result);
        return result;
    }

    // Set GPIO pin as output
    result = gpio_direction_output(PIN, 1); // Initial state: ON
    if (result < 0) {
        pr_err("LED Module: Failed to set GPIO direction, error %d\n", result);
        gpio_free(PIN);
        return result;
    }
    gpio_set_value(PIN, 1);

    msleep(5000);

    gpio_set_value(PIN, 0);

    return 0;
}

static void __exit led_off(void) {

    gpio_free(PIN);
}


module_init(led_on);
module_exit(led_off);
