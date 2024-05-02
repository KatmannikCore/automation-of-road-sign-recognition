h_max = 143
w_max = 151
h_min = 29
w_min = 27
l = 18
area_max = h_max * w_max
area_min = h_min * w_min
CF = round( (area_max - area_min) / l, 0)
CS = round( area_max / area_min, 1)
print(f"max: {area_max} min: {area_min} CF: {CF} CS : {CS}")

