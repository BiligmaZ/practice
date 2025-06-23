import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageProcessorApp:
    def __init__(self, root):
        self.canvas = None
        self.root = root
        self.root.title("Обработка изображений")
        self.image = None
        self.photo = None
        self.create_widgets()

    def create_widgets(self):
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
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=im)
        self.photo = imgtk
        self.canvas.config(image=imgtk)

    def load_image(self):
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
        if self.image is None:
            messagebox.showwarning("Нет изображения", "Сначала загрузите или сделайте снимок")
            return
        zeros = np.zeros_like(self.image)
        zeros[:, :, channel] = self.image[:, :, channel]
        self.show_image(zeros)

    def blur_image(self):
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
        if self.image is None:
            messagebox.showwarning("Нет изображения", "Сначала загрузите или сделайте снимок")
            return
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # чтобы отображалось как цветное
        self.show_image(gray_bgr)

    def draw_rectangle(self):
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
