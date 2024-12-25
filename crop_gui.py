import tkinter as tk
from bounding_box_center_crop import process_images_and_text

def on_button_click():
    class_name = class_name_entry.get()
    if class_name:
        label.config(text=f"클래스 '{class_name}'에 대한 처리 시작...")
        process_images_and_text(class_name)
        label.config(text=f"클래스 '{class_name}'에 대한 처리 완료")
    else:
        label.config(text="클래스 이름을 입력하세요.")

window = tk.Tk()
window.title("이미지 처리 프로그램")

window.geometry("530x180")

class_name_label = tk.Label(window, text="클래스 이름 입력:")
class_name_label.grid(row=0, column=0, padx=10, pady=10) 

class_name_entry = tk.Entry(window, width=40)
class_name_entry.grid(row=0, column=1, padx=10, pady=10)

button = tk.Button(window, text="처리 시작", command=on_button_click, width=10, height=1)
button.grid(row=0, column=2, padx=10, pady=10)

label = tk.Label(window, text="")
label.grid(row=1, column=0, columnspan=3, pady=20) 

window.mainloop()
