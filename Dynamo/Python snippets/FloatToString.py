def float_to_str(input_value):
    # Float to string without trailing zeros
    # https://stackoverflow.com/a/37736333
    result = ('%.14f' % input_value).rstrip('0').rstrip('.')
    return '0' if result == '-0' else result


# input number or list of numbers
f = IN[0]

if hasattr(f, '__iter__'):
    s = map(float_to_str, f)
else:
    s = float_to_str(f)

OUT = s
