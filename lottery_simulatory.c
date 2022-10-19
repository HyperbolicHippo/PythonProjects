// simulates MANY random lottery draws and outputs the results
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NUMBER_OF_NUMBERS 6
#define MAX_NUMBER 59
#define MIN_NUMBER 1

int contains_number(const int numbersArray[NUMBER_OF_NUMBERS], const int target) {
    for (int i = 0; i < NUMBER_OF_NUMBERS; i++) {
        if (numbersArray[i] == target) {
            return 1;
        }
    }
    return 0;
}

void choose_random_numbers(int ticketNumbersArray[NUMBER_OF_NUMBERS]) {
    // fill the given array with random, unique ticket numbers
    int arrayFilled = 0;
    int index = 0;
    while (!arrayFilled) {
        int number = rand() % MAX_NUMBER + MIN_NUMBER;
        if (contains_number(ticketNumbersArray, number)) continue;
        ticketNumbersArray[index] = number;
        if ((index++) == 6) arrayFilled = 1;
    }
}

void display_numbers_array(int array[], int length) {
    // displays the numbers array in a nice, formatted way
    printf("[ ");
    for (int i = 0; i < length; i++) {
        printf("%d, ", array[i]);
    }
    printf("]\n");
}

void compare_numbers(const int ticketNumbers[NUMBER_OF_NUMBERS], const int lotteryNumbers[NUMBER_OF_NUMBERS], int results[NUMBER_OF_NUMBERS + 1]) {
    // compare the ticket with the actual numbers, then update the results array accordingly
    int match = 0;
    for (int i = 0; i < NUMBER_OF_NUMBERS; i++) {
        if (contains_number(lotteryNumbers, ticketNumbers[i]))
            match++;
    }
    results[match]++;
}

int main(void) {
    int ticketNumbers[NUMBER_OF_NUMBERS] = {0, 0, 0, 0, 0, 0};
    int lotteryNumbers[NUMBER_OF_NUMBERS] = {0, 0, 0, 0, 0, 0};
    int results[NUMBER_OF_NUMBERS + 1] = {0, 0, 0, 0, 0, 0, 0};

    srand(time((void*)0));
    
    choose_random_numbers(ticketNumbers);
    for (int i = 0; i < 100000000; i++) {
        choose_random_numbers(lotteryNumbers);

        compare_numbers(ticketNumbers, lotteryNumbers, results);
    }
    display_numbers_array(results, NUMBER_OF_NUMBERS + 1);
    
    return 0;
}
