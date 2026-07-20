import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

BG_MAIN = "#09090b"      
CARD_BG = "#18181b"      
BORDER = "#27272a"       
ACCENT = "#6366f1"       
TEXT_PRIMARY = "#fafafa" 
TEXT_SECONDARY = "#a1a1aa"
SUCCESS = "#22c55e"

def text_to_binary(text):
    return ''.join([format(ord(i), "08b") for i in text])

def encode_logic(img_path, message, save_path):
    img = Image.open(img_path).convert('RGB')
    pixels = img.load()
    width, height = img.size
    binary_msg = text_to_binary(message) + '1111111111111110' 
    if len(binary_msg) > width * height:
        raise ValueError("Image is too small for this message!")
    data_idx = 0
    for y in range(height):
        for x in range(width):
            if data_idx < len(binary_msg):
                r, g, b = pixels[x, y]
                new_r = (r & ~1) | int(binary_msg[data_idx])
                pixels[x, y] = (new_r, g, b)
                data_idx += 1
            else: break
        if data_idx >= len(binary_msg): 
            break
    img.save(save_path, "PNG")

def decode_logic(img_path):
    img = Image.open(img_path)
    pixels = img.load()
    binary_data = ""
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            if binary_data.endswith('1111111111111110'):
                clean_binary = binary_data[:-16]
                return "".join(chr(int(clean_binary[i:i+8], 2)) for i in range(0, len(clean_binary), 8))
    return "No hidden message found!"

class SteganoLens:
    def __init__(self, root):
        self.root = root
        self.root.title("SteganoLens")
        self.root.geometry("850x750")
        self.root.configure(bg=BG_MAIN)
        self.image_path = None

        self.main_frame = tk.Frame(root, bg=BG_MAIN)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        header = tk.Frame(self.main_frame, bg=BG_MAIN)
        header.pack(fill="x", pady=(0, 10))
        tk.Label(header, text="SteganoLens", font=("Inter", 24, "bold"), fg=TEXT_PRIMARY, bg=BG_MAIN).pack()
        tk.Label(header, text="Professional Image Data Masking Engine", font=("Inter", 9), fg=TEXT_SECONDARY, bg=BG_MAIN).pack()

        self.card = tk.Frame(self.main_frame, bg=CARD_BG, padx=25, pady=20, highlightthickness=1, highlightbackground=BORDER)
        self.card.pack(fill="both", expand=True)

        self.mode = tk.StringVar(value="encode")
        tab_frame = tk.Frame(self.card, bg=CARD_BG)
        tab_frame.pack(fill="x", pady=(0, 15))
        
        for m in [("ENCODE", "encode"), ("DECODE", "decode")]:
            tk.Radiobutton(tab_frame, text=m[0], variable=self.mode, value=m[1], command=self.update_ui,
                           indicatoron=0, width=12, pady=8, font=("Inter", 9, "bold"), bg=BG_MAIN, 
                           fg=TEXT_SECONDARY, selectcolor=ACCENT, activebackground=ACCENT, borderwidth=0).pack(side="left", expand=True, padx=5)

        self.drop_frame = tk.Frame(self.card, bg=BG_MAIN, highlightthickness=1, highlightbackground=BORDER)
        self.drop_frame.pack(fill="x", pady=5)
        self.preview_canvas = tk.Canvas(self.drop_frame, width=400, height=150, bg=BG_MAIN, highlightthickness=0)
        self.preview_canvas.pack(pady=10)
        self.preview_canvas.create_text(200, 75, text="Click to Select Image", fill=TEXT_SECONDARY, font=("Inter", 9))
        self.preview_canvas.bind("<Button-1>", lambda e: self.load_image())

        self.input_label = tk.Label(self.card, text="SECRET PAYLOAD", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Inter", 8, "bold"))
        self.input_label.pack(anchor="w", pady=(10, 2))
        self.text_input = tk.Text(self.card, height=4, bg=BG_MAIN, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, 
                                 borderwidth=0, padx=15, pady=15, font=("Consolas", 10), highlightthickness=1, highlightbackground=BORDER)
        self.text_input.pack(fill="both", expand=True, pady=(0, 15))

        self.process_btn = tk.Button(self.card, text="INITIALIZE ENCODE", command=self.handle_action,
                                     bg=ACCENT, fg=TEXT_PRIMARY, font=("Inter", 10, "bold"),
                                     borderwidth=0, cursor="hand2", activebackground="#4f46e5")
        self.process_btn.pack(fill="x", ipady=10)

        self.update_ui()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if file_path:
            self.image_path = file_path
            img = Image.open(file_path)
            img.thumbnail((400, 150))
            self.img_disp = ImageTk.PhotoImage(img)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(200, 75, image=self.img_disp)

    def update_ui(self):
        self.text_input.delete("1.0", tk.END)
        if self.mode.get() == "decode":
            self.input_label.config(text="EXTRACTED MESSAGE")
            self.process_btn.config(text="EXECUTE DECODE", bg="#3f3f46")
        else:
            self.input_label.config(text="SECRET PAYLOAD")
            self.process_btn.config(text="INITIALIZE ENCODE", bg=ACCENT)

    def handle_action(self):
        if not self.image_path:
            messagebox.showwarning("Incomplete", "Source image missing.")
            return
            
        if self.mode.get() == "encode":
            msg = self.text_input.get("1.0", tk.END).strip()
            if not msg:
                messagebox.showwarning("Empty", "Nothing to hide.")
                return
            
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
            if save_path:
                try:
                    encode_logic(self.image_path, msg, save_path)
                    messagebox.showinfo("Done", "Payload embedded successfully.")
                    
                    self.image_path = None
                    self.preview_canvas.delete("all")
                    self.preview_canvas.create_text(200, 75, text="Click to Select Image", fill=TEXT_SECONDARY, font=("Inter", 9))
                    self.text_input.delete("1.0", tk.END)

                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            try:
                result = decode_logic(self.image_path)
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert("1.0", result)
                self.text_input.config(fg=SUCCESS)
                messagebox.showinfo("Success", "Message decoded!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganoLens(root)
    root.mainloop()