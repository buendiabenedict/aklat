import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading

class DeployerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AKLAT System - Deployment Console")
        self.root.geometry("500x550")
        self.root.configure(bg='#121212')

        # Header
        self.label = tk.Label(root, text="🚀 DEPLOYMENT CENTER", font=("Arial", 16, "bold"), bg='#121212', fg='white')
        self.label.pack(pady=20)

        # Status Indicator
        self.status_frame = tk.Frame(root, bg='#121212')
        self.status_frame.pack(pady=5)
        self.indicator = tk.Canvas(self.status_frame, width=20, height=20, bg='#121212', highlightthickness=0)
        self.indicator.pack(side=tk.LEFT, padx=5)
        self.dot = self.indicator.create_oval(2, 2, 18, 18, fill="gray")
        self.status_text = tk.Label(self.status_frame, text="Ready to Deploy", fg="#aaaaaa", bg='#121212', font=("Arial", 10))
        self.status_text.pack(side=tk.LEFT)

        # Input Box Label
        tk.Label(root, text="What did you change?", bg='#121212', fg='#888888', font=("Arial", 9)).pack(anchor="w", padx=40)
        
        # Commit Message Entry
        self.entry = tk.Entry(root, font=("Arial", 12), bg='#1e1e1e', fg='white', insertbackground='white', borderwidth=0)
        self.entry.pack(fill=tk.X, padx=40, pady=5, ipady=8)
        self.entry.insert(0, "Minor updates")

        # Deploy Button
        self.deploy_btn = tk.Button(root, text="PUSH TO CLOUDFLARE", font=("Arial", 10, "bold"), 
                                    bg='#ffffff', fg='black', activebackground='#cccccc',
                                    command=self.start_deploy_thread, borderwidth=0, cursor="hand2")
        self.deploy_btn.pack(fill=tk.X, padx=40, pady=20, ipady=10)

        # Logs Console
        tk.Label(root, text="Activity Logs:", bg='#121212', fg='#888888', font=("Arial", 9)).pack(anchor="w", padx=40)
        self.log_area = scrolledtext.ScrolledText(root, width=50, height=12, bg='#000000', fg='#00ff00', 
                                                  font=("Consolas", 9), borderwidth=0)
        self.log_area.pack(padx=20, pady=10)

    def log(self, message):
        self.log_area.insert(tk.END, f"> {message}\n")
        self.log_area.see(tk.END)

    def set_status(self, color, text):
        self.indicator.itemconfig(self.dot, fill=color)
        self.status_text.config(text=text, fg=color)

    def start_deploy_thread(self):
        # I-run sa background thread para hindi mag-hang yung window
        thread = threading.Thread(target=self.run_deployment)
        thread.start()

    def run_deployment(self):
        msg = self.entry.get()
        if not msg:
            messagebox.showwarning("Warning", "Please enter a commit message!")
            return

        self.deploy_btn.config(state=tk.DISABLED)
        self.set_status("yellow", "Deploying... Please wait.")
        self.log("Initializing git commands...")

        try:
            # Git Add
            self.log("Staging changes (git add)...")
            subprocess.run(["git", "add", "."], check=True, capture_output=True)

            # Git Commit
            self.log(f"Committing: {msg}")
            subprocess.run(["git", "commit", "-m", msg], check=True, capture_output=True)

            # Git Push
            self.log("Pushing to GitHub & Cloudflare...")
            subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)

            self.log("✅ DEPLOYMENT SUCCESSFUL!")
            self.set_status("#00ff00", "Live & Updated!")
            messagebox.showinfo("Success", "Website is now updating on Cloudflare!")

        except subprocess.CalledProcessError as e:
            self.log(f"❌ ERROR: {e.stderr.decode()}")
            self.set_status("red", "Failed to Deploy")
            messagebox.showerror("Deployment Error", "Check logs for details.")
        
        finally:
            self.deploy_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeployerApp(root)
    root.mainloop()