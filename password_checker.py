import tkinter as tk
from tkinter import ttk
import re
import random
import string
import nltk
from nltk.corpus import words

# Download NLTK corpus if not already available
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

english_words = set(words.words())

# ---------------- Password Logic ----------------
def check_password_strength(password):
    suggestions = []

    if len(password) < 8:
        return "Weak", ["Use at least 8 characters."]

    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

    if not (has_upper and has_lower):
        suggestions.append("Use both uppercase and lowercase letters.")
    if not has_digit:
        suggestions.append("Include at least one number.")
    if not has_special:
        suggestions.append("Include at least one special character (!, @, #, etc).")

    if password.lower() in english_words:
        suggestions.append("Avoid using dictionary words.")

    if suggestions:
        return "Weak", suggestions
    else:
        return "Strong", ["✅ Excellent! Your password is strong."]

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))

# ---------------- GUI Logic ----------------
def evaluate_password():
    password = entry.get()
    if not password:
        result_label.config(text="Please enter a password.", fg="red")
        suggestion_text.delete("1.0", tk.END)
        progress_bar['value'] = 0
        generate_btn.pack_forget()
        return

    strength, suggestions = check_password_strength(password)

    result_label.config(
        text=f"Strength: {strength} {'🔴' if strength == 'Weak' else '🟢'}",
        fg="red" if strength == "Weak" else "green"
    )

    progress_bar['value'] = 33 if strength == "Weak" else 100

    suggestion_text.delete("1.0", tk.END)
    for s in suggestions:
        suggestion_text.insert(tk.END, f"• {s}\n")

    generate_btn.pack(pady=10)

def generate_and_fill_password():
    new_pwd = generate_password()
    entry.delete(0, tk.END)
    entry.insert(0, new_pwd)
    evaluate_password()

def toggle_password():
    if entry.cget('show') == '*':
        entry.config(show='')
        toggle_btn.config(text='🙈 Hide')
    else:
        entry.config(show='*')
        toggle_btn.config(text='👁 Show')

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("🔐 Password Strength Checker")
root.geometry("500x560")
root.configure(bg="#f9f9f9")

# Title
tk.Label(root, text="🔐 Password Strength Checker", font=("Helvetica", 16, "bold"), bg="#f9f9f9").pack(pady=10)

# Input Area
entry_frame = tk.Frame(root, bg="#f9f9f9")
entry_frame.pack()

entry = tk.Entry(entry_frame, show="*", font=("Arial", 14), width=30)
entry.pack(side="left", padx=5)

toggle_btn = tk.Button(entry_frame, text="👁 Show", command=toggle_password, bg="lightgray")
toggle_btn.pack(side="left")

check_btn = tk.Button(root, text="Check Strength", font=("Arial", 12, "bold"), command=evaluate_password, bg="#007bff", fg="white")
check_btn.pack(pady=10)

# Result
result_label = tk.Label(root, text="", font=("Arial", 14), bg="#f9f9f9")
result_label.pack(pady=5)

# Progress Bar
style = ttk.Style()
style.theme_use('clam')
style.configure("green.Horizontal.TProgressbar", troughcolor='white', background='green')
progress_bar = ttk.Progressbar(root, style="green.Horizontal.TProgressbar", orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=5)

# Suggestions
tk.Label(root, text="Suggestions:", font=("Arial", 12, "bold"), bg="#f9f9f9").pack()
suggestion_text = tk.Text(root, height=5, width=50, font=("Arial", 10))
suggestion_text.pack(pady=5)

# Generate Button (Initially hidden)
generate_btn = tk.Button(root, text="🎲 Generate Strong Password", command=generate_and_fill_password, bg="green", fg="white", font=("Arial", 11, "bold"))

# Info Section
tk.Label(root, text="What makes a strong password?", font=("Arial", 12, "bold"), bg="#f9f9f9", fg="blue").pack(pady=10)
info = """✔ At least 8 characters
✔ Mix of uppercase and lowercase letters
✔ Include numbers (0–9)
✔ Include special symbols (! @ # $)
✔ Avoid using dictionary words or personal info"""
tk.Label(root, text=info, font=("Arial", 10), bg="#f9f9f9", justify="left", fg="#333333").pack()

# Footer
tk.Label(root, text="Made with ❤️ using Python & Tkinter", font=("Arial", 9), bg="#f9f9f9", fg="gray").pack(side="bottom", pady=10)

root.mainloop()
