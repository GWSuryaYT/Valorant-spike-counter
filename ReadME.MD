# ⏱️ Valorant Spike Timer Overlay (OCR-Based)

A sleek, lightweight Python tool that **automatically detects the "SPIKE PLANTED" message** in Valorant using OCR and displays a **transparent, frameless 44-second countdown overlay** to assist with defuses.

---

## 📸 Preview

> 🔹 Timer overlay appears as soon as the spike is planted.
> 🔹 Designed for **Windowed Fullscreen** mode for overlay compatibility.

---

## 🎯 Features

* 🔍 **Real-Time Spike Detection** using Tesseract OCR
* ⏲️ **Frameless 44-Second Countdown** timer (default)
* ✨ **Clean Minimal UI** with no buttons or borders
* ♻️ **Auto-Restarts Detection** 25 seconds after spike explodes
* ⚙️ **Easily Customizable Duration and Screen Region**

---

## 🧰 Requirements

### ✔ Python Libraries

Install using pip:

```bash
pip install PyQt5 opencv-python numpy mss pytesseract
```

### ✔ Tesseract OCR Engine

* 📅 Download: [Tesseract OCR](https://github.com/tesseract-ocr/tesseract/wiki)
* 🔍 Set its path in your script:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

## 🚀 How to Use

1. Run Valorant in **Windowed Fullscreen** mode.
2. Download or clone this repository.
3. Adjust `OCR_REGION` if needed (based on your screen setup).
4. Run the script:

```bash
python spike_timer.py
```

---

## ⚙️ Customization

### 🗺 OCR Detection Region

Adjust based on where the "SPIKE PLANTED" message appears:

```python
OCR_REGION = {
    "top": 130,
    "left": 850,
    "width": 200,
    "height": 50
}
```

📌 Use ShareX or Snipping Tool to identify the correct region.

### ⏱ Change Countdown Duration

```python
MinimalSpikeTimer(duration=44)  # Default: 44 seconds
```

🌟 Tweak for testing or if game mechanics change.

### 📍 Reposition the Overlay

Inside the `MinimalSpikeTimer` class:

```python
self.move(x, y)  # Example: self.move(100, 100)
```

Customize to match your monitor setup.

---

## ⚠ Known Limitations

* ❌ **Won't appear in exclusive fullscreen mode**.
* 🔮 OCR accuracy varies by resolution and UI scale.
* ⏳ May slightly lag due to screen grabbing.
* 💻 Optimized for 1080p. May need tuning for others.

---

## 💡 Roadmap

*

---

## 📜 License

MIT License — free to use, modify, and distribute.
Built by players, for players. GG!

---

## 🙌 Credits

* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
* [OpenCV](https://opencv.org/)
* [PyQt5](https://pypi.org/project/PyQt5/)
* [Valorant](https://playvalorant.com/) — for keeping us on edge ✨
