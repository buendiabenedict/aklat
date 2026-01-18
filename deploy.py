import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import os

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

        # Update Type Selection
        tk.Label(root, text="Select Update Type:", bg='#121212', fg='#888888', font=("Arial", 9)).pack(anchor="w", padx=40, pady=(15, 0))
        
        self.update_type = tk.StringVar(value="Minor Updates 🛠️")
        
        self.radio_frame = tk.Frame(root, bg='#121212')
        self.radio_frame.pack(fill=tk.X, padx=40, pady=5)

        self.r1 = tk.Radiobutton(self.radio_frame, text="Minor Updates", variable=self.update_type, 
                                 value="Minor Updates 🛠️", bg='#121212', fg='white', 
                                 selectcolor='#121212', activebackground='#121212', 
                                 activeforeground='white', font=("Arial", 10))
        self.r1.pack(side=tk.LEFT, padx=(0, 20))

        self.r2 = tk.Radiobutton(self.radio_frame, text="Major Updates", variable=self.update_type, 
                                 value="Major System Overhaul 🚀", bg='#121212', fg='white', 
                                 selectcolor='#121212', activebackground='#121212', 
                                 activeforeground='white', font=("Arial", 10))
        self.r2.pack(side=tk.LEFT)

        # Deploy Button
        self.deploy_btn = tk.Button(root, text="PUSH TO CLOUDFLARE", font=("Arial", 10, "bold"), 
                                    bg='#ffffff', fg='black', activebackground='#cccccc',
                                    command=self.start_deploy_thread, borderwidth=0, cursor="hand2")
        self.deploy_btn.pack(fill=tk.X, padx=40, pady=25, ipady=12)

        # Logs Console
        tk.Label(root, text="Activity Logs:", bg='#121212', fg='#888888', font=("Arial", 9)).pack(anchor="w", padx=40)
        self.log_area = scrolledtext.ScrolledText(root, width=50, height=15, bg='#000000', fg='#00ff00', 
                                                  font=("Consolas", 9), borderwidth=0)
        self.log_area.pack(padx=20, pady=10)

    def log(self, message):
        self.log_area.insert(tk.END, f"> {message}\n")
        self.log_area.see(tk.END)

    def set_status(self, color, text):
        self.indicator.itemconfig(self.dot, fill=color)
        self.status_text.config(text=text, fg=color)

    def start_deploy_thread(self):
        thread = threading.Thread(target=self.run_deployment)
        thread.start()

    def run_deployment(self):
        msg = self.update_type.get()
        self.deploy_btn.config(state=tk.DISABLED)
        self.set_status("yellow", "Processing...")
        
        try:
            # 1. Check if Git is initialized
            if not os.path.exists(".git"):
                self.log("❌ ERROR: No .git folder found. Run 'git init' first.")
                self.set_status("red", "Repo Not Found")
                return

            # 2. Git Add
            self.log("Staging changes...")
            result = subprocess.run(["git", "add", "."], capture_output=True, text=True)
            if result.returncode != 0:
                self.log(f"❌ ADD ERROR: {result.stderr}")
                return

            # 3. Git Commit
            self.log(f"Applying: {msg}")
            # Check if there are changes to commit
            status_check = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            if not status_check.stdout.strip():
                self.log("ℹ️ No changes to commit. Working tree clean.")
            else:
                result = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
                if result.returncode != 0:
                    self.log(f"❌ COMMIT ERROR: {result.stderr}")
                    return

            # 4. Git Push
            self.log("Uploading to GitHub...")
            result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
            if result.returncode != 0:
                self.log(f"❌ PUSH ERROR: {result.stderr}")
                self.set_status("red", "Push Failed")
                return

            # Success
            self.log("--------------------------------------")
            self.log("✅ DEPLOYMENT SUCCESSFUL!")
            self.log("--------------------------------------")
            self.set_status("#00ff00", "Live & Updated!")

        except Exception as e:
            self.log(f"❌ SYSTEM ERROR: {str(e)}")
            self.set_status("red", "Critical Failure")
        
        finally:
            self.deploy_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeployerApp(root)
    root.mainloop()