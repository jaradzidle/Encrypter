import tkinter as tk
import string
import json
import logging
import os

# ---- LOGGING SETUP ----
logger = logging.getLogger()
logger.setLevel(logging.INFO)
for handler in logger.handlers[:]:
    logger.removeHandler(handler)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("program_log.txt", mode="a", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

error_handler = logging.FileHandler("errors.log", mode="a", encoding="utf-8")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(error_handler)

logger.info("Program spuštěn.")

# ---- UŽIVATELÉ ----
users_file = "users.json"
if os.path.exists(users_file):
    with open(users_file, "r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = {"admin": "admin"}  # výchozí účet
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def save_users():
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# ---- ŠIFROVÁNÍ ----
klice = string.ascii_lowercase
hodnoty = string.punctuation[:26]
tab_sifruj = str.maketrans(klice, hodnoty)
tab_desifruj = str.maketrans(hodnoty, klice)

def zasifruj(text):
    return text.lower().translate(tab_sifruj)

def desifruj(text):
    return text.translate(tab_desifruj)

# ---- GUI ----
window = tk.Tk()
window.geometry("400x400")
window.title("Login")
window.configure(bg="lightblue")

frame_login = tk.Frame(window, bg="lightblue")
frame_login.pack(pady=20)

tk.Label(frame_login, text="Uživatelské jméno:", bg="lightblue").pack()
entry_user = tk.Entry(frame_login)
entry_user.pack()

tk.Label(frame_login, text="Heslo:", bg="lightblue").pack()
entry_pass = tk.Entry(frame_login, show="*")
entry_pass.pack()

msg_label = tk.Label(frame_login, text="", bg="lightblue")
msg_label.pack()

# ---- REGISTER WINDOW ----
def open_register_window():
    reg_win = tk.Toplevel(window)
    reg_win.title("Registrovat")
    reg_win.geometry("350x250")

    tk.Label(reg_win, text="Nový uživatel:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_new_user = tk.Entry(reg_win)
    entry_new_user.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(reg_win, text="Heslo:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_new_pass = tk.Entry(reg_win, show="*")
    entry_new_pass.grid(row=1, column=1, padx=5, pady=5)
    btn_show1 = tk.Button(reg_win, text="Zobrazit")
    btn_show1.grid(row=1, column=2, padx=5)

    tk.Label(reg_win, text="Potvrdit heslo:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_conf_pass = tk.Entry(reg_win, show="*")
    entry_conf_pass.grid(row=2, column=1, padx=5, pady=5)
    btn_show2 = tk.Button(reg_win, text="Zobrazit")
    btn_show2.grid(row=2, column=2, padx=5)

    msg_reg = tk.Label(reg_win, text="")
    msg_reg.grid(row=4, column=0, columnspan=3, pady=10)

    # toggle heslo 1
    def toggle_pass1():
        if entry_new_pass.cget("show") == "*":
            entry_new_pass.config(show="")
            btn_show1.config(text="Schovat")
        else:
            entry_new_pass.config(show="*")
            btn_show1.config(text="Zobrazit")
    btn_show1.config(command=toggle_pass1)

    # toggle heslo 2
    def toggle_pass2():
        if entry_conf_pass.cget("show") == "*":
            entry_conf_pass.config(show="")
            btn_show2.config(text="Schovat")
        else:
            entry_conf_pass.config(show="*")
            btn_show2.config(text="Zobrazit")
    btn_show2.config(command=toggle_pass2)

    def register_user():
        u = entry_new_user.get()
        p = entry_new_pass.get()
        c = entry_conf_pass.get()

        if u in users:
            msg_reg.config(text="Uživatel už existuje!", fg="red")
            logger.warning(f"Pokus o registraci existujícího uživatele: {u}")
        elif p != c:
            msg_reg.config(text="Hesla se neshodují!", fg="red")
            logger.warning(f"Neshodná hesla při registraci uživatele: {u}")
        elif len(p) < 6 or len(p) > 16:
            msg_reg.config(text="Heslo musí mít 6-16 znaků!", fg="red")
            logger.warning(f"Heslo špatné délky při registraci uživatele: {u}")
        else:
            users[u] = p
            save_users()
            msg_reg.config(text="Účet úspěšně vytvořen!", fg="green")
            logger.info(f"Nový uživatel zaregistrován: {u}")
            reg_win.after(1000, reg_win.destroy)

    tk.Button(reg_win, text="Register", command=register_user).grid(row=3, column=0, columnspan=3, pady=10)

# ---- LOGIN FUNKCE ----
def login():
    u = entry_user.get()
    p = entry_pass.get()
    if u in users and users[u] == p:
        msg_label.config(text="Úspěšně přihlášeno!", fg="green")
        logger.info(f"Uživatel přihlášen: {u}")
        frame_login.pack_forget()
        show_gif(u)  # zobrazí gif místo okamžitého otevření hlavního okna
    else:
        msg_label.config(text="Špatné přihlašovací údaje!", fg="red")
        logger.error(f"Neplatný login pokus: {u}")

tk.Button(frame_login, text="Login", command=login).pack(pady=5)
tk.Button(frame_login, text="Register", command=open_register_window).pack(pady=5)

# ---- ANIMOVANÝ GIF PO LOGINU ----
def show_gif(username):
    gif_win = tk.Toplevel(window)
    gif_win.title("Načítání...")
    gif_win.geometry("400x300")
    gif_win.configure(bg="black")

    frames = []
    i = 0
    path = r"C:\image\loading.gif"

    while True:
        try:
            frame = tk.PhotoImage(file=path, format=f"gif - {i}")
            frames.append(frame)
            i += 1
        except tk.TclError:
            break

    label = tk.Label(gif_win, bg="black")
    label.pack(expand=True)

    def animace(index=0):
        frame = frames[index]
        label.config(image=frame)
        index = (index + 1) % len(frames)
        gif_win.after(50, animace, index)

    animace()

    # Po 3 sekundách zavřít GIF a otevřít hlavní okno
    def open_main():
        gif_win.destroy()
        show_main(username)

    gif_win.after(2000, open_main)

# ---- Hlavní šifrovací část ----
def show_main(username):
    frame_main = tk.Frame(window)
    frame_main.pack(pady=20)

    tk.Label(frame_main, text=f"Přihlášen jako {username}", font=("Arial", 12, "bold")).pack(pady=5)

    tk.Label(frame_main, text="Zadejte text:").pack()
    entry_text = tk.Entry(frame_main, width=40)
    entry_text.pack(pady=5)

    result_enc = tk.Label(frame_main, text="", fg="blue", wraplength=350, justify="left")
    result_enc.pack(pady=5)
    result_dec = tk.Label(frame_main, text="", fg="green", wraplength=350, justify="left")
    result_dec.pack(pady=5)

    def sifruj():
        txt = entry_text.get()
        enc = zasifruj(txt)
        result_enc.config(text=f"Zašifrovaný: {enc}")
        logger.info(f"Text zašifrován uživatelem {username}")

    def desifruj_text():
        txt = entry_text.get()
        dec = desifruj(txt)
        result_dec.config(text=f"Dešifrovaný: {dec}")
        logger.info(f"Text dešifrován uživatelem {username}")

    tk.Button(frame_main, text="Zašifrovat", command=sifruj).pack(pady=5)
    tk.Button(frame_main, text="Dešifrovat", command=desifruj_text).pack(pady=5)

window.mainloop()
