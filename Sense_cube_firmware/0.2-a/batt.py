from machine import Pin, ADC


def adc_to_voltage(unscaled):  # Функция перевода значения с АЦП в напряжение
    to_min = 0
    to_max = 2
    from_min = 0
    from_max = 4095
    return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min


batt = ADC(Pin(36))  #
batt.atten(ADC.ATTN_6DB)  # Full range: 2.0v
ADC.width(ADC.WIDTH_12BIT)  # Расширение 4095


def get_bat():
    adc_value = batt.read()  # Получение значения с АЦП
    
    # print(adc_value)
    
    x = adc_to_voltage(adc_value) * 2.92
    k = (-0.0241 * x) + 1.074  # Формула для вычисления коэфицента
    return adc_to_voltage(adc_value) * 2.92 * k


    
    
    
# print(get_bat())
