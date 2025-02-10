# https://stackoverflow.com/questions/72472167/deprecation-warning-the-system-version-of-tk-is-deprecated-m1-mac-in-vs-code

# tkinter for UI
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import numpy as np
import os


# constants declared here:
FONT_SIZE = 12    #originally 2


FOREGROUND = 'lime green'
# FONT = 'TkFixedFont'
RATIO = 2
FONT = ("Courier", 2)

def rgb_to_brightness(image):
    rgb_data = np.array(image.convert('RGBA'))[:, :, :3]
    weights = np.array([0.21, 0.72, 0.07])
    brightness_matrix = np.dot(rgb_data, weights).astype(int)
    return brightness_matrix

def map_transform(val, range1, range2):
    step = range2 / range1
    newVal = int(val * step)
    return newVal

def to_ascii(matrix):
    characters = list("`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$")
    range2 = len(characters)
    range1 = 254

    ascii_matrix = []
    for row in matrix:
        ascii_row = ""
        for value in row:
            index = map_transform(value, range1, range2)
            ascii_row += characters[index - 1] * RATIO  # Adjust for better aspect ratio
        ascii_matrix.append(ascii_row)

    return "\n".join(ascii_matrix)

def image_to_ascii(image_path):
    image = Image.open(image_path)
    brightness_matrix = rgb_to_brightness(image)
    ascii_art = to_ascii(brightness_matrix)
    return ascii_art

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to ASCII Art Converter")
        self.root.geometry("1200x800")  # Increased window size

        self.image_path = None

        self.label = tk.Label(root, text="Select an image to convert to ASCII art")
        self.label.pack(pady=5)

        self.select_button = tk.Button(root, text="Select Image", command=self.select_image)
        self.select_button.pack(pady=5)

        self.convert_button = tk.Button(root, text="Convert to ASCII", command=self.convert_to_ascii)
        self.convert_button.pack(pady=5)

        self.text_area = tk.Text(
            root, 
            wrap=tk.WORD, 
            font=FONT,  # monospaced, smaller
            height=30,   #originally 200
            width=100,         #originally 1000
            background="black",   # Set background to black
            foreground=FOREGROUND    # Set text color to green
        )
        self.text_area.config(state="normal", background='black')
        
        self.text_area.insert(tk.INSERT, "ascii text image will be displayed here")

        
        self.text_area.pack(expand=True, fill=tk.BOTH, pady=10, padx=10)
    
        

    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[
                ("PNG Files", "*.png"),
                ("JPEG Files", "*.jpg"),
                ("JPEG Files", "*.jpeg"),
                ("BMP Files", "*.bmp"),
                ("GIF Files", "*.gif"),
                ("All Files", "*.*")
            ]
        )

        if self.image_path:
            self.label.config(text=f"Selected Image: {os.path.basename(self.image_path)}")

    def convert_to_ascii(self):
        if self.image_path:
            print(f"Image Path: {self.image_path}")
            ascii_art = image_to_ascii(self.image_path)
            print('IMAGE CONVERTED TO ASCII@@@')
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, ascii_art)
        else:
            messagebox.showerror("Error", "Please select an image first.")

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

