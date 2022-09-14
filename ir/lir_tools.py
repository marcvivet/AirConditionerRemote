# Code prived by AnalysIR Team info@analysir.com
# https://www.analysir.com/blog/ 


def lir_2_raw(sig: str) -> str:
     sig = sig.upper().replace("LIR:", "").strip()
     # signal now in desired format
     parts = sig.split()  # list now contains all of the elements of the signal

     carrier_hz = int(parts[0], 16)
     raw_sig = "Raw (): "

     t = 1  # pointer into parts

     marks = [0] * 15  # init to all 0s
     spaces = [0] * 15  # init to all 0s

     # first build up arrays for mark and space timings
     #
     while (len(parts[t]) == 4):
         idx = int(t/2)

         marks[idx] = int(parts[t], 16)
         spaces[idx] = int(parts[t + 1], 16)
         t = t+2
         # now check if long sigs if value is odd = > add 0x10000. 
         # Longer signal lengths are stored in 16 bit value by making them odd -
         # see syntax docs
         if marks[idx] & 1:  # if odd then add longer value
             marks[idx] += 65536
         if spaces[idx] & 1:
             spaces[idx] += 65536

     # now process individual pulses
     pulse_train = "".join(parts[t:])

     i = 0
     while i < len(pulse_train):
         if pulse_train[i] == "F":  # compress pulses
             if i == len(pulse_train)-1:
                 break  # special case for F in last position - ignore as it is a terminator
             i += 1
             p = int(pulse_train[i], 16)  # pulse to repeat
             i += 1
             cnt = int(pulse_train[i], 16)  # number of times to repeat pulse

             for j in range(0, cnt):
                 raw_sig += str(marks[p]) + " -"
                 raw_sig += str(spaces[p]) + " "

         else:
             p = int(pulse_train[i], 16)  # pulse to repeat
             raw_sig += str(marks[p]) + " -"
             raw_sig += str(spaces[p]) + " "
             #print(marks[int(pulse_train[i], 16)], aspaces[int(pulse_train[i], 16)])
         i += 1

     raw_sig = raw_sig.rstrip(" ")
     idx = raw_sig.rindex(" ")
     raw_sig = raw_sig[:idx]
     return raw_sig  # also strip hte comma and space from end of string
