import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

DATA_FILE = "data.json"

MOOD_COLORS = {
    "Happy": "green",
    "Sad": "blue",
    "Anxious": "orange",
    "Excited": "purple",
    "Neutral": "gray"
}

# Load existing entries
def load_entries():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save a new entry
def save_entry(mood, journal):
    entries = load_entries()
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mood": mood,
        "journal": journal
    }
    entries.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=4)

# Submit action
def submit():
    mood = mood_var.get()
    journal = journal_text.get("1.0", tk.END).strip()
    if not mood:
        messagebox.showwarning("Missing Mood", "Please select your mood")
        return
    save_entry(mood, journal)
    messagebox.showinfo("Saved", "Your entry has been saved!")
    journal_text.delete("1.0", tk.END)
    mood_var.set(None)
    display_entries()
    display_summary()

# Display past entries
def display_entries():
    entries = load_entries()
    display_text.config(state=tk.NORMAL)
    display_text.delete("1.0", tk.END)
    for entry in reversed(entries):
        color = MOOD_COLORS.get(entry["mood"], "black")
        display_text.insert(tk.END, f"{entry['date']} | Mood: {entry['mood']}\nJournal: {entry['journal']}\n\n", entry["mood"])
        display_text.tag_config(entry["mood"], foreground=color)
    display_text.config(state=tk.DISABLED)

# Display summary counts
def display_summary():
    entries = load_entries()
    summary_text.config(state=tk.NORMAL)
    summary_text.delete("1.0", tk.END)
    mood_counts = {m:0 for m in MOOD_COLORS.keys()}
    for entry in entries:
        mood_counts[entry["mood"]] += 1
    for mood, count in mood_counts.items():
        summary_text.insert(tk.END, f"{mood}: {count}\n", mood)
        summary_text.tag_config(mood, foreground=MOOD_COLORS[mood])
    summary_text.config(state=tk.DISABLED)

# GUI setup
root = tk.Tk()
root.title("Mental Wellness Check-In")
root.geometry("500x650")  # set window size

# Mood frame
frame_mood = tk.Frame(root, pady=10)
frame_mood.pack()
tk.Label(frame_mood, text="Select your mood:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
mood_var = tk.StringVar()
for mood_option in MOOD_COLORS.keys():
    tk.Radiobutton(frame_mood, text=mood_option, variable=mood_var, value=mood_option).pack(anchor=tk.W)

# Journal frame
frame_journal = tk.Frame(root, pady=10)
frame_journal.pack()
tk.Label(frame_journal, text="Journal Entry:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
journal_text = tk.Text(frame_journal, height=5, width=50)
journal_text.pack()

tk.Button(root, text="Submit Entry", command=submit, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=10)

# Past entries frame
frame_entries = tk.Frame(root, pady=10)
frame_entries.pack()
tk.Label(frame_entries, text="Past Entries:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
display_text = tk.Text(frame_entries, height=10, width=60, state=tk.DISABLED)
display_text.pack()

# Summary frame
frame_summary = tk.Frame(root, pady=10)
frame_summary.pack()
tk.Label(frame_summary, text="Mood Summary:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
summary_text = tk.Text(frame_summary, height=6, width=60, state=tk.DISABLED)
summary_text.pack()

# Initial display
display_entries()
display_summary()

root.mainloop()