# Lottery Simulator
import random
import time
import sys

LOTTERY_NUMBERS = []
CHOSEN_NUMBERS = []
RESULTS = [ 0, 0, 0, 0, 0, 0, 0]

def chooseTicketNumbers():
    print('Choose your numbers.')
    print('Type "custom" to select personal numbers. Type "lucky dip" to select random numbers. Type "exit" to exit.')
    mode = ''
    while mode == '':
        mode = input().lower()
        if mode == 'custom':
            print('Ok. Type 6 different numbers from 1 to 59, pressing enter after each number.')
            for x in range(1, 7):
                CHOSEN_NUMBERS.append(int(input()))
        elif mode == 'lucky dip':
            print('The computer is choosing random numbers. Please wait...')
            chooseRandomTicketNumbers()
        elif mode == 'exit':
            sys.exit()

def chooseLotteryNumbers():
    x = 1
    while x < 7:
        number = random.randint(1, 59)
        if number not in LOTTERY_NUMBERS:
            LOTTERY_NUMBERS.append(number)
            x = x + 1

def compareNumbers():
    match = 0
    for i in range(6):
        if CHOSEN_NUMBERS[i] in LOTTERY_NUMBERS:
            match = match + 1
    RESULTS[match] = RESULTS[match] + 1

def chooseRandomTicketNumbers():
    i = 1
    while i < 7:
        number = random.randint(1, 59)
        if number not in CHOSEN_NUMBERS:
            CHOSEN_NUMBERS.append(number)
            i = i + 1

chooseTicketNumbers()
t0 = time.time()
for x in range(100000000):
    chooseLotteryNumbers()
    #print(CHOSEN_NUMBERS)
    #print(LOTTERY_NUMBERS)
    compareNumbers()
    LOTTERY_NUMBERS.clear()
print(RESULTS)
print(time.time() - t0, 'seconds to process')
