import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import photo_manager
import ttkbootstrap as ttk
from ttkbootstrap import Style

class PhotoSortApp:
    def __init__(self, root):
        self.style = Style(theme='darkly')
        self.root = root
        self.root.title("PhotoSort")
        self.root.geometry("600x900")

        self.folder_path = ""
        self.image_files = []
        self.current_index = 0
        self.categories = []
        self.target_folders = {}

        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill='both', expand=True)
        
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.pack(fill='x', pady=5)

        self.label = ttk.Label(self.top_frame, text="Pilih folder berisi foto", font=("Arial", 12))
        self.label.pack(anchor='w')

        self.btn_select_folder = ttk.Button(self.top_frame, text="Pilih Folder", bootstyle="primary", command=self.select_folder)
        self.btn_select_folder.pack(pady=5)
        
        self.category_frame = ttk.Labelframe(self.main_frame, text="Kategori", padding=10)
        self.category_frame.pack(fill='x', pady=5)

        self.entry_category = ttk.Entry(self.category_frame, width=20)
        self.entry_category.pack(side=tk.LEFT, padx=5)
        
        self.btn_add_category = ttk.Button(self.category_frame, text="+", bootstyle="success", command=self.add_category)
        self.btn_add_category.pack(side=tk.LEFT)

        self.category_listbox = tk.Listbox(self.category_frame, height=5)
        self.category_listbox.pack(fill='x', pady=5)

        self.btn_start = ttk.Button(self.main_frame, text="Mulai Klasifikasi", bootstyle="info", command=self.sorting)
        self.btn_start.pack(pady=5)

        self.image_frame = ttk.Labelframe(self.main_frame, text="Preview Gambar", padding=10)
        self.image_frame.pack(fill='both', expand=True, pady=5)

        self.canvas = tk.Canvas(self.image_frame, width=400, height=400, bg="#2a2a2a")
        self.canvas.pack()

        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_frame.pack(fill='x', pady=5)
    
    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.image_files = photo_manager.get_images(self.folder_path)
            if not self.image_files:
                messagebox.showerror("Error", "Folder tidak mengandung gambar.")
            else:
                self.label.config(text=f"Folder terpilih: {self.folder_path}")
    
    def add_category(self):
        category = self.entry_category.get().strip()
        if category and category not in self.categories:
            self.categories.append(category)
            self.category_listbox.insert(tk.END, category)
            self.entry_category.delete(0, tk.END)
    
    def sorting(self):
        if not self.folder_path:
            messagebox.showerror("Error", "Pilih folder gambar terlebih dahulu!")
            return
        
        if not self.categories:
            messagebox.showerror("Error", "Tambahkan minimal satu kategori!")
            return
        
        self.target_folders = photo_manager.create_dir(self.folder_path, self.categories)
        self.create_category_buttons()
        self.show_image()
    
    def create_category_buttons(self):
        for widget in self.btn_frame.winfo_children():
            widget.destroy()
        
        for category in self.categories:
            btn = ttk.Button(self.btn_frame, text=category, bootstyle="secondary", command=lambda c=category: self.move_image(c))
            btn.pack(side=tk.LEFT, padx=5)
        
        btn_delete = ttk.Button(self.btn_frame, text="Hapus", bootstyle="danger", command=self.delete_image)
        btn_delete.pack(side=tk.LEFT, padx=5)
        
        self.root.update_idletasks()
    
    def show_image(self):
        if self.current_index < len(self.image_files):
            img_path = os.path.join(self.folder_path, self.image_files[self.current_index])
            img = Image.open(img_path)
            img.thumbnail((400, 400))
            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(200, 200, image=self.tk_img)
        else:
            self.label.config(text="Semua foto telah diproses!")
            self.canvas.delete("all")
    
    def move_image(self, category_target):
        src = os.path.join(self.folder_path, self.image_files[self.current_index])
        dst = os.path.join(self.target_folders[category_target], self.image_files[self.current_index])
        photo_manager.move_image(src, dst)
        self.next_image()
    
    def delete_image(self):
        src = os.path.join(self.folder_path, self.image_files[self.current_index])
        photo_manager.delete_image(src)
        self.next_image()
    
    def next_image(self):
        self.current_index += 1
        if self.current_index < len(self.image_files):
            self.show_image()
        else:
            self.label.config(text="Semua foto telah diproses!")
            self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoSortApp(root)
    root.mainloop()
