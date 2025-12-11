import cv2

def resize_scale(input_path, scale, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {input_path}")

    h, w = img.shape[:2]
    new_w = max(1, w // scale)
    new_h = max(1, h // scale)

    # RGBA を扱う場合、色とアルファを分けて縮小→最近傍で拡大
    if img.ndim == 3 and img.shape[2] == 4:
        color = img[:, :, :3]
        alpha = img[:, :, 3]

        small_color = cv2.resize(color, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
        small_alpha = cv2.resize(alpha, (new_w, new_h), interpolation=cv2.INTER_NEAREST)

        resized_color = cv2.resize(small_color, (w, h), interpolation=cv2.INTER_NEAREST)
        resized_alpha = cv2.resize(small_alpha, (w, h), interpolation=cv2.INTER_NEAREST)

        result = cv2.merge([
            resized_color[:, :, 0],
            resized_color[:, :, 1],
            resized_color[:, :, 2],
            resized_alpha,
        ])
    else:
        small = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
        result = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    cv2.imwrite(output_path, result)
    print(f"Scaled image saved to {output_path}")
