grouped_names = {'седлішча': {'accuracy': 6.923076923076923, 'count': 8}, 'седча': {'accuracy': 9.0, 'count': 8}, 'сетча': {'accuracy': 7.199999999999999, 'count': 8}}


min_accuracy_key = max(grouped_names, key=lambda x: grouped_names[x]['accuracy'])

print(min_accuracy_key)