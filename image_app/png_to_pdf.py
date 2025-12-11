from pathlib import Path
from PIL import Image


def png_to_pdf(input_path: str, output_path: str) -> None:
    src = Path(input_path)
    if not src.exists():
        raise FileNotFoundError(f"Cannot read image: {input_path}")
    if output_path == "default":
        output_path = src.with_suffix(".pdf")
    with Image.open(src) as img:
        if img.mode in ("RGBA", "LA"):
            # PDFs do not store alpha channels, so flatten onto white
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            pdf_ready = background
        else:
            pdf_ready = img.convert("RGB")

        pdf_ready.save(output_path, "PDF")
