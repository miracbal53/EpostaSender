import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

def convert_excel_to_txt(excel_file_path, txt_file_path):
    try:
        # Excel dosyasını oku
        df = pd.read_excel(excel_file_path, usecols=[0])  # Sadece A sütununu oku

        # E-posta sütununu al
        email_series = df.iloc[:, 0]  # A sütunu

        # E-posta adreslerini bir .txt dosyasına yaz
        with open(txt_file_path, 'w') as txt_file:
            for email in email_series:
                txt_file.write(str(email) + '\n')

        log_message(f"E-posta adresleri {txt_file_path} dosyasına başarıyla kaydedildi.")
    except Exception as e:
        log_message(f"Hata: {str(e)}")

def browse_excel_file():
    excel_file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if excel_file_path:
        excel_file_label.config(text=f"Seçilen Dosya: {excel_file_path}")
        return excel_file_path
    return None

def save_txt_file():
    txt_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if txt_file_path:
        txt_file_label.config(text=f"Kaydedilecek Dosya: {txt_file_path}")
        return txt_file_path
    return None

def start_conversion():
    excel_file_path = browse_excel_file()
    if not excel_file_path:
        messagebox.showerror("Hata", "Lütfen bir Excel dosyası seçin.")
        return

    txt_file_path = save_txt_file()
    if not txt_file_path:
        messagebox.showerror("Hata", "Lütfen kaydedilecek bir .txt dosyası seçin.")
        return

    threading.Thread(target=convert_excel_to_txt, args=(excel_file_path, txt_file_path)).start()

def log_message(message):
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)

# Kullanıcı arayüzü oluşturma
root = tk.Tk()
root.title("Excel'den .txt'ye E-posta Dönüştürücü")

# Responsive layout için column ve row configure
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

tk.Button(root, text="Excel Dosyası Seç ve Dönüştür", command=start_conversion).grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

excel_file_label = tk.Label(root, text="Henüz dosya seçilmedi.")
excel_file_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

txt_file_label = tk.Label(root, text="Henüz kaydedilecek dosya seçilmedi.")
txt_file_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

log_text = tk.Text(root, width=80, height=10)
log_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

root.mainloop()
