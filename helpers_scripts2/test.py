def levenshtein_distance(s1, s2):
    m = len(s1)
    n = len(s2)

    # Создаем матрицу размером (m+1) x (n+1) и заполняем ее нулями
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # Инициализируем первую строку и первый столбец матрицы
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Заполняем матрицу по правилам алгоритма Левенштейна
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,  # удаление
                           dp[i][j - 1] + 1,  # вставка
                           dp[i - 1][j - 1] + cost)  # замена или совпадение

    return dp[m][n]


# Пример использования
s1 = "НОВОРОЛАЦК"
s2 = "НОВОПОЛОЦК"
print(levenshtein_distance(s1, s2))  # Расстояние Левенштейна между "кот" и "скот"