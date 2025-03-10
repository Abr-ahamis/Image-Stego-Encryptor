# PRODIGY_CS_02
A GUI-based image encryption tool that demonstrates pixel-level manipulation to:   - Encrypt and decrypt an image (using arithmetic transformation and mirror flipping)   - Optionally hide a text message inside the image using simple LSB steganography.
# Image Stego Encryptor

This is a simple GUI application that allows users to **encrypt and decrypt images** while also embedding **hidden text messages** using **steganography**. The tool provides an easy-to-use interface for secure image manipulation.

## Features

✔ **Encrypt and Decrypt Images** using pixel transformations  
✔ **Hide and Extract Secret Messages** within images using LSB steganography  
✔ **User-Friendly GUI** built with Tkinter for easy interaction  
✔ **Supports JPG & PNG images** for processing  
✔ **Custom Encryption Key** for added security  
✔ **Lightweight & Fast Processing** using Python, Pillow, and NumPy  

---

## Requirements

Make sure you have the following installed:

- **Python 3.x**
- **Pillow** (for image processing)
- **NumPy** (for fast numerical operations)
- **Tkinter** (comes with Python)

To install the required packages, run:

```bash
pip install pillow numpy
```
# How to Use
Open the application by running the script:

```bash
python image_stego_encryptor.py
```

Select an image to encrypt or decrypt.

Enter a numeric key for encryption/decryption.

(Optional) Enter a secret message to hide inside the image.

Click Encrypt to scramble the image and embed the message.

Click Decrypt to restore the original image and extract the hidden message.

# Code Structure
```bash
encrypt_image(img, key) → Encrypts the image using pixel transformations

decrypt_image(img, key) → Reverses the encryption to restore the image

hide_text(img, message) → Embeds a secret message inside the image

extract_text(img) → Retrieves the hidden message from the image

Tkinter GUI Elements → Provides an interactive interface for users
```











# script.py

## A simple image encryption and decryption tool that work in terminal that demonstrates pixel-level manipulation.
### This tool uses two basic operations:
  1. Arithmetic transformation: Add (or subtract) an integer key to each pixel's color channels (mod 256).
  2. Pixel swapping: Mirror the image by flipping it horizontally and vertically.

# Usage:
```bash
    python image_encryptor.py encrypt input_image.jpg encrypted.png 42
    python image_encryptor.py decrypt encrypted.png decrypted.png 42
```
# Requirements:
```bash
    - Python 3.x
    - Pillow library (install via: pip install Pillow)
    - NumPy library (install via: pip install numpy)
```
### Note: This example is for educational purposes. It demonstrates a simple reversible image transformation that makes the image unrecognizable without the key but does not provide robust cryptographic security.
