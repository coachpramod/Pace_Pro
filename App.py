import tkinter as tk
from tkinter import messagebox

def format_pace(decimal_minutes):
    """Converts decimal minutes (e.g., 7.5) to MM:SS string."""
    if decimal_minutes < 0: return "0:00"
    minutes = int(decimal_minutes)
    seconds = int(round((decimal_minutes - minutes) * 60))
    if seconds == 60:
        minutes += 1
        seconds = 0
    return f"{minutes}:{seconds:02d}"

def calculate_paces():
    try:
        # B1 in your Excel formula is the target 10k time
        b1_target = float(entry_target.get())
        
        # Your base formula: ($B$1/10)
        base = b1_target / 10
        
        # Applying your specific multipliers
        logic = {
            "--- RACE PACES ---": None,
            "10K Pace": base * 1.0,
            "Marathon": base * 1.085,
            "Half Marathon": base * 1.05,
            "5K Pace": base * 0.96,
            "3K Pace": base * 0.93,
            "--- TRAINING ZONES ---": None,
            "Easy (Aerobic)": base * 1.22,
            "Steady": base * 1.07,
            "Threshold": base * 0.965,
            "Hills Reps": base * 0.88,
            "Intervals / Reps": base * 0.85
        }
        
        # Refresh the display
        for widget in result_frame.winfo_children():
            widget.destroy()
            
        for name, pace in logic.items():
            if pace is None:
                lbl = tk.Label(result_frame, text=name, fg="#00ced1", bg="#031633", font=("Arial", 10, "bold"))
            else:
                display_text = f"{name:18} |  {format_pace(pace)} min/km"
                lbl = tk.Label(result_frame, text=display_text, fg="white", bg="#031633", font=("Consolas", 11))
            lbl.pack(anchor="w", pady=2)
            
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number (e.g., 71)")

# UI Construction
root = tk.Tk()
root.title("Pace Pro 2026 - Windows Edition")
root.geometry("480x680")
root.configure(bg="#031633")

# Header
tk.Label(root, text="RUNNING PACE CALCULATOR", fg="#00ced1", bg="#031633", font=("Arial", 14, "bold")).pack(pady=20)

# Input Section
input_frame = tk.Frame(root, bg="#031633")
input_frame.pack(pady=10)
tk.Label(input_frame, text="10K Target (Minutes):", fg="white", bg="#031633", font=("Arial", 11)).pack(side=tk.LEFT, padx=10)
entry_target = tk.Entry(input_frame, font=("Arial", 12), width=10, justify='center', insertbackground='white')
entry_target.pack(side=tk.LEFT)
entry_target.insert(0, "71")

# Calculate Button
btn = tk.Button(root, text="GENERATE TABLES", command=calculate_paces, bg="#1e90ff", fg="white", font=("Arial", 10, "bold"), padx=20, pady=5, cursor="hand2")
btn.pack(pady=20)

# Results Display
result_frame = tk.Frame(root, bg="#031633", bd=1, relief=tk.FLAT, padx=20, pady=20)
result_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

# Run initial calc
calculate_paces()

root.mainloop()