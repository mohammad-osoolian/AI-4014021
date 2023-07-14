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
# open legs when falling

# def f2(s,a):
#     return 10*s[VX]*(-1)*s[HALLA]*(1-s[LEG1GC])*a[HIP1]
# def f3(s,a):
#     return 10*s[VX]*(-1)*s[HALLA]*(1-s[LEG2GC])*a[HIP2]

# def f2(s, a):
#     return a[KNEE2] * (s[HIPJ2A])

# def f3(s, a):
#     return a[KNEE1] * (s[HIPJ1A])

# def f2(s,a):
#     return s[LEG1GC]*a[KNEE2]
# def f3(s,a):
#     return s[LEG2GC]*a[KNEE1]

# def f4(s,a):
#     return s[HIPJ1A]*a[KNEE1]
# def f5(s,a):
#     return s[HIPJ2A]*a[KNEE2]
# front leg should have close knee and back leg sould have open knee

def f4(s,a):
    return s[VX]*(1-s[LEG1GC])*a[HIP1]
def f5(s,a):
    return s[VX]*(1-s[LEG2GC])*a[HIP2]

feature_list = [f1,f2,f3, f4, f5]