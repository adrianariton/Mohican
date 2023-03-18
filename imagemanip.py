from PIL import Image
from colorthief import ColorThief
from collections import Counter

im = Image.open("logos/1530.jpg")
width, height = im.size

color_thief = ColorThief('logos/1530.jpg')
# get the dominant color
dominant_color = color_thief.get_color(quality=1)
# build a color palette
palette = color_thief.get_palette(color_count=6)
print(palette)



colortuples = Counter(im.getdata())   # dict: color -> number

print(colortuples)
mycolor1 = min(colortuples)[1]
mycolor2 = max(colortuples)[1]

dark_mode = True

print(mycolor1, mycolor2)
pix = im.load()
for x in range(0, width):
    for y in range(0, height):
        # print(pix[x,y][1])
        if pix[x,y][1] >= 200 and pix[x, y][2] >= 200 and pix[x, y][0] >= 200:
            im.putpixel((x, y), (255, 255, 255))
            if dark_mode:
                im.putpixel((x, y), (0, 0, 0))

            
im.show()
print('AAAA')