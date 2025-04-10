import numpy as np


def vector_product(v1, v2):
    return np.cross(v1, v2)


def calculate_tau(T, N):
    return T / N


def create_quaternion(axis, angle):
    half_angle = angle / 2
    w = np.cos(half_angle)
    x, y, z = axis * np.sin(half_angle)
    return np.array([w, x, y, z])


def rotate_vector(initial_vector, rotation_quaternion, T, N):
    tau = calculate_tau(T, N)
    current_vector = initial_vector.copy()

    for n in range(1, N + 1):
        t = n * tau
        interpolated_angle = (t / T) * 2 * np.arccos(rotation_quaternion[0])
        current_rotation_quaternion = create_quaternion(
            rotation_quaternion[1:] / np.linalg.norm(rotation_quaternion[1:]),
            interpolated_angle
        )
        rotated_vector = quaternion_rotate(current_vector, current_rotation_quaternion)
        current_vector = rotated_vector

    angle_of_rotation = np.arccos(np.dot(initial_vector, current_vector) /
                                  (np.linalg.norm(initial_vector) * np.linalg.norm(current_vector)))
    return current_vector, angle_of_rotation


def quaternion_rotate(vector, quaternion):
    q_w, q_x, q_y, q_z = quaternion
    q_conjugate = np.array([q_w, -q_x, -q_y, -q_z])
    vector_quaternion = np.array([0, vector[0], vector[1], vector[2]])
    rotated_quaternion = quaternion_multiply(quaternion_multiply(quaternion, vector_quaternion), q_conjugate)
    return rotated_quaternion[1:]


def quaternion_multiply(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])


if __name__ == "__main__":
    initial_vector = np.array([1, 0, 0])
    axis = np.array([0, 0, 1])
    angle = np.pi / 2
    T = 10
    N = 100

    rotation_quaternion = create_quaternion(axis, angle)
    final_vector, rotation_angle = rotate_vector(initial_vector, rotation_quaternion, T, N)

    print("Конечный вектор:", final_vector)
    print("Угол поворота (в радианах):", rotation_angle)
    print("Угол поворота (в градусах):", np.degrees(rotation_angle))