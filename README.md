# [Gesture Classification By OMG Data](https://www.kaggle.com/competitions/motorica-x-skillfactory-internship-test-task/data)
## [Skillfactory](https://skillfactory.ru) Data Science Diploma Project

sklearn LogisticRegression, Optuna  
matplotlib.pyplot, pickle, zipfile.ZipFile

:arrow_down: [Problem](README.md#problem)  
:arrow_down: [Hypothesis](README.md#hypothesis)  
:arrow_down: [Results](README.md#results)
<hr>
<br>

Follow [classification_research.ipynb](classification_research.ipynb) to deep into the project.  
Or just start [gesture_classification.py](gesture_classification.py) to visualise the prediction of the model.
<br>

### Data  

A pilot is a person from whom the data is collected.

The pilot receives visual commands to perform gestures and performs gestures *with some natural delay*. The commands given are recorded in a file.

A cuff with sensors is attached to the pilot's wrist. Sensors detect movements of the muscles and ligaments of the pilot's arm. Sensors data at every time tick are recorded in a file also.

While collecting this dataset the pilot accepted commands to perform the following gestures:

    0  "open",
    1  "little",
    2  "ring",
    3  "middle",
    4  "gun",
    5  "index",
    6  "thumb",
    7  "ОК",
    8  "grab".

"Open" - to open palm, others - to bend corresponding fingers.
<br>

### Problem  

In some words:  
to train the model we have the sensors data as features and the commands as the prototype of the target

<center> <img src=figures/sample_121.png width="500"/> </center>
<br>

but we want to build a model that predicts labels of gestures

<center> <img src=figures/sample_test14.png width="500"/> </center>
<hr>

Figures above exhibit the main difficulty of our problem. We have no real "target" to train the model. Y-data contains protocol of data production that works at the following schema.

OMG-sensors are fixed at a pilot wrist. The pilot gets a visual command to perform a gesture at the moment when command label changes in the protocol.

OMG-sensors change later at the process of the gesture performing by the pilot.

So, we have a transit zone consisting of two time intervals:
- the pilot sees the command and prepare to perform the gesture (here the command and the gesture labels do not coinsides because the command label has already changed but the pilot still hasn't started the gesture performing);
- the pilot is performing the gesture (at some moment of this interval the gesture label changes from the old to the actual and we hope it again coinsides with the command label).

Thus, the problem divides in two:
1. to construct a target label that coincides with gesture at every time moment, that is we have to find the very moment of the gesture change;
2. to train a model to predict gesture labels relying on the target from the step 1.

Out of the boundary of this notebook it was shown that the moment of the gesture change couldn't be revealed at narrow time window (5 time ticks) with such mathematical models as derivative analisys, crosspoint of different moving averages and so on without "looking into the future".
<br>

### Hypothesis

We can train an additional model at the "clear" gestures - at the part of the data out of transit zone. This model would be able to predict gradual shift of probabilities from class corresponding the gesture before movement to class after movement. So we would get prediction  of the gesture change moment.
<br>

### Results

The model predicting gesture labels was build. 

It was trained at predictions of the additional model trained at the part of the training dataset where target (gesture labels) coinsided with commands.

The model is able to predict the current gesture by 5-timestamps window of OMG sensors with very high quality even in transit zones. 
It is sophisticated enough to distinguish the cases like plotted below where some changes registered by sensors does not correspond the gesture change. 

<center> <img src=figures/sample_test1.png width="500"/> </center>

The palm stays open despite some minor movements of the muscles and ligaments of the pilot's arm and our model understands it.

Restrictions.  
The train and test datasets were collected at the same consecutive process. We have no data to check the quality of the model predictions at test data collected from the same pilot but after the cuff with sensors is dismounted and mounted the next time.


<br>

:arrow_up: [to begin](README.md#skillfactory-data-science-project)

<br><br>
Star ⭐️⭐️⭐️⭐️️⭐️ my project if you like it or think it is useful
