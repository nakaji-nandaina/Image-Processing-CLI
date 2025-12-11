"""MMPX pixel-art scaling.

Port of the MMPX 2x magnification algorithm by Morgan McGuire and Mara Gagiu.
Original reference implementation is MIT licensed and published at
https://casual-effects.com/research/McGuire2021PixelArt/ .
"""

from typing import Optional, Tuple

import cv2
import numpy as np


def _luma(color: int) -> int:
    alpha = (color >> 24) & 0xFF
    red = (color >> 16) & 0xFF
    green = (color >> 8) & 0xFF
    blue = color & 0xFF
    return (red + green + blue + 1) * (256 - alpha)


def _all_eq(value: int, *others: int) -> bool:
    return all(value == other for other in others)


def _none_eq(value: int, *others: int) -> bool:
    return all(value != other for other in others)


def _any_eq(value: int, *others: int) -> bool:
    return any(value == other for other in others)


def _sample(src: np.ndarray, x: int, y: int) -> int:
    max_y, max_x = src.shape[0] - 1, src.shape[1] - 1
    if x < 0:
        x = 0
    elif x > max_x:
        x = max_x
    if y < 0:
        y = 0
    elif y > max_y:
        y = max_y
    return int(src[y, x])


def _mmpx_scale2x_core(src: np.ndarray) -> np.ndarray:
    height, width = src.shape
    dst = np.zeros((height * 2, width * 2), dtype=np.uint32)

    for y in range(height):
        for x in range(width):
            A = _sample(src, x - 1, y - 1)
            B = _sample(src, x, y - 1)
            C = _sample(src, x + 1, y - 1)
            D = _sample(src, x - 1, y)
            E = _sample(src, x, y)
            F = _sample(src, x + 1, y)
            G = _sample(src, x - 1, y + 1)
            H = _sample(src, x, y + 1)
            I = _sample(src, x + 1, y + 1)

            J = K = L = M = E

            if not (
                A == E
                and B == E
                and C == E
                and D == E
                and F == E
                and G == E
                and H == E
                and I == E
            ):
                P = _sample(src, x, y - 2)
                S = _sample(src, x, y + 2)
                Q = _sample(src, x - 2, y)
                R = _sample(src, x + 2, y)

                Bl = _luma(B)
                Dl = _luma(D)
                El = _luma(E)
                Fl = _luma(F)
                Hl = _luma(H)

                # 1:1 slope rules
                if (
                    D == B
                    and D != H
                    and D != F
                    and (El >= Dl or E == A)
                    and _any_eq(E, A, C, G)
                    and ((El < Dl) or A != D or E != P or E != Q)
                ):
                    J = D
                if (
                    B == F
                    and B != D
                    and B != H
                    and (El >= Bl or E == C)
                    and _any_eq(E, A, C, I)
                    and ((El < Bl) or C != B or E != P or E != R)
                ):
                    K = B
                if (
                    H == D
                    and H != F
                    and H != B
                    and (El >= Hl or E == G)
                    and _any_eq(E, A, G, I)
                    and ((El < Hl) or G != H or E != S or E != Q)
                ):
                    L = H
                if (
                    F == H
                    and F != B
                    and F != D
                    and (El >= Fl or E == I)
                    and _any_eq(E, C, G, I)
                    and ((El < Fl) or I != H or E != R or E != S)
                ):
                    M = F

                # Intersection rules
                if (
                    E != F
                    and _all_eq(E, C, I, D, Q)
                    and _all_eq(F, B, H)
                    and F != _sample(src, x + 3, y)
                ):
                    K = M = F
                if (
                    E != D
                    and _all_eq(E, A, G, F, R)
                    and _all_eq(D, B, H)
                    and D != _sample(src, x - 3, y)
                ):
                    J = L = D
                if (
                    E != H
                    and _all_eq(E, G, I, B, P)
                    and _all_eq(H, D, F)
                    and H != _sample(src, x, y + 3)
                ):
                    L = M = H
                if (
                    E != B
                    and _all_eq(E, A, C, H, S)
                    and _all_eq(B, D, F)
                    and B != _sample(src, x, y - 3)
                ):
                    J = K = B

                if Bl < El and _all_eq(E, G, H, I, S) and _none_eq(E, A, D, C, F):
                    J = K = B
                if Hl < El and _all_eq(E, A, B, C, P) and _none_eq(E, D, G, I, F):
                    L = M = H
                if Fl < El and _all_eq(E, A, D, G, Q) and _none_eq(E, B, C, I, H):
                    K = M = F
                if Dl < El and _all_eq(E, C, F, I, R) and _none_eq(E, B, A, G, H):
                    J = L = D

                # 2:1 slope rules
                if H != B:
                    if H != A and H != E and H != C:
                        if _all_eq(H, G, F, R) and _none_eq(H, D, _sample(src, x + 2, y - 1)):
                            L = M
                        if _all_eq(H, I, D, Q) and _none_eq(H, F, _sample(src, x - 2, y - 1)):
                            M = L

                    if B != I and B != G and B != E:
                        if _all_eq(B, A, F, R) and _none_eq(B, D, _sample(src, x + 2, y + 1)):
                            J = K
                        if _all_eq(B, C, D, Q) and _none_eq(B, F, _sample(src, x - 2, y + 1)):
                            K = J

                if F != D:
                    if D != I and D != E and D != C:
                        if _all_eq(D, A, H, S) and _none_eq(D, B, _sample(src, x + 1, y + 2)):
                            J = L
                        if _all_eq(D, G, B, P) and _none_eq(D, H, _sample(src, x + 1, y - 2)):
                            L = J

                    if F != E and F != A and F != G:
                        if _all_eq(F, C, H, S) and _none_eq(F, B, _sample(src, x - 1, y + 2)):
                            K = M
                        if _all_eq(F, I, B, P) and _none_eq(F, H, _sample(src, x - 1, y - 2)):
                            M = K

            dst_y = y * 2
            dst_x = x * 2
            dst[dst_y, dst_x] = J
            dst[dst_y, dst_x + 1] = K
            dst[dst_y + 1, dst_x] = L
            dst[dst_y + 1, dst_x + 1] = M

    return dst


def _to_bgra(img: np.ndarray) -> Tuple[np.ndarray, int]:
    if img.ndim == 2:
        bgra = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)
        channels = 1
    elif img.shape[2] == 3:
        alpha = np.full((*img.shape[:2], 1), 255, dtype=img.dtype)
        bgra = np.concatenate([img, alpha], axis=2)
        channels = 3
    elif img.shape[2] == 4:
        bgra = img
        channels = 4
    else:
        raise ValueError("Unsupported image format for MMPX")
    return bgra, channels


def _bgra_to_argb(bgra: np.ndarray) -> np.ndarray:
    b = bgra[:, :, 0].astype(np.uint32)
    g = bgra[:, :, 1].astype(np.uint32)
    r = bgra[:, :, 2].astype(np.uint32)
    a = bgra[:, :, 3].astype(np.uint32)
    return (a << 24) | (r << 16) | (g << 8) | b


def _argb_to_bgra(argb: np.ndarray) -> np.ndarray:
    a = ((argb >> 24) & 0xFF).astype(np.uint8)
    r = ((argb >> 16) & 0xFF).astype(np.uint8)
    g = ((argb >> 8) & 0xFF).astype(np.uint8)
    b = (argb & 0xFF).astype(np.uint8)
    return np.stack([b, g, r, a], axis=2)


def mmpx_scale2x(input_path: str, output_path: str) -> None:
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {input_path}")

    bgra, original_channels = _to_bgra(img)
    argb = _bgra_to_argb(bgra)
    scaled = _mmpx_scale2x_core(argb)
    scaled_bgra = _argb_to_bgra(scaled)

    if original_channels == 4:
        output = scaled_bgra
    elif original_channels == 3:
        output = scaled_bgra[:, :, :3]
    else:
        output = cv2.cvtColor(scaled_bgra, cv2.COLOR_BGRA2GRAY)

    cv2.imwrite(output_path, output)
