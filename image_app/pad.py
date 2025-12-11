from typing import Optional

import cv2


def _resolve_border_value(img, value):
    """Return a border fill tuple compatible with copyMakeBorder."""
    if value is not None:
        if img.ndim == 2:
            return value
        channels = img.shape[2]
        return tuple([value] * channels)

    # Auto mode: transparent if alpha channel, otherwise black
    if img.ndim == 3 and img.shape[2] == 4:
        return (0, 0, 0, 0)
    if img.ndim == 3:
        return (0, 0, 0)
    return 0


def pad_image(input_path: str, padding: int, output_path: str, value: Optional[int] = None, quiet: bool = False) -> None:
    if padding < 0:
        raise ValueError("padding must be >= 0")

    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {input_path}")

    if padding == 0:
        cv2.imwrite(output_path, img)
        if not quiet:
            print(f"No padding applied. Saved to {output_path}")
        return

    border_value = _resolve_border_value(img, value)
    padded = cv2.copyMakeBorder(
        img,
        padding,
        padding,
        padding,
        padding,
        borderType=cv2.BORDER_CONSTANT,
        value=border_value,
    )
    cv2.imwrite(output_path, padded)
    if not quiet:
        print(f"Padded image saved to {output_path}")
