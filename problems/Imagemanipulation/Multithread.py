from PIL import Image
import turtle
import random

# ============================================================
# IMAGE SETTINGS
# ============================================================
# image location on my pc
image_path = (
    r"C:\Users\Rheyan Shah\Documents\Intro To Computer Science"
    r"\Python\SoundDesign\imagemanipulation\input.jpg")

# turtle gets REALLY slow on giant images
# lowering this makes testing faster
max_size = 700

# ============================================================
# LOAD IMAGE
# ============================================================
print("loading image...")
image = Image.open(image_path)
image = image.convert("RGB")
width = image.width
height = image.height

# ============================================================
# RESIZE IMAGE IF TOO BIG
# ============================================================
if width > max_size or height > max_size:
    print("resizing image...")
    scale = min(
        max_size / width,
        max_size / height
    )
    width = int(width * scale)
    height = int(height * scale)
    image = image.resize((width, height))

# access pixels directly
pixels = image.load()

# ============================================================
# TURTLE SETUP
# ============================================================
print("setting up turtle...")
screen = turtle.Screen()
# important for RGB colors
screen.colormode(255)
# little extra room around image
screen.setup(width + 100, height + 100)
# warm background looked nicer
screen.bgcolor((240, 235, 220))
# massive speed boost
turtle.tracer(0, 0)

# ============================================================
# CREATE BRUSH
# ============================================================
brush = turtle.Turtle()
brush.speed(0)
brush.hideturtle()
brush.penup()


# ============================================================
# CONVERT IMAGE COORDS
# ============================================================
# PIL:
# top left is (0,0)
#
# turtle:
# center is (0,0)
#
# so convert coords
def convert_x(x):
    return x - (width / 2)

def convert_y(y):
    return (height / 2) - y

# ============================================================
# KEEP RGB VALUES SAFE
# ============================================================
def clamp(number):
    return max(0, min(255, number))

# ============================================================
# GET BRIGHTNESS
# ============================================================
# simple brightness estimate
# not physically accurate or anything
def get_brightness(pixel):
    return (
        pixel[0] +
        pixel[1] +
        pixel[2]
    ) / 3

# ============================================================
# GET STROKE ANGLE
# ============================================================
# comparing nearby pixels
# trying to follow image structure
#
# not real edge detection
# but works enough for this
def get_angle(x, y):
    # edge safety checks
    if x <= 1 or x >= width - 2:
        return random.randint(0, 360)
    if y <= 1 or y >= height - 2:
        return random.randint(0, 360)
    left_pixel = pixels[x - 1, y]
    right_pixel = pixels[x + 1, y]
    up_pixel = pixels[x, y - 1]
    down_pixel = pixels[x, y + 1]
    horizontal_change = abs(
        get_brightness(right_pixel) -
        get_brightness(left_pixel)
    )
    vertical_change = abs(
        get_brightness(down_pixel) -
        get_brightness(up_pixel)
    )
    # horizontal-ish brush strokes
    if horizontal_change > vertical_change:
        angle = random.randint(-20, 20)
    # vertical-ish brush strokes
    else:
        angle = random.randint(70, 110)
    # slight randomness
    # bigger values looked too messy
    angle += random.randint(-3, 3)
    return angle

# ============================================================
# ADD SMALL COLOR VARIATION
# ============================================================
# paintings are not perfectly flat
# this adds tiny pigment variation
def vary_color(color, amount):
    red = clamp(
        color[0] + random.randint(-amount, amount)
    )
    green = clamp(
        color[1] + random.randint(-amount, amount)
    )
    blue = clamp(
        color[2] + random.randint(-amount, amount)
    )
    return (red, green, blue)

# ============================================================
# DRAW ONE STROKE
# ============================================================
# straight lines looked too digital
# slight curves looked nicer
def draw_stroke(
    x,
    y,
    color,
    angle,
    length,
    thickness):
    brush.penup()
    brush.goto(x, y)
    brush.setheading(angle)
    # tiny pigment breakup
    variation = 3
    stroke_color = (
        clamp(
            color[0] + random.randint(-variation, variation)
        ),
        clamp(
            color[1] + random.randint(-variation, variation)
        ),
        clamp(
            color[2] + random.randint(-variation, variation)
        )
    )
    brush.pencolor(stroke_color)
    brush.pensize(thickness)
    brush.pendown()
    # slightly curved stroke
    for _ in range(3):
        brush.forward(length / 3)
        brush.right(
            random.randint(-3, 3)
        )
    # sometimes extend stroke slightly
    # creates rough bristle texture
    if random.random() < 0.15:
        brush.pensize(
            max(1, thickness - 1)
        )
        brush.forward(length * 0.3)
    brush.penup()

# ============================================================
# DRAW SMALL PAINT PATCH
# ============================================================
# one stroke alone looked weak
# grouped strokes looked more paint-like
def draw_patch(
    x,
    y,
    color,
    angle,
    length,
    thickness):
    for i in range(3):
        offset_x = random.randint(
            -thickness,
            thickness
        )
        offset_y = random.randint(
            -thickness,
            thickness
        )
        draw_stroke(
            x + offset_x,
            y + offset_y,
            color,
            angle,
            length + random.randint(-2, 2),
            thickness
        )

# ============================================================
# PAINTING LAYERS
# ============================================================
# bigger strokes first
# smaller details later
layers = [
    # big background shapes
    {
        "step": 28,
        "length": 34,
        "thickness": 18,
        "variation": 3
    },
    # large forms
    {
        "step": 20,
        "length": 24,
        "thickness": 12,
        "variation": 4
    },
    # medium forms
    {
        "step": 14,
        "length": 18,
        "thickness": 8,
        "variation": 5
    },
    # structure layer
    {
        "step": 10,
        "length": 12,
        "thickness": 6,
        "variation": 6
    },
    # detail layer
    {
        "step": 7,
        "length": 8,
        "thickness": 4,
        "variation": 7
    },
    # finer detail
    {
        "step": 5,
        "length": 5,
        "thickness": 3,
        "variation": 6
    },
    # extra detail
    {
        "step": 4,
        "length": 4,
        "thickness": 2,
        "variation": 5
    },
    # tiny details
    {
        "step": 2,
        "length": 2,
        "thickness": 1,
        "variation": 4
    }]

# ============================================================
# PAINT ONE LAYER
# ============================================================
def paint_layer(layer):
    print()
    print("painting layer...")
    print(layer)
    step = layer["step"]
    length = layer["length"]
    thickness = layer["thickness"]
    variation = layer["variation"]
    for y in range(0, height, step):
        # offset rows slightly
        # avoids obvious grids
        x_offset = random.randint(0, step)
        for x in range(x_offset, width, step):
            color = pixels[x, y]
            # small paint variation
            color = vary_color(
                color,
                variation
            )
            angle = get_angle(x, y)
            draw_x = convert_x(x)
            draw_y = convert_y(y)
            draw_patch(
                draw_x,
                draw_y,
                color,
                angle,
                length,
                thickness
            )
        turtle.update()

# ============================================================
# MAIN PAINT LOOP
# ============================================================
print()
print("starting painting...")

for layer in layers:
    paint_layer(layer)

# ============================================================
# FINISH
# ============================================================
turtle.update()
print()
print("finished!")
turtle.done()