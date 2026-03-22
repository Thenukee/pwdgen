import secrets
import string
import tkinter as tk
from tkinter import messagebox, ttk


def generate_password(length: int, use_symbols: bool) -> str:
    if length < 8:
        raise ValueError("Password length should be at least 8.")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{};:,.?/"

    if use_symbols:
        all_chars = lowercase + uppercase + digits + symbols
        required_groups = [lowercase, uppercase, digits, symbols]
    else:
        all_chars = lowercase + uppercase + digits
        required_groups = [lowercase, uppercase, digits]

    # Guarantee at least one character from each required group.
    password_chars = [secrets.choice(group) for group in required_groups]

    # Fill remaining length with random characters from the full set.
    while len(password_chars) < length:
        password_chars.append(secrets.choice(all_chars))

    # Shuffle securely to avoid predictable group ordering.
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)


def calculate_strength(password: str) -> tuple[int, str]:
    if not password:
        return 0, "No password"

    score = 0
    if len(password) >= 8:
        score += 20
    if len(password) >= 12:
        score += 20
    if len(password) >= 16:
        score += 20
    if any(c.islower() for c in password):
        score += 10
    if any(c.isupper() for c in password):
        score += 10
    if any(c.isdigit() for c in password):
        score += 10
    if any(c in "!@#$%^&*()-_=+[]{};:,.?/" for c in password):
        score += 10

    score = min(score, 100)
    if score < 40:
        label = "Weak"
    elif score < 70:
        label = "Moderate"
    else:
        label = "Strong"

    return score, label


def update_strength_label(*_args) -> None:
    score, label = calculate_strength(output_var.get())
    strength_bar["value"] = score
    strength_var.set(f"Strength: {label} ({score}%)")


def on_generate() -> None:
    try:
        length = int(length_var.get())
        password = generate_password(length, symbols_var.get())
    except ValueError as exc:
        messagebox.showerror("Invalid Input", str(exc))
        return

    output_var.set(password)
    update_strength_label()


def copy_password() -> None:
    password = output_var.get()
    if not password:
        messagebox.showinfo("Copy Password", "Generate a password first.")
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()
    messagebox.showinfo("Copy Password", "Password copied to clipboard.")


root = tk.Tk()
root.title("Strong Password Generator")
root.geometry("520x300")
root.resizable(False, False)

main_frame = tk.Frame(root, padx=14, pady=14)
main_frame.pack(fill="both", expand=True)

header = tk.Label(main_frame, text="Strong Password Generator", font=("Segoe UI", 14, "bold"))
header.grid(row=0, column=0, columnspan=3, pady=(0, 12), sticky="w")

length_label = tk.Label(main_frame, text="Password Length:", font=("Segoe UI", 10))
length_label.grid(row=1, column=0, sticky="w")

length_var = tk.IntVar(value=16)
length_scale = tk.Scale(
    main_frame,
    from_=8,
    to=64,
    orient="horizontal",
    variable=length_var,
    length=230,
    resolution=1,
)
length_scale.grid(row=1, column=1, sticky="w")

length_value_label = tk.Label(main_frame, textvariable=length_var, width=3, font=("Segoe UI", 10, "bold"))
length_value_label.grid(row=1, column=2, padx=(6, 0), sticky="w")

symbols_var = tk.BooleanVar(value=True)
symbols_check = tk.Checkbutton(
    main_frame,
    text="Include symbols",
    variable=symbols_var,
    font=("Segoe UI", 10),
)
symbols_check.grid(row=2, column=0, columnspan=2, pady=(8, 10), sticky="w")

generate_btn = tk.Button(main_frame, text="Generate", width=14, command=on_generate)
generate_btn.grid(row=2, column=2, padx=(12, 0), sticky="e")

output_label = tk.Label(main_frame, text="Generated Password:", font=("Segoe UI", 10))
output_label.grid(row=3, column=0, columnspan=3, pady=(6, 6), sticky="w")

output_var = tk.StringVar()
output_var.trace_add("write", update_strength_label)
output_entry = tk.Entry(main_frame, textvariable=output_var, width=56, font=("Consolas", 11))
output_entry.grid(row=4, column=0, columnspan=3, sticky="we")

strength_var = tk.StringVar(value="Strength: No password")
strength_label = tk.Label(main_frame, textvariable=strength_var, font=("Segoe UI", 10))
strength_label.grid(row=5, column=0, columnspan=3, pady=(10, 4), sticky="w")

strength_bar = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate", maximum=100)
strength_bar.grid(row=6, column=0, columnspan=3, sticky="we")

copy_btn = tk.Button(main_frame, text="Copy Password", width=14, command=copy_password)
copy_btn.grid(row=7, column=0, columnspan=3, pady=(12, 0), sticky="e")

update_strength_label()

root.mainloop()
