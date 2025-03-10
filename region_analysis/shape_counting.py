import dip
from dip import *

class ShapeCounting:
    def __init__(self):
        pass

    def blob_coloring(self, image):
        """Implement the blob coloring algorithm
        takes as input:
        image: binary image
        return: a list/dict of regions
        """
        blob_img = [[0] * len(image[0]) for _ in range(len(image))] #create array with same dimensions as n

        for i in range(len(image)):     #put values into blob_img but with datatype int now so that if there are more than 256 regions there arent issues uint8 would cause issues
            for j in range(len(image[i])):
                blob_img[i][j] = image[i][j]

        regions = dict()

        #this function will iterate through the blob_image get the intensity value, compare it to the above and left blob values, and change to correct region. 
        #in blob_img 0 == background, >0 == foreground regions

        for i in range(len(blob_img)):   #iterate through rows
            for j in range(len(blob_img[i])): #iterate through columns
                
                #get current pixel value
                curr_pixel = blob_img[i][j]
                top_pixel = None
                left_pixel = None
                #get region values of above and left pixels
                if i > 0:
                    top_pixel = blob_img[i-1][j]
                if j > 0:
                    left_pixel = blob_img[i][j-1]
                

                if curr_pixel == 255:
                    #check if both above pixel and left pixel are part of blob if so if they are not the same add left pixel blob to top blob, if they are same just add curr pixel to blob
                    if left_pixel is not None and left_pixel != 0 and top_pixel is not None and top_pixel != 0:
                        if left_pixel != top_pixel:
                            blob_img[i][j] = top_pixel
                            regions[top_pixel].append((i,j))
                            regions[top_pixel].extend(regions[left_pixel])
                            regions[left_pixel] = []
                        else:
                            blob_img[i][j] = top_pixel
                            regions[top_pixel].append((i,j))
                    #if top pixel present add current to that blob
                    elif top_pixel is not None and top_pixel != 0:
                        blob_img[i][j] = top_pixel
                        regions[top_pixel].append((i,j))
                    #if left pixel present add current to that blob
                    elif left_pixel is not None and left_pixel != 0:
                        blob_img[i][j] = left_pixel
                        regions[left_pixel].append((i,j))
                    
                    else:    #if no blobs connected left or right then add new region
                        blob_img[i][j] = (max(list(regions.keys())) + 1)
                        regions[blob_img[i][j]] = [(i,j)]

                else:
                    blob_img[i][j] = 0
                    regions.setdefault(0,[]).append((i,j))
        """      
        #get rid of keys with less than 10 pixels
        keys_list = list(regions.keys())
        print(len(regions.keys()))
        for key in keys_list:
            if len(regions[key]) < 10:
                del regions[key]
        print(len(regions.keys()))
        #should print 101 regions after reduction 0 is background and the rest are the 100 foreground elements """

        return regions

    def identify_shapes(self, region):
        """Compute shape features area and centroid, and shape
        Ignore shapes smaller than 10 pixels in area.
        takes as input
        region: a list/dict of pixels in a region
        returns: shapes, a data structure with centroid, area, and shape (c, s, r, or e) for each region
        c - circle, s - squares, r - rectangle, and e - ellipse
        """

        # Please print your shape statistics to stdout, one line for each shape
        # Region: <region_no>, centroid: <centroid>, area: <shape area>, shape: <shape type>
        # Example: Region: 871, centroid: (969.11, 51.11), area: 707, shape: c

        shapes = dict()

        return shapes

    def count_shapes(self, shapes_data):
        """Compute the count of shapes using the shapes data returned from identify shapes function
           takes as input
           shapes_data: a list/dict of regions, with centroid, shape, and area for each shape
           returns: a dictionary with count of each shape
           Example return value: {'circles': 21, 'ellipses': 25, 'rectangles': 31, 'squares': 23}
           """
        return {"circles": 0, "ellipses": 0, "rectangles": 0, "squares": 0}

    def mark_image_regions(self, image, shapes_data):
        """Creates a new image with computed stats for each shape
        Make a copy of the image on which you can write text.
        takes as input
        image: binary image
        shapes_data: a list/dict of regions, with centroid, shape, and area for each shape
        returns: image marked with center and shape_type"""

        return image

