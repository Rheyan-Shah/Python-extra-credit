from PIL import Image
import turtle
import random
import math

# ============================================================
# LOAD IMAGE
# ============================================================
# Open image
image = Image.open(
    r"C:\Users\Rheyan Shah\Documents\Intro To Computer Science\Python\SoundDesign\imagemanipulation\input.jpg")

# Convert image to RGB
image = image.convert("RGB")

# ============================================================
# IMAGE SIZE
# ============================================================
width = image.width
height = image.height

# ============================================================
# OPTIONAL RESIZE
# ============================================================
# Turtle becomes VERY slow on huge images.
#
# Resize large images for painting.
#
# You can increase this later.
max_size = 500
if width > max_size or height > max_size:
    scale = min(
        max_size / width,
        max_size / height
    )
    width = int(width * scale)
    height = int(height * scale)
    image = image.resize((width, height))

# ============================================================
# ACCESS PIXELS
# ============================================================
pixels = image.load()

# ============================================================
# TURTLE SETUP
# ============================================================
screen = turtle.Screen()
# Screen size
screen.setup(width + 100, height + 100)
# Black background makes colors pop
screen.bgcolor("black")
# Disable animation for speed
turtle.tracer(0, 0)
paint_brush = turtle.Turtle()
paint_brush.speed(0)
paint_brush.hideturtle()
paint_brush.penup()

# ============================================================
# CONVERT IMAGE COORDINATES
# ============================================================
# PIL:
#
# (0,0) is top-left
#
# Turtle:
#
# (0,0) is center
#
# So we convert coordinates.
def convert_x(x):
    return x - (width / 2)

def convert_y(y):
    return (height / 2) - y

# ============================================================
# BRUSH STROKE FUNCTION
# ============================================================
# This draws ONE paint stroke.
#
# Instead of drawing pixels,
# we draw little colored lines.
#
# THAT is what creates
# the painted look.
def brush_stroke(x, y, color, angle, length, thickness):
    paint_brush.penup()
    paint_brush.goto(x, y)
    paint_brush.setheading(angle)
    paint_brush.pencolor(color)
    paint_brush.pensize(thickness)
    paint_brush.pendown()
    paint_brush.forward(length)
    paint_brush.penup()

# ============================================================
# SIMPLE EDGE DIRECTION
# ============================================================
# We estimate image direction
# using nearby brightness.
#
# This is a simplified
# edge detector.
def get_direction(x, y):
    if x <= 0 or x >= width - 1:
        return random.randint(0, 360)
    if y <= 0 or y >= height - 1:
        return random.randint(0, 360)
    left_pixel = pixels[x - 1, y]
    right_pixel = pixels[x + 1, y]
    up_pixel = pixels[x, y - 1]
    down_pixel = pixels[x, y + 1]
    horizontal_change = (
        abs(right_pixel[0] - left_pixel[0]) +
        abs(right_pixel[1] - left_pixel[1]) +
        abs(right_pixel[2] - left_pixel[2])
    )
    vertical_change = (
        abs(down_pixel[0] - up_pixel[0]) +
        abs(down_pixel[1] - up_pixel[1]) +
        abs(down_pixel[2] - up_pixel[2])
    )
    # If horizontal edges stronger:
    # use horizontal strokes
    if horizontal_change > vertical_change:
        return random.randint(-20, 20)
    # Otherwise vertical-ish strokes
    else:
        return random.randint(70, 110)

# ============================================================
# PAINTING PASSES
# ============================================================
# REAL paintings are layered.
#
# Large strokes first
# smaller strokes later.
#
# This creates depth.
layers = [
    # large strokes
    {
        "step": 12,
        "length": 14,
        "thickness": 8
    },
    # medium strokes
    {
        "step": 8,
        "length": 10,
        "thickness": 5
    },
    # small detail strokes
    {
        "step": 4,
        "length": 6,
        "thickness": 3
    }]

# ============================================================
# PAINT IMAGE
# ============================================================
for layer in layers:
    step = layer["step"]
    length = layer["length"]
    thickness = layer["thickness"]
    print("Painting layer:", layer)
    for y in range(0, height, step):
        for x in range(0, width, step):
            # Get pixel color
            pixel = pixels[x, y]
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]
            # Slight paint randomness
            red += random.randint(-10, 10)
            green += random.randint(-10, 10)
            blue += random.randint(-10, 10)
            red = max(0, min(255, red))
            green = max(0, min(255, green))
            blue = max(0, min(255, blue))
            # Get brush direction
            angle = get_direction(x, y)
            # Convert coordinates
            draw_x = convert_x(x)
            draw_y = convert_y(y)
            # Draw stroke
            brush_stroke(
                draw_x,
                draw_y,
                (red, green, blue),
                angle,
                length + random.randint(-2, 2),
                thickness
            )

# ============================================================
# UPDATE SCREEN
# ============================================================
turtle.update()
print("Finished painting!")
turtle.done()
