import subprocess
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import threading
from multiping import multi_ping, MultiPing

def check_unused_ips():
    button.configure(state=tk.DISABLED)
    ip_range = entry.get()
    output.delete(1.0, tk.END)
    address = ["{0}.{1}".format(ip_range,i) for i in range(0, 256)]
    # Create a MultiPing object to test three hosts / addresses
    mp = MultiPing(address)
    # Send the pings to those addresses
    mp.send()
    (ok,fail) = mp.receive(1)

    displayAddr=["{0}.{1}".format(ip_range,i) for i in range(0, 256)] if v.get()==0 else ok.keys()
    progress_bar['maximum'] = len(displayAddr)
    progress_bar['value'] = 0
    for i in displayAddr:
        delay = "{:.2f}".format(ok[i] * 1000) if i in ok else None
        fg_color = "green" if i in ok else "red"
        output.tag_configure(fg_color, foreground=fg_color)  # 创建颜色标签
        output.tag_configure(fg_color, foreground=fg_color)  # 创建颜色标签
        output.insert(tk.END, '{0}:{1} ms\n'.format(i, delay), fg_color)
        output.see(tk.END)
        progress_bar['value'] += 1
        window.update_idletasks()
    button.configure(state=tk.NORMAL)

def check_unused_ips_thread():
    thread1 = threading.Thread(target=check_unused_ips)
    thread1.start()

# pyinstaller -F -w --uac-admin -i .\img\ip_set.ico -n PingTool .\pingTool.py
window = tk.Tk()
window.title("已使用的IP地址检测工具")
window.geometry("400x500")
label = tk.Label(window, text="请输入要检测的网段（例如：192.168.0）:", font=("Arial", 12))
label.pack(pady=10)
entry_text_var = tk.StringVar()  # 创建StringVar变量
entry_text_var.set("192.168.0")  # 设置初始值
entry = tk.Entry(window, width=20, justify='center', font=('Arial', 12),textvariable=entry_text_var)
entry.pack()
button = tk.Button(window, text="检测", command=check_unused_ips_thread, font=("Arial", 12))
button.pack(pady=10)

v = tk.IntVar()
v.set(1)
rad_showall = tk.Radiobutton(window, text="显示所有",variable=v,value=0)
rad_showall.pack()
rad_showok = tk.Radiobutton(window, text="显示成功",variable=v,value=1)
rad_showok.pack()

progress_bar = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=200, mode='determinate')
progress_bar.pack(pady=10)
output = scrolledtext.ScrolledText(window, width=40, height=50, font=("Arial", 12))
output.pack(pady=10)
window.mainloop()
