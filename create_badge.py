# This function takes a picture as an input and does the following : 

# resize it to 512*512 pixels
# Add a happy feeling to the picture 
# deletes all the pixels outside the circle

import sys
import os
from PIL import Image

from check_badge import check_badge, happy_pixel,get_pixels_outside_circle,PIXEL_OUTSIDE_CIRCLE_512x512


import os

def is_png(file_path):
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        return False

    # Get the file extension
    _, file_extension = os.path.splitext(file_path)

    # Check if the file extension is ".png"
    return file_extension.lower() == ".png"

def resize(image,width,height):

    # Resize the image
    img = image.resize((width, height))
    return img

def add_happy_feeling(image,width,height):
    # Convert the image to the HSV color space
    hsv_img = image.convert('HSV')

    for x in range(width):
        for y in range(height):

            pixel = hsv_img.getpixel((x, y))

            if not happy_pixel(pixel):
                hsv_img.putpixel((x, y), (pixel[0], pixel[1] + 10, pixel[2] + 75))

    # Convert the image back to RGBA color space
    image = hsv_img.convert('RGBA')
    return image
            
def delete_pixels_outside_circle(image,width,height):
    image = image.convert('RGBA') 
    if (width,height) != (512, 512):
        pixels_outside_circle = get_pixels_outside_circle(width,height)
    else:
        pixels_outside_circle = PIXEL_OUTSIDE_CIRCLE_512x512

    # Iterate over the pixels outside the circle
    for pixel in pixels_outside_circle:

    # Set the pixel value to transparent
        image.putpixel(pixel, (0, 0, 0, 0))
    return image       

def create_badge(image_path,width,height,output_path):

    try:
        # Open the image file
        with Image.open(image_path) as img:

            status = check_badge(img,width,height)

            if status == [True,True,True] and is_png(image_path):

                print("BADGE already matches the qualifications")
                return True
            
            elif status == [True,True,True] and not is_png(image_path):

                print("BADGE already matches the qualifications but is not a png file")
                print("Converting to png file..")
                img.save(output_path,"PNG")
                return True
            

            if status[0] == False: img = resize(img,width,height)
            if status[1] == False: img = add_happy_feeling(img,width,height) 
            if status[2] == False or status[1] == False: img = delete_pixels_outside_circle(img,width,height)
   
            # Save the image
            print("-"*80)
            print("Badge created and saved at : ",output_path)
            img.save(output_path, "PNG")
            
    except Exception as e:
        print(f"Error: {e}")



if __name__ == "__main__":

    image_path = sys.argv[1] if len(sys.argv)>1 else "./test_avatars/Test.png"
    width = int(sys.argv[2]) if len(sys.argv)>2 else 512
    height =  int(sys.argv[3]) if len(sys.argv)>3 else 512
    

    create_badge(image_path,width,height,f"{image_path[:-4]}_badge.png")

