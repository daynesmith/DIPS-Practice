import dip
from dip import *

class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """ Computes the histogram of the input image
        takes as input:
        image: a greyscale image
        returns a histogram as a list """
        
        
        hist = [0]*256
        """
        image = [
            [z,x,c,v,b],
            [s,d,f,g,h],
            [w,e,r,t,y],
        ]
        """

        #iterate through each pixel in each row and add add to respective greyscale value
        for row in image:
            for pixel in row:
                hist[pixel] += 1

        return hist

    def find_threshold(self, hist):
        """ analyses a histogram to find the optimal threshold assuming that the input histogram is bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value
        Note: Use the iterative method to calculate the histogram. Do not use the Otsu's method
        Write your code to compute the optimal threshold method.
        This should be implemented using the iterative algorithm discussed in class (See Week 4, Lecture 7, slide 40
        on teams). Do not implement the Otsu's thresholding method. No points are awarded for Otsu's method.
        """

        #starting threshold will be between min and max pixel values
        oldthreshold =  256 // 2
        while True:
            lower_sum = 0
            upper_sum = 0
            lower_count = 0
            upper_count = 0


            for i in range(0,oldthreshold):
                lower_sum += i* hist[i] #weighted sum lower pixels
                lower_count += hist[i]  #number of pixels in lower threshold
                

            for i in range(oldthreshold,256):
                upper_sum += i * hist[i] #weighted sum upper pixels
                upper_count += hist[i]   #number of pixels in upper


            lower_mean = lower_sum // lower_count #calc means for new threshold
            upper_mean = upper_sum // upper_count
            
            
            newthreshold = (upper_mean + lower_mean) // 2
            print(newthreshold-oldthreshold)
            if abs(newthreshold - oldthreshold) == 0:
                break
            else:
                oldthreshold = newthreshold


        return newthreshold

    def binarize(self, image, threshold):
        """ Comptues the binary image of the input image based on histogram analysis and thresholding
        takes as input
        image: a greyscale image
        threshold: to binarize the greyscale image
        returns: a binary image """

        bin_img = image.copy()

        return bin_img


