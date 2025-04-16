# Импорт модуля copy для создания независимых копий объектов
import copy

# Функция для чтения матрицы из файла
def read_matrix(filename):
    # Открытие файла в режиме чтения
    with open(filename, 'r') as file:
        # Чтение всех строк файла
        lines = file.readlines()
        # Преобразование каждой строки в список целых чисел
        matrix = [list(map(int, line.strip().split())) for line in lines]
    # Возврат матрицы
    return matrix

# Функция для красивого вывода матрицы
def print_matrix(matrix, title="Matrix"):
    # Печать заголовка
    print(f"\n{title}:")
    # Печать каждой строки матрицы с выравниванием по 3 символа
    for row in matrix:
        print(" ".join(f"{val:3}" for val in row))

# Функция для ввода числа K пользователем
def get_k():
    # Преобразование введенного значения в целое число
    return int(input("Введите число K: "))

# Функция для получения границы верхнего правого треугольника (область 2)
def get_top_border(matrix):
    size = len(matrix)  # Размер матрицы
    positions = set()  # Множество координат граничных элементов
    for i in range(size):
        for j in range(size):
            # Проверка: принадлежность к области 2
            if i < j and i + j < size - 1:
                # Проверка: принадлежность к границе области 2
                if i == 0 or j == size - 1 or i + j == size - 2:
                    positions.add((i, j))
    # Извлечение значений по координатам
    values = [matrix[i][j] for i, j in positions]
    print(f"\nобласть 2: {values}")
    return values

# Функция для получения границы нижнего левого треугольника (область 3)
def get_bottom_border(matrix):
    size = len(matrix)  # Размер матрицы
    positions = set()  # Множество координат граничных элементов
    for i in range(size):
        for j in range(size):
            # Проверка: принадлежность к области 3
            if i > j and i + j > size - 1:
                # Проверка: принадлежность к границе области 3
                if i == size - 1 or j == 0 or i + j == size:
                    positions.add((i, j))
    # Извлечение значений по координатам
    values = [matrix[i][j] for i, j in positions]
    print(f"область 3: {values}")
    return values

# Функция симметричного обмена элементов между областями 2 и 3
def swap_symmetric(matrix, size):
    for i in range(size):
        for j in range(size):
            # Проверка: принадлежность к области 2
            if (i < j and i + j < size - 1):
                # Определение симметричной позиции
                sym_i, sym_j = size - 1 - i, size - 1 - j
                # Проверка: симметричная позиция в области 3
                if (sym_i > sym_j and sym_i + sym_j > size - 1):
                    # Обмен значениями между симметричными позициями
                    matrix[i][j], matrix[sym_i][sym_j] = matrix[sym_i][sym_j], matrix[i][j]
    return matrix

# Функция несимметричного обмена по порядку между областями 2 и 3
def swap_non_symmetric(matrix, size):
    top_coords, bottom_coords = [], []
    for i in range(size):
        for j in range(size):
            if i < j and i + j < size - 1:
                top_coords.append((i, j))
            elif i > j and i + j > size - 1:
                bottom_coords.append((i, j))
    # Сортируем координаты по порядку прохода
    top_coords.sort()  # слева направо, сверху вниз
    bottom_coords.sort(reverse=True)  # справа налево, снизу вверх

    for (i2, j2), (i3, j3) in zip(top_coords, bottom_coords):
        matrix[i2][j2], matrix[i3][j3] = matrix[i3][j3], matrix[i2][j2]

    return matrix

# Функция транспонирования матрицы (поворот по диагонали)
def transpose(matrix):
    size = len(matrix)
    # Меняем строки и столбцы местами
    return [[matrix[j][i] for j in range(size)] for i in range(size)]

# Функция сложения двух матриц
def add_matrices(mat1, mat2):
    size = len(mat1)
    return [[mat1[i][j] + mat2[i][j] for j in range(size)] for i in range(size)]

# Функция умножения матрицы на скаляр
def multiply_by_scalar(matrix, scalar):
    size = len(matrix)
    return [[scalar * matrix[i][j] for j in range(size)] for i in range(size)]

# Функция перемножения двух матриц
def multiply_matrices(mat1, mat2):
    size = len(mat1)
    result = [[0] * size for _ in range(size)]  # Результирующая матрица
    for i in range(size):
        for j in range(size):
            # Скалярное произведение строки и столбца
            result[i][j] = sum(mat1[i][k] * mat2[k][j] for k in range(size))
    return result

# Функция вычитания одной матрицы из другой
def subtract_matrices(mat1, mat2):
    size = len(mat1)
    return [[mat1[i][j] - mat2[i][j] for j in range(size)] for i in range(size)]

# --- Главная логика программы ---

k = get_k()  # Ввод значения K пользователем
matrix_a = read_matrix('matrix.txt')  # Чтение исходной матрицы A из файла
size = len(matrix_a)  # Размер матрицы

print_matrix(matrix_a, "Исходная матрица A")

matrix_f = copy.deepcopy(matrix_a)  # Копия матрицы A для преобразований

# Получение границ и их характеристик
top_border = get_top_border(matrix_a)
bottom_border = get_bottom_border(matrix_a)

top_count = len(top_border)  # Кол-во элементов области 2
bottom_product = 1
for num in bottom_border:
    bottom_product *= num if num != 0 else 1  # Произведение с пропуском нулей

# Сравнение характеристик и выбор типа обмена
print(f"\nЭлементов на границе области 2: {top_count}")
print(f"Произведение элементов на границе области 3: {bottom_product}")

if top_count > bottom_product:
    print("\nВыполняется симметричный обмен областей")
    matrix_f = swap_symmetric(matrix_f, size)
else:
    print("\nВыполняется несимметричный обмен областей")
    matrix_f = swap_non_symmetric(matrix_f, size)

print_matrix(matrix_f, "Измененная матрица F")

# Вычисление итоговой формулы: (K*Aᵀ)*(F+A) - K*Fᵀ
a_transposed = transpose(matrix_a)
print_matrix(a_transposed, "Транспонированная матрица Aᵀ")

k_a_transposed = multiply_by_scalar(a_transposed, k)
print_matrix(k_a_transposed, "Матрица K*Aᵀ")

f_plus_a = add_matrices(matrix_f, matrix_a)
print_matrix(f_plus_a, "Сумма F + A")

first_part = multiply_matrices(k_a_transposed, f_plus_a)
print_matrix(first_part, "Произведение (K*Aᵀ)*(F+A)")

f_transposed = transpose(matrix_f)
k_f_transposed = multiply_by_scalar(f_transposed, k)
print_matrix(k_f_transposed, "Матрица K*Fᵀ")

result = subtract_matrices(first_part, k_f_transposed)
print_matrix(result, "Итоговый результат")

