from pathlib import Path
from typing import Iterable, Optional, Set

from .resize import resize

DEFAULT_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp"]


def _normalize_extensions(ext_list: Optional[Iterable[str]]) -> Set[str]:
    normalized: Set[str] = set()
    if not ext_list:
        return set(DEFAULT_EXTENSIONS)

    for ext in ext_list:
        cleaned = ext.strip().lower()
        if not cleaned:
            continue
        if not cleaned.startswith("."):
            cleaned = f".{cleaned}"
        normalized.add(cleaned)

    return normalized or set(DEFAULT_EXTENSIONS)


def batch_resize(input_dir: str, output_root: str, width: int, height: int, extensions: Optional[Iterable[str]]) -> None:
    src_root = Path(input_dir)
    if not src_root.exists() or not src_root.is_dir():
        raise NotADirectoryError(f"Input directory not found: {input_dir}")

    dst_root = Path(output_root)
    allowed_exts = _normalize_extensions(extensions)
    processed = 0

    for file_path in src_root.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in allowed_exts:
            continue

        relative = file_path.relative_to(src_root)
        output_path = dst_root / relative
        output_path.parent.mkdir(parents=True, exist_ok=True)

        resize(str(file_path), width, height, str(output_path))
        processed += 1

    if processed == 0:
        print("No matching images were found to resize.")
    else:
        print(f"Resized {processed} file(s) into {dst_root}")
