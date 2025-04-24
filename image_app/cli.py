import argparse
from .resize import resize
from .quantize import quantize
from .resize_scale import resize_scale  # ← 新しく追加

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

    args = parser.parse_args()

    if args.command == "resize":
        resize(args.input, args.width, args.height, args.output)
    elif args.command == "quantize":
        quantize(args.input, args.k, args.output)
    elif args.command == "scale":
        resize_scale(args.input, args.scale, args.output)
    else:
        parser.print_help()
