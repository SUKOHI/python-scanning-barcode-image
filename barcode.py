import cv2
import zbar

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

im = cv2.imread('images/barcode1.jpg')
# im = cv2.imread('images/qrcode.jpg')
# im = cv2.imread('images/barcode2.jpg')  # Not working because the image is titled. Use barcode2.py
gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
rows,cols = im.shape[:2]

image = zbar.Image(cols, rows, 'Y800', gray_im.tostring())
scanner.scan(image)

for symbol in image:
    print 'Type: %s, Data: %s' % (symbol.type, symbol.data)

del(image)
