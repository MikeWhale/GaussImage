    
from PIL import Image
from PIL import ImageChops
import sys, time
from cStringIO import StringIO
import urllib

def dhash(gurl, hash_size = 8):
	
    file_jpgdata = StringIO(gurl)
    image = Image.open(file_jpgdata)
    
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize((hash_size + 1, hash_size),Image.ANTIALIAS)

    pixels = list(image.getdata())

    # Compare adjacent pixels.
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # Convert the binary array to a hexadecimal string.
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0

    return ''.join(hex_string)
    
def compare_hash(hash1, hash2):

	hash_list = [int(hash1[i:i+1] == hash2[i:i+1]) for i in range(max(len(hash1), len(hash2)))]

	total_chars = len(hash_list)
	total_matches = sum(hash_list)

	hash_sim = float(total_matches) / total_chars
	hash_diff = 1 - hash_sim
	
	return hash_sim
