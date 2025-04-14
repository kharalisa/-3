import numpy as np
import matplotlib.pyplot as plt

# Чтение матрицы из файла
def read_matrix_from_file(filename):
    with open(filename, 'r') as f:
        return np.array([[int(num) for num in line.split()] for line in f])

# Разделение матрицы A на подматрицы B, C, D, E
def split_submatrices(A):
    N = A.shape[0]
    half = N // 2
    E = A[:half, :half]
    B = A[:half, half:]
    D = A[half:, :half]
    C = A[half:, half:]
    print("\nПодматрицы:")
    print("B:\n", B)
    print("C:\n", C)
    print("D:\n", D)
    print("E:\n", E)
    return B, C, D, E

# Подсчет количества нулей в C по заданному условию
def count_zeros_C(C):
    count = 0
    for i in range(C.shape[0]):
        if (i + 1) % 2 == 0:  # четные строки, начиная с 1
            for j in range(C.shape[1]):
                if (j + 1) % 2 == 1 and C[i, j] == 0:  # нечетные столбцы, начиная с 1
                    count += 1
    print("подсчёт нулей в C (чётные строки, нечётные столбцы — индексация с 1):", count)
    return count

# Произведение элементов по периметру C
def perimeter_product(C):
    top = C[0, :]
    bottom = C[-1, :]
    left = C[1:-1, 0]
    right = C[1:-1, -1]
    perimeter = np.concatenate([top, bottom, left, right])
    print("\nПериметр C:", perimeter)
    product = 1
    for num in perimeter:
        product *= num
    print("Произведение элементов периметра C:", product)
    return product

# Симметричный обмен

def symmetric_swap(B, C):
    print("\nВыполняем симметричный обмен B <-> C")
    return C.copy(), B.copy()

# Несимметричный обмен

def nonsymmetric_swap(C, E):
    print("\nВыполняем несимметричный обмен C <-> E (плоский -> reshape)")
    C_flat = C.flatten()
    E_flat = E.flatten()
    C_new = E_flat.reshape(C.shape)
    E_new = C_flat.reshape(E.shape)
    return C_new, E_new

# Сборка полной матрицы F из подматриц
def construct_F(B, C, D, E):
    top = np.hstack((E, B))
    bottom = np.hstack((D, C))
    return np.vstack((top, bottom))

# Графики матрицы F

def show_graphs(F):
    fig1 = plt.figure("Heatmap")
    plt.imshow(F, cmap='coolwarm', interpolation='none')
    plt.title("Heatmap of Matrix F")
    plt.colorbar()

    fig2 = plt.figure("Histogram")
    plt.hist(F.flatten(), bins=10, color='skyblue', edgecolor='black')
    plt.title("Histogram of F Values")

    fig3 = plt.figure("3D Surface")
    ax = fig3.add_subplot(111, projection='3d')
    x = np.arange(F.shape[0])
    y = np.arange(F.shape[1])
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X, Y, F.T, cmap='viridis')
    ax.set_title("3D Surface of F")

    plt.show()

# --- Основной блок ---

K = int(input("Введите число K: "))
A = read_matrix_from_file("matrix.txt")
print("\nМатрица A:\n", A)

B, C, D, E = split_submatrices(A)

zeros_count = count_zeros_C(C)
prod = perimeter_product(C)

# Выбор обмена
if zeros_count > prod:
    print("\nУсловие: нулей больше, чем произведение —> симметричный обмен")
    B, C = symmetric_swap(B, C)
else:
    print("\nУсловие: произведение больше либо равно —> несимметричный обмен")
    C, E = nonsymmetric_swap(C, E)

F = construct_F(B, C, D, E)
print("\nМатрица F после обмена:\n", F)

# Выбор формулы на основе det и trace
if np.linalg.det(A) > np.trace(F):
    print("\nВыполняем: A⁻¹ * Aᵗ – K * Fᵗ")
    result = np.linalg.inv(A) @ A.T - K * F.T
else:
    print("\nВыполняем: (A + G - F⁻¹) * K")
    G = np.tril(A)
    try:
        F_inv = np.linalg.inv(F)
    except np.linalg.LinAlgError:
        print("⚠️ Матрица F необратима, используем псевдообратную")
        F_inv = np.linalg.pinv(F)
    result = (A + G - F_inv) * K

print("\nРезультат:\n", result)

show_graphs(F)
