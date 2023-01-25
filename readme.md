# Extract frames from videos

## 1- Create a conda environment

```
conda create -n extframes python=3.9
```

## 2- cd to the extract_frames repository
```
cd YOUR_PARENT_PATH/extract_frames
```


## 3- Install the requirements.txt file
```
pip install -r requirements.txt
```

## 4- Extract the segments
The command has 4 parameters:

`video_path` : path to the video

`save_path`: path to save the frames (a whole folder will be generated automatically)

`start`: List of initial second of each segment Ex: [0,23,43,60]

`end`: List of the last second of each segment Ex: [1,25,45,64]

`save_csv`: true/false saves a csv with the frame number and path


```
python main.py video_path= parent_path/video.mp4 save_path= parent_path start=[0,23,43,60] end=[1,25,45,64]

```