import cv2
import glob
import os
import time
from utils import make_folder
from tqdm import tqdm


try:
    os.system("cls")
except:
    os.system("clear")


# videos = glob.glob(os.path.join("Dataset", "*.mp4"))

videos = [os.path.join("Dataset", video) 
            for video in os.listdir("Dataset")
            if ".mp4" in video]

# print(videos)
# list comprehension
# list_one = [element for element in itirable condition]


for video in tqdm(videos):
    # get name of suit and make a folder
    name = video.split("\\")[-1][:-4]
    frame_folder = os.path.join("Dataset", name)
    make_folder(frame_folder)

    # initialize video object
    video = cv2.VideoCapture(video) 

    # get video details
    fps= video.get(cv2.CAP_PROP_FPS)
    num_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = num_frames/fps

    print("", end="\n")
    print(f"Video duration is {duration :.2f} seconds and is recorded at {fps :.2f} FPS.")

    # save everz nth frame
    save_every = 30
    
    # frame number
    i = 0
    while(video.isOpened()):
        ret, frame = video.read()
        if ret:
            # get frame shape
            w, h, c = frame.shape
            
            # Rotate and resize
            scale = 2
            if h < w:
                frame = cv2.rotate(frame,  cv2.ROTATE_90_CLOCKWISE)
                frame = cv2.resize(frame, (w//scale, h//scale), interpolation= cv2.INTER_LINEAR)
            elif h > w:
                frame = cv2.resize(frame, (h//scale, w//scale), interpolation= cv2.INTER_LINEAR)

            # save frane
            file_name =  os.path.join(frame_folder, f"{name}_{str(i)}.png")
            if i % save_every == 0:
                cv2.imwrite(file_name, frame)

            # update frame name variable
            i += 1

        elif not ret:
            break