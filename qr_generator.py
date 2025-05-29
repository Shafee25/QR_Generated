import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

myqr = qrcode.make("https://www.youtube.com/watch?v=IUQVO97zcE0&t=2s")

myqr.save("myqr.png", scale = 8)

img = decode(Image.open("myqr.png"))

print(img[0].data.decode("ascii"))