import os
import subprocess
import tkinter as tk
from tkinter import scrolledtext, font, messagebox, simpledialog
import re
import webbrowser

def scan_subdomains():
    domain = domain_entry.get()
    command = f'subfinder -d {domain} | httpx -sc -td -title -probe -fhr -location -mc 200 -o .result.txt'
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result_text.config(state=tk.NORMAL)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, "Scanning is in progress. Please wait for the results.\n")
    result_text.config(state=tk.DISABLED)
    hide_file(".result.txt")

def find_js():
    domain = domain_entry.get()
    command = f'subfinder -d {domain} | httpx | waybackurls > .js_result.txt'
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result_text.config(state=tk.NORMAL)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, "Finding JavaScript files. Please wait for the results.\n")
    result_text.config(state=tk.DISABLED)
    hide_file(".js_result.txt")

def display_results():
    try:
        with open('.result.txt', 'r', encoding="utf-8") as file:
            results = file.read()
            results = strip_color_escape_sequences(results)
            result_text.config(state=tk.NORMAL)
            result_text.delete('1.0', tk.END)
            result_text.insert(tk.END, results)
            make_urls_clickable()
            result_text.config(state=tk.DISABLED)
    except FileNotFoundError:
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "No results found. Please perform a scan first.\n")
        result_text.config(state=tk.DISABLED)

def display_js_results():
    try:
        with open('.js_result.txt', 'r', encoding="utf-8") as file:
            results = file.read()
            result_text.config(state=tk.NORMAL)
            result_text.delete('1.0', tk.END)
            result_text.insert(tk.END, results)
            make_urls_clickable()
            result_text.config(state=tk.DISABLED)
    except FileNotFoundError:
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "No JavaScript files found.\n")
        result_text.config(state=tk.DISABLED)

def filter_results():
    keyword = filter_entry.get()
    if keyword:
        text = result_text.get("1.0", tk.END)
        filtered_text = '\n'.join(line for line in text.split('\n') if keyword in line)
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, filtered_text)
        result_text.config(state=tk.DISABLED)

def strip_color_escape_sequences(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        delete_file(".result.txt")
        delete_file(".js_result.txt")
        root.destroy()

def make_urls_clickable():
    text = result_text.get("1.0", tk.END)
    urls = re.findall(r'(https?://\S+)', text)
    for url in urls:
        start = result_text.search(url, "1.0", stopindex=tk.END)
        end = f"{start}+{len(url)}c"
        result_text.tag_add(url, start, end)
        result_text.tag_config(url, foreground="blue", underline=True)
        result_text.tag_bind(url, "<Button-1>", lambda event, u=url: open_url(u))

def open_url(url):
    webbrowser.open_new(url)

def zoom_in():
    global font_size
    font_size += 2
    result_text.config(font=("Arial", font_size))

def zoom_out():
    global font_size
    font_size -= 2
    result_text.config(font=("Arial", font_size))

def hide_file(file_path):
    try:
        if os.path.exists(file_path):
            os.system(f'attrib +h "{file_path}"')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to hide file: {e}")

def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete file: {e}")
        
def open_youtube_channel():
    channel_url = "https://www.youtube.com/channel/UCqrrkRB1VUhotw9aSXCpjHg?sub_confirmation=1"
    webbrowser.open_new(channel_url)   

def display_urls_with_checkbox(urls_text):
    lines = urls_text.split("\n")
    for url in lines:
        if url.strip():
            url_checkbox = tk.Checkbutton(result_text, text=url, command=make_urls_clickable(url))
            result_text.window_create(tk.END, window=url_checkbox)
            result_text.insert(tk.END, "\n")         
    
root = tk.Tk()
root.title("SainiON Hacks Secret Finder")

# Configure style
root.tk_setPalette(background="#F0F0F0", foreground="black", activeBackground="#D0D0D0", activeForeground="black")
root.option_add("*TButton.relief", "raised")
root.option_add("*TButton.borderWidth", 1)
root.option_add("*TButton.padding", 5)
root.option_add("*TButton.font", ("Arial", 10))
root.option_add("*TEntry.borderWidth", 1)
root.option_add("*TEntry.font", ("Arial", 10))
root.option_add("*TLabel.font", ("Arial", 10))

# Define widgets
domain_label = tk.Label(root, text="Enter Domain:")
domain_entry = tk.Entry(root)
scan_button = tk.Button(root, text="Live Host", command=scan_subdomains)
js_button = tk.Button(root, text="Waybackurls", command=find_js)
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg='white', fg='black', insertbackground='black', height=100, width=300)
display_button = tk.Button(root, text="Live Subdomain", command=display_results)
display_js_button = tk.Button(root, text="Live JS File", command=display_js_results)
filter_label = tk.Label(root, text="Filter:")
filter_entry = tk.Entry(root)
filter_button = tk.Button(root, text="Filter", command=filter_results)
zoom_in_button = tk.Button(root, text="Zoom In", command=zoom_in)
zoom_out_button = tk.Button(root, text="Zoom Out", command=zoom_out)
youtube_button = tk.Button(root, text="YouTube Channel", command=open_youtube_channel, bg='red', fg='white', font=("Arial", 14, "bold"))

# Grid layout
domain_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
domain_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
scan_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
js_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
result_text.grid(row=1, column=0, columnspan=5, padx=10, pady=5, sticky="nsew")
display_button.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
display_js_button.grid(row=2, column=3, padx=5, pady=5, sticky="ew")
filter_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
filter_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
filter_button.grid(row=3, column=2, padx=5, pady=5, sticky="ew")
zoom_in_button.grid(row=3, column=3, padx=5, pady=5, sticky="ew")
zoom_out_button.grid(row=3, column=4, padx=5, pady=5, sticky="ew")
youtube_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

# Font size for zooming
font_size = 12

root.protocol("WM_DELETE_WINDOW", on_closing)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Title
title_label = tk.Label(root, text="SainiON Hacks Secret Finder", font=("Arial", 14, "bold"), fg="blue")
title_label.grid(row=4, column=0, columnspan=5, padx=10, pady=(20, 10), sticky="nsew")

root.mainloop()
