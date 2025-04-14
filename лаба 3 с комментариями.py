# Импорт модуля для создания полных копий объектов
import copy

# Функция чтения матрицы из файла
def read_matrix(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        matrix = [list(map(int, line.strip().split())) for line in lines]
    return matrix

# Функция вывода матрицы
def print_matrix(matrix, title="Matrix"):
    print(f"\n{title}:")
    for row in matrix:
        print(" ".join(f"{val:3}" for val in row))

# Ввод значения K
def get_k():
    return int(input("Введите число K: "))

# Граница верхнего правого треугольника
def get_top_border(matrix):
    size = len(matrix)
    positions = set()
    for i in range(size):
        for j in range(size):
            if i < j and i + j < size - 1:
                if i == 0 or j == size - 1 or i + j == size - 2:
                    positions.add((i, j))
    values = [matrix[i][j] for i, j in positions]
    print(f"\nобласть 2: {values}")
    return values

# Граница нижнего левого треугольника
def get_bottom_border(matrix):
    size = len(matrix)
    positions = set()
    for i in range(size):
        for j in range(size):
            if i > j and i + j > size - 1:
                if i == size - 1 or j == 0 or i + j == size:
                    positions.add((i, j))
    values = [matrix[i][j] for i, j in positions]
    print(f"область 3: {values}")
    return values

# Симметричный обмен
def swap_symmetric(matrix, size):
    for i in range(size):
        for j in range(size):
            if (i < j and i + j < size - 1):
                sym_i, sym_j = size - 1 - i, size - 1 - j
                if (sym_i > sym_j and sym_i + sym_j > size - 1):
                    matrix[i][j], matrix[sym_i][sym_j] = matrix[sym_i][sym_j], matrix[i][j]
    return matrix

# Несимметричный обмен
def swap_non_symmetric(matrix, size):
    top_coords, bottom_coords = [], []
    for i in range(size):
        for j in range(size):
            if i < j and i + j < size - 1:
                top_coords.append((i, j))
            elif i > j and i + j > size - 1:
                bottom_coords.append((i, j))
    for idx in range(min(len(top_coords), len(bottom_coords))):
        i1, j1 = top_coords[idx]
        i3, j3 = bottom_coords[idx]
        matrix[i1][j1], matrix[i3][j3] = matrix[i3][j3], matrix[i1][j1]
    return matrix

# Транспонирование матрицы
def transpose(matrix):
    size = len(matrix)
    return [[matrix[j][i] for j in range(size)] for i in range(size)]

# Сложение матриц
def add_matrices(mat1, mat2):
    size = len(mat1)
    return [[mat1[i][j] + mat2[i][j] for j in range(size)] for i in range(size)]

# Умножение на число
def multiply_by_scalar(matrix, scalar):
    size = len(matrix)
    return [[scalar * matrix[i][j] for j in range(size)] for i in range(size)]

# Перемножение матриц
def multiply_matrices(mat1, mat2):
    size = len(mat1)
    result = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            result[i][j] = sum(mat1[i][k] * mat2[k][j] for k in range(size))
    return result

# Вычитание матриц
def subtract_matrices(mat1, mat2):
    size = len(mat1)
    return [[mat1[i][j] - mat2[i][j] for j in range(size)] for i in range(size)]

# Главная логика
k = get_k()
matrix_a = read_matrix('matrix.txt')
size = len(matrix_a)
print_matrix(matrix_a, "Исходная матрица A")

matrix_f = copy.deepcopy(matrix_a)
top_border = get_top_border(matrix_a)
bottom_border = get_bottom_border(matrix_a)

top_count = len(top_border)
bottom_product = 1
for num in bottom_border:
    bottom_product *= num if num != 0 else 1

print(f"\nЭлементов на границе области 2: {top_count}")
print(f"Произведение элементов на границе области 3: {bottom_product}")

if top_count > bottom_product:
    print("\nВыполняется симметричный обмен областей")
    matrix_f = swap_symmetric(matrix_f, size)
else:
    print("\nВыполняется несимметричный обмен областей")
    matrix_f = swap_non_symmetric(matrix_f, size)

print_matrix(matrix_f, "Измененная матрица F")

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

