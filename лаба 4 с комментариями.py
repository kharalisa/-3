import numpy as np  # Импорт библиотеки numpy для работы с матрицами
import matplotlib.pyplot as plt  # Импорт библиотеки matplotlib для визуализации

# Функция чтения матрицы из текстового файла

def read_matrix_from_file(filename):
    with open(filename, 'r') as f:  # Открываем файл для чтения
        return np.array([[int(num) for num in line.split()] for line in f])  # Преобразуем каждую строку в список целых чисел и собираем в numpy-массив

# Делим матрицу A на 4 равные подматрицы: B, C, D, E

def split_submatrices(A):
    N = A.shape[0]  # Размерность матрицы (предполагается квадратная)
    half = N // 2  # Половина размера — для деления на квадранты
    E = A[:half, :half]  # Верхний левый блок
    B = A[:half, half:]  # Верхний правый блок
    D = A[half:, :half]  # Нижний левый блок
    C = A[half:, half:]  # Нижний правый блок
    print("\nПодматрицы:")  # Выводим все подматрицы
    print("B:\n", B)
    print("C:\n", C)
    print("D:\n", D)
    print("E:\n", E)
    return B, C, D, E  # Возвращаем подматрицы

# Считаем количество нулей в подматрице C в четных строках и нечетных столбцах (индексация с 1)

def count_zeros_C(C):
    count = 0  # Счетчик нулей
    for i in range(C.shape[0]):  # Перебираем строки
        if (i + 1) % 2 == 0:  # Четные строки (по индексации с 1)
            for j in range(C.shape[1]):  # Перебираем столбцы
                if (j + 1) % 2 == 1 and C[i, j] == 0:  # Нечетные столбцы (индексация с 1) и нулевой элемент
                    count += 1  # Увеличиваем счетчик
    print("Обновлённый подсчёт нулей в C (чётные строки, нечётные столбцы — индексация с 1):", count)  # Вывод результата
    return count  # Возвращаем количество

# Считаем произведение всех значений на периметре матрицы C

def perimeter_product(C):
    top = C[0, :]  # Верхняя строка
    bottom = C[-1, :]  # Нижняя строка
    left = C[1:-1, 0]  # Левая граница (без углов)
    right = C[1:-1, -1]  # Правая граница (без углов)
    perimeter = np.concatenate([top, bottom, left, right])  # Объединяем в один массив
    print("\nПериметр C:", perimeter)  # Показываем периметр
    product = 1  # Начальное значение произведения
    for num in perimeter:  # Проходим по каждому элементу
        product *= num  # Умножаем
    print("Произведение элементов периметра C:", product)  # Выводим результат
    return product  # Возвращаем произведение

# Обмениваем местами матрицы B и C (симметрично)

def symmetric_swap(B, C):
    print("\nВыполняем симметричный обмен B <-> C")  # Комментарий
    return C.copy(), B.copy()  # Возвращаем копии C и B в обратном порядке

# Обмениваем содержимое C и E поэлементно, без учета структуры (несимметрично)

def nonsymmetric_swap(C, E):
    print("\nВыполняем несимметричный обмен C <-> E (плоский -> reshape)")  # Комментарий
    C_flat = C.flatten()  # Преобразуем C в плоский массив
    E_flat = E.flatten()  # Преобразуем E в плоский массив
    C_new = E_flat.reshape(C.shape)  # Переформатируем E в форму C
    E_new = C_flat.reshape(E.shape)  # Переформатируем C в форму E
    return C_new, E_new  # Возвращаем новые матрицы

# Собираем новую матрицу F из подматриц E, B, D, C

def construct_F(B, C, D, E):
    top = np.hstack((E, B))  # Склеиваем горизонтально E и B
    bottom = np.hstack((D, C))  # Склеиваем горизонтально D и C
    return np.vstack((top, bottom))  # Склеиваем вертикально top и bottom

# Визуализируем матрицу F с помощью трех графиков

def show_graphs(F):
    fig1 = plt.figure("Heatmap")  # Создаем график тепловой карты
    plt.imshow(F, cmap='coolwarm', interpolation='none')  # Визуализируем матрицу
    plt.title("Heatmap of Matrix F")  # Заголовок
    plt.colorbar()  # Цветовая шкала

    fig2 = plt.figure("Histogram")  # Создаем гистограмму
    plt.hist(F.flatten(), bins=10, color='skyblue', edgecolor='black')  # Распределение значений
    plt.title("Histogram of F Values")  # Заголовок

    fig3 = plt.figure("3D Surface")  # 3D поверхность
    ax = fig3.add_subplot(111, projection='3d')  # 3D ось
    x = np.arange(F.shape[0])  # Ось X
    y = np.arange(F.shape[1])  # Ось Y
    X, Y = np.meshgrid(x, y)  # Создаем сетку координат
    ax.plot_surface(X, Y, F.T, cmap='viridis')  # 3D поверхность
    ax.set_title("3D Surface of F")  # Заголовок

    plt.show()  # Показываем все графики

# --- Основной исполняемый блок ---

K = int(input("Введите число K: "))  # Ввод коэффициента K пользователем
A = read_matrix_from_file("matrix.txt")  # Чтение исходной матрицы A из файла
print("\nМатрица A:\n", A)  # Печать матрицы A

B, C, D, E = split_submatrices(A)  # Делим матрицу A на 4 части

zeros_count = count_zeros_C(C)  # Считаем количество нулей в C
prod = perimeter_product(C)  # Считаем произведение по периметру C

# Сравниваем метрики и выбираем тип обмена
if zeros_count > prod:
    print("\nУсловие: нулей больше, чем произведение —> симметричный обмен")
    B, C = symmetric_swap(B, C)  # Выполняем симметричный обмен
else:
    print("\nУсловие: произведение больше либо равно —> несимметричный обмен")
    C, E = nonsymmetric_swap(C, E)  # Выполняем несимметричный обмен

F = construct_F(B, C, D, E)  # Сборка новой матрицы F
print("\nМатрица F после обмена:\n", F)  # Вывод результата обмена

# Выбор формулы на основе det(A) и trace(F)
if np.linalg.det(A) > np.trace(F):
    print("\nВыполняем: A⁻¹ * Aᵗ – K * Fᵗ")  # Если определитель A больше следа F
    result = np.linalg.inv(A) @ A.T - K * F.T  # Расчет результата по формуле 1
else:
    print("\nВыполняем: (A + G - F⁻¹) * K")  # Иначе используем формулу 2
    G = np.tril(A)  # Нижняя треугольная часть A
    try:
        F_inv = np.linalg.inv(F)  # Обратная к F
    except np.linalg.LinAlgError:
        print("⚠️ Матрица F необратима, используем псевдообратную")
        F_inv = np.linalg.pinv(F)  # Псевдообратная матрица
    result = (A + G - F_inv) * K  # Финальный расчет

print("\nРезультат:\n", result)  # Печать результата

show_graphs(F)  # Визуализация
