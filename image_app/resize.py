import cv2

def resize(input_path, width, height, output_path):
    img = cv2.imread(input_path)
    resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(output_path, resized)
