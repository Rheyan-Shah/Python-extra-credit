from PIL import Image
import turtle
import random

# ============================================================
# SETTINGS
# ============================================================
IMAGE_PATH = (
    r"C:\Users\Rheyan Shah\Documents\Intro To Computer Science"
    r"\Python\SoundDesign\imagemanipulation\input.jpg")
MAX_SIZE = 700
CANVAS_COLOR = (240, 235, 220)

# ============================================================
# LOAD IMAGE
# ============================================================
def load_image(path, max_size):
    image = Image.open(path)
    image = image.convert("RGB")
    width = image.width
    height = image.height
    # Resize large images
    if width > max_size or height > max_size:
        scale = min(
            max_size / width,
            max_size / height
        )
        width = int(width * scale)
        height = int(height * scale)
        image = image.resize((width, height))
    return image

image = load_image(
    IMAGE_PATH,
    MAX_SIZE)
pixels = image.load()
width = image.width
height = image.height

# ============================================================
# TURTLE SETUP
# ============================================================
def setup_turtle_screen(width, height):
    screen = turtle.Screen()
    screen.colormode(255)
    screen.setup(width + 100, height + 100)
    screen.bgcolor(CANVAS_COLOR)
    turtle.tracer(0, 0)
    return screen

def create_brush():
    brush = turtle.Turtle()
    brush.speed(0)
    brush.hideturtle()
    brush.penup()
    return brush

screen = setup_turtle_screen(
    width,
    height)
brush = create_brush()

# ============================================================
# COORDINATE CONVERSION
# ============================================================
def convert_x(x):
    return x - (width / 2)

def convert_y(y):
    return (height / 2) - y

# ============================================================
# BRIGHTNESS
# ============================================================
def get_brightness(pixel):
    return (
        int(pixel[0]) +
        int(pixel[1]) +
        int(pixel[2])
    ) / 3

# ============================================================
# EDGE DIRECTION
# ============================================================
def get_direction(x, y):
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
    # Horizontal structure
    if horizontal_change > vertical_change:
        angle = random.randint(-20, 20)
    # Vertical structure
    else:
        angle = random.randint(70, 110)
    # Small natural variation
    angle += random.randint(-4, 4)
    return angle

# ============================================================
# COLOR VARIATION
# ============================================================
def clamp(value):
    return max(0, min(255, value))

def vary_color(color, variation):
    red = clamp(
        color[0] + random.randint(-variation, variation)
    )
    green = clamp(
        color[1] + random.randint(-variation, variation)
    )
    blue = clamp(
        color[2] + random.randint(-variation, variation)
    )
    return (red, green, blue)

# ============================================================
# DRAW SINGLE STROKE
# ============================================================
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
    # Slight pigment breakup
    stroke_color = (
        clamp(color[0] + random.randint(-5, 5)),
        clamp(color[1] + random.randint(-5, 5)),
        clamp(color[2] + random.randint(-5, 5))
    )
    brush.pencolor(stroke_color)
    brush.pensize(thickness)
    brush.pendown()
    # Slight curve
    for i in range(3):
        brush.forward(length / 3)
        brush.right(
            random.randint(-2, 2)
        )
    brush.penup()

# ============================================================
# DRAW PAINT PATCH
# ============================================================
def draw_paint_patch(
    x,
    y,
    color,
    angle,
    length,
    thickness):
    # Small grouped strokes
    for stroke in range(2):
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
# LAYERS
# ============================================================
layers = [
    # Underpainting
    {
        "step": 28,
        "length": 34,
        "thickness": 18,
        "color_variation": 3
    },
    # Large forms
    {
        "step": 20,
        "length": 24,
        "thickness": 12,
        "color_variation": 4
    },
    # Medium forms
    {
        "step": 14,
        "length": 18,
        "thickness": 8,
        "color_variation": 5
    },
    # Structure
    {
        "step": 10,
        "length": 12,
        "thickness": 6,
        "color_variation": 6
    },
    # Detail
    {
        "step": 7,
        "length": 8,
        "thickness": 4,
        "color_variation": 7
    },
    # Fine detail
    {
        "step": 5,
        "length": 5,
        "thickness": 3,
        "color_variation": 8
    },
    # Micro detail
    {
        "step": 3,
        "length": 3,
        "thickness": 2,
        "color_variation": 10
    }]

# ============================================================
# PAINT LAYER
# ============================================================
def paint_layer(layer):
    step = layer["step"]
    length = layer["length"]
    thickness = layer["thickness"]
    color_variation = layer["color_variation"]
    print()
    print("Painting layer:")
    print(layer)
    for y in range(0, height, step):
        # Offset avoids visible grids
        x_offset = random.randint(0, step)
        for x in range(x_offset, width, step):
            original_color = pixels[x, y]
            paint_color = vary_color(
                original_color,
                color_variation
            )
            angle = get_direction(x, y)
            draw_x = convert_x(x)
            draw_y = convert_y(y)
            draw_paint_patch(
                draw_x,
                draw_y,
                paint_color,
                angle,
                length,
                thickness
            )

# ============================================================
# MAIN PAINTING LOOP
# ============================================================
for layer in layers:
    paint_layer(layer)

# ============================================================
# FINISH
# ============================================================
turtle.update()
print()
print("Finished painting!")
turtle.done()
