import dip
from dip import *
import math
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
            
        #get rid of keys with less than 10 pixels so we dont have to worry about it in next section
        keys_list = list(regions.keys())
        for key in keys_list:
            if len(regions[key]) < 10:
                del regions[key]
        
        #101 regions after eliminating regions < 10 pixels in size, key 0 is background and the rest are the 100 foreground elements

        del regions[0] #delete 0 because we dont need to get the information for the background
        return regions

    def identify_shapes(self, regions):
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

        #shapes = {"key : [centroid, area, region_shape]"}
        shapes = dict()
        region_keys = regions.keys()

        for key in region_keys:
            #get i and j of each pixel in region weighted sum for centroid.
            i_sum = 0
            j_sum = 0
            for i, j in regions[key]:
                i_sum += i
                j_sum += j
            centroid = (i_sum / len(regions[key]), j_sum / len(regions[key]))
            #area is just all pixels in the region
            area = len(regions[key])
            
            #check for shapes
            #we will check for shapes by calculating max and min i and j within each region.
            max_i = None
            min_i = None
            max_j = None
            min_j = None

            for i, j in regions[key]:
                if min_i is None or i < min_i:
                    min_i = i
                if max_i is None or i > max_i:
                    max_i = i
                if min_j is None or j < min_j:
                    min_j = j
                if max_j is None or j > max_j:
                    max_j = j

            #check heigh and width if they are same or similar you should check for square then circle
            i_length = max_i - min_i
            j_length = max_j - min_j
            region_shape = None
            if abs((max_i - min_i) - (max_j - min_j)) < 2:
                #for a circle that has the same width and height as a square the circles area will be 78.5%.
                #to check for square or circle i will calculate area and say anything > 89.25% is a square
                if area > (i_length * j_length * .8925):
                    region_shape = "s"
                else:
                    region_shape = "c"
            else:
                #same check for rectangle or ellipse, ellipse is 78.5% of the area within rectangle based on i length and j length
                if area > (i_length * j_length * .8925):
                    region_shape = "r"
                else:
                    region_shape = "e"



            shapes[key] = [centroid, area, region_shape]

        

        print(*shapes.values(), sep = '\n')
        return shapes

    def count_shapes(self, shapes_data):
        """Compute the count of shapes using the shapes data returned from identify shapes function
           takes as input
           shapes_data: a list/dict of regions, with centroid, shape, and area for each shape
           returns: a dictionary with count of each shape
           Example return value: {'circles': 21, 'ellipses': 25, 'rectangles': 31, 'squares': 23}
           """
        shapes = shapes_data.keys()
        circles = 0
        ellipses = 0
        squares = 0
        rectangles = 0

        for key in shapes:
            for s in shapes_data[key]:
                if s == "c":
                    circles +=1
                elif s == "s":
                    squares += 1
                elif s == "r":
                    rectangles += 1
                elif s == "e":
                    ellipses += 1

        return {"circles": circles, "ellipses": ellipses, "rectangles": rectangles, "squares": squares}

    def mark_image_regions(self, image, shapes_data):
        """Creates a new image with computed stats for each shape
        Make a copy of the image on which you can write text.
        takes as input
        image: binary image
        shapes_data: a list/dict of regions, with centroid, shape, and area for each shape
        returns: image marked with center and shape_type"""
        final_image = image.copy()
        
        for key, shape_info in shapes_data.items():
            pixel = tuple(math.floor(x) for x in reversed(shape_info[0]))
            text = shape_info[2]
            putText(
                final_image,
                text,
                pixel,
                1,
                2,
                (0,0,0),
                1
            )


        return final_image

