import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import time

# Specify canvas parameters in application

def make_frame():
    cap = cv2.VideoCapture("data/2.mp4")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        image = Image.fromarray(frame)
        break
    cap.release()
    return image

#task = Thread(target=make_video)
#task.start()


# Define o tamanho do canvas de desenho
canvas_width = 704

scale_w = 0
scale_h = 0
# Cria um canvas de desenho
bg_image = make_frame()
W, H = bg_image.size
canvas = st_canvas(
    width=canvas_width,
    stroke_width=3,
    stroke_color="black",
    fill_color="rgba(220, 30, 150, 0.15)",
    drawing_mode="rect",
    background_image=bg_image,
    key="canvas",
    )

if canvas:
    try:
        canva_size = canvas.image_data.shape[:2]
        scale_w = W/canva_size[1]
        scale_h = H/canva_size[0]
    except Exception as e:
        print(e)
video = st.empty()
cap = cv2.VideoCapture("data/2.mp4")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if canvas.json_data is not None:
        data = canvas.json_data["objects"]
        for obj in data:
            if obj["type"] == "rect":
                x1, y1 = obj["left"], obj["top"]
                x1 = int(x1*scale_w)
                y1 = int(y1*scale_h)
                x2, y2 = obj["left"] + obj["width"], obj["top"] + obj["height"]
                x2= int(x2*scale_w)
                y2= int(y2*scale_h)
                frame[y1:y1+2, x1:x2] = [255, 0, 0]
                frame[y2:y2+2, x1:x2] = [255, 0, 0]
                frame[y1:y2, x1:x1+2] = [255, 0, 0]
                frame[y1:y2, x2:x2+2] = [255, 0, 0]
    image = Image.fromarray(frame)
    video.image(image)
    #time.sleep(1/30)
cap.release()
# Libera os recursos