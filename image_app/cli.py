import argparse
from .resize import resize
from .quantize import quantize
from .resize_scale import resize_scale  # ← 新しく追加
from .png_to_pdf import png_to_pdf
from .batch_resize import batch_resize
from .pad import pad_image
from .batch_pad import batch_pad
from .mmpx import mmpx_scale2x
from .batch_mmpx import batch_mmpx

def main():
    parser = argparse.ArgumentParser(prog="app", description="Image processing CLI tool")
    subparsers = parser.add_subparsers(dest="command")

    # resize
    resize_parser = subparsers.add_parser("resize")
    resize_parser.add_argument("input")
    resize_parser.add_argument("--width", type=int, required=True)
    resize_parser.add_argument("--height", type=int, required=True)
    resize_parser.add_argument("--output", default="resized.jpg")

    # quantize
    quant_parser = subparsers.add_parser("quantize")
    quant_parser.add_argument("input")
    quant_parser.add_argument("--k", type=int, required=True)
    quant_parser.add_argument("--output", default="quantized.jpg")

    # scale（今回の追加）
    scale_parser = subparsers.add_parser("scale")
    scale_parser.add_argument("input")
    scale_parser.add_argument("--scale", type=int, required=True)
    scale_parser.add_argument("--output", default="scaled.png")

    # mmpx (pixel art magnification)
    mmpx_parser = subparsers.add_parser("mmpx")
    mmpx_parser.add_argument("input")
    mmpx_parser.add_argument("--output", default="mmpx.png")

    # batch mmpx over folder tree
    batch_mmpx_parser = subparsers.add_parser("batch-mmpx")
    batch_mmpx_parser.add_argument("input_dir")
    batch_mmpx_parser.add_argument("output_root")
    batch_mmpx_parser.add_argument(
        "--ext",
        nargs="+",
        default=[".png", ".jpg", ".jpeg", ".bmp"],
        help="File extensions to include (e.g. .png .jpg)",
    )

    # png -> pdf
    png2pdf_parser = subparsers.add_parser("png2pdf")
    png2pdf_parser.add_argument("input")
    png2pdf_parser.add_argument("--output", default="converted.pdf")

    # batch resize over folder tree
    batch_parser = subparsers.add_parser("batch-resize")
    batch_parser.add_argument("input_dir")
    batch_parser.add_argument("output_root")
    batch_parser.add_argument("--width", type=int, required=True)
    batch_parser.add_argument("--height", type=int, required=True)
    batch_parser.add_argument(
        "--ext",
        nargs="+",
        default=[".png", ".jpg", ".jpeg", ".bmp"],
        help="File extensions to include (e.g. .png .jpg)",
    )

    # pad with constant border
    pad_parser = subparsers.add_parser("pad")
    pad_parser.add_argument("input")
    pad_parser.add_argument("--padding", type=int, required=True, help="Pixels to pad on every side")
    pad_parser.add_argument(
        "--value",
        type=int,
        default=None,
        help="Constant value (0-255) used to fill the border (default: black or transparent)",
    )
    pad_parser.add_argument("--output", default="padded.png")

    # batch pad over folder tree
    batch_pad_parser = subparsers.add_parser("batch-pad")
    batch_pad_parser.add_argument("input_dir")
    batch_pad_parser.add_argument("output_root")
    batch_pad_parser.add_argument("--padding", type=int, required=True)
    batch_pad_parser.add_argument(
        "--value",
        type=int,
        default=None,
        help="Constant value (0-255) used to fill the border (default: black or transparent)",
    )
    batch_pad_parser.add_argument(
        "--ext",
        nargs="+",
        default=[".png", ".jpg", ".jpeg", ".bmp"],
        help="File extensions to include (e.g. .png .jpg)",
    )

    args = parser.parse_args()

    if args.command == "resize":
        resize(args.input, args.width, args.height, args.output)
    elif args.command == "quantize":
        quantize(args.input, args.k, args.output)
    elif args.command == "scale":
        resize_scale(args.input, args.scale, args.output)
    elif args.command == "mmpx":
        mmpx_scale2x(args.input, args.output)
    elif args.command == "batch-mmpx":
        batch_mmpx(args.input_dir, args.output_root, args.ext)
    elif args.command == "png2pdf":
        png_to_pdf(args.input, args.output)
    elif args.command == "batch-resize":
        batch_resize(args.input_dir, args.output_root, args.width, args.height, args.ext)
    elif args.command == "pad":
        pad_value = None if args.value is None else max(0, min(255, args.value))
        pad_image(args.input, args.padding, args.output, pad_value)
    elif args.command == "batch-pad":
        pad_value = None if args.value is None else max(0, min(255, args.value))
        batch_pad(args.input_dir, args.output_root, args.padding, pad_value, args.ext)
    else:
        parser.print_help()
