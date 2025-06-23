import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import torch
from PIL import Image, ImageTk
import cv2

class ImageProcessorApp:
    """Приложение для базовой обработки изображений с использованием OpenCV, Tkinter и PyTorch"""

    def __init__(self, root):
        """Инициализация интерфейса приложения"""
        self.canvas = None
        self.root = root
        self.root.title("Обработка изображений")
        self.image = None
        self.photo = None
        self.create_widgets()

    def create_widgets(self):
        """Создание всех кнопок управления и области отображения"""
        tk.Button(self.root, text="Загрузить изображение", command=self.load_image).pack(fill='x')
        tk.Button(self.root, text="Сделать снимок с камеры", command=self.capture_image).pack(fill='x')
        tk.Button(self.root, text="Показать красный канал", command=lambda: self.show_channel(2)).pack(fill='x')
        tk.Button(self.root, text="Показать зеленый канал", command=lambda: self.show_channel(1)).pack(fill='x')
        tk.Button(self.root, text="Показать синий канал", command=lambda: self.show_channel(0)).pack(fill='x')
        tk.Button(self.root, text="Усреднение изображения", command=self.blur_image).pack(fill='x')
        tk.Button(self.root, text="Преобразовать в оттенки серого", command=self.to_grayscale).pack(fill='x')
        tk.Button(self.root, text="Нарисовать прямоугольник", command=self.draw_rectangle).pack(fill='x')
        self.canvas = tk.Label(self.root)
        self.canvas.pack()

    def show_image(self, img):
        """Отображение изображения на экране"""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=im)
        self.photo = imgtk
        self.canvas.config(image=imgtk)

    def load_image(self):
        """Загрузка изображения с диска с проверкой на корректность формата"""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if not file_path:
            return
        img = cv2.imread(file_path)
        if img is None:
            messagebox.showerror("Ошибка", "Файл не является изображением или поврежден")
            return
        self.image = img
        self.show_image(self.image)

    def capture_image(self):
        """Захват изображения с веб-камеры и отображение его в окне"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror(
                "Ошибка камеры",
                "Не удалось подключиться к веб-камере.\n\nВозможные решения:\n"
                "- Проверьте, подключена ли камера.\n- Убедитесь, что она не используется другим приложением.\n"
                "- Проверьте разрешения системы на доступ к камере."
            )
            return
        ret, frame = cap.read()
        cap.release()
        if not ret:
            messagebox.showerror("Ошибка камеры", "Не удалось получить изображение с камеры")
            return
        self.image = frame
        self.show_image(self.image)

    def show_channel(self, channel):
        """Отображение одного из цветовых каналов (R, G или B)"""
        if self.image is None:
            messagebox.showwarning("Нет изображения", "Сначала загрузите или сделайте снимок")
            return
        img_tensor = torch.from_numpy(self.image).clone()
        zeros = torch.zeros_like(img_tensor)
        zeros[:, :, channel] = img_tensor[:, :, channel]
        img_np = zeros.numpy()
        self.show_image(img_np)

    def blur_image(self):
        """Усреднение изображения с помощью фильтра размытия
        Пользователь вводит размер ядра (только нечётные значения)
        Применяется фильтр сглаживания (cv2.blur)"""
        if self.image is None:
            messagebox.showwarning("Нет изображения", "Сначала загрузите или сделайте снимок")
            return
        k = simpledialog.askinteger("Размер ядра", "Введите нечетное целое число > 1:", minvalue=3)
        if k is None:
            return
        if k % 2 == 0:
            messagebox.showerror("Ошибка", "Размер ядра должен быть нечетным")
            return
        blurred = cv2.blur(self.image, (k, k))
        self.show_image(blurred)

    def to_grayscale(self):
        """Преобразование изображения в оттенки серого и отображение его в цветном формате для Tkinter"""
        if self.image is None:
            messagebox.showwarning("Нет изображения", "Сначала загрузите или сделайте снимок")
            return
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # чтобы отображалось как цветное
        self.show_image(gray_bgr)

    def draw_rectangle(self):
        """Рисование синего прямоугольника по координатам, введённым пользователем
        Проверка на корректность введённых координат (в пределах изображения)"""
        if self.image is None:
            messagebox.showwarning("Нет изображения", "Сначала загрузите или сделайте снимок")
            return
        x1 = simpledialog.askinteger("X1", "Введите X1:")
        y1 = simpledialog.askinteger("Y1", "Введите Y1:")
        x2 = simpledialog.askinteger("X2", "Введите X2:")
        y2 = simpledialog.askinteger("Y2", "Введите Y2:")
        if None in (x1, y1, x2, y2):
            return
        img_copy = self.image.copy()
        h, w = img_copy.shape[:2]
        if not (0 <= x1 < w and 0 <= x2 < w and 0 <= y1 < h and 0 <= y2 < h):
            messagebox.showerror("Ошибка", "Координаты вне изображения")
            return
        cv2.rectangle(img_copy, (x1, y1), (x2, y2), (255, 0, 0), 2)
        self.show_image(img_copy)

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
