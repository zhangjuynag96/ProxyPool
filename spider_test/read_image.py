import pytesseract
from PIL import Image
import PIL.ImageOps
import numpy as np

#--------------------------------
#numpy方法
# img = Image.open('test.bmp')
# img = np.array(img)
# img_ = np.array(list(map(lambda obj: obj if obj<1 else 255, img.ravel()))).reshape(img.shape)
# img = PIL.Image.fromarray(img_.astype(np.uint8))
# image = img.convert('L')
# threshold = 80
# table = []
# for j in range(256):
#     if j < threshold:
#         table.append(0)
#     else:
#         table.append(1)
# image = image.point(table, '1')
# port = pytesseract.image_to_string(img)
# print(port)
# print(port)

#-----------------------------------------------------------------
#填充背景色
# img.paste(img,(0,0,x,y),img)
# img.show()
# table = []
# for j in range(256):
#     if j < threshold:
#         table.append(0)
#     else:
#         table.append(1)
# image = image.point(table, '1')
# port = pytesseract.image_to_string(image,config='-psm 7 outputbase digits')
# print(port)


#------------------------------------------------------------------------
# im = Image.open('test.jpg','r')
# x,y = im.size
# p = Image.new('RGBA',im.size,(255,255,255))
# p.paste(im,(0,0,x,y),im)
# p.save('test1.png')
# img = Image.open('test1.png')
# image = img.convert('L')
# threshold = 80
# table = []
# for j in range(256):
#     if j < threshold:
#         table.append(0)
#     else:
#         table.append(1)
# image = image.point(table, '1')
# port = pytesseract.image_to_string(image,config='-psm 7 outputbase digits')

x = '505'
y = []
for i in range(0,len(x)):
    if x[i] == '5':
        y.append('8')
    else:
        y.append(x[i])
print(y)



