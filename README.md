# 🔐 SteganoLens

**A professional desktop application for hiding and extracting secret text messages inside images using LSB (Least Significant Bit) steganography.**

SteganoLens provides a clean, modern GUI built with Tkinter that lets you embed confidential text into PNG/JPG images imperceptibly, and later decode it back — no external servers, no data leaves your machine.

---

## ✨ Features

- 🖼️ **Encode** — Hide any text message inside an image using LSB steganography
- 🔍 **Decode** — Extract hidden messages from previously encoded images
- 🎨 **Modern dark-themed UI** with an intuitive tabbed encode/decode interface
- 📌 **Image preview** before processing
- ⚡ **Lightweight** — pure Python, no heavy dependencies
- 🔒 **Fully offline** — your data and images never leave your device

---

## 🛠️ Tech Stack

- **Python 3**
- **Tkinter** — GUI framework
- **Pillow (PIL)** — image processing

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/SteganoLens.git
   cd SteganoLens
   ```

2. Install dependencies:
   ```bash
   pip install pillow
   ```

3. Run the application:
   ```bash
   python Steganography.py
   ```

---

## 🚀 Usage

### Encoding a message
1. Launch the app and select the **ENCODE** tab.
2. Click the preview area to select a source image (PNG/JPG).
3. Type your secret message in the **Secret Payload** box.
4. Click **INITIALIZE ENCODE** and choose where to save the output PNG.

### Decoding a message
1. Switch to the **DECODE** tab.
2. Select the image containing a hidden message.
3. Click **EXECUTE DECODE** to reveal the extracted text.

> ⚠️ **Note:** Always save encoded images as **PNG**. Lossy formats like JPG will corrupt the hidden data.

---

## 🧠 How It Works

SteganoLens uses **LSB (Least Significant Bit) steganography**: each character of your message is converted to binary and embedded into the least significant bit of the red channel of each pixel. A unique 16-bit delimiter marks the end of the message so the decoder knows where to stop reading.

---

## 📂 Project Structure

```
SteganoLens/
├── Steganography.py     # Main application (GUI + encode/decode logic)
└── README.md
```

---


## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Musfirah Kashan**
🔗 [LinkedIn](https://www.linkedin.com/in/musfirah-kashan-487aa626a/) • 💻 [GitHub](https://github.com/musfirah-kashan)
