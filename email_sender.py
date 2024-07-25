import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import os
from datetime import datetime, timedelta
import json
import requests
import zipfile
import sys

recipient_file_path = ""
sent_emails_file_path = "sent_emails.txt"
email_count_file_path = "email_count.json"
stop_sending = False

# Saatlik, günlük ve dakikalık limitler
MAX_EMAILS_PER_HOUR = 300
MAX_EMAILS_PER_DAY = 5000
MAX_EMAILS_PER_MINUTE = 30
MAX_RECIPIENTS = 500

def browse_file():
    global recipient_file_path
    recipient_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if recipient_file_path:
        file_label.config(text=f"Seçilen Dosya: {recipient_file_path}")

def load_sent_emails():
    if os.path.exists(sent_emails_file_path):
        with open(sent_emails_file_path, 'r') as file:
            return {line.strip() for line in file.readlines()}
    return set()

def save_sent_email(email):
    with open(sent_emails_file_path, 'a') as file:
        file.write(email + '\n')

def load_email_counts():
    if os.path.exists(email_count_file_path):
        with open(email_count_file_path, 'r') as file:
            return json.load(file)
    return {
        "emails_sent_in_hour": 0,
        "emails_sent_in_day": 0,
        "emails_sent_in_minute": 0,
        "hour_start_time": str(datetime.now()),
        "day_start_time": str(datetime.now()),
        "minute_start_time": str(datetime.now()),
        "last_email_sent_time": str(datetime.now())
    }

def save_email_counts(counts):
    with open(email_count_file_path, 'w') as file:
        json.dump(counts, file)

def check_limits(counts, recipients_to_send):
    current_time = datetime.now()
    emails_sent_in_hour = counts["emails_sent_in_hour"]
    emails_sent_in_day = counts["emails_sent_in_day"]
    emails_sent_in_minute = counts["emails_sent_in_minute"]
    hour_start_time = datetime.fromisoformat(counts["hour_start_time"])
    day_start_time = datetime.fromisoformat(counts["day_start_time"])
    minute_start_time = datetime.fromisoformat(counts["minute_start_time"])

    remaining_recipients = min(len(recipients_to_send), MAX_RECIPIENTS)

    # Günlük limit kontrolü
    if (current_time - day_start_time).days >= 1:
        emails_sent_in_day = 0
        counts["day_start_time"] = str(current_time)
    if emails_sent_in_day + remaining_recipients > MAX_EMAILS_PER_DAY:
        remaining_recipients = MAX_EMAILS_PER_DAY - emails_sent_in_day

    # Saatlik limit kontrolü
    if (current_time - hour_start_time).seconds >= 3600:
        emails_sent_in_hour = 0
        counts["hour_start_time"] = str(current_time)
    if emails_sent_in_hour + remaining_recipients > MAX_EMAILS_PER_HOUR:
        remaining_recipients = min(remaining_recipients, MAX_EMAILS_PER_HOUR - emails_sent_in_hour)

    # Dakikalık limit kontrolü
    if (current_time - minute_start_time).seconds >= 60:
        emails_sent_in_minute = 0
        counts["minute_start_time"] = str(current_time)
    if emails_sent_in_minute + remaining_recipients > MAX_EMAILS_PER_MINUTE:
        remaining_recipients = min(remaining_recipients, MAX_EMAILS_PER_MINUTE - emails_sent_in_minute)

    save_email_counts(counts)
    return remaining_recipients

def send_email(sender_email, password, subject, message, recipient_list, delay):
    global stop_sending
    try:
        # SMTP sunucusuna bağlanma
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(sender_email, password)

        counts = load_email_counts()
        emails_sent_in_hour = counts["emails_sent_in_hour"]
        emails_sent_in_day = counts["emails_sent_in_day"]
        emails_sent_in_minute = counts["emails_sent_in_minute"]
        hour_start_time = datetime.fromisoformat(counts["hour_start_time"])
        day_start_time = datetime.fromisoformat(counts["day_start_time"])
        minute_start_time = datetime.fromisoformat(counts["minute_start_time"])

        unique_recipients = set()

        for i, recipient in enumerate(recipient_list):
            if stop_sending:
                log_message("E-posta gönderimi durduruldu.")
                break

            current_time = datetime.now()

            # Günlük limit kontrolü
            if (current_time - day_start_time).days >= 1:
                day_start_time = current_time
                emails_sent_in_day = 0

            if emails_sent_in_day >= MAX_EMAILS_PER_DAY:
                wait_time = 24 * 60 * 60 - (current_time - day_start_time).seconds
                log_message(f"Günlük limitine ulaşıldı. {wait_time // 3600} saat {wait_time % 3600 // 60} dakika bekleniyor...")
                time.sleep(wait_time)
                day_start_time = datetime.now()
                emails_sent_in_day = 0

            # Saatlik limit kontrolü
            if (current_time - hour_start_time).seconds >= 3600:
                hour_start_time = current_time
                emails_sent_in_hour = 0

            if emails_sent_in_hour >= MAX_EMAILS_PER_HOUR:
                wait_time = 3600 - (current_time - hour_start_time).seconds
                log_message(f"Saatlik limitine ulaşıldı. {wait_time // 60} dakika bekleniyor...")
                time.sleep(wait_time)
                hour_start_time = datetime.now()
                emails_sent_in_hour = 0

            # Dakikalık limit kontrolü
            if (current_time - minute_start_time).seconds >= 60:
                minute_start_time = current_time
                emails_sent_in_minute = 0

            if emails_sent_in_minute >= MAX_EMAILS_PER_MINUTE:
                wait_time = 60 - (current_time - minute_start_time).seconds
                log_message(f"Dakikalık limitine ulaşıldı. {wait_time} saniye bekleniyor...")
                time.sleep(wait_time)
                minute_start_time = datetime.now()
                emails_sent_in_minute = 0

            try:
                # E-posta oluşturma
                email = MIMEMultipart()
                email['From'] = sender_email
                email['To'] = recipient
                email['Subject'] = subject
                email.attach(MIMEText(message, 'plain'))

                # E-postayı gönderme
                server.sendmail(sender_email, recipient, email.as_string())
                save_sent_email(recipient)
                log_message(f"{recipient} adresine e-posta gönderildi.")
                unique_recipients.add(recipient)
                emails_sent_in_hour += 1
                emails_sent_in_day += 1
                emails_sent_in_minute += 1
                counts["last_email_sent_time"] = str(current_time)
                time.sleep(delay)  # Kullanıcının belirlediği bekleme süresi

            except Exception as e:
                log_message(f"{recipient} adresine e-posta gönderilemedi: {str(e)}")

        counts["emails_sent_in_hour"] = emails_sent_in_hour
        counts["emails_sent_in_day"] = emails_sent_in_day
        counts["emails_sent_in_minute"] = emails_sent_in_minute
        counts["hour_start_time"] = str(hour_start_time)
        counts["day_start_time"] = str(day_start_time)
        counts["minute_start_time"] = str(minute_start_time)
        save_email_counts(counts)

        server.quit()
        return f"E-postalar başarıyla gönderildi. Farklı alıcı sayısı: {len(unique_recipients)}"
    except Exception as e:
        return f"E-postalar gönderilirken bir hata oluştu: {str(e)}"

def log_message(message):
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)

def send_emails():
    global stop_sending
    stop_sending = False

    if not recipient_file_path:
        messagebox.showerror("Hata", "Lütfen bir dosya seçin.")
        return

    with open(recipient_file_path, 'r') as file:
        all_recipients = [line.strip() for line in file.readlines()]

    sent_emails = load_sent_emails()
    recipients_to_send = [email for email in all_recipients if email not in sent_emails]

    sender_email = email_entry.get()
    password = password_entry.get()
    subject = subject_entry.get()
    message = message_entry.get("1.0", tk.END)

    try:
        delay = int(delay_entry.get())
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin.")
        return

    limit = check_limits(load_email_counts(), recipients_to_send)
    num_emails_to_send = min(limit, int(num_emails_entry.get()))
    
    if num_emails_to_send <= 0:
        messagebox.showerror("Hata", "Gönderilebilecek e-posta sayısı yok veya limit aşıldı.")
        return

    result = send_email(sender_email, password, subject, message, recipients_to_send[:num_emails_to_send], delay)
    log_message(result)

    messagebox.showinfo("Sonuç", "E-posta gönderim işlemi tamamlandı.")
    update_counts_display()

def start_sending_emails():
    thread = threading.Thread(target=send_emails)
    thread.start()

def stop_sending_emails():
    global stop_sending
    stop_sending = True

def update_counts_display():
    counts = load_email_counts()
    counts_display.config(state=tk.NORMAL)
    counts_display.delete(1.0, tk.END)
    counts_display.insert(tk.END, f"Son 1 Dakikada Gönderilen E-postalar: {counts.get('emails_sent_in_minute', 0)}\n")
    counts_display.insert(tk.END, f"Son 1 Saatte Gönderilen E-postalar: {counts['emails_sent_in_hour']}\n")
    counts_display.insert(tk.END, f"Son 1 Günde Gönderilen E-postalar: {counts['emails_sent_in_day']}\n")
    last_email_sent_time = counts.get('last_email_sent_time', None)
    if last_email_sent_time:
        last_email_sent_time = datetime.fromisoformat(last_email_sent_time)
        counts_display.insert(tk.END, f"Son E-posta Gönderim Zamanı: {last_email_sent_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    counts_display.config(state=tk.DISABLED)

def update_email_counts_periodically():
    while True:
        update_counts_display()
        time.sleep(60)

def check_for_updates(repo_url, current_version, root):
    try:
        response = requests.get(repo_url)
        response.raise_for_status()
        latest_version = response.json()["tag_name"]
        if latest_version != current_version:
            messagebox.showinfo("Güncelleme", "Güncelleme mevcut! Uygulama güncelleniyor...")
            download_and_update(response.json()["zipball_url"])
        else:
            log_message("Yazılımınız güncel.")
    except Exception as e:
        messagebox.showerror("Güncelleme Hatası", f"Güncellemeler kontrol edilirken bir hata oluştu: {str(e)}")

def download_and_update(zip_url):
    try:
        response = requests.get(zip_url)
        response.raise_for_status()
        with open("update.zip", "wb") as file:
            file.write(response.content)
        with zipfile.ZipFile("update.zip", "r") as zip_ref:
            zip_ref.extractall("update")
        for root, dirs, files in os.walk("update"):
            for file in files:
                os.replace(os.path.join(root, file), file)
        os.remove("update.zip")
        os.rmdir("update")
        messagebox.showinfo("Güncelleme", "Güncelleme tamamlandı. Uygulama yeniden başlatılıyor...")
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        messagebox.showerror("Güncelleme Hatası", f"Güncelleme sırasında bir hata oluştu: {str(e)}")

# Mevcut sürüm ve GitHub API URL'si
current_version = "v1.0.0"
repo_url = "https://api.github.com/repos/kullanici_adi/eposta_sender/releases/latest"

# Kullanıcı arayüzü oluşturma
root = tk.Tk()
root.title("Toplu E-posta Gönderimi")

# Responsive layout için column ve row configure
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_rowconfigure(8, weight=1)
root.grid_rowconfigure(9, weight=1)

tk.Label(root, text="Gönderici E-posta Adresi:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
email_entry = tk.Entry(root, width=50)
email_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

tk.Label(root, text="Gönderici Şifre:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
password_entry = tk.Entry(root, show="*", width=50)
password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

tk.Label(root, text="Konu:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
subject_entry = tk.Entry(root, width=50)
subject_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

tk.Label(root, text="Mesaj:").grid(row=3, column=0, padx=10, pady=10, sticky="ne")
message_entry = tk.Text(root, width=50, height=10)
message_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

tk.Button(root, text="Dosya Seç", command=browse_file).grid(row=4, column=0, padx=10, pady=10, sticky="ew")
file_label = tk.Label(root, text="Henüz dosya seçilmedi.")
file_label.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

tk.Label(root, text="Gönderilecek Kişi Sayısı:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
num_emails_entry = tk.Entry(root, width=10)
num_emails_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

tk.Label(root, text="Bekleme Süresi (saniye):").grid(row=6, column=0, padx=10, pady=10, sticky="e")
delay_entry = tk.Entry(root, width=10)
delay_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

tk.Button(root, text="Gönder", command=start_sending_emails).grid(row=7, column=0, padx=10, pady=10, sticky="ew")
tk.Button(root, text="Durdur", command=stop_sending_emails).grid(row=7, column=1, padx=10, pady=10, sticky="ew")

log_text = tk.Text(root, width=80, height=10)
log_text.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

tk.Label(root, text="E-posta Gönderim Bilgileri:").grid(row=9, column=0, padx=10, pady=10, sticky="ne")
counts_display = tk.Text(root, width=50, height=5, state=tk.DISABLED)
counts_display.grid(row=9, column=1, padx=10, pady=10, sticky="ew")

update_counts_display()

# E-posta gönderim bilgilerini periyodik olarak güncelleyen bir iş parçacığı başlat
threading.Thread(target=update_email_counts_periodically, daemon=True).start()

# Güncellemeleri kontrol et
threading.Thread(target=check_for_updates, args=(repo_url, current_version, root), daemon=True).start()

root.mainloop()


