import cv2
import numpy as np
import os
import pandas as pd


RUN_MULTITRI = True

# Load dataframe
df = pd.read_csv(
    "/Heichole/230323_HeiChole_Activity_Data/230323-043125_OHE_every8thframe.csv"
)
trimap = pd.read_csv(
    "/Heichole/230323_HeiChole_Activity_Data/230323-043125_map_triplets.csv"
)

# Create triplet column in the format [instrument, action, target]
trimap["triplet"] = (
    trimap["Instrument"] + "," + trimap["Action"] + "," + trimap["Target"]
)

# Create the path column
df["path"] = df.Video + "/" + df.Frame


## Create a column to save the multiple triplet indexes
##
##   YOU ONLY NEED TO RUN THIS ONCE AND SAVE THE DATAFRAME
## This takes some time to process, it's ideal to use the jupyter notebook instead

if RUN_MULTITRI:
    ##Find the combination of triplets in each row
    all_tri = []
    df["multi_tri"] = -1
    df["invivo"] = -1
    for i in range(len(df)):
        triplets = []
        row = df.iloc[:, :90].loc[i]
        for j, k in enumerate(range(2, 90)):
            if row[k] == 1:
                triplets.append(j)
                print(triplets)
        np_arr = np.array(triplets)
        all_tri.append(triplets)

        if "exvivo" in df.at[i, "Video"]:
            df.at[i, "invivo"] = 0
        else:
            df.at[i, "invivo"] = 1

    ##Save the triplet combination in a new column
    df["multi_tri"] = all_tri

    df.to_csv("df.csv")


# Create a dictionarry to map the triplets
# initializing lists
tri_keys = trimap.id.tolist()
tri_text = trimap.triplet.tolist()

# using naive method
# to convert lists to dictionary
tridic = {}
for key in tri_keys:
    for value in tri_text:
        tridic[key] = value
        tri_text.remove(value)
        break


folder = "/Heichole/frames/"
output_path = "/Heichole/plot_frames/"

video = "HeiChole17_25FPS"
vid_df = df[df["Video"] == video].reset_index(drop=True)

if not os.path.exists(output_path + video):
    os.mkdir(output_path + video)

for i in range(len(vid_df)):

    path = vid_df.loc[i, "path"]
    frame = vid_df.loc[i, "Frame"]
    TRAIN_PATH = folder + path
    tris = vid_df.loc[i, "multi_tri"]

    targets = []
    print(tris)
    for t in range(len(tris)):
        tar = tridic[tris[t]]
        targets.append(tar)

    print(TRAIN_PATH, targets)
    img = cv2.imread(TRAIN_PATH)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.putText(
        img,
        f"{frame}",
        (50, 50 - 2),
        0,
        4.5 / 3,
        [255, 0, 0],
        thickness=3,
        lineType=cv2.LINE_AA,
    )

    for idx, onto in enumerate(targets):
        cv2.putText(
            img,
            f"{onto}",
            (80, 450 - 2 + idx * 50),
            0,
            4.5 / 5,
            [178, 235, 242],
            thickness=2,
            lineType=cv2.LINE_AA,
        )

    cv2.imwrite(f"{output_path}{video}/{i}.jpg", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # plt.imshow(img)
    # plt.show()
