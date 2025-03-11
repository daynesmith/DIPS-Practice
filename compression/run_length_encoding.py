import dip
from dip import *

class Rle:
    def __init__(self):
        pass

    def encode_image(self,binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        img = binary_image.copy()

        rle_code = [[]for _ in range(img.shape[0])]
        #rle code will be stored in 2d array each row will contain runlength encoding for each row in the image. if white w if black b
        for row_count, row in enumerate(img):
            prev_pixel = row[0] #start with first pixel
            count = 1   #count = 1 to account for first pixel

            for pixel in row[1:]: #loop starts at second pixel
                if pixel == prev_pixel:
                    count += 1
                else: #if current pixel doesnt match prev append prev run length to rle and reset count
                    rle_code[row_count].append([prev_pixel, count])
                    prev_pixel = pixel
                    count = 1
            
            #append last run length in row
            rle_code[row_count].append([prev_pixel, count])


        return rle_code  # replace zeros with rle_code

    def decode_image(self, rle_code, height , width):
        """
        Get original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """
        #rle_code each element has [pixel_value, count]

        img = zeros((height, width), dtype = uint8)#create an array to store image with height and width given

        for row_count , row in enumerate(rle_code):
            col_count = 0
            for rle in row:
                for _ in range(rle[1]):
                    img[row_count][col_count] = rle[0] 
                    col_count += 1   

        return  img  # replace zeros with image reconstructed from rle_Code





        




