# Image Stego Encryptor
### A GUI-based image encryption tool that demonstrates pixel-level manipulation to:

Encrypt and decrypt an image using arithmetic transformations and mirror flipping.
Optionally hide a text message inside the image using simple LSB steganography.
This tool allows users to securely encrypt images while also embedding hidden text messages for added security. It is designed to be lightweight, fast, and easy to use—ideal for both beginners and enthusiasts exploring cryptography and steganography.

## 🔥 Features
Encrypt & Decrypt Images: Utilizes reversible pixel transformations.
Steganography: Hide and extract secret messages via LSB manipulation.
User-Friendly GUI: Built with Tkinter for straightforward interaction.
Multi-Format Support: Works with JPG and PNG images.
Custom Encryption Key: Adds an extra layer of security.
Fast Processing: Powered by Python, Pillow, and NumPy.
## 🛠️ How It Works
Arithmetic Manipulation: Each pixel's RGB values is modified using a numeric key.
Pixel Swapping: The image is flipped both horizontally and vertically to further obfuscate its data.
LSB Steganography (Optional): A secret text message is embedded within the least significant bits of the image pixels.
During decryption, the same key reverses these operations, restoring the original image and retrieving any hidden message.

## 🖥️ GUI Version – How to Use
Run the script:
```sh
python image_stego_encryptor.py
```
step 1>>  Select an image to encrypt or decrypt.
step 2>>  Enter a numeric key (the same key must be used for both encryption and decryption).
step 3>>  (Optional) Enter a secret message to hide within the image.
step 4>>  Click Encrypt to scramble the image and embed the message.
step 5>>  Click Decrypt to restore the original image and extract the hidden message.
### Code Structure
encrypt_image(img, key): Encrypts the image using pixel transformations.
decrypt_image(img, key): Reverses the encryption to restore the image.
hide_text(img, message): Embeds a secret message inside the image.
extract_text(img): Retrieves the hidden message from the image.
Tkinter GUI Elements: Provide an interactive user interface.




# 🖥️ Terminal Version (CLI)
## use is script.py
For those who prefer command-line execution, a simplified version is available:

## Usage
```sh
python image_encryptor.py encrypt input.jpg encrypted.png 42
python image_encryptor.py decrypt encrypted.png decrypted.png 42
```
## how It Works
Encryption: Each pixel’s RGB values is modified by adding/subtracting a key (mod 256).
Decryption: Reverses the arithmetic operations to restore the original image.
Pixel Swapping: Flips the image horizontally and vertically for added obfuscation.

## 📦 Requirements
Ensure you have the following dependencies installed:

Python 3.x
Pillow: For image processing.
NumPy: For efficient numerical operations.
Tkinter: Typically pre-installed with Python.
To install the required packages, run:

```sh
pip install pillow numpy
```
## ⚠️ Security Disclaimer
This tool is intended for educational purposes only. While it applies basic image encryption and steganography techniques, it does not provide robust cryptographic security. For sensitive data, consider using industry-standard methods like AES.

###📜 License
This project is open-source and free to use. Contributions and improvements are welcome!


## 🔥 Improvements
Enhanced Explanations: Clearer breakdown of the encryption and steganography methods.
Structured Sections: Organized formatting for easier reading.
Separated CLI Instructions: Distinct guidelines for command-line users.
Clear Security Disclaimer: Highlights the limitations of the encryption approach.
Let me know if you need any modifications or additional features! 🚀
