import os
import sys
import zipfile
import tkinter as tk
from tkinter import filedialog, scrolledtext
import time

class ShellEmulator:
    def __init__(self, root, username, vfs_path):
        self.username = username
        self.root = root
        self.vfs_path = vfs_path
        self.current_dir = ""
        self.vfs_root = "vfs_root"
        self.start_time = time.time()
        
        self.setup_gui()
        self.load_vfs()

    def setup_gui(self):
        self.root.title("Shell Emulator")
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20, width=80)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_area.bind("<Return>", self.process_command)
        self.text_area.insert(tk.END, f"{self.username}@shell:~$ ")
        self.text_area.focus()

    def load_vfs(self):
        if os.path.exists(self.vfs_root):
            os.system(f'rm -rf {self.vfs_root}')
        with zipfile.ZipFile(self.vfs_path, 'r') as zip_ref:
            zip_ref.extractall(self.vfs_root)
        self.current_dir = self.vfs_root

    def process_command(self, event):
        command = self.text_area.get("end-2l", "end-1c").strip().split("$ ")[-1]
        self.execute_command(command)

    def execute_command(self, command):
        args = command.split()
        if not args:
            self.display_output("")
            return

        cmd = args[0]
        if cmd == "ls":
            self.ls(args)
        elif cmd == "cd":
            self.cd(args)
        elif cmd == "pwd":
            self.pwd()
        elif cmd == "rev":
            self.rev(args)
        elif cmd == "uptime":
            self.uptime()
        elif cmd == "exit":
            self.root.quit()
        else:
            self.display_output(f"Command not found: {cmd}")

        self.text_area.insert(tk.END, "\n")
        self.text_area.insert(tk.END, f"{self.username}@shell:{self.get_prompt_path()}$ ")

    def ls(self, args):
        try:
            items = os.listdir(self.current_dir)
            output = "\n"+"\n".join(items) + " "
            self.display_output(output)
        except Exception as e:
            self.display_output(f"Error: {str(e)}")

    def cd(self, args):
        if len(args) < 2:
            self.display_output("cd: missing operand")
            return

        new_path = args[1]
        full_path = os.path.join(self.current_dir, new_path)

        if new_path == "..":
            full_path = os.path.dirname(self.current_dir)

        if os.path.exists(full_path) and os.path.isdir(full_path):
            self.current_dir = full_path
        else:
            self.display_output(f"cd: {new_path}: No such file or directory")

    def pwd(self):
        virtual_path = os.path.relpath(self.current_dir, self.vfs_root)
        self.display_output(f"/{virtual_path}")

    def rev(self, args):
        if len(args) < 2:
            self.display_output("rev: missing operand")
            return

        reversed_string = args[1][::-1]
        self.display_output(reversed_string)

    def uptime(self):
        elapsed_time = time.time() - self.start_time
        self.display_output(f"Uptime: {elapsed_time:.2f} seconds")

    def display_output(self, output):
        if output:
            self.text_area.insert(tk.END, f"{output}\n")

    def get_prompt_path(self):
        virtual_path = os.path.relpath(self.current_dir, self.vfs_root)
        return f"/{virtual_path}" if virtual_path != "" else "~"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python emulator.py <username> <path_to_vfs_zip>")
        sys.exit(1)

    username = sys.argv[1]
    vfs_zip_path = sys.argv[2]

    if not os.path.exists(vfs_zip_path):
        print(f"Error: File {vfs_zip_path} not found")
        sys.exit(1)

    root = tk.Tk()
    emulator = ShellEmulator(root, username, vfs_zip_path)
    root.mainloop()
