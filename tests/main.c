#include<stdio.h>
#include<stdlib.h>

int main(int argc, char *argv[]) {
    char buff[5];
    int num;

    if (argc != 2) {
        printf("Usage: program_name <num>\n");
        return 1;
    }

    num = atoi(argv[1]);

    for(int i = 0; i < 10; i++) {
        buff[i] = 'A';
    }

    if (num == 120) {
        printf("The number matched! Congrats!\n");
    } else {
        printf("Wrong Number!\n");
    }

    return 0;
}
