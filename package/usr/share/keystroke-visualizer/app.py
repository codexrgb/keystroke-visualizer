import csv
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class KeystrokeVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Keystroke Visualizer (focus-only)")
        self.root.geometry("720x480")

        # Enable dark theme
        self.root.tk_setPalette(background="#1e1e1e", foreground="white")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", background="#333", foreground="white", padding=6)
        style.configure("TLabel", background="#1e1e1e", foreground="white")
        style.configure("TFrame", background="#1e1e1e")

        # Toolbar Frame
        toolbar = ttk.Frame(root)
        toolbar.pack(fill="x", padx=12, pady=8)

        self.clear_btn = ttk.Button(toolbar, text="Clear", command=self.clear)
        self.clear_btn.pack(side="left", padx=5)

        self.save_btn = ttk.Button(toolbar, text="Save to CSV…", command=self.save_csv)
        self.save_btn.pack(side="left", padx=5)

        self.stats_btn = ttk.Button(toolbar, text="Show Stats", command=self.show_stats)
        self.stats_btn.pack(side="left", padx=5)

        self.info_label = ttk.Label(
            root,
            text="Focus this window and type… (works only when this app is focused)",
            font=("Segoe UI", 10)
        )
        self.info_label.pack(padx=12, pady=4, anchor="w")

        self.text = tk.Text(
            root,
            height=20,
            bg="#252526",
            fg="white",
            insertbackground="white",
            font=("Consolas", 11)
        )
        self.text.pack(expand=True, fill="both", padx=12, pady=8)

        self.status = ttk.Label(root, text="Ready", anchor="w")
        self.status.pack(fill="x", padx=12)

        self.records = []
        self.start_time = None
        self.root.bind("<KeyPress>", self.on_keypress)

    def on_keypress(self, event):
        ts = time.time()
        if self.start_time is None:
            self.start_time = ts

        human_ts = time.strftime("%H:%M:%S", time.localtime(ts))
        key = event.keysym
        record = {"timestamp": human_ts, "unix": f"{ts:.3f}", "key": key}
        self.records.append(record)
        self._append_line(f"[{human_ts}] key: {key}")
        self.status.config(text=f"Captured: {key}")

    def _append_line(self, line):
        self.text.insert("end", line + "\n")
        self.text.see("end")

    def clear(self):
        self.records.clear()
        self.text.delete("1.0", "end")
        self.status.config(text="Cleared.")

    def save_csv(self):
        if not self.records:
            messagebox.showinfo("Nothing to save", "No keystrokes recorded yet.")
            return
        path = filedialog.asksaveasfilename(
            title="Save CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "unix", "key"])
            writer.writeheader()
            writer.writerows(self.records)
        messagebox.showinfo("Saved", f"Saved {len(self.records)} keys to:\n{path}")

    def show_stats(self):
        if not self.records:
            messagebox.showinfo("No Data", "No keys recorded yet.")
            return
        duration = time.time() - self.start_time if self.start_time else 0
        total_keys = len(self.records)
        wpm = (total_keys / 5) / (duration / 60) if duration > 0 else 0
        messagebox.showinfo(
            "Typing Stats",
            f"Total Keys: {total_keys}\nDuration: {duration:.1f} sec\nSpeed: {wpm:.1f} WPM"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = KeystrokeVisualizer(root)
    root.mainloop()
