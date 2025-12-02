"""
chat_app.py
Simple local chat GUI (single-file) using Tkinter.
How to use:
  - Run: python3 chat_app.py
  - Type messages into the input box and press Enter or click Send.
  - This app stores the conversation in a local file named "chat_history.txt".
  - It's a local chat UI with an optional simple bot reply (toggleable).

Designed for learning and simple local use. No network access required.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import datetime
import os

HISTORY_FILE = "chat_history.txt"

class ChatApp:
    def __init__(self, root):
        self.root = root
        root.title("Yozishdigan Chat — chat_app.py")
        root.geometry("600x450")
        root.resizable(False, False)

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=20)
        self.chat_display.pack(padx=10, pady=(10,5), fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = tk.Frame(root)
        input_frame.pack(padx=10, pady=(0,10), fill=tk.X)

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(input_frame, textvariable=self.input_var)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        self.input_entry.bind("<Return>", self.on_send)

        send_btn = tk.Button(input_frame, text="Send", width=10, command=self.on_send)
        send_btn.pack(side=tk.LEFT)

        # Bottom controls
        controls = tk.Frame(root)
        controls.pack(padx=10, pady=(0,10), fill=tk.X)

        self.bot_enabled = tk.BooleanVar(value=True)
        bot_check = tk.Checkbutton(controls, text="Bot reply enabled", variable=self.bot_enabled)
        bot_check.pack(side=tk.LEFT)

        save_btn = tk.Button(controls, text="Save history...", command=self.save_history_as)
        save_btn.pack(side=tk.RIGHT, padx=(5,0))

        clear_btn = tk.Button(controls, text="Clear display", command=self.clear_display)
        clear_btn.pack(side=tk.RIGHT, padx=(5,0))

        load_btn = tk.Button(controls, text="Load history", command=self.load_history)
        load_btn.pack(side=tk.RIGHT, padx=(5,0))

        # Load existing history if present
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    data = f.read().strip()
                if data:
                    self.append_system("Loaded previous chat history.")
                    self.append_text(data + "\n", tag=None, save=False)
            except Exception as e:
                self.append_system(f"Could not load history: {e}")

    def append_text(self, text, tag='user', save=True):
        """Append text to the chat display. If save=True, also append to HISTORY_FILE."""
        self.chat_display.configure(state='normal')
        if tag == 'user':
            self.chat_display.insert(tk.END, text + "\n")
        elif tag == 'bot':
            self.chat_display.insert(tk.END, text + "\n")
        else:
            self.chat_display.insert(tk.END, text + "\n")
        self.chat_display.see(tk.END)
        self.chat_display.configure(state='disabled')

        if save:
            try:
                with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
                    f.write(text + "\n")
            except Exception as e:
                # If saving fails, show a small non-blocking message in the display
                self.chat_display.configure(state='normal')
                self.chat_display.insert(tk.END, f"[Save error: {e}]\n")
                self.chat_display.configure(state='disabled')

    def append_system(self, text):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.append_text(f"[{ts}] SYSTEM: {text}", tag='system')

    def on_send(self, event=None):
        message = self.input_var.get().strip()
        if not message:
            return
        ts = datetime.datetime.now().strftime("%H:%M")
        user_line = f"You ({ts}): {message}"
        self.append_text(user_line, tag='user')
        self.input_var.set("")

        # Simple bot reply to demonstrate automated response
        if self.bot_enabled.get():
            reply = self.generate_bot_reply(message)
            bot_line = f"Bot ({ts}): {reply}"
            # small delay simulation using after
            self.root.after(250, lambda: self.append_text(bot_line, tag='bot'))

    def generate_bot_reply(self, message):
        """Very simple rule-based replies for demonstration."""
        msg = message.lower()
        if any(g in msg for g in ["hello", "hi", "salom"]):
            return "Salom! Qanday yordam bera olaman?"
        if "ism" in msg or "who are you" in msg.lower():
            return "Men oddiy o'quvchi botman."
        if "tayyor" in msg or "ready" in msg:
            return "Ha, tayyorman."
        if "rahmat" in msg or "thanks" in msg:
            return "Marhamat!"
        if msg.endswith("?"):
            return "Bu yaxshi savol — men hali buni o'rganmayapman, lekin sinab ko'rdim."
        # Default echo-like reply
        return "Siz aytdingiz: " + (message if len(message) <= 80 else message[:77] + "...")

    def save_history_as(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt"),("All files","*.*")])
        if not filepath:
            return
        try:
            content = self.chat_display.get("1.0", tk.END)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content.strip() + "\n")
            messagebox.showinfo("Saved", f"History saved to: {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

    def load_history(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files","*.txt"),("All files","*.*")])
        if not filepath:
            return
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if content:
                self.append_system(f"Loaded history from: {os.path.basename(filepath)}")
                self.append_text(content + "\n", tag=None, save=False)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file: {e}")

    def clear_display(self):
        if messagebox.askyesno("Clear display", "Are you sure you want to clear the displayed chat (this does NOT delete chat_history.txt)?"):
            self.chat_display.configure(state='normal')
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.configure(state='disabled')
            self.append_system("Display cleared. Chat history file remains unchanged.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
