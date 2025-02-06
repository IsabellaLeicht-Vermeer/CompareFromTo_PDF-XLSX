import fitz
import pyautogui

def on_click(event, x, y, flags, param):
   if event == cv2.EVENT_LBUTTONDOWN:
       print(f"Mouse coordinates: ({x}, {y})")

pdf_path = input("PDF Path: ")
doc = fitz.open(pdf_path)
page = doc[0]  # Get the first page

# Render the page as an image
pix = page.get_pixmap()
pix.save("temp.png")

# Display the image using OpenCV
import cv2
img = cv2.imread("temp.png")
cv2.imshow("PDF Page", img)
cv2.setMouseCallback("PDF Page", on_click)
cv2.waitKey(0)
cv2.destroyAllWindows()
