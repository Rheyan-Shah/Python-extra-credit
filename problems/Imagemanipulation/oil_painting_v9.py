from PIL import Image
import turtle
import random

#THIS CODE SHOULD BE LEFT RUNNING FOR A WHILE, IT IS PAINTING THE IMAGE WITH TURTLE, IT IS NOT INSTANT, BUT THE RESULT LOOKS REALLY GOOD(i hope)

# ID SUDGEST LEAVING IT RUNNING OVERNIGHT OR WHEN U GO FOR A MEAL 

# this code is a reworked version of a previous code that used kernels to try and do the same 
#the previous code used NPR techniques and kernels to make it an oil painting but the output wasnt pleasing enough(Anisotropic Kuwahara Filtering+kernals(i initially tried to do it via kernels only and then realised it wasnt possibel))

#WARNING:
#THIS CODE HAS A LONG RUNTIME. THERE IS A LINE AT 289 IF YOU DONT HAVE THE TIME PLS COMMENT IT OUT. TY

#this need to be in the same location as ur terminal
image_path ="input.jpg" 

# turtle took a ridiculous amount of time with with huge images(like 30 hours atp)
# this was mostly for testing
# but became kinda necessary affter i left the code running for a day and it still wasnt done,
# so i had to stop it and make this change to get it to a point where it would finish in a reasonable time frame
max_size = 700


# LOAD IMAGE

print("loading image...")

image = Image.open(image_path)
image = image.convert("RGB")

width = image.width
height = image.height


# RESIZE IMAGE

# i commented this out for final renders before, but i would keep it enabled
# full res = much nicer detail and looks realy good,
# my pc could not handel it(olny way it worked was when i tried multithreading but was way too complex and out of the scope of the assignment)

if width > max_size or height > max_size:

    print("resizing image...")

    scale = min(max_size / width, max_size / height)

    width = int(width * scale)
    height = int(height * scale)

    image = image.resize((width, height))


# lets access pix directly
pix = image.load()


# TURTLE SETUP

print("setting up turtle...")

screen = turtle.Screen()

# turtle normally wants colors from 0 to 1
# this switches it to normal RGB values

screen.colormode(255)

screen.setup(width + 100, height + 100)

# warm background looked more like a vintage oil painting
screen.bgcolor((240, 235, 220))#suggested by an Ai

# huge speed boost
turtle.tracer(0, 0)


# CREATE BRUSH

t = turtle.Turtle()

t.speed(0)
t.hideturtle()
t.penup()


# CONVERT IMAGE COORDS

# PIL starts from top left
# turtle starts from center
# so this shifts coords into turtle space

def convert_x(x):

    return x - (width / 2)


def convert_y(y):

    return (height / 2) - y


# KEEP RGB VALUES VALID

def clamp(num):

    return max(0, min(255, num))


# GET BRIGHTNESS

# #AI used 

# super rough brightness estimate
# just averaging rgb values

def getbright(Pix):

    brightness = (Pix[0] + Pix[1] + Pix[2]) / 3

    return brightness


# TRY TO FOLLOW IMAGE FLOW

# this compares nearby pix
# and tries to aim strokes based on sourunding pixels
# added this control(by mistake trying to do edge detection, but looked better so i amde it more prominent)
# helped a LOT compared to random directions

def get_angle(x, y):#ressult of an AI sudegetion affter seeing a version with no structure at all

    # stops crashes near edges
    if x <= 1 or x >= width - 2:
        return random.randint(0, 360)

    if y <= 1 or y >= height - 2:
        return random.randint(0, 360)

    lpix = pix[x - 1, y]
    rpix = pix[x + 1, y]

    uppix = pix[x, y - 1]
    dwnpix = pix[x, y + 1]

    horizontal_change = abs(getbright(rpix) - getbright(lpix))

    vertical_change = abs(getbright(dwnpix) - getbright(uppix))

    # if nearby pix change more sideways
    # use more horizontal strokes

    if horizontal_change > vertical_change:

        angle = random.randint(-20, 20)

    # otherwise lean more vertical

    else:

        angle = random.randint(70, 110)

    # tiny wobble helped it feel less like a pixilated picture

    angle = angle + random.randint(-3, 3)

    return angle


# SLIGHT COLOR VARIATION

# flat colors looked too digital
# this breaks them up a little and maed the picture more random

def vary_color(color, amount):

    red = color[0] + random.randint(-amount, amount)
    green = color[1] + random.randint(-amount, amount)
    blue = color[2] + random.randint(-amount, amount)

    red = clamp(red)
    green = clamp(green)
    blue = clamp(blue)

    return (red, green, blue)


# DRAW SINGLE STROKE

# perfectly straight lines looked fake
# slight curves looked way more paint-like

def draw_stroke(x, y, color, angle, length, thickness):

    t.penup()

    t.goto(x, y)

    t.setheading(angle)

    # tiny pigment breakup
    # helps stop everything looking flat

    

    stroke_red = clamp(color[0] + random.randint(-3, 3))
    stroke_green = clamp(color[1] + random.randint(-3, 3))
    stroke_blue = clamp(color[2] + random.randint(-3, 3))

    stroke_color = (stroke_red, stroke_green, stroke_blue)

    t.pencolor(stroke_color)

    t.pensize(thickness)

    t.pendown()

    # little curves inside each stroke
    # this helped a lot visually

    for i in range(3):

        t.forward(length / 3)

        turn_amount = random.randint(-3, 3)

        t.right(turn_amount)

    # sometimes extend the stroke slightly
    # gives rough bristle/a psay can texture

    if random.random() < 0.15:

        t.pensize(max(1, thickness - 1))

        t.forward(length * 0.3)

    t.penup()


# DRAW SMALL PAINT PATCH

# one line alone looked really realy weird 
# grouping strokes together made it feel and got rid of some ghost empty pixels

def draw_patch(x, y, color, angle, length, thickness):

    for i in range(3):

        offset_x = random.randint(-thickness, thickness)
        offset_y = random.randint(-thickness, thickness)
        random_length = length + random.randint(-2, 2)
        draw_stroke(x + offset_x, y + offset_y, color, angle, random_length, thickness)


# PAINTING LAYERS

# bigger strokes first, giving a base for the colours…
# then smaller detail passes later
 #used ai to make this
#inspertaion was from https://www.cl.cam.ac.uk/teaching/0910/RSL/Richardt.pdf page 55(saw it in a vid once)
layers = [

    # [step, length, thickness, variation]

    # big background colors
    [28, 34, 18, 3],

    # large forms
    [20, 24, 12, 4],

    # medium shapes
    [14, 18, 8, 5],

    # structure pass
    [10, 12, 6, 6],

    # starts bringing detail back
    [7, 8, 4, 7],

    # smaller texture
    [5, 5, 3, 6],

    # finer details
    [4, 4, 2, 5],

    # tiny detail layer; MAKE THIS A COMMENT IF U WANT A QUICK RUN TIME BUT LOW QUALITY
    [2, 2, 1, 4]

]

# PAINT LAYER


def paint_layer(layer):

    updater = 0

    step = layer[0]
    length = layer[1]
    thickness = layer[2]
    variation = layer[3]

    print()
    print("painting layer...")
    print("step =", step)
    print("length =", length)
    print("thickness =", thickness)
    print("variation =", variation)
    for y in range(0, height, step):

        # offset rows a bit
        # stops visible grid patterns

        x_offset = random.randint(0, step)

        for x in range(x_offset, width, step):

            color = pix[x, y]

            color = vary_color(color, variation)

            angle = get_angle(x, y)

            draw_x = convert_x(x)
            draw_y = convert_y(y)

            draw_patch(draw_x,draw_y, color, angle, length, thickness)

            updater = updater + 1 #using this to showe whats the proces on the screen

            # updating every single stroke was too slow
            # this felt like a decent balance

            if updater % 20 == 0:

                turtle.update()


# MAIN PAINT LOOP

print()
print("starting painting...")

for layer in layers:

    paint_layer(layer)


# FINISH

turtle.update()

print()
print("finished!")

turtle.done()
