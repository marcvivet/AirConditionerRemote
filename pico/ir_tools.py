from machine import PWM, Pin


def send_ir_code(pin: Pin, code: list, frequency: int):
    pwm = PWM(pin)
    pwm.freq(frequency)

    for element in code:
        if element > 0:           
            pwm.duty_u16((2**16)//3)
        else:
            pwm.duty_u16(0)
            
        utime.sleep_us(abs(element))
               
    pwm.deinit()
    pin.off()
