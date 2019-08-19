import qrcode
import random
chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def rnd(length):
    global chars
    return ''.join(random.choice(chars) for p in range(length))


a = open('codes/codes.txt', 'w')
a.close()


for i in range(7):
    code = rnd(5)
    with open('codes/codes.txt', 'a') as f:
        f.write(str(code) + '\n')
    img = qrcode.make(code)
    img.save(f"codes/qr-code{i + 1}.png")
