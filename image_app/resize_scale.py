import cv2

def resize_scale(input_path, scale, output_path):
    img = cv2.imread(input_path)
    h, w = img.shape[:2]

    # 縮小
    small = cv2.resize(img, (w // scale, h // scale), interpolation=cv2.INTER_AREA)
    # 元サイズに拡大（最近傍）
    resized = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(output_path, resized)
    print(f"Scaled image saved to {output_path}")
