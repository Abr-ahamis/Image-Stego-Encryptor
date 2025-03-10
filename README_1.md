
image_encryptor.py

A simple image encryption and decryption tool that demonstrates pixel-level manipulation.
This tool uses two basic operations:
  1. Arithmetic transformation: Add (or subtract) an integer key to each pixel's color channels (mod 256).
  2. Pixel swapping: Mirror the image by flipping it horizontally and vertically.

Usage:
    python image_encryptor.py encrypt input_image.jpg encrypted.png 42
    python image_encryptor.py decrypt encrypted.png decrypted.png 42

Requirements:
    - Python 3.x
    - Pillow library (install via: pip install Pillow)
    - NumPy library (install via: pip install numpy)

Note: This example is for educational purposes. It demonstrates a simple reversible
image transformation that makes the image unrecognizable without the key but does not
provide robust cryptographic security.

