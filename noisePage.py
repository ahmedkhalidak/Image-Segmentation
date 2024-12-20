import tkinter as tk
from tkinter import Label, messagebox
from PIL import Image, ImageTk
import sqlite3
from Addnoise import AddNoise
from Removenoise import RemoveNoise

class Noise:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg="#FFFFFF")

        Label(self.parent, text=" Noise Processing Page", font=("Montserrat", 14), bg="#FFFFFF").pack(pady=10)

        self.db = sqlite3.connect("gallery.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, path TEXT)")
        self.db.commit()

        self.image_paths = self.get_images_from_db()
        self.current_index = 0

        self.image_size = (800, 600)
        self.content_frame = tk.Frame(self.parent, bg="#FFFFFF")
        self.content_frame.pack(pady=10, fill="both")

        
        self.button_frame = tk.Frame(self.content_frame, bg="#FFFFFF")
        self.button_frame.pack(pady=5)

        
        button_config = {
            "font": ("Arial", 12, "bold"),
            "bg": "#176782",
            "fg": "white",
            "width": 20
        }

        self.btn_previous = tk.Button(self.button_frame, text="Previous", command=self.previous_image, **button_config)
        self.btn_previous.pack(side="left", padx=5)

        self.btn_next = tk.Button(self.button_frame, text="Next", command=self.next_image, **button_config)
        self.btn_next.pack(side="left", padx=5)

        self.add_noise_btn = tk.Button(self.button_frame, text="Add Noise ", command=self.Add_on_image, **button_config)
        self.add_noise_btn.pack(side="left", padx=5)

        self.remove_noise_btn = tk.Button(self.button_frame, text="Remove Noise ", command=self.remove_on_image, **button_config)
        self.remove_noise_btn.pack(side="left", padx=5)

       
        self.img_label = tk.Label(self.content_frame, text="No images available", font=("Arial", 16), bg="#FFFFFF")
        self.img_label.pack(pady=20)

        self.update_image()

    def get_images_from_db(self):

        try:
            self.cursor.execute("SELECT path FROM images")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load images from database: {e}")
            return []

    def update_image(self):
      
        if self.image_paths:
            try:
                image_path = self.image_paths[self.current_index]
                image = Image.open(image_path)
                image = image.resize(self.image_size)
                photo = ImageTk.PhotoImage(image)

                self.img_label.config(image=photo, text="")
                self.img_label.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {e}")
        else:
            self.img_label.config(text="No images available", image="")

    def next_image(self):
       
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.update_image()

    def previous_image(self):
       
        if self.image_paths:
            self.current_index = (self.current_index - 1) % len(self.image_paths)
            self.update_image()

    def Add_on_image(self):
        
        if not self.image_paths:
            messagebox.showerror("Error", "No image available to process.")
            return
        try:
            AddNoise(self.image_paths[self.current_index])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")

    def remove_on_image(self):
       
        if not self.image_paths:
            messagebox.showerror("Error", "No image available to process.")
            return
        try:
            RemoveNoise(self.image_paths[self.current_index])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Noise(root)
    root.mainloop()
