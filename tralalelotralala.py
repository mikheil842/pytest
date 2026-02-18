import tkinter as tk
from tkinter import filedialog, messagebox

current_file = None

def new_file():
    global current_file
    text_area.delete(1.0, tk.END)
    current_file = None
    root.title("Untitled - ტექსტური რედაქტორი")

def open_file():
    global current_file
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, file.read())
            current_file = file_path
            root.title(f"{file_path} - ტექსტური რედაქტორი")
        except Exception as e:
            messagebox.showerror("შეცდომა", f"ფაილის გახსნა ვერ მოხერხდა:\n{e}")

def save_file():
    global current_file
    if current_file:
        try:
            with open(current_file, "w", encoding="utf-8") as file:
                file.write(text_area.get(1.0, tk.END))
        except Exception as e:
            messagebox.showerror("შეცდომა", f"ფაილის შენახვა ვერ მოხერხდა:\n{e}")
    else:
        save_as_file()

def save_as_file():
    global current_file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        current_file = file_path
        save_file()
        root.title(f"{file_path} - ტექსტური რედაქტორი")

def exit_app():
    if messagebox.askokcancel("გასვლა", "ნამდვილად გსურთ პროგრამიდან გასვლა?"):
        root.destroy()

# --- რედაქტირების ფუნქციები ---

def undo():
    try:
        text_area.edit_undo()
    except:
        pass

def redo():
    try:
        text_area.edit_redo()
    except:
        pass

def cut():
    text_area.event_generate("<<Cut>>")

def copy():
    text_area.event_generate("<<Copy>>")

def paste():
    text_area.event_generate("<<Paste>>")

def select_all():
    text_area.tag_add("sel", "1.0", "end")

# მთავარი ფანჯარა
root = tk.Tk()
root.title("ტექსტური რედაქტორი")
root.geometry("800x600")

# მენიუს ზოლი
menu_bar = tk.Menu(root)

# File მენიუ
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit მენიუ
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

root.config(menu=menu_bar)

# ტექსტის სამუშაო არე (Undo აქტიური)
text_area = tk.Text(root, wrap="word", font=("Arial", 12), undo=True)
text_area.pack(expand=True, fill="both")

# კლავიატურის მალსახმობები
root.bind("<Control-n>", lambda event: new_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-a>", lambda event: select_all())
root.bind("<Control-z>", lambda event: undo())
root.bind("<Control-y>", lambda event: redo())

root.mainloop()
