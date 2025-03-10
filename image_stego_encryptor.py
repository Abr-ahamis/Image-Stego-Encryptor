#!/usr/bin/env python3
"""
image_stego_encryptor.py

A GUI-based image encryption tool that demonstrates pixel-level manipulation to:
  - Encrypt and decrypt an image (using arithmetic transformation and mirror flipping)
  - Optionally hide a text message inside the image using simple LSB steganography.

Requirements:
  - Python 3.x
  - Pillow (install via: pip install Pillow)
  - NumPy  (install via: pip install numpy)
  - Tkinter (usually comes with Python)

Usage:
  Launch the script:
      python image_stego_encryptor.py

In the GUI:
  1. Browse and select an input image.
  2. Choose an output file location.
  3. Enter a numeric key for encryption/decryption.
  4. (Optional) Enter a text message to hide (for encryption mode).
  5. Click "Encrypt Image" to generate an encrypted image with hidden text.
  6. Click "Decrypt Image" to recover the original image and retrieve the hidden text.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import os
import sys


# --- Steganography Functions ---

def hide_text(image, text):
    """
    Hides the provided text inside the image using LSB steganography (red channel).
    The first 32 pixels store a header representing the message length in bits.

    Parameters:
        image (PIL.Image): The input image (mode should be RGB).
        text (str): The text message to hide.

    Returns:
        PIL.Image: A new image with the text hidden.
    """
    # Convert image to numpy array (RGB assumed)
    img_array = np.array(image)
    h, w, channels = img_array.shape

    # Flatten the red channel
    flat_red = img_array[:, :, 0].flatten()

    # Convert text to bytes and then to a bit string
    text_bytes = text.encode('utf-8')
    text_bits = ''.join(f'{byte:08b}' for byte in text_bytes)
    msg_length = len(text_bits)  # number of bits in the message

    # Create a 32-bit header from msg_length
    header = f'{msg_length:032b}'
    full_data = header + text_bits  # total bits to embed

    if len(full_data) > flat_red.size:
        raise ValueError("Text too long to hide in this image.")

    # Embed bits into the LSB of each pixel in the red channel
    for i, bit in enumerate(full_data):
        pixel_val = flat_red[i]
        # Set the LSB to match the bit
        if int(bit) != (pixel_val & 1):
            if pixel_val & 1:
                flat_red[i] = pixel_val - 1  # make even
            else:
                flat_red[i] = pixel_val + 1  # make odd

    # Reshape modified red channel and put back into image array
    img_array[:, :, 0] = flat_red.reshape((h, w))
    return Image.fromarray(img_array)


def extract_text(image):
    """
    Extracts a hidden text message from the image's red channel LSB.
    It reads the first 32 pixels to get the header (message length in bits),
    then extracts that many bits and converts them back into text.

    Parameters:
        image (PIL.Image): The image with hidden text.

    Returns:
        str: The extracted text message.
    """
    img_array = np.array(image)
    h, w, channels = img_array.shape
    flat_red = img_array[:, :, 0].flatten()

    # Read the first 32 bits for the header
    header_bits = ''.join(str(flat_red[i] & 1) for i in range(32))
    msg_length = int(header_bits, 2)

    if msg_length <= 0 or msg_length > (flat_red.size - 32):
        return ""  # No valid hidden text found

    # Read the next msg_length bits for the message
    msg_bits = ''.join(str(flat_red[i] & 1) for i in range(32, 32 + msg_length))

    # Convert bits to bytes and then to string
    bytes_list = [msg_bits[i:i + 8] for i in range(0, len(msg_bits), 8)]
    message_bytes = bytearray(int(b, 2) for b in bytes_list if len(b) == 8)

    try:
        message = message_bytes.decode('utf-8')
    except UnicodeDecodeError:
        message = ""
    return message


# --- Encryption / Decryption Functions ---

def encrypt_image_obj(image, key):
    """
    Encrypts the image by adding the key to each pixel (mod 256) and mirror flipping it.

    Parameters:
        image (PIL.Image): The input image.
        key (int): Numeric key for arithmetic transformation.

    Returns:
        PIL.Image: The encrypted image.
    """
    img_array = np.array(image)
    # Arithmetic operation: add key (mod 256)
    encrypted_array = (img_array.astype(np.int16) + key) % 256
    # Pixel swapping: mirror flip (both axes)
    encrypted_array = np.flip(encrypted_array, axis=(0, 1))
    return Image.fromarray(encrypted_array.astype(np.uint8))


def decrypt_image_obj(image, key):
    """
    Decrypts the image by mirror flipping and subtracting the key (mod 256).

    Parameters:
        image (PIL.Image): The encrypted image.
        key (int): Numeric key used for decryption.

    Returns:
        PIL.Image: The decrypted image.
    """
    img_array = np.array(image)
    # Reverse mirror flip
    decrypted_array = np.flip(img_array, axis=(0, 1))
    # Reverse arithmetic operation: subtract key (mod 256)
    decrypted_array = (decrypted_array.astype(np.int16) - key) % 256
    return Image.fromarray(decrypted_array.astype(np.uint8))


# --- GUI Functions ---

class ImageStegoEncryptorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Image Encryption & Text Hiding Tool")

        # Input image selection
        tk.Label(master, text="Select Image to Encrypt/Decrypt:").pack(pady=5)
        self.input_image_label = tk.Label(master, text="No image selected")
        self.input_image_label.pack(pady=5)
        tk.Button(master, text="Browse", command=self.select_input_image).pack(pady=5)

        # Output image path selection
        tk.Label(master, text="Output Image Path:").pack(pady=5)
        self.output_image_label = tk.Label(master, text="No output path selected")
        self.output_image_label.pack(pady=5)
        tk.Button(master, text="Save As", command=self.select_output_image).pack(pady=5)

        # Key entry
        tk.Label(master, text="Enter Numeric Key:").pack(pady=5)
        self.key_entry = tk.Entry(master)
        self.key_entry.pack(pady=5)

        # Text to hide (optional)
        tk.Label(master, text="Enter text to hide (optional):").pack(pady=5)
        self.text_entry = tk.Entry(master, width=50)
        self.text_entry.pack(pady=5)

        # Encrypt and Decrypt buttons
        tk.Button(master, text="Encrypt Image", command=self.encrypt).pack(pady=5)
        tk.Button(master, text="Decrypt Image", command=self.decrypt).pack(pady=5)

    def select_input_image(self):
        self.input_image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All Files", "*.*")]
        )
        if self.input_image_path:
            self.input_image_label.config(text=self.input_image_path)

    def select_output_image(self):
        self.output_image_path = filedialog.asksaveasfilename(
            title="Save Image As",
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg;*.jpeg"), ("All Files", "*.*")]
        )
        if self.output_image_path:
            self.output_image_label.config(text=self.output_image_path)

    def encrypt(self):
        # Get parameters from GUI
        try:
            key = int(self.key_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer.")
            return

        if not hasattr(self, 'input_image_path') or not self.input_image_path:
            messagebox.showerror("Error", "Please select an input image.")
            return
        if not hasattr(self, 'output_image_path') or not self.output_image_path:
            messagebox.showerror("Error", "Please select an output path.")
            return

        try:
            image = Image.open(self.input_image_path).convert("RGB")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {e}")
            return

        # If text is provided, hide it first in the original image.
        text_to_hide = self.text_entry.get().strip()
        if text_to_hide:
            try:
                image = hide_text(image, text_to_hide)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to hide text: {e}")
                return

        # Encrypt the image
        encrypted_image = encrypt_image_obj(image, key)

        try:
            encrypted_image.save(self.output_image_path)
            messagebox.showinfo("Success", f"Encrypted image saved to {self.output_image_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")

    def decrypt(self):
        # Get parameters from GUI
        try:
            key = int(self.key_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Key must be an integer.")
            return

        if not hasattr(self, 'input_image_path') or not self.input_image_path:
            messagebox.showerror("Error", "Please select an input image.")
            return
        if not hasattr(self, 'output_image_path') or not self.output_image_path:
            messagebox.showerror("Error", "Please select an output path.")
            return

        try:
            image = Image.open(self.input_image_path).convert("RGB")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {e}")
            return

        # Decrypt the image
        decrypted_image = decrypt_image_obj(image, key)

        # Try to extract hidden text from the decrypted image
        hidden_text = extract_text(decrypted_image)
        if hidden_text:
            messagebox.showinfo("Hidden Text", f"Extracted hidden text:\n{hidden_text}")
        else:
            messagebox.showinfo("Hidden Text", "No hidden text found.")

        try:
            decrypted_image.save(self.output_image_path)
            messagebox.showinfo("Success", f"Decrypted image saved to {self.output_image_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")


# --- Main GUI Loop ---

if __name__ == "__main__":
    root = tk.Tk()
    gui = ImageStegoEncryptorGUI(root)
    root.mainloop()
