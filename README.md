# Road-Lane detection for self driving cars

Detecting a road lanes is the first step towards self driving cars. It gives the correct direction to the car and avoid accident and errors.
We human can detect the lanes with our eyes but a machine requires a technique and algorithm to do so.

This project do the same i.e it tries to provide EYES to the machine/computer using python and opencv.

**Project steps:**
**1. importing important libraries**
```
import cv2
import numpy as np
import math
from moviepy.editor import VideoFileClip
```

**2. Reading video**
As we know video is nothing but just an sequence of images therefore we will work on images in a loop to handle all images in a video.
> **Reading image**
```
img = cv2.imread(IMAGE_NAME)
```
![Road](https://miro.medium.com/max/600/1*Vhsx_OoRVEeqgFcX56g6Pg.jpeg)

**3. Processing image**
> ** Converting colored image to gray image -> Applying gaussian blur -> Converting to canny -> Applying dilation**

![Filtered Image](https://miro.medium.com/max/600/1*YK2fRrL_vziybWRGLK0WcA.jpeg)

**4. Area of Interest - Triangle**

![Area of interest triangle](https://miro.medium.com/max/600/1*yp4X0FFNc-Ht7-Rwpy6bng.jpeg)

**5 Applying Hough Transform to detect line**

![Result](https://miro.medium.com/max/1250/1*RKs77nfqXQQ30WnvkAsHHw.png)
