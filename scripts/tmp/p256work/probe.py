from PIL import Image
import os
os.makedirs('/tmp/p256/probe', exist_ok=True)
# s4: zgornji del leve strani, x 40–640 (datum+vas+hiša+začetek imena), y 280–900, ×3
im = Image.open('/tmp/p256/s4.jpg')
c = im.crop((40, 280, 640, 900))
c = c.resize((c.width*3, c.height*3), Image.LANCZOS)
c.save('/tmp/p256/probe/s4_topL.jpg', quality=92)
print('s4_topL', c.size)
