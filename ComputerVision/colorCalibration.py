import tkinter as tk
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import time, cv2
import numpy as np
from threading import Thread
import pyautogui

once = True
img_screenshot = None
cam = cv2.VideoCapture(0)


class App:
    original_image = None
    hsv_image = None
    taking_screenshot = False

    def __init__(self, master):
        self.img_path = None
        frame = tk.Frame(master)
        frame.grid()
        root.title("Sliders")

        self.hue_lbl = tk.Label(text="Hue", fg='red')
        self.hue_lbl.grid(row=2)

        self.low_hue = tk.Scale(master, label='Low', from_=0, to=179, length=500, orient=tk.HORIZONTAL,
                                command=self.show_changes)
        self.low_hue.grid(row=3)

        self.high_hue = tk.Scale(master, label='High', from_=0, to=179, length=500, orient=tk.HORIZONTAL,
                                 command=self.show_changes)
        self.high_hue.set(179)
        self.high_hue.grid(row=4)

        self.sat_lbl = tk.Label(text="Saturation", fg='green')
        self.sat_lbl.grid(row=5)

        self.low_sat = tk.Scale(master, label='Low', from_=0, to=255, length=500, orient=tk.HORIZONTAL,
                                command=self.show_changes)
        self.low_sat.set(100)
        self.low_sat.grid(row=6)

        self.high_sat = tk.Scale(master, label='High', from_=0, to=255, length=500, orient=tk.HORIZONTAL,
                                 command=self.show_changes)
        self.high_sat.set(255)
        self.high_sat.grid(row=7)

        self.val_lbl = tk.Label(text="Value", fg='Blue')
        self.val_lbl.grid(row=8)

        self.low_val = tk.Scale(master, label="Low", from_=0, to=255, length=500, orient=tk.HORIZONTAL,
                                command=self.show_changes)
        self.low_val.set(100)
        self.low_val.grid(row=9)

        self.high_val = tk.Scale(master, label="High", from_=0, to=255, length=500, orient=tk.HORIZONTAL,
                                 command=self.show_changes)
        self.high_val.set(255)
        self.high_val.grid(row=10)

        self.print_btn = tk.Button(text='Print', command=self.print_values)
        self.print_btn.grid(row=2, column=1)

        self.reds = tk.Button(text="Reds", fg='red', command=self.preset_r)
        self.reds.grid(row=3, column=1)

        self.greens = tk.Button(text="Greens", fg='green', command=self.preset_g)
        self.greens.grid(row=4, column=1)

        self.blues = tk.Button(text="Blues", fg='blue', command=self.preset_b)
        self.blues.grid(row=5, column=1)

        self.open_btn = tk.Button(text="Open", command=self.open_file)
        self.open_btn.grid(row=6, column=1)

        self.screenshot_btn = tk.Button(text="Screenshot", command=self.screenshot_standby)
        self.screenshot_btn.grid(row=7, column=1)

        self.screenshot_timer_lbl = tk.Label(text="Timer", fg='Red')
        self.screenshot_timer_lbl.grid(row=8, column=1)

        self.hsv_img_lbl = tk.Label(text="HSV", image=None)
        self.hsv_img_lbl.grid(row=0, column=0)

        self.original_img_lbl = tk.Label(text='Original', image=None)
        self.original_img_lbl.grid(row=0, column=1)

    def open_file(self):
        global once
        once = True
        img_file = "input.jpg"
        print(img_file)
        if img_file != '':
            self.img_path = img_file
            self.low_hue.set(self.low_hue.get() + 1)
            self.low_hue.set(self.low_hue.get() - 1)
        else:
            print('picked nothing')
            return 0

    def preset_r(self, *args):
        self.low_hue.set(0)
        self.high_hue.set(13)
        self.low_sat.set(100)
        self.high_sat.set(255)
        self.low_val.set(50)
        self.high_val.set(255)

    def preset_g(self, *args):
        self.low_hue.set(36)
        self.high_hue.set(90)
        self.low_sat.set(100)
        self.high_sat.set(255)
        self.low_val.set(50)
        self.high_val.set(255)

    def preset_b(self, *args):
        self.low_hue.set(80)
        self.high_hue.set(125)
        self.low_sat.set(100)
        self.high_sat.set(255)
        self.low_val.set(75)
        self.high_val.set(255)

    def show_changes(self, *args):
        global once, img_screenshot
        if self.img_path is None:
            return 0

        low_hue = self.low_hue.get()
        low_sat = self.low_sat.get()
        low_val = self.low_val.get()

        high_hue = self.high_hue.get()
        high_sat = self.high_sat.get()
        high_val = self.high_val.get()

        if low_val > high_val or low_sat > high_sat or low_hue > high_hue:
            return 0

        if once:
            if self.img_path != 'screenshot':
                s, im = cam.read()
                if not s:
                    print("Failed to capture image from camera.")
                    return 0
                self.original_image = im
            else:
                self.original_image = img_screenshot

            if self.original_image is None:
                print("Error: original image not set.")
                return 0

            self.original_image = self.resize_image(self.original_image)
            if self.original_image is None:
                print("Error resizing image.")
                return 0

            self.hsv_image = self.original_image.copy()
            self.hsv_image = cv2.cvtColor(self.hsv_image, cv2.COLOR_BGR2HSV)

            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.original_image = Image.fromarray(self.original_image)
            self.original_image = ImageTk.PhotoImage(self.original_image)

            self.original_img_lbl.configure(image=self.original_image)
            self.original_img_lbl.image = self.original_image
            once = False

        lower_color = np.array([low_hue, low_sat, low_val])
        upper_color = np.array([high_hue, high_sat, high_val])

        mask = cv2.inRange(self.hsv_image, lower_color, upper_color)
        mask = Image.fromarray(mask)
        mask = ImageTk.PhotoImage(mask)
        self.hsv_img_lbl.configure(image=mask)
        self.hsv_img_lbl.image = mask

    def print_values(self, *args):
        print("Low = [{},{},{}]".format(self.low_hue.get(), self.low_sat.get(), self.low_val.get()))
        print("High= [{},{},{}]".format(self.high_hue.get(), self.high_sat.get(), self.high_val.get()))

    def screenshot_standby(self, *args):
        if not self.taking_screenshot:
            take_screenshot_thread = Thread(target=self.take_screenshot)
            take_screenshot_thread.start()
        else:
            return 0

    def take_screenshot(self, *args):
        global img_screenshot, once
        self.taking_screenshot = True
        once = True
        self.img_path = 'screenshot'

        screenshot_timer_thread = Thread(target=self.screenshot_timer_lbl_update)
        screenshot_timer_thread.start()
        for i in range(2):
            for _ in range(3):
                time.sleep(1)
            try:
                if i == 0:
                    x1, y1 = pyautogui.position()
                else:
                    x2, y2 = pyautogui.position()

            except Exception as e:
                print("ERROR: {}".format(e))
                continue

        if x2 - x1 < 1 or y2 - y1 < 1:
            print("Retake Screenshot")
            return

        try:
            screenshoted_image = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
            screenshoted_image = np.array(screenshoted_image)
        except Exception as e:
            print(e)
            return

        img_screenshot = cv2.cvtColor(screenshoted_image, cv2.COLOR_RGB2BGR)
        img_screenshot = self.resize_image(img_screenshot)
        self.low_hue.set(self.low_hue.get() + 1)
        self.low_hue.set(self.low_hue.get() - 1)
        self.taking_screenshot = False

    def screenshot_timer_lbl_update(self, *args):
        for _ in range(2):
            for i in range(3):
                self.screenshot_timer_lbl.config(text="{}".format(i + 1))
                time.sleep(1)
        self.screenshot_timer_lbl.config(text=" ")

    def resize_image(self, img, *args):
        height, width, _ = img.shape
        count_times_resized = 0
        while width > 500 or height > 500:
            width = width / 2
            height = height / 2
            count_times_resized += 1
        if count_times_resized > 0:
            img = cv2.resize(img, (int(width), int(height)))
        return img


root = tk.Tk()
app = App(root)
root.mainloop()
