from cffi import FFI

ffi = FFI()

ffi.cdef('''
    #include <wiringPi.h>
''')

c_libs = ffi.dlopen(None)

c_libs.wiringPiSetupGpio
