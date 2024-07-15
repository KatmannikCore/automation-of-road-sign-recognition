import matplotlib.pyplot as plt
name_one = "krug"
name_two = "3.24"

w =  [31, 33, 37, 33, 35, 33, 38]
h = [38, 43, 44, 48, 54, 61, 71]
x =  [1468, 1533, 1571, 1611, 1655, 1816, 1879]
y =  [483, 461, 450, 436, 421, 374, 354]

w1 = [36, 38, 44, 44, 40, 47, 43, 44]
h1 = [46, 49, 54, 59, 55, 64, 59, 52]
x1 = [1654, 1737, 1756, 1779, 1804, 1826, 1853, 1876]
y1 =  [528, 523, 518, 513, 518, 505, 500, 496]


def split_array( arr):
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    return left, right

max_w = max(w)
max_h = max(h)
min_w = min(w)
min_h = min(h)
names_signs_for_side = ["parkovka", "ostanovka i parkovka zapreshena", "krug", "red", "tupik", "zhilaya zona",
                        "red"]
CS = (max_w * max_h) / (min_h * min_w)
proportions = [w[index] / h[index] for index in range(len(h))]
left_half, right_half = split_array(proportions)

different_left = abs(min(left_half) - max(left_half))
different_right = abs(min(right_half) - max(right_half))
average = sum(proportions) / len(proportions)

#TODO or CS < 2 странная заглушка
bol = (CS < 10 and \
      (max_w * max_h) < 20500 and \
      x[0] > 1000 and \
      len(w) >= 4 and \
      name_one in names_signs_for_side and \
      (round( different_left,1) > round( different_right,1) and abs(different_right-different_left) > 0.7  or \
      (average < 0.75 and abs(different_right-different_left + abs(average-0.75)) > 1.5))) or CS < 2

# print(new_arr)
#plt.figure(figsize=(12, 7))

print( f'CS:{CS}\n'
       f' x:{x[0]}\n '
       f'len:{len(w)} \n '
       f'{round(different_left, 1)} > {round(different_right, 1)} {round( different_left,2) > round( different_right,2) or average < 0.7}\n '
       f'average:{average}\n'
       f'{average < 0.75 and abs(different_right - different_left + abs(average - 0.75)) > 1.5} dr: {different_right} dl: {different_left} dr-dl: {different_right - different_left} res: {abs(different_right - different_left + abs(average - 0.75))}\n'
       f'bol: {bol}')
#plt.show()

