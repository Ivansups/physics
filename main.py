import numpy as np


def create_rotation_matrix(axis, angle):
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    c = np.cos(angle)
    s = np.sin(angle)
    C = 1 - c
    return np.array([
        [x * x * C + c, x * y * C - z * s, x * z * C + y * s],
        [y * x * C + z * s, y * y * C + c, y * z * C - x * s],
        [z * x * C - y * s, z * y * C + x * s, z * z * C + c]
    ])


def calculate_tau(T, N):
    return T / N


def rotate_vector(initial_vector, rotation_axis, total_angle, T, N):
    tau = calculate_tau(T, N)
    current_vector = initial_vector.copy()

    for n in range(1, N + 1):
        t = n * tau
        interpolated_angle = (t / T) * total_angle
        rotation_matrix = create_rotation_matrix(rotation_axis, interpolated_angle)
        current_vector = np.dot(rotation_matrix, current_vector)

    angle_of_rotation = np.arccos(np.dot(initial_vector, current_vector) /
                                  (np.linalg.norm(initial_vector) * np.linalg.norm(current_vector)))
    return current_vector, angle_of_rotation


if __name__ == "__main__":
    initial_vector = np.array([1, 0, 0])
    axis = np.array([0, 0, 1])
    angle = np.pi / 2
    T = 10
    N = 100

    final_vector, rotation_angle = rotate_vector(initial_vector, axis, angle, T, N)

    print("Конечный вектор:", final_vector)
    print("Угол поворота (в радианах):", rotation_angle)
    print("Угол поворота (в градусах):", np.degrees(rotation_angle))