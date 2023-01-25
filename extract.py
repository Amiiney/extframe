import os
import cv2
import pandas as pd

# Path to the folder containing the mp4 videos
VID_PATH = ""

# Empty folder to save the videos: MAIN_SAVE_PATH/VIDEOS/FRAMES
MAIN_SAVE_PATH = ""

# Get a list of all the videos (They should all be in the same folder)
vids = os.listdir(VID_PATH)


# Initiate an empty dataframe to save the videos, frames and paths
df = pd.DataFrame()
VERBOSE = False

# Empty lists to save the videos, frames, paths
frames = []
videos = []
image_path = []

# Loop over the videos
for vid in vids:

    # Capture the frames
    vidcap = cv2.VideoCapture(f"{VID_PATH}/{vid}")

    # Get the fps of the individual video
    # Get fps of the video
    fps = vidcap.get(cv2.CAP_PROP_FPS)

    success, image = vidcap.read()
    count = 0

    # Generate the video name for the folder
    vid_id = vid.replace(".mp4", "")
    save_path = f"{MAIN_SAVE_PATH}/{vid_id}"

    # Create the video folders
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    while success:

        # Save the frames based on the frame rate

        #### Add the condition for the extraction of 2 and 5 fps

        if (count % fps) == 0:
            cv2.imwrite(f"{save_path}/{count}.jpg", image)  # save frame as JPEG file
            success, image = vidcap.read()

            if VERBOSE:
                print(f"{count}: Read a new frame: ", success)

            frames.append(count)
            videos.append(vid.replace(".mp4", ""))
            image_path.append(f"{vid_id}/{count}.jpg")

        success, image = vidcap.read()
        count += 1

# Store all the saved images to csv
df["clip_name"] = videos
df["frames"] = frames
df["image_path"] = image_path
df.to_csv(f"{MAIN_SAVE_PATH}/dataset_fr.csv")
