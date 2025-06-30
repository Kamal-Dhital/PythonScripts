# Image Compressor

A CLI tool to compress JPG/PNG images to a user-specified file size.

## Features
- Compress single images or all images in a folder
- Target file size (in KB)
- Optional manual quality override
- Logs before/after sizes

## Usage

```bash
# Compress a single image to 200KB
printf "python image_compressor.py --input path/to/image.jpg --target-size 200"

# Compress all images in a folder to 150KB
printf "python image_compressor.py --folder path/to/folder --target-size 150"

# Compress with manual quality override (quality 70)
printf "python image_compressor.py --input path/to/image.png --target-size 100 --quality 70"
```

## Arguments
- `--input`: Path to input image
- `--folder`: Path to folder containing images
- `--target-size`: Target file size in KB
- `--quality`: (Optional) Manual quality override (1-95)

## Output
Compressed images are saved with `_compressed` suffix in the same directory.
