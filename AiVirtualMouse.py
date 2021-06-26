import cv2 
import numpy as np
import HandTrackingModule as hD
import autopy 
import time

wCam = 640
hCam = 480
frameR = 100
smoothening = 7


pTime = 0

plocX = 0
plocY = 0
clocX = 0
clocY = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = hD.handDetector(maxHands = 1)
wScr, hScr = autopy.screen.size()

while(True):
    # Find
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bBox = detector.findPosition(img)

    # Get tip of index and Middle Finger
    if(len(lmList) != 0):
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
    
        # Check which fingers are up
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # Check for Only Index Finger : Movement
        if(fingers[1] == 1 and fingers[2] == 0):
            # Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # Smoothening out the Values
            clocX = plocX + (x3 - plocX)/smoothening
            clocY = plocY + (y3 - plocY)/smoothening

            # Move the pointer
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # Check for both Index and Middle Finger : Click Action
        if(fingers[1] == 1 and fingers[2] == 1):
            # Distance between the two fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)

            # Action Click when distance is short
            if(length < 40):
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
    
# Frame Rate
cTime = time.time()
fps = 1/(cTime - pTime)
pTime = cTime
cv2.putText(img, str(int(fps)), (28, 58), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)

# Display
cv2.imshow("Image", img)
cv2.waitKey(1)