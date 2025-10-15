# Import the tkinter library for GUI creation
import tkinter as tk

# Import the string module for character sets
import string

# Import the json module for saving/loading user data
import json

# Import the logging module for recording program events
import logging

# Import the os module for checking file existence
import os


# ---- LOGGING SETUP ----
# Create a logger object for logging messages
logger = logging.getLogger()

# Set the logging level to INFO (records info, warnings, and errors)
logger.setLevel(logging.INFO)

# Remove any pre-existing handlers to avoid duplicate logs
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Define the format for log messages (time, level, and message)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Create a file handler that writes general program logs to a text file
file_handler = logging.FileHandler("program_log.txt", mode="a", encoding="utf-8")

# Set the level of the file handler to INFO (won’t log debug messages)
file_handler.setLevel(logging.INFO)

# Apply the formatter to the file handler
file_handler.setFormatter(formatter)

# Create a console handler that displays logs in the terminal
console_handler = logging.StreamHandler()

# Set the console handler to INFO level
console_handler.setLevel(logging.INFO)

# Apply the same formatter to the console handler
console_handler.setFormatter(formatter)

# Create a second file handler that records only errors
error_handler = logging.FileHandler("errors.log", mode="a", encoding="utf-8")

# Set this handler to capture only ERROR-level logs
error_handler.setLevel(logging.ERROR)

# Apply the formatter to the error handler as well
error_handler.setFormatter(formatter)

# Attach all handlers (file, console, error) to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(error_handler)

# Log that the program has started
logger.info("Program spuštěn.")


# ---- UŽIVATELÉ (USER SYSTEM) ----
# Define the path for the users file
users_file = "users.json"

# Check if the users.json file exists
if os.path.exists(users_file):
    # If it exists, load the user data
    with open(users_file, "r", encoding="utf-8") as f:
        users = json.load(f)
else:
    # If it doesn't exist, create a default user ("admin": "admin")
    users = {"admin": "admin"}
    # Save this default data to the file
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# Function to save users back into users.json when they register
def save_users():
    # Open the file in write mode and save the updated dictionary
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


# ---- ŠIFROVÁNÍ (ENCRYPTION) ----
# Define the lowercase alphabet as keys
klice = string.ascii_lowercase

# Define the first 26 punctuation marks as replacement values
hodnoty = string.punctuation[:26]

# Create a translation table for encryption
tab_sifruj = str.maketrans(klice, hodnoty)

# Create a translation table for decryption
tab_desifruj = str.maketrans(hodnoty, klice)

# Define the encryption function
def zasifruj(text):
    # Convert text to lowercase and translate letters into punctuation
    return text.lower().translate(tab_sifruj)

# Define the decryption function
def desifruj(text):
    # Translate punctuation back into letters
    return text.translate(tab_desifruj)


# ---- GUI (GRAPHICAL USER INTERFACE) ----
# Create the main application window
window = tk.Tk()

# Set the size of the main window
window.geometry("400x400")

# Set the title of the window
window.title("Login")

# Set the background color to light blue
window.configure(bg="lightblue")

# Create a frame for the login elements
frame_login = tk.Frame(window, bg="lightblue")

# Add the frame to the window with padding
frame_login.pack(pady=20)

# Add a label prompting the user for their username
tk.Label(frame_login, text="Uživatelské jméno:", bg="lightblue").pack()

# Create an input box for the username
entry_user = tk.Entry(frame_login)
entry_user.pack()

# Add a label prompting the user for their password
tk.Label(frame_login, text="Heslo:", bg="lightblue").pack()

# Create an input box for the password (hidden with "*")
entry_pass = tk.Entry(frame_login, show="*")
entry_pass.pack()

# Create a label for displaying login messages
msg_label = tk.Label(frame_login, text="", bg="lightblue")
msg_label.pack()


# ---- REGISTER WINDOW ----
# Function to open the registration window
def open_register_window():
    # Create a new top-level window for registration
    reg_win = tk.Toplevel(window)
    reg_win.title("Registrovat")  # Set title
    reg_win.geometry("350x250")   # Set size

    # Username label and entry
    tk.Label(reg_win, text="Nový uživatel:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_new_user = tk.Entry(reg_win)
    entry_new_user.grid(row=0, column=1, padx=5, pady=5)

    # Password label and entry
    tk.Label(reg_win, text="Heslo:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_new_pass = tk.Entry(reg_win, show="*")
    entry_new_pass.grid(row=1, column=1, padx=5, pady=5)

    # Button to toggle password visibility
    btn_show1 = tk.Button(reg_win, text="Zobrazit")
    btn_show1.grid(row=1, column=2, padx=5)

    # Confirm password label and entry
    tk.Label(reg_win, text="Potvrdit heslo:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_conf_pass = tk.Entry(reg_win, show="*")
    entry_conf_pass.grid(row=2, column=1, padx=5, pady=5)

    # Button to toggle confirm password visibility
    btn_show2 = tk.Button(reg_win, text="Zobrazit")
    btn_show2.grid(row=2, column=2, padx=5)

    # Label for registration messages
    msg_reg = tk.Label(reg_win, text="")
    msg_reg.grid(row=4, column=0, columnspan=3, pady=10)

    # Function to show/hide password field
    def toggle_pass1():
        if entry_new_pass.cget("show") == "*":
            entry_new_pass.config(show="")        # Show password
            btn_show1.config(text="Schovat")      # Change button text
        else:
            entry_new_pass.config(show="*")       # Hide password
            btn_show1.config(text="Zobrazit")     # Change button text back

    # Assign the toggle function to the button
    btn_show1.config(command=toggle_pass1)

    # Function to show/hide confirm password field
    def toggle_pass2():
        if entry_conf_pass.cget("show") == "*":
            entry_conf_pass.config(show="")        # Show password
            btn_show2.config(text="Schovat")       # Change text
        else:
            entry_conf_pass.config(show="*")       # Hide password
            btn_show2.config(text="Zobrazit")      # Change back

    # Assign the function to button
    btn_show2.config(command=toggle_pass2)

    # Function to register a new user
    def register_user():
        u = entry_new_user.get()   # Get username
        p = entry_new_pass.get()   # Get password
        c = entry_conf_pass.get()  # Get confirmed password

        # Check if username already exists
        if u in users:
            msg_reg.config(text="Uživatel už existuje!", fg="red")
            logger.warning(f"Pokus o registraci existujícího uživatele: {u}")
        # Check if passwords match
        elif p != c:
            msg_reg.config(text="Hesla se neshodují!", fg="red")
            logger.warning(f"Neshodná hesla při registraci uživatele: {u}")
        # Check password length constraints
        elif len(p) < 6 or len(p) > 16:
            msg_reg.config(text="Heslo musí mít 6-16 znaků!", fg="red")
            logger.warning(f"Heslo špatné délky při registraci uživatele: {u}")
        # If all checks pass, save the new user
        else:
            users[u] = p
            save_users()
            msg_reg.config(text="Účet úspěšně vytvořen!", fg="green")
            logger.info(f"Nový uživatel zaregistrován: {u}")
            # Automatically close window after 1 second
            reg_win.after(1000, reg_win.destroy)

    # Create the register button
    tk.Button(reg_win, text="Register", command=register_user).grid(row=3, column=0, columnspan=3, pady=10)


# ---- LOGIN FUNKCE ----
# Define the login function
def login():
    u = entry_user.get()  # Get entered username
    p = entry_pass.get()  # Get entered password

    # Check if user exists and password matches
    if u in users and users[u] == p:
        msg_label.config(text="Úspěšně přihlášeno!", fg="green")
        logger.info(f"Uživatel přihlášen: {u}")
        frame_login.pack_forget()  # Hide login form
        show_gif(u)                # Display GIF loading animation
    else:
        msg_label.config(text="Špatné přihlašovací údaje!", fg="red")
        logger.error(f"Neplatný login pokus: {u}")

# Create login and register buttons
tk.Button(frame_login, text="Login", command=login).pack(pady=5)
tk.Button(frame_login, text="Register", command=open_register_window).pack(pady=5)


# ---- ANIMOVANÝ GIF PO LOGINU ----
# Function to show an animated GIF after login
def show_gif(username):
    gif_win = tk.Toplevel(window)        # Create a new top-level window
    gif_win.title("Načítání...")         # Set title
    gif_win.geometry("400x300")          # Set size
    gif_win.configure(bg="black")        # Set background

    frames = []   # List to store frames of the GIF
    i = 0         # Start frame index
    path = r"C:\image\loading.gif"  # Path to your GIF file

    # Load all frames from the GIF
    while True:
        try:
            frame = tk.PhotoImage(file=path, format=f"gif - {i}")
            frames.append(frame)
            i += 1
        except tk.TclError:
            break  # Stop when no more frames

    # Create a label to display the GIF frames
    label = tk.Label(gif_win, bg="black")
    label.pack(expand=True)

    # Function to loop through frames (animation)
    def animace(index=0):
        frame = frames[index]
        label.config(image=frame)
        index = (index + 1) % len(frames)
        gif_win.after(50, animace, index)

    # Start the animation
    animace()

    # Function to open the main app window after delay
    def open_main():
        gif_win.destroy()  # Close the GIF window
        show_main(username)  # Open main screen

    # Wait 2 seconds before calling open_main
    gif_win.after(2000, open_main)


# ---- Hlavní šifrovací část ----
# Function to display the main encryption/decryption window
def show_main(username):
    frame_main = tk.Frame(window)
    frame_main.pack(pady=20)

    # Display the logged-in username
    tk.Label(frame_main, text=f"Přihlášen jako {username}", font=("Arial", 12, "bold")).pack(pady=5)

    # Input label and box for text
    tk.Label(frame_main, text="Zadejte text:").pack()
    entry_text = tk.Entry(frame_main, width=40)
    entry_text.pack(pady=5)

    # Labels to show encrypted and decrypted results
    result_enc = tk.Label(frame_main, text="", fg="blue", wraplength=350, justify="left")
    result_enc.pack(pady=5)
    result_dec = tk.Label(frame_main, text="", fg="green", wraplength=350, justify="left")
    result_dec.pack(pady=5)

    # Define encryption button function
    def sifruj():
        txt = entry_text.get()
        enc = zasifruj(txt)
        result_enc.config(text=f"Zašifrovaný: {enc}")
        logger.info(f"Text zašifrován uživatelem {username}")

    # Define decryption button function
    def desifruj_text():
        txt = entry_text.get()
        dec = desifruj(txt)
        result_dec.config(text=f"Dešifrovaný: {dec}")
        logger.info(f"Text dešifrován uživatelem {username}")

    # Buttons for encrypting and decrypting text
    tk.Button(frame_main, text="Zašifrovat", command=sifruj).pack(pady=5)
    tk.Button(frame_main, text="Dešifrovat", command=desifruj_text).pack(pady=5)


# ---- MAIN LOOP ----
# Start the tkinter event loop (keeps window open)
window.mainloop()
