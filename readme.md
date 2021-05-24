# Facial Recognition Attendance System
## About
This repository contains the thesis of [Samuel Matthew](https://instagram.com/samuelmtthw) © 2021

Thesis Title:
**Attendance Machine Development based on Facial Recognition Method using Raspberry Pi Embedded System**

## Requirements
This repository requires you to:
- Install Python, OpenCV, and several modules
- Configure MySQL in Raspberry Pi
- Use Raspberry Pi 4B (with Raspberry Pi Camera Module) and an MLX90614 for the temperature sensor

Resources & Installation Guide:
- [Raspberry Pi OS](https://www.raspberrypi.org/software/)
- [OpenCV in Raspberry Pi](https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/)
- [OpenCV in macOS](https://www.pyimagesearch.com/2018/08/17/install-opencv-4-on-macos/)
- [MLX90614 Module](https://www.youtube.com/watch?v=CftxT8k0jww)
- [MySQL Connector (Raspberry Pi & macOS)](https://www.youtube.com/watch?v=3vsC05rxZ8c)
- [Other Libraries & Basic Concepts](https://www.pyimagesearch.com/2018/06/25/raspberry-pi-face-recognition/)

## Contents

1. Dataset Folders
2. Face Encoder 
3. Face Encodings
4. Attendance System for macOS 
5. Attendance System for Raspberry Pi
6. Misc Tutorial Applications

## Dataset Folders
There are 8 folders that contains face images of 20 peoples. 

The 8 folders contain different amount of images per person.
| Folder Name | Contents |
| ------ | ------ |
| dataset-5 | Contains 5 images per person, 100 images total |
| dataset-10 | Contains 10 images per person, 200 images total |
| dataset-15 | Contains 15 images per person, 300 images total |
| dataset-20 | Contains 20 images per person, 400 images total |
| dataset-25 | Contains 25 images per person, 500 images total |
| dataset-30 | Contains 30 images per person, 600 images total |
| test | Used to test the model / encodings |
| dataset-full | Complete version of the dataset|

The faces that are inside this dataset:
1. Ian Malcolm (Jeff Goldblum)
2. Ellie Sattler (Laura Dern )
3. Samuel Matthew
4. Claire Dearing (Bryce Dallas Howard)
5. Alan Grant (Sam Neill)
6. Owen Grady (Chris Pratt)
7. John Hammond (Richard Attenborough)
8. Jackie Chan
9. Hillary Clinton
10. Joko Widodo
11. Jacob Pernell
12. Michelle Obama
13. Agnez Mo
14. Gal Gadot
15. Whoopi Goldberg
16. Jennie (BLACKPINK)
17. Zoe Saldana
18. Lisa (BLACKPINK)
19. Sylvester Stallone
20. Kobe Bryant

## Face Encoder
This program takes in the dataset and outputs face encodings inside a ".pickle" format

You can use this program and create / update new face encodings using this format:
```sh
python3 encode_faces.py -i [your dataset folder] -e [your face encodings]
```


Example:
```sh
python3 encode_faces.py -i dataset-20 -e encodings-20.pickle
```

## Face Encodings
These files are created from the dataset folders using the face encoder program. 
Each files is named based on the dataset used for creating it. 

| File Name | Dataset Used |
| ------ | ------ |
| encodings-5.pickle | dataset-5|
| encodings-10.pickle | dataset-5|
| encodings-15.pickle | dataset-5|
| encodings-20.pickle | dataset-5|
| encodings-25.pickle | dataset-5|
| encodings-30.pickle | dataset-5|
| encodings.pickle | dataset-full|

Larger dataset = More accuracy = Higher load = Lower graphic performance

## Attendance System for macOS

## Attendance System for Raspberry Pi

## Misc Tutorial Applications

