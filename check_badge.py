# This function takes a picture as an input and investigates if it is a valid badge by checking : 

# the size of the picture
# the presence of a circle
# the presence of a happy feeling by checking the saturation and value channels of the HSV color space and comparing them to a threshold value




import sys
from PIL import Image

# The percentage of pixels that need to be happy for the image to be considered to communicate a happy feeling
OPTIMISTIC_PARAM = 25

def check_size(img,width,height):
    if img.size == (width,height): 
        print("PASSED : SIZE OK")
        return True
    print("FAILED : SIZE ERROR")
    return False

def happy_pixel(pixel):
    try:

        # Get the saturation and value channels
        saturation = pixel[1]
        value = pixel[2]

        return (saturation > 0.1 * 255 and value > 0.75 * 255)  or (saturation > 0.2 * 255 and value > 0.60 * 255) or (saturation > 0.3 * 255 and value > 0.40 * 255)
    except Exception as e:
        print(f"Error: {e}")

def check_happy_feeling(image):

    width, height = image.size

    # Convert the image to the HSV color space
    hsv_img = image.convert('HSV')

    # Check if the image is happy
    optimistic_pixels = 0

    for x in range(width):
        for y in range(height):
            # Get the pixel value at (x, y)
            pixel = hsv_img.getpixel((x, y))
            if happy_pixel(pixel):
                optimistic_pixels += 1

    if optimistic_pixels / (width * height) * 100 < OPTIMISTIC_PARAM: 
        print("FAILED : HAPPY FEELING NOT DETECTED : ", int(optimistic_pixels / (width * height) * 100), "% <", OPTIMISTIC_PARAM, "%" )
        return False
    
    print("PASSED : HAPPY FEELING DETECTED : ", int(optimistic_pixels / (width * height) * 100), "% >", OPTIMISTIC_PARAM, "%")
    return True

def get_pixels_outside_circle(width, height):

    # Initialize the array
    pixels_outside_circle = []
    radius = min(width, height) / 2

    # Iterate over all the pixels
    for x in range(width):
        for y in range(height):

            # Check if the pixel is outside the circle
            if (x - width / 2)**2 + (y - height / 2)**2 > radius**2:
                pixels_outside_circle.append((x, y))

    return pixels_outside_circle

PIXEL_OUTSIDE_CIRCLE_512x512 = get_pixels_outside_circle(512, 512)


def check_circle(image):
    
    image = image.convert('RGBA')
    width, height = image.size


    if (width,height) != (512, 512):
        pixels_outside_circle = get_pixels_outside_circle(width,height)
    else:
        pixels_outside_circle = PIXEL_OUTSIDE_CIRCLE_512x512

    # Iterate over the pixels outside the circle
    for pixel in pixels_outside_circle:

        # Get the pixel value at (x, y)
        pixel_value = image.getpixel(pixel)

        # Check if the pixel is transparent (alpha = 0)
        if pixel_value[3] != 0:
            print("FAILED : NONE-TRANSPARENT PIXEL OUTSIDE CIRCLE DETECTED")
            return False
        print("PASSED : NO NONE-TRANSPARENT PIXELS OUTSIDE CIRCLE DETECTED")
        return True

def check_badge(img,width,height):

    size_check = check_size(img,width,height)
    circle_check = check_circle(image=img)
    happy_check = check_happy_feeling(image=img)


    if circle_check == True & happy_check == True & size_check == True:
        print("-"*80)
        print(f"{img} passed all tests succefully.")


    return [size_check,happy_check,circle_check]



if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv)>1 else "./test_avatars/Avatar_in_circle/Icons_01.png"
    width = int(sys.argv[2]) if len(sys.argv)>2 else 512
    height =  int(sys.argv[3]) if len(sys.argv)>3 else 512
    
    try:
        # Open the image file
        with Image.open(image_path).convert("RGBA") as img:
            status = check_badge(img,width,height)
        
    except Exception as e:
        print(f"Error: {e}")