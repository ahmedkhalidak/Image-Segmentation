from tkinter import *
from AddPhoto import Add_Photo
from EdgePage import Edge
from noisePage import Noise
from histogrampage import histo
from allopertion import GalleryApp
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class MainPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Page")
        self.root.geometry("800x600")

        self.sidebar_frame = tk.Frame(self.root, bg="#D8BFD8", height=50)
        self.sidebar_frame.pack(side="top", fill="x")

        self.buttons = [
            ("ADD Photo", self.add_action),
            ("Noise", self.noise_action),
            ("histogram Equalization", self.histo_action),
            ("Edge", self.edge_action),
            ("ALL operation", self.all_action),
            ("Exit", self.exit_action),
        ]

        for text, command in self.buttons:
            button = tk.Button(
                self.sidebar_frame,
                text=text,
                font=("Arial", 12, "bold"),
                bg="#176782",
                fg="white",
                command=command
            )
            button.pack(side="left", fill="x", expand=True)

        
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        self.set_background()

    def set_background(self):
      
        self.main_frame_image = Image.open("back.png")
        self.main_frame_image = self.main_frame_image.resize((1300, 800))  
        self.main_frame_photo = ImageTk.PhotoImage(self.main_frame_image)

        self.bg_label = tk.Label(self.main_frame, image=self.main_frame_photo)
        self.bg_label.place(relwidth=1, relheight=1)
        self.bg_label.lower()  
    def update_content(self,page_class):
       
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        page_class(self.main_frame)

    def add_action(self):
        
        self.update_content(Add_Photo)
       
    def noise_action(self):
        
        self.update_content(Noise)
       
    def histo_action(self):
        
        self.update_content(histo)
        
    def edge_action(self):
        
        self.update_content(Edge)
        
    def all_action(self):
        
        self.update_content(GalleryApp)
       
    def exit_action(self):
        msq= messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if msq:
            self.root.quit()
        

if __name__ == "__main__":
    root = tk.Tk()
    app = MainPage(root)
    root.mainloop()
