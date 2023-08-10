def encrypt(text, key=3):
    encrypted_text = ""
    for char in text:
        if char.isdigit():
            encrypted_text += chr((int(char) + key) % 26 + ord('A'))
        else:
            encrypted_text += chr((ord(char) + key) % 26 + ord('a'))
    return encrypted_text