# s observations
HALLA   = 0
HALLAV  = 1
VX      = 2
VY      = 3
HIPJ1A  = 4
HIPJ1S  = 5
KNEEJ1A = 6
KNEEJ1S = 7
LEG1GC  = 8
HIPJ2A  = 9
HIPJ2S  = 10
KNEEJ1A = 11
KNEEJ2S = 12
LEG2GC  = 13

# a space
HIP1    = 0
KNEE1   = 1
HIP2    = 2
KNEE2   = 3


def f1(s, a):
    return abs(a[HIP1] - a[HIP2])*s[VY]

    
feature_list = [f1]