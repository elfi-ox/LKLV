import keyboard
import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk  
import json
import os
import threading
from flask import Flask, request
import subprocess
import signal
import ctypes
from ctypes import wintypes

ctypes.windll.shcore.SetProcessDpiAwareness(True)
ahk_process = subprocess.Popen(["C:\\Program Files\\AutoHotkey\\v2\\AutoHotkey64.exe", os.path.join( os.path.dirname(os.path.realpath(__file__)), "hotkeymonitor.ahk")])
os.chdir(os.path.dirname(os.path.realpath(__file__)))
stop_threads = False
CONFIG_FILE = "config.json"
# Ratio
Hsize = 877
Lsize = 2560

if os.path.exists("key_correspondance.json"):
            with open("key_correspondance.json", 'r') as f:
                key_correspondance = json.load(f)

class ImageWindow(tk.Toplevel):
    def __init__(self, master):

        super().__init__(master)
        self.master = master
        self.overrideredirect(False)  # titlebar

        self.wm_attributes("-topmost", False)
        self.wm_attributes("-toolwindow", False)
        self.wm_attributes("-disabled", False)
        self.wm_attributes("-transparentcolor", "")
        self.iconify()
        self.deiconify()

        self.title("Live Keybord Layout Vizualizer")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Control-m>", self.toggle_titlebar)
        self.resizable(True, False)
        self.iconbitmap("icon.ico")
        self.current_key_code = "000000"
        self.titlebar_enabled = True
        self.image_label = tk.Label(self, bg="black")
        self.image_label.pack(fill=tk.BOTH, expand=True)

        self.current_size_index = 2  
        self.load_config()
        self.after(200, self.enable_resizing)
        self.current_img = None
        self.update_idletasks()
        enable_dark_title_bar(self.winfo_id())

     
        self.image_cache = {} # Image caching
        for key, path in key_correspondance.items():
            try:
                img = Image.open(path)
                self.image_cache[key] = img
            except Exception as e:
                print(f"Erreur chargement image {path} : {e}")



# ----------- Size Manager ----------- 



        self.bind("<Control-plus>", self.increase_size)
        self.bind("<Control-minus>", self.decrease_size)

    def enable_resizing(self):
        self.bind("<Configure>", self.on_resize)

    def increase_size(self, event=None):
        w = self.winfo_width()
        self.geometry(f"{round(w * 1.1)}x{round(w / Lsize * Hsize * 1.1)}")
        self.after(1, self.update_image_size)

    def decrease_size(self, event=None):
        w = self.winfo_width()
        self.geometry(f"{round(w * 0.9)}x{round(w / Lsize * Hsize * 0.9)}")
        self.after(1, self.update_image_size)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                cfg = json.load(f)
                self.geometry(f"{cfg['width']}x{cfg['height']}")
        else:
            self.geometry("938x320") 

    def on_close(self):
        width = self.winfo_width()
        height = self.winfo_height()
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"width": width, "height": height}, f)
        if ahk_process.poll() is None:
            ahk_process.send_signal(signal.SIGTERM)
        self.destroy()
        self.master.quit()
    
    def on_resize(self, event):
        if event.widget != self:
            return
        w = self.winfo_width()
        if w < 200:
            return
        desired_h = round(Hsize / Lsize * w) 
        current_h = self.winfo_height()
        if abs(current_h - desired_h) > 2:
            self.geometry(f"{w}x{desired_h}")
            self.after(1, self.update_image_size)





# ----------- Title Bar Manager ----------- 

    def toggle_titlebar(self, event=None):
        self.titlebar_enabled = not self.titlebar_enabled
        self.overrideredirect(not self.titlebar_enabled)
        enable_dark_title_bar(self.winfo_id())

    def change_img(self, key):
        if key in self.image_cache:
            self.current_img = self.image_cache[key]
            self.after(50, self.update_image_size)
        else:
            print(f"Image non trouvée pour la touche : {key}")



# ----------- Image Updater ----------- 

    def update_image_size(self):
        if not self.current_img:
            return

        self.update_idletasks()
        frame_width = self.image_label.winfo_width()
        frame_height = self.image_label.winfo_height()

        if frame_width < 10 or frame_height < 10:
            return self.after(100, self.update_image_size)

        img_width, img_height = self.current_img.size
        img_ratio = img_width / img_height
        frame_ratio = frame_width / frame_height

        if frame_ratio > img_ratio:
            new_height = frame_height
            new_width = int(new_height * img_ratio)
        else:
            new_width = frame_width
            new_height = int(new_width / img_ratio)

        resized = self.current_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)
        self.image_label.configure(image=self.tk_image)



# ----------- AltTab Monitor ----------- 

    def bring_to_front_temporarily(self):
        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)
        self.after(1000, lambda: self.attributes("-topmost", False))

    def titlebar_status(self):
        return self.titlebar_enabled

def watch_alt_tab(app):
    while True:
        if app.titlebar_status() == False and ((keyboard.is_pressed('alt') and keyboard.is_pressed('tab')) or \
           (keyboard.is_pressed('ctrl') and keyboard.is_pressed('alt') and keyboard.is_pressed('tab'))):
            app.bring_to_front_temporarily()
            time.sleep(2)
        time.sleep(0.3)
        



# ----------- API ----------- 

def start_api(app_instance):
    flask_app = Flask(__name__)

    @flask_app.route('/key_state', methods=['POST'])
    def receive_key_state():
        data = request.get_json()
        key_code = data.get("code")

        if key_code in key_correspondance:
            app_instance.change_img(key_code)
            return {"status": f"ok, {key_code} applied"}
        return {"status": "unknown key"}, 400
            
    flask_app.run(host="127.0.0.1", port=8765)

def enable_dark_title_bar(window_id):
    hwnd = ctypes.windll.user32.GetParent(window_id)
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20

    value = ctypes.c_int(1)
    ctypes.windll.dwmapi.DwmSetWindowAttribute(
        hwnd,
        DWMWA_USE_IMMERSIVE_DARK_MODE,
        ctypes.byref(value),
        ctypes.sizeof(value)
    )

def disable_maximize_button(hwnd):
    GWL_STYLE = -16
    WS_MAXIMIZEBOX = 0x00010000

    current_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)

    new_style = current_style & ~WS_MAXIMIZEBOX

    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, new_style)
    ctypes.windll.user32.SetWindowPos(
        hwnd, None, 0, 0, 0, 0,
        0x0001 | 0x0002 | 0x0020  # SWP_NOMOVE | SWP_NOSIZE | SWP_FRAMECHANGED
    )


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = ImageWindow(root)
    app.change_img("220000")
    threading.Thread(target=watch_alt_tab, args=(app,), daemon=True).start()
    threading.Thread(target=start_api, args=(app,), daemon=True).start()
    root.after(100, lambda: disable_maximize_button(root.winfo_id()))
    app.mainloop()

