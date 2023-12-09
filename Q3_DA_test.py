import pandas as pd
from PIL import Image, ImageDraw
import os

# Step 1: Load the detection file
detection_file = 'Q3_Draw_task_labels.tsv'
output_folder = 'Images_draw_output'
draw_task_images = 'Q3_Draw_task_images\Q3_Draw_task_images'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

df = pd.read_csv(detection_file, sep='\t')

# Step 2: Draw the objects for every image
for image_name, group in df.groupby('name'):
    image_path = os.path.join(draw_task_images, image_name)
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Draw rectangles for each detected object
    for _, row in group.iterrows():
        x_center = row['x_center']
        y_center = row['y_center']
        width = row['width']
        height = row['height']

        # Calculate bounding box coordinates
        left = x_center - width / 2
        top = y_center - height / 2
        right = x_center + width / 2
        bottom = y_center + height / 2

        # Draw the rectangle
        draw.rectangle([left, top, right, bottom], outline='red', width=2)

    # Step 3: Save the output
    output_path = os.path.join(output_folder, f'drawn_{image_name}')
    img.save(output_path)

print("Drawing completed. Images saved in 'Images_draw_output' folder.")
