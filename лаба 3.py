import copy

def read_matrix(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        matrix = [list(map(int, line.strip().split())) for line in lines]
    return matrix

def print_matrix(matrix, title="Matrix"):
    print(f"\n{title}:")
    for row in matrix:
        print(" ".join(f"{val:3}" for val in row))

def get_k():
    return int(input("Введите число K: "))

def get_top_border(matrix):
    size = len(matrix)
    positions = set()
    for i in range(size):
        for j in range(size):
            if i < j and i + j < size - 1:
                if i == 0 or j == size - 1 or i + j == size - 2:
                    positions.add((i, j))
    return [matrix[i][j] for i, j in positions]

def get_bottom_border(matrix):
    size = len(matrix)
    positions = set()
    for i in range(size):
        for j in range(size):
            if i > j and i + j > size - 1:
                if i == size - 1 or j == 0 or i + j == size:
                    positions.add((i, j))
    return [matrix[i][j] for i, j in positions]

def swap_symmetric(matrix, size):
    for i in range(size):
        for j in range(size):
            if (i < j and i + j < size - 1):
                sym_i, sym_j = size - 1 - i, size - 1 - j
                if (sym_i > sym_j and sym_i + sym_j > size - 1):
                    matrix[i][j], matrix[sym_i][sym_j] = matrix[sym_i][sym_j], matrix[i][j]
    return matrix

def swap_non_symmetric(matrix, size):
    top_coords = []
    bottom_coords = []

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

def transpose(matrix):
    size = len(matrix)
    return [[matrix[j][i] for j in range(size)] for i in range(size)]

def add_matrices(mat1, mat2):
    size = len(mat1)
    return [[mat1[i][j] + mat2[i][j] for j in range(size)] for i in range(size)]

def multiply_by_scalar(matrix, scalar):
    size = len(matrix)
    return [[scalar * matrix[i][j] for j in range(size)] for i in range(size)]

def multiply_matrices(mat1, mat2):
    size = len(mat1)
    result = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            result[i][j] = sum(mat1[i][k] * mat2[k][j] for k in range(size))
    return result

def subtract_matrices(mat1, mat2):
    size = len(mat1)
    return [[mat1[i][j] - mat2[i][j] for j in range(size)] for i in range(size)]

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

print(f"\nЭлементов в верхней границе: {top_count}")
print(f"Произведение в нижней границе: {bottom_product}")

if top_count > bottom_product:
    print("Симметричный обмен областей")
    matrix_f = swap_symmetric(matrix_f, size)
else:
    print("Несимметричный обмен областей")
    matrix_f = swap_non_symmetric(matrix_f, size)

print_matrix(matrix_f, "Измененная матрица F")

a_transposed = transpose(matrix_a)
f_transposed = transpose(matrix_f)

k_a_transposed = multiply_by_scalar(a_transposed, k)
f_plus_a = add_matrices(matrix_f, matrix_a)
first_part = multiply_matrices(k_a_transposed, f_plus_a)
k_f_transposed = multiply_by_scalar(f_transposed, k)
result = subtract_matrices(first_part, k_f_transposed)

print_matrix(result, "Итоговый результат")
