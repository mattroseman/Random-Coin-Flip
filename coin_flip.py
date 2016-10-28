#!/usr/bin/python3
import os, sys, struct, time, re

log_name = 'log.txt'

_random = open("/dev/random", "rb")

bit_mask = 1 #  00000000 00000000 00000000 00000001
heads = 0
tails = 0

if os.path.exists(log_name):
    log = open(log_name, 'r+')
else:
    print ('{} doesn\'t exist so one is being created'.format(log_name))
    log = open(log_name, 'w')
match = re.search('^heads=(\d+) tails=(\d+)$', log.readline())
if match:
    heads = int(match.group(1))
    tails = int(match.group(2))
else:
    print ('{} was formatted incorrectly'.format(log_name))
log.seek(0)
log.truncate()

def uint32_to_int(bin_num):
    """
    Converts the 32 bit bin_num to an in
    @param: bin_num the 32 bit binary number
    @return: the integer representation of bin_num
    """
    return struct.unpack("I", bin_num)[0]

def main():
    global heads, tails, bit_mask, _random, log_name

    try:
        #  run until user kills process
        while True:
            #  generates 4 bytes or an unsigned int
            rand_bytes = _random.read(4)
            #  converts bytes to integer
            rand_int = uint32_to_int(rand_bytes)
            #  print heads for every 1 bit and tails for every 0 bit
            for i in range(32):

                #   xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx
                #  &00000000 00000000 00000000 00000001
                #  ------------------------------------
                #   00000000 00000000 00000000 0000000x
                masked_int = rand_int & bit_mask
                print ("", end="\r")
                if masked_int == 1:
                    heads += 1
                else:
                    tails += 1
                rand_int = rand_int >> 1
                print ("flips: {} | heads: {} | tails: {} | percent heads: {}".format(heads
                    + tails, heads, tails,
                    heads / (heads + tails)), end="")
                time.sleep(.5)
    except (KeyboardInterrupt, SystemExit):
        print ('\nwriting current score to {}'.format(log_name))
        log.write('heads={} tails={}'.format(heads, tails))
        log.close()
        sys.exit()

if __name__ == "__main__":
    main()
