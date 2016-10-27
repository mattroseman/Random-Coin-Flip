import struct
import time

_random = open("/dev/random", "rb")

def uint32_to_int(bin_num):
    """
    Converts the 32 bit bin_num to an in
    @param: bin_num the 32 bit binary number
    @return: the integer representation of bin_num
    """
    return struct.unpack("I", bin_num)[0]

def main():

    bit_mask = 1 #  00000000 00000000 00000000 00000001
    heads = 0
    tails = 0

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

if __name__ == "__main__":
    main()
