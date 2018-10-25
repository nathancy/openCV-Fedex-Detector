'''
Filename: gimptoHSV.py
Description: Convert Gimp HSV values into OpenCV HSV values 
Usage: python gimptoHSV.py 
'''

colors = raw_input("GIMP HSV values\n")
l = [int(x) for x in colors.split()]
gimpH = l[0]
gimpS = l[1]
gimpV = l[2]
opencvH = gimpH / 2
opencvS = (gimpS / 100) * 255
opencvV = (gimpV / 100) * 255
print('')
print('H: ' + str(opencvH) + "\n" + 'S: ' + str(opencvS) + '\n' + 'V: ' + str(opencvV))

