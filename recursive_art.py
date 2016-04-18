""" This code randomly generates computational art. The two functions I defined were squared and cubed which square and cube x.  """

import random
from PIL import Image
import math

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    operations = ['t','x','y','prod','avg','cubed','cos_pi','sin_pi','squared']
    #If max depth is zero, then the function has to end
    if max_depth == 0:
        index = random.randint(0,2)
    #If min depth is less than or equal to zero then the function can end
    elif min_depth <= 0:
        index = random.randint(0,8)
    #Otherwise, the function cannot end because it has not reached the minimum depth
    else:
        index = random.randint(3,8)
    #If the randomly generated index pertains to one of the first three operations in the list
    if index <= 2:
        return [operations[index]]
    #If the index pertains to either the fourth or fifth operations in the list
    elif index <=4:
        return [operations[index],build_random_function(min_depth-1,max_depth-1),build_random_function(min_depth-1,max_depth-1)]
    #Otherwise one of the last operations in the list
    else:
        return [operations[index],build_random_function(min_depth-1,max_depth-1)] 
    
def evaluate_random_function(f, x, y, t):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        t: the frame number
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75,1)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02,1)
        0.02
        >>> evaluate_random_function(['avg',['cubed',['x']],['y']],1,2,1)
        1.5
        >>> evaluate_random_function(['cubed',['x']],1.0,3,1)
        1.0
    """
    #This block of code checks the first item of the given function and executes the operation for the designated string
    if f[0] == 'prod':
        return evaluate_random_function(f[1],x,y,t)*evaluate_random_function(f[2],x,y,t)
    elif f[0] == 'avg':
        return .5*(evaluate_random_function(f[1],x,y,t)+evaluate_random_function(f[2],x,y,t))
    elif f[0] == 'cubed':
        return evaluate_random_function(f[1],x,y,t)**3.
    elif f[0] == 'sin_pi':
        return math.sin(math.pi*evaluate_random_function(f[1],x,y,t))
    elif f[0] == 'cos_pi':
        return math.cos(math.pi*evaluate_random_function(f[1],x,y,t)) 
    elif f[0] == 'squared':
        return evaluate_random_function(f[1],x,y,t)**2.
    elif f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    else:
        return t


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
        >>> remap_interval(3, -5, 5, 10, 20)
        18.0
    """
    val_fraction = float(val-input_interval_start)/(input_interval_end-input_interval_start)
    val_weighted = val_fraction*(output_interval_end-output_interval_start)+output_interval_start
    return val_weighted


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1.0, 1.0, 0.0, 255.0)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, num_frames, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(6,9)
    green_function = build_random_function(7,9)
    blue_function = build_random_function(8,13)

    for k in range(num_frames):
        # Create image and loop over all pixels
        im = Image.new("RGB", (x_size, y_size))
        pixels = im.load()
        t = remap_interval(k, 0, num_frames-1, -1, 1)
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                pixels[i, j] = (
                        color_map(evaluate_random_function(red_function, x, y, t)),
                        color_map(evaluate_random_function(green_function, x, y, t)),
                        color_map(evaluate_random_function(blue_function, x, y, t))
                        )
        im.save(filename + '_' + str(k) + '.png')


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art('frame',100)

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
