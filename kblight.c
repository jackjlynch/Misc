//quick utility to adjust keyboard backlight brightness on Asus UX32VD
//assumes range 0-3
#include <stdio.h>
#include <fcntl.h>

#define PATH "/sys/class/leds/asus::kbd_backlight/brightness"
#define MAX '3'

int main(int argc, char* argv[]) {
    if(argc < 2) {
        return -1;
    }

    int brightness = open(PATH, O_RDWR);
    if(brightness == -1) {
        return -1;
    }

    char currentLevel = '0';
    read(brightness, &currentLevel, 1);

    printf("%c\n", currentLevel);

    if(argv[1][0] == '+' && currentLevel != MAX) {
        currentLevel += 1;
    }
    else if(argv[1][0] == '-' && currentLevel != '0') {
        currentLevel -= 1;
    }
    else {
         return -1;
    }

    write(brightness, &currentLevel, 1);
    close(brightness);

    return 0;

}
