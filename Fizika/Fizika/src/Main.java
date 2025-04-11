
public class Main {
    public static void main(String[] args) {
        Quaternion start = new Quaternion (0, 0.5, 0.3, 0.8).normalize();
        double T = 1.0;
        int N = 10;

        solution(start, T, N);
    }

    public static void solution(Quaternion q, double T, int N) {
        Quaternion qn = new Quaternion(1, 0, 0, 0);
        double tau = T / N;
        System.out.println("Входящий кватернион: " + qn + " (длина вектора = " + qn.size() + ")");
        for (int i = 0; i <= N; i++) {
            double t = i * tau; // Текущее время

            // 1. Вычисляем производную кватерниона: dq/dt = 0.5 * ω * q
            Quaternion dqdt = q.multiply(qn).multiply(0.5);

            // 2. Обновляем кватернион
            qn = qn.add(dqdt.multiply(tau)).normalize();

            // 3. Проверяем нормировку
            double size = qn.size();
            if (Math.abs(size - 1.0) > 1e-6) {
                System.err.println("Ошибка: Размер кватерниона не соответствует единичному вектору: " + size);
            }

            // 4. Вычисляем угол поворота и ось
            double fi = 2 * Math.acos(qn.w);
            double fiX = qn.x / Math.sqrt(1 - qn.w * qn.w);
            double fiY = qn.y / Math.sqrt(1 - qn.w * qn.w);
            double fiZ = qn.z / Math.sqrt(1 - qn.w * qn.w);

            // 5. Выводим результаты
            System.out.printf("\nШаг %d (t = %.2f):\n", i, t);
            System.out.println("Положение вектора: " + qn);
            System.out.printf("Угол поворота: %.4f rad (%.2f°)\n", fi, Math.toDegrees(fi));
            System.out.printf("Проверка вектора: [%.4f, %.4f, %.4f]\n", fiX, fiY, fiZ);
        }
    }

    static class Quaternion {
        public final double w, x, y, z;

        public Quaternion(double w, double x, double y, double z) {
            this.w = w;
            this.x = x;
            this.y = y;
            this.z = z;
        }

        // Умножение кватернионов
        public Quaternion multiply(Quaternion other) {
            double newW = w * other.w - x * other.x - y * other.y - z * other.z;
            double newX = w * other.x + x * other.w + y * other.z - z * other.y;
            double newY = w * other.y - x * other.z + y * other.w + z * other.x;
            double newZ = w * other.z + x * other.y - y * other.x + z * other.w;
            return new Quaternion(newW, newX, newY, newZ);
        }

        // Умножение на скаляр
        public Quaternion multiply(double scalar) {
            return new Quaternion(w * scalar, x * scalar, y * scalar, z * scalar);
        }

        // Сложение кватернионов
        public Quaternion add(Quaternion other) {
            return new Quaternion(w + other.w, x + other.x, y + other.y, z + other.z);
        }

        // Проверка размера кватерниона
        public Quaternion normalize() {
            double size = size();
            return new Quaternion(w / size, x / size, y / size, z / size);
        }

        // Длина кватерниона
        public double size() {
            return Math.sqrt(w * w + x * x + y * y + z * z);
        }

        @Override
        public String toString() {
            return String.format("[%.4f, %.4f, %.4f, %.4f]", w, x, y, z);
        }
    }
}