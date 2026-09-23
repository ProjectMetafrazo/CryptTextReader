import tkinter as tk
from tkinter import messagebox, filedialog
from crypto import encrypt_text, decrypt_text


def encrypt():
    text = input_box.get("1.0", tk.END).strip()
    password = password_box.get()

    if not text or not password:
        messagebox.showwarning(
            "Warning",
            "Please enter text and password."
        )
        return

    try:
        result = encrypt_text(text, password)

        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, result)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def decrypt():
    text = input_box.get("1.0", tk.END).strip()
    password = password_box.get()

    if not text or not password:
        messagebox.showwarning(
            "Warning",
            "Please enter encrypted text and password."
        )
        return

    try:
        result = decrypt_text(text, password)

        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, result)

    except Exception:
        messagebox.showerror(
            "Error",
            "Wrong password or invalid encrypted text."
        )


def toggle_password():
    if password_box.cget("show") == "*":
        password_box.config(show="")
        toggle_button.config(text="Hide")
    else:
        password_box.config(show="*")
        toggle_button.config(text="Show")


def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            input_box.delete("1.0", tk.END)
            input_box.insert(tk.END, text)

        except Exception as e:
            messagebox.showerror("Error", str(e))


def save_encrypted_file():
    result = output_box.get("1.0", tk.END).strip()

    if not result:
        messagebox.showwarning(
            "Warning",
            "There is no encrypted text to save."
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".enc",
        filetypes=[
            ("Encrypted Files", "*.enc"),
            ("Text Files", "*.txt")
        ]
    )

    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(result)

            messagebox.showinfo(
                "Success",
                "Encrypted file saved successfully."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))


def load_encrypted_file():
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Encrypted Files", "*.enc"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                encrypted_text = file.read()

            input_box.delete("1.0", tk.END)
            input_box.insert(tk.END, encrypted_text)

        except Exception as e:
            messagebox.showerror("Error", str(e))


def copy_result():
    result = output_box.get("1.0", tk.END).strip()

    if result:
        root.clipboard_clear()
        root.clipboard_append(result)

        messagebox.showinfo(
            "Copied",
            "Result copied to clipboard."
        )


def clear():
    input_box.delete("1.0", tk.END)
    password_box.delete(0, tk.END)
    output_box.delete("1.0", tk.END)


# -----------------------------
# Main Window
# -----------------------------

root = tk.Tk()

root.title("CryptText Reader")
root.geometry("750x750")
root.resizable(False, False)
root.configure(bg="#121212")


# -----------------------------
# Title
# -----------------------------

title = tk.Label(
    root,
    text="🔐 CryptText Reader",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#121212"
)

title.pack(pady=20)


# -----------------------------
# Input Label
# -----------------------------

input_label = tk.Label(
    root,
    text="Enter Text / Encrypted Text",
    font=("Arial", 12, "bold"),
    fg="white",
    bg="#121212"
)

input_label.pack(anchor="w", padx=40)


# -----------------------------
# Input Box
# -----------------------------

input_box = tk.Text(
    root,
    height=7,
    width=70,
    font=("Arial", 11),
    bg="#1e1e1e",
    fg="white",
    insertbackground="white"
)

input_box.pack(
    padx=40,
    pady=10
)


# -----------------------------
# Password Label
# -----------------------------

password_label = tk.Label(
    root,
    text="Password",
    font=("Arial", 12, "bold"),
    fg="white",
    bg="#121212"
)

password_label.pack(
    anchor="w",
    padx=40
)


# -----------------------------
# Password Box + Toggle
# -----------------------------

password_frame = tk.Frame(
    root,
    bg="#121212"
)

password_frame.pack(
    pady=10
)


password_box = tk.Entry(
    password_frame,
    width=42,
    show="*",
    font=("Arial", 12),
    bg="#1e1e1e",
    fg="white",
    insertbackground="white"
)

password_box.grid(
    row=0,
    column=0,
    padx=(0, 8)
)


toggle_button = tk.Button(
    password_frame,
    text="Show",
    command=toggle_password,
    width=8,
    font=("Arial", 10, "bold")
)

toggle_button.grid(
    row=0,
    column=1
)


# -----------------------------
# Encrypt / Decrypt Buttons
# -----------------------------

button_frame = tk.Frame(
    root,
    bg="#121212"
)

button_frame.pack(
    pady=10
)


encrypt_button = tk.Button(
    button_frame,
    text="🔒 Encrypt",
    command=encrypt,
    width=15,
    font=("Arial", 11, "bold"),
    bg="#6C4AB6",
    fg="white"
)

encrypt_button.grid(
    row=0,
    column=0,
    padx=10
)


decrypt_button = tk.Button(
    button_frame,
    text="🔓 Decrypt",
    command=decrypt,
    width=15,
    font=("Arial", 11, "bold"),
    bg="#4A7AB6",
    fg="white"
)

decrypt_button.grid(
    row=0,
    column=1,
    padx=10
)


# -----------------------------
# File Buttons
# -----------------------------

file_frame = tk.Frame(
    root,
    bg="#121212"
)

file_frame.pack(
    pady=10
)


open_button = tk.Button(
    file_frame,
    text="📂 Open Text File",
    command=open_file,
    width=18,
    font=("Arial", 10, "bold")
)

open_button.grid(
    row=0,
    column=0,
    padx=5
)


load_button = tk.Button(
    file_frame,
    text="🔐 Load Encrypted File",
    command=load_encrypted_file,
    width=20,
    font=("Arial", 10, "bold")
)

load_button.grid(
    row=0,
    column=1,
    padx=5
)


save_button = tk.Button(
    file_frame,
    text="💾 Save Encrypted File",
    command=save_encrypted_file,
    width=20,
    font=("Arial", 10, "bold")
)

save_button.grid(
    row=0,
    column=2,
    padx=5
)


# -----------------------------
# Result Label
# -----------------------------

output_label = tk.Label(
    root,
    text="Result",
    font=("Arial", 12, "bold"),
    fg="white",
    bg="#121212"
)

output_label.pack(
    anchor="w",
    padx=40,
    pady=(15, 0)
)


# -----------------------------
# Result Box
# -----------------------------

output_box = tk.Text(
    root,
    height=7,
    width=70,
    font=("Arial", 11),
    bg="#1e1e1e",
    fg="white",
    insertbackground="white"
)

output_box.pack(
    padx=40,
    pady=10
)


# -----------------------------
# Copy / Clear Buttons
# -----------------------------

bottom_frame = tk.Frame(
    root,
    bg="#121212"
)

bottom_frame.pack(
    pady=10
)


copy_button = tk.Button(
    bottom_frame,
    text="📋 Copy",
    command=copy_result,
    width=12,
    font=("Arial", 10, "bold")
)

copy_button.grid(
    row=0,
    column=0,
    padx=10
)


clear_button = tk.Button(
    bottom_frame,
    text="🗑 Clear",
    command=clear,
    width=12,
    font=("Arial", 10, "bold")
)

clear_button.grid(
    row=0,
    column=1,
    padx=10
)


# -----------------------------
# Start Application
# -----------------------------

root.mainloop()