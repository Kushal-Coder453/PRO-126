import cv2 
import numpy as np
import pandas as pd 
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from PIL import Image
import PIL.ImageOps
import os, ssl, time
if(not os.environ.get('PYTHONHTTPSVERIFY', '')and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context=ssl._create_unverified_context
X, y=fetch_openml('mnist_784', version=1, return_X_y=True)
print(pd.Series(y).value_counts())
classes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 
nclasses=len(classes)
xtrain, xtest, ytrain, ytest=train_test_split(X, y, random_state=9, train_size=7500, test_size=2500)
xtrainScaled=xtrain/255.0
xtestScaled=xtest/255.0
classifire=LogisticRegression(solver='saga', multi_class='multinomial').fit(xtrainScaled, ytrain)
ypredict=classifire.predict(xtestScaled)
accuracy=accuracy_score(ytest, ypredict)
print(accuracy)
cap=cv2.VideoCapture(0)
while(True):
    try:
        ret, frame=cap.read()
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width=gray.shape
        upperLeft=(int(width/2-56), int(height/2-56))
        bottomright=(int(width/2+56), int(height/2+56))
        cv2.rectangle(gray, upperLeft, bottomright, (0, 255, 0), 2)
        roi=gray[upperLeft[1]:bottomright[1], upperLeft[0]:bottomright[0]]
        impil=Image.fromarray(roi)
        ImageBw=impil.convert('L')
        ImageResized=ImageBw.resize((28, 28), Image.ANTIALIAS)
        ImageInverted=PIL.ImageOps.invert(ImageResized)
        pixelFilter=20
        minPixel=np.percentile(ImageInverted, pixelFilter)
        ImageImvertedScaled=np.clip(ImageInverted-minPixel, 0, 255)
        maxPixel=np.max(ImageInverted)
        ImageInvertedScaled=np.asarray(ImageInvertedScaled)/maxPixel
        testSample=np.array(ImageInvertedScaled).reshaped(1, 784)
        testPredict=classifire.predict(testSample)
        print("predictedNumber", testPredict)
        cv2.imshow('frame', gray)
        if cv2.waitKey(1)& 0xFF==ord('q'):
            break
    except Exception as e:
        pass
cap.release()
cv2.destroyAllWindows()