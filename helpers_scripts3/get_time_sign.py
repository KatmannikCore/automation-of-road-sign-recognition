number = 38226
frame = round(number / 60, 0)
minute = int(frame / 60)
part_seconds = (frame / 60) - minute
seconds = int(60 * part_seconds)
print(f"Time: {minute}.{seconds}")
