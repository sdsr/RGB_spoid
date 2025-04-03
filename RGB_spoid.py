import tkinter as tk
import pyautogui
import win32api
import win32con
import time
import threading

class ColorPickerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("RGB 색상 추출기")
        self.master.geometry("320x330")

        self.rgb_label = tk.Label(master, text="RGB:", font=("Arial", 14))
        self.rgb_label.pack(pady=10)

        self.hex_label = tk.Label(master, text="HEX:", font=("Arial", 14))
        self.hex_label.pack(pady=5)

        self.color_preview = tk.Label(master, bg="#ffffff", width=20, height=2)
        self.color_preview.pack(pady=10)

        self.info_label = tk.Label(master, text="", font=("Arial", 10), fg="green")
        self.info_label.pack(pady=5)

        self.pick_button = tk.Button(master, text="화면에서 색상 추출하기", command=self.start_pick, font=("Arial", 12))
        self.pick_button.pack(pady=10)

    def start_pick(self):
        self.master.withdraw()  # hide GUI
        threading.Thread(target=self.wait_for_click, daemon=True).start()

    def wait_for_click(self):
        print("클릭 대기 중... 화면 클릭 시 RGB 추출됩니다.")
        while True:
            if win32api.GetAsyncKeyState(win32con.VK_LBUTTON):
                x, y = win32api.GetCursorPos()
                rgb = pyautogui.screenshot().getpixel((x, y))
                hex_code = '#{:02X}{:02X}{:02X}'.format(*rgb)
                print(f"위치 ({x}, {y}) → RGB: {rgb}, HEX: {hex_code}")
                self.master.after(0, lambda: self.update_result(rgb, hex_code))
                break
            time.sleep(0.01)

    def update_result(self, rgb, hex_code):
        self.rgb_label.config(text=f"RGB: {rgb}")
        self.hex_label.config(text=f"HEX: {hex_code}")
        self.color_preview.config(bg=hex_code)
        self.master.clipboard_clear()
        self.master.clipboard_append(hex_code)
        self.info_label.config(text=f"{hex_code} (클립보드에 복사됨!)")
        self.master.deiconify()

# run
if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPickerApp(root)
    root.mainloop()
