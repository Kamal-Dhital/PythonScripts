import os
import sys
import argparse
from PIL import Image
import io

def get_file_size_kb(path):
    return os.path.getsize(path) // 1024

def compress_image(input_path, target_size_kb, quality=None, output_path=None):
    img = Image.open(input_path)
    img_format = img.format
    if img_format not in ["JPEG", "PNG"]:
        print(f"[!] Skipping unsupported format: {input_path}")
        return
    if not output_path:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_compressed{ext}"
    orig_size = get_file_size_kb(input_path)
    print(f"Compressing: {input_path} ({orig_size} KB)")
    if quality:
        # Manual override
        img.save(output_path, quality=quality, optimize=True)
    else:
        # Binary search for best quality
        min_q, max_q = 10, 95
        best_q = max_q
        for q in range(max_q, min_q - 1, -5):
            buf = io.BytesIO()
            img.save(buf, quality=q, optimize=True)
            size_kb = buf.tell() // 1024
            if size_kb <= target_size_kb:
                best_q = q
                break
        img.save(output_path, quality=best_q, optimize=True)
    new_size = get_file_size_kb(output_path)
    print(f"Saved: {output_path} ({new_size} KB)")

def compress_folder(folder, target_size_kb, quality=None):
    for fname in os.listdir(folder):
        if fname.lower().endswith((".jpg", ".jpeg", ".png")):
            fpath = os.path.join(folder, fname)
            compress_image(fpath, target_size_kb, quality)

def main():
    parser = argparse.ArgumentParser(description="Compress JPG/PNG images to a target file size.")
    parser.add_argument("--input", type=str, help="Path to input image")
    parser.add_argument("--folder", type=str, help="Path to folder containing images")
    parser.add_argument("--target-size", type=int, required=True, help="Target file size in KB")
    parser.add_argument("--quality", type=int, help="Manual quality override (1-95)")
    args = parser.parse_args()
    if not args.input and not args.folder:
        print("[!] Please provide --input or --folder.")
        sys.exit(1)
    if args.input:
        compress_image(args.input, args.target_size, args.quality)
    if args.folder:
        compress_folder(args.folder, args.target_size, args.quality)

if __name__ == "__main__":
    main()
