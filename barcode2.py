import cv2
import zbar

im = cv2.imread('images/barcode2.jpg')
# im = cv2.imread('images/barcode1.jpg')
# im = cv2.imread('images/qrcode.jpg')
rows,cols = im.shape[:2]
gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret,threshold_im = cv2.threshold(gray_im, 150, 255, cv2.THRESH_BINARY)
im,contours,hierarchy = cv2.findContours(threshold_im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

scanner = zbar.ImageScanner()
scanner.parse_config('enable')
scanned_data = {}

for i,contour in enumerate(contours):
    rect = cv2.minAreaRect(contour)
    w = int(rect[1][0])
    h = int(rect[1][1])
    min_w = cols*0.1
    min_h = rows*0.1
    if w > min_w and h > min_h:
        w_half = int(w*0.5)
        h_half = int(h*0.5)
        center_pt = (int(rect[0][0]), int(rect[0][1]))
        top = center_pt[1] - h_half
        right = center_pt[0] + w_half
        bottom = center_pt[1] + h_half
        left = center_pt[0] - w_half
        angle = int(rect[2])
        cropped_im = gray_im[top:bottom, left:right]
        M = cv2.getRotationMatrix2D(center_pt, angle, 1)
        rotated_im = cv2.warpAffine(im.copy(), M, (cols,rows))
        zbar_image = zbar.Image(cols, rows, 'Y800', rotated_im.tostring())
        scanner.scan(zbar_image)
        for symbol in zbar_image:
            symbol_type = symbol.type
            symbol_data = symbol.data
            if(symbol_type not in scanned_data.keys()):
                scanned_data[symbol_type] = []
                if symbol_data not in scanned_data[symbol_type]:
                    scanned_data[symbol_type].append(symbol_data)
        del(zbar_image)
print scanned_data
