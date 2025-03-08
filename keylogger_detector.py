import sys
from PIL import Image
from cryptography.fernet import Fernet
from io import BytesIO

class SteganographyTool:
    def __init__(self):
        self.encryption_key = None

    def _int_to_bin(self, x):
        """Convert integer to 8-bit binary"""
        return format(x, '08b')

    def _bin_to_int(self, bin_str):
        """Convert binary string to integer"""
        return int(bin_str, 2)

    def _encode_data_to_image(self, img, data):
        """Encode data into image using LSB"""
        encoded = img.copy()
        width, height = img.size
        data += "====="  # End-of-data marker

        # Convert data to binary
        binary_data = ''.join([self._int_to_bin(byte) for byte in data.encode('utf-8')])

        if len(binary_data) > width * height * 3:
            raise ValueError("Image too small to hold this data!")

        data_index = 0

        for y in range(height):
            for x in range(width):
                pixel = list(encoded.getpixel((x, y)))

                for color_channel in range(3):  # R, G, B
                    if data_index < len(binary_data):
                        pixel[color_channel] = pixel[color_channel] & ~1 | int(binary_data[data_index])
                        data_index += 1

                encoded.putpixel((x, y), tuple(pixel))

                if data_index >= len(binary_data):
                    return encoded
        return encoded

    def _decode_data_from_image(self, img):
        """Extract hidden data from image"""
        binary_data = []
        width, height = img.size

        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                for color_channel in range(3):  # R, G, B
                    binary_data.append(str(pixel[color_channel] & 1))

        # Convert binary to bytes
        all_bytes = [self._bin_to_int(''.join(binary_data[i:i+8]))
                    for i in range(0, len(binary_data), 8)]

        # Find end marker
        decoded_bytes = bytes()
        for i, byte in enumerate(all_bytes):
            decoded_bytes += bytes([byte])
            if decoded_bytes[-5:] == b'=====':
                return decoded_bytes[:-5].decode('utf-8')

        return decoded_bytes.decode('utf-8')

    def encrypt_data(self, data, password=None):
        """Encrypt data before encoding"""
        if password:
            key = Fernet.generate_key()
            cipher = Fernet(key)
            encrypted_data = cipher.encrypt(data.encode())
            return key + encrypted_data
        return data

    def decrypt_data(self, encrypted_data, password=None):
        """Decrypt extracted data"""
        if password:
            key = encrypted_data[:44]  # Fernet key length
            cipher = Fernet(key)
            return cipher.decrypt(encrypted_data[44:]).decode()
        return encrypted_data

    def encode(self, input_image, output_image, secret_data, password=None):
        """Main encode function"""
        img = Image.open(input_image)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Encrypt data if password provided
        if password:
            secret_data = self.encrypt_data(secret_data, password)

        encoded_img = self._encode_data_to_image(img, secret_data)
        encoded_img.save(output_image, format='PNG')

    def decode(self, encoded_image, password=None):
        """Main decode function"""
        img = Image.open(encoded_image)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        extracted_data = self._decode_data_from_image(img)

        if password:
            return self.decrypt_data(extracted_data, password)
        return extracted_data

if __name__ == "__main__":
    tool = SteganographyTool()

    if len(sys.argv) < 4:
        print("Usage:")
        print("Encode: python stego.py encode input.png output.png 'secret message' [password]")
        print("Decode: python stego.py decode encoded.png [password]")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "encode":
        input_img = sys.argv[2]
        output_img = sys.argv[3]
        secret = sys.argv[4]
        password = sys.argv[5] if len(sys.argv) > 5 else None
        tool.encode(input_img, output_img, secret, password)
        print(f"Data encoded to {output_img}")

    elif mode == "decode":
        encoded_img = sys.argv[2]
        password = sys.argv[3] if len(sys.argv) > 3 else None
        result = tool.decode(encoded_img, password)
        print("Extracted data:")
        print(result)

    else:
        print("Invalid mode! Use 'encode' or 'decode'")

