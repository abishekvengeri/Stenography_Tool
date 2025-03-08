
---

# **Steganography Tool for Hiding Data in Images** 🖼️🔒

## **Overview**

This tool allows users to hide and extract data from images using steganography. It supports encryption for added security.

## **Features** 🚀

- **Encode**: Hide text or files inside PNG images.
- **Decode**: Extract hidden data from images.
- **Encryption**: Optional AES encryption for secure hidden data.
- **Multiple Formats**: Supports PNG, BMP (lossless formats).

---

## **Installation** 📦

Ensure you have Python 3 installed, then install the required dependencies:

```bash
pip install pillow cryptography
```

---

## **Usage** ⚡

### **Encoding Data into an Image**
#### Without encryption:
```bash
python stego.py encode input.png output.png "This is a secret message"
```

#### With AES encryption:
```bash
python stego.py encode input.png output.png "Top secret" mypassword
```

---

### **Decoding Data from an Image**
#### Without a password:
```bash
python stego.py decode output.png
```

#### With a password:
```bash
python stego.py decode output.png mypassword
```

---

## **How It Works** 🛠️

1. **Encoding**:
   - Converts secret data into a binary format.
   - Hides data in the least significant bits (LSB) of image pixels.
   - Saves the modified image.

2. **Decoding**:
   - Extracts the binary data from the image.
   - Converts it back to readable text.
   - If encrypted, decrypts using the provided password.

---

## **Example Workflow** 📋

```bash
python stego.py encode cover.png secret.png "Confidential Data"
python stego.py decode secret.png
```

Output:
```
Extracted data: Confidential Data
```

