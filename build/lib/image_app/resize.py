import cv2

def resize(input_path, width, height, output_path):
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {input_path}")

    # RGBA の場合は色チャネルとアルファを分離してリサイズし、再結合する
    if img.ndim == 3 and img.shape[2] == 4:
        color = img[:, :, :3]
        alpha = img[:, :, 3]

        resized_color = cv2.resize(color, (width, height), interpolation=cv2.INTER_NEAREST)
        resized_alpha = cv2.resize(alpha, (width, height), interpolation=cv2.INTER_NEAREST)

        # チャネルを B,G,R,A の順でマージ
        result = cv2.merge([
            resized_color[:, :, 0],
            resized_color[:, :, 1],
            resized_color[:, :, 2],
            resized_alpha,
        ])
    else:
        result = cv2.resize(img, (width, height), interpolation=cv2.INTER_NEAREST)

    cv2.imwrite(output_path, result)
