""" Program 7-5: Data logging of the reading from the LM34 temperature sensor.
"""

from machine import ADC, Pin, RTC, Timer

LM34 = ADC(Pin(27))   # instantiate an ADC object using GP27 pin.
rtc = RTC()           # instantiate the RTC

fh = open('log.txt', 'w')      # open the log file for write

def get_temp():
    """Function to read the LM34 and convert to temperature"""
    value = LM34.read_u16()    # read a conversion result
    
    mV = (value  / 65520) * 3.3  # convert to millivolts
    return mV * 100             # LM34 has the output of 10mV per degree F

# rtc_data[0] is the year (e.g., 2022),
# rtc_data[1] is the month (e.g., 2),
# rtc_data[2] is the day (e.g., 3),
# rtc_data[4] is the hour (e.g., 15),
# rtc_data[5] is the minute (e.g., 30),
# rtc_data[6] is the second (e.g., 0).

def log_an_entry(_):
    """Timer callback function"""
    temp = get_temp()           # take a temperature reading
    tm = rtc.datetime()        # take a timestamp
#   logline = '{:2d}:{:02d},{:3.1f}\n'.format(tm[4], tm[5], temp) # v1.16 or earlier
    logline = f'{tm[4]:2d}:{tm[5]:02d},{temp:3.1f}\n'             # v1.17 or later
    print(logline)             # print an entry
    fh.write(logline)          # write the entry to the log file

# Start a periodic timer to log an entry every minute
tmr = Timer(period = 6000, mode = Timer.PERIODIC, callback = log_an_entry)

halt = input('Hit any key to stop logging.\n')
tmr.deinit()   # stop the timer
fh.close()     # close the log file
print('Data logging terminated')
