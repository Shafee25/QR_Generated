import qrcode

myqr = qrcode.make("https://www.youtube.com/watch?v=IUQVO97zcE0&t=2s")

myqr.save("myqr.png", scale = 8)