import tkinter as tk
from tkinter import Label, Button, filedialog, messagebox, Frame
from PIL import Image, ImageTk
import sqlite3
import os

class Add_Photo:
    def __init__(self, master):
        self.master = master
        self.db = sqlite3.connect("gallery.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, path TEXT)")
        self.db.commit()

        self.image_paths = self.get_images_from_db()
        self.current_index = 0

        self.image_size = (800, 600)

        self.content_frame = Frame(master, bg="#FFFFFF")
        self.content_frame.pack(fill="both", expand=True)

        self.button_frame = Frame(self.content_frame, bg="#FFFFFF")
        self.button_frame.pack(pady=10)

        button_config = {
            "font": ("Arial", 12, "bold"),
            "bg": "#176782",
            "fg": "white",
            "width": 10  
        }

        self.btn_previous = Button(self.button_frame, text="Prev", command=self.previous_image, **button_config)
        self.btn_previous.pack(side="left", padx=5)

        self.btn_next = Button(self.button_frame, text="Next", command=self.next_image, **button_config)
        self.btn_next.pack(side="left", padx=5)

        self.btn_add = Button(self.button_frame, text="Add Photo", command=self.add_image, **button_config)
        self.btn_add.pack(side="left", padx=5)

        self.btn_delete = Button(self.button_frame, text="Delete Photo", command=self.delete_image, font=("Arial", 12, "bold"), bg="#E74C3C", fg="white", width=10)
        self.btn_delete.pack(side="left", padx=5)

        self.img_label = Label(self.content_frame, text="No images available", font=("Arial", 16))
        self.img_label.pack(pady=20)

        self.update_image()

    def get_images_from_db(self):
        self.cursor.execute("SELECT path FROM images")
        return [row[0] for row in self.cursor.fetchall()]

    def update_image(self):
        if self.image_paths:
            image = Image.open(self.image_paths[self.current_index])
            image = image.resize(self.image_size)  
            photo = ImageTk.PhotoImage(image)
            self.img_label.config(image=photo, text="")
            self.img_label.image = photo 
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

    def add_image(self):
        file_path = filedialog.askopenfilename(title="Select Image",)
        if file_path:
            try:
                save_dir = "images"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                file_name = os.path.basename(file_path)
                new_path = os.path.join(save_dir, file_name)
                if not os.path.exists(new_path):  
                    with open(file_path, "rb") as src, open(new_path, "wb") as dst:
                        dst.write(src.read())

                self.cursor.execute("INSERT INTO images (path) VALUES (?)", (new_path,))
                self.db.commit()
                self.image_paths = self.get_images_from_db()
                self.update_image()
                messagebox.showinfo("Success", "Image added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add image: {str(e)}")

    def delete_image(self):
        if not self.image_paths:
            messagebox.showerror("Error", "No images to delete.")
            return

        current_image_path = self.image_paths[self.current_index]
        response = messagebox.askyesno("Delete Image", f"Are you sure you want to delete this image?\n{current_image_path}")
        if response:
            try:
                self.cursor.execute("DELETE FROM images WHERE path=?", (current_image_path,))
                self.db.commit()

                if os.path.exists(current_image_path):
                    os.remove(current_image_path)

                self.image_paths = self.get_images_from_db()
                if not self.image_paths:
                    self.current_index = 0
                else:
                    self.current_index = self.current_index % len(self.image_paths)

                self.update_image()
                messagebox.showinfo("Success", "Image deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete image: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Add_Photo(root)
    root.mainloop()
