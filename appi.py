import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("900x600")
app.title("Image Enhancer")

image_label = ctk.CTkLabel(app, text="")
image_label.pack(pady=20)

selected_image = None


def select_image():
    global selected_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if file_path:
        selected_image = file_path

        img = Image.open(file_path)
        img = img.resize((400, 400))
        tk_img = ImageTk.PhotoImage(img)

        image_label.configure(image=tk_img)
        image_label.image = tk_img


def enhance_image():
    if selected_image is None:
        return

    img = cv2.imread(selected_image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Denoise
    denoised = cv2.fastNlMeansDenoisingColored(img, None, 7, 7, 5, 9)

    # Sharpen
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharp = cv2.filter2D(denoised, -1, kernel)

    # Upscale 2x
    upscaled = cv2.resize(sharp, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG File", "*.png")]
    )

    if save_path:
        final = Image.fromarray(upscaled)
        final.save(save_path)


select_btn = ctk.CTkButton(app, text="انتخاب عکس", command=select_image)
select_btn.pack(pady=10)

enhance_btn = ctk.CTkButton(app, text="پردازش و ذخیره", command=enhance_image)
enhance_btn.pack(pady=10)

app.mainloop()