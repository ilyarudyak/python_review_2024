import time

"""
At a high level, here’s what your program will do:
1. Track the amount of time elapsed between presses of the enter key,
with each key press starting a new “lap” on the timer.
2. Print the lap number, total time, and lap time.

This means your code will need to do the following:
1. Find the current time by calling time.time() and store it as a timestamp
at the start of the program, as well as at the start of each lap.
2. Keep a lap counter and increment it every time the user presses enter.
3. Calculate the elapsed time by subtracting timestamps.
4. Handle the KeyboardInterrupt exception so the user can press ctrl-C
to quit.
"""
def stop_watch():
    # Display the program's instructions.
    print('Press ENTER to begin. Afterwards, press ENTER to "click" the stopwatch. Press Ctrl-C to quit.')

    input() # press Enter to begin
    print('Started.')
    start_time = time.time() # get the first lap's start time
    last_time = start_time
    lap_num = 1

    # Start tracking the lap times.
    try:
        while True:
            input()
            lap_time = round(time.time() - last_time, 2)
            total_time = round(time.time() - start_time, 2)
            print(f'Lap #{lap_num}: {total_time} ({lap_time})', end='')
            lap_num += 1
            last_time = time.time() # reset the last lap time
    except KeyboardInterrupt:
        # Handle the Ctrl-C exception to keep its error message from displaying.
        print('\nDone.')

if __name__ == '__main__':
    stop_watch()
