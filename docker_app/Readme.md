# [Gesture Classification By OMG Data](https://www.kaggle.com/competitions/motorica-x-skillfactory-internship-test-task/data)
## [Skillfactory](https://skillfactory.ru) Data Science Diploma Project

<br>

Load docker container  
```
$ docker pull maplebloom/server_image
```

Start server  
```
$ docker run -it --rm --name=server_container -p=80:80 maplebloom/server_image
```
<br>

Use [gesture_classification_client.py](https://github.com/MapleBloom/GestureClassificationByOMG/blob/main/gesture_classification_client.py) from [Gesture Classification By OMG Data](https://github.com/MapleBloom/GestureClassificationByOMG) in order to request gesture prediction for [X_test.zip](https://github.com/MapleBloom/GestureClassificationByOMG/blob/main/data/X_test.zip) in [data](https://github.com/MapleBloom/GestureClassificationByOMG/tree/main/data).

It returns `.csv` with predicted gesture labels and plots prediction vs OMG sensors data. 

<center> <img src=https://github.com/MapleBloom/GestureClassificationByOMG/blob/main/figures/sample_test14.png align="center" width="800"/> </center>
<hr>
