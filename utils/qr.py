import qrcode  

def generate_qr(string):
    qr_img = qrcode.make(string)  
    path = f"media/qr_codes/{string}.jpg"
    qr_img.save(path)  
    return path