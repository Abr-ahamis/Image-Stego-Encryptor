#!/usr/bin/env python3

import argparse
import numpy as np
from PIL import Image
import sys


def encrypt_image(input_path, output_path, key):
    """
    Encrypts an image by first adding a fixed key to every pixel's RGB values (modulo 256)
    and then flipping the image horizontally and vertically (mirror flip).

    Parameters:
        input_path (str): Path to the input image file.
        output_path (str): Path where the encrypted image will be saved.
        key (int): Encryption key used to modify pixel values.

    Returns:
        None
    """
    try:
        image = Image.open(input_path)
    except Exception as e:
        print("Error loading image:", e)
        sys.exit(1)

    # Convert image to numpy array for fast processing.
    img_array = np.array(image)

    # Arithmetic Operation: Add key to each pixel (modulo 256)
    # Use int16 to avoid overflow before applying modulo
    encrypted_array = (img_array.astype(np.int16) + key) % 256
    encrypted_array = encrypted_array.astype(np.uint8)

    # Pixel Swapping: Mirror flip the image.
    # This swaps pixel at (x, y) with pixel (width-x-1, height-y-1)
    encrypted_array = np.flip(encrypted_array, axis=(0, 1))

    # Save the encrypted image.
    encrypted_image = Image.fromarray(encrypted_array)
    encrypted_image.save(output_path)
    print(f"Encrypted image saved to {output_path}")


def decrypt_image(input_path, output_path, key):
    """
    Decrypts an image that was encrypted by the encrypt_image() function.
    It reverses the operations:
      1. Flips the image (mirror flip).
      2. Subtracts the key from each pixel's RGB values (modulo 256).

    Parameters:
        input_path (str): Path to the encrypted image file.
        output_path (str): Path where the decrypted image will be saved.
        key (int): The same key that was used for encryption.

    Returns:
        None
    """
    try:
        image = Image.open(input_path)
    except Exception as e:
        print("Error loading image:", e)
        sys.exit(1)

    img_array = np.array(image)

    # Reverse Pixel Swapping: Mirror flip the image back.
    decrypted_array = np.flip(img_array, axis=(0, 1))

    # Reverse Arithmetic Operation: Subtract key (modulo 256)
    decrypted_array = (decrypted_array.astype(np.int16) - key) % 256
    decrypted_array = decrypted_array.astype(np.uint8)

    # Save the decrypted image.
    decrypted_image = Image.fromarray(decrypted_array)
    decrypted_image.save(output_path)
    print(f"Decrypted image saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Simple Image Encryption and Decryption using Pixel Manipulation"
    )
    parser.add_argument("mode", choices=["encrypt", "decrypt"],
                        help="Operation mode: encrypt or decrypt")
    parser.add_argument("input", help="Path to the input image file")
    parser.add_argument("output", help="Path to the output image file")
    parser.add_argument("key", type=int, help="Encryption key (integer) for arithmetic operations")

    args = parser.parse_args()

    if args.mode == "encrypt":
        encrypt_image(args.input, args.output, args.key)
    else:
        decrypt_image(args.input, args.output, args.key)


if __name__ == "__main__":
    main()
