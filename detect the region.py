import cv2

# === CONFIG ===
image_path = "sample.png"  # Replace this with your image path

# === LOAD IMAGE ===
img = cv2.imread(image_path)
if img is None:
    print(f"[ERROR] Failed to load image: {image_path}")
    exit(1)

ocr_region = []

def select_region(event, x, y, flags, param):
    global ocr_region
    if event == cv2.EVENT_LBUTTONDOWN:
        ocr_region = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP:
        ocr_region.append((x, y))
        cv2.rectangle(img, ocr_region[0], ocr_region[1], (0, 255, 0), 2)
        cv2.imshow("Select OCR Region", img)

        x1, y1 = ocr_region[0]
        x2, y2 = ocr_region[1]
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)

        print(f"\n[INFO] OCR_REGION = {{'top': {top}, 'left': {left}, 'width': {width}, 'height': {height}}}\n")

# === OPEN FULLSCREEN WINDOW ===
cv2.namedWindow("Select OCR Region", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Select OCR Region", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback("Select OCR Region", select_region)

cv2.imshow("Select OCR Region", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
