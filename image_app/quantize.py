import cv2
import numpy as np

def quantize(input_path, k, output_path):
    img = cv2.imread(input_path)
    Z = img.reshape((-1, 3)).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, label, center = cv2.kmeans(Z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    result = center[label.flatten()].reshape(img.shape).astype(np.uint8)
    cv2.imwrite(output_path, result)
