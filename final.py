import pytesseract
import cv2
import numpy as np
import mss
import time
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal

# Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

DETECTION_COOLDOWN = 50
OCR_REGION = {
    "top": 130,
    "left": 850,
    "width": 200,
    "height": 50
}


class SpikeDetectionThread(QThread):
    spike_detected = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._running = True
        self.last_detection_time = 0

    def run(self):
        with mss.mss() as sct:
            monitor = {
                "top": OCR_REGION["top"],
                "left": OCR_REGION["left"],
                "width": OCR_REGION["width"],
                "height": OCR_REGION["height"]
            }

            while self._running:
                screenshot = np.array(sct.grab(monitor))
                gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

                resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                blurred = cv2.GaussianBlur(resized, (3, 3), 0)
                processed = cv2.adaptiveThreshold(
                    blurred, 255,
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY,
                    11, 2
                )

                custom_config = r'--oem 3 --psm 6'
                text = pytesseract.image_to_string(processed, config=custom_config).upper().strip()
                print(f"OCR Text: '{text}'", end='\r')

                if "SPIKE PLANTED" in text and time.time() - self.last_detection_time > DETECTION_COOLDOWN:
                    print("\n[!] Spike Detected via OCR!")
                    self.last_detection_time = time.time()
                    self.spike_detected.emit()
                    self._running = False  # Stop this thread for now

                time.sleep(0.3)

    def stop(self):
        self._running = False


class MinimalSpikeTimer(QWidget):
    def __init__(self, duration=44, on_finish=None):
        super().__init__()
        self.duration = duration
        self.remaining = float(duration)
        self.on_finish = on_finish

        # Frameless, always on top, transparent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(200, 100)
        self.move(0, 0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(10)  # 10ms for hundredths of a second
        self.show()

    def update_timer(self):
        self.remaining -= 0.01
        self.update()
        if self.remaining <= 0:
            self.timer.stop()
            self.close()
            if self.on_finish:
                QTimer.singleShot(25000, self.on_finish)  # 25 sec wait before restarting detection

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        qp.setPen(QColor(255, 102, 0))
        qp.setFont(QFont("Arial", 40, QFont.Bold))
        # Format as ss.xx
        display_text = f"{self.remaining:05.2f}"
        qp.drawText(self.rect(), Qt.AlignCenter, display_text)


class SpikeApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.detector = None
        self.start_detection()

    def start_detection(self):
        self.detector = SpikeDetectionThread()
        self.detector.spike_detected.connect(self.launch_minimal_gui)
        self.detector.start()

    def launch_minimal_gui(self):
        self.timer_window = MinimalSpikeTimer(duration=44, on_finish=self.start_detection)

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = SpikeApp()
    app.run()