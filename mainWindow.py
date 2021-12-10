import PySimpleGUI as sg
import cv2
import matplotlib.pyplot as plt
from fer import FER

cat = 0

emotions = {
    "angry": 0.00,
    "disgust": 0.00,
    "fear": 0.00,
    "happy": 0.00,
    "sad": 0.00,
    "surprise": 0.00,
    "neutral": 0.00,
}


def medie_emotii(frame):
    cv2.imwrite('Frame' + '.jpg', frame)
    # image = Image.open('Frame.jpg')
    # image.show()

    img = plt.imread("Frame.jpg")
    detector = FER(mtcnn=True)
    dict = detector.detect_emotions(img)
    print(type(dict))
    for x in dict[0]['emotions']:
        print(x)
        print(dict[0]['emotions'][x])
        emotions[x] = emotions[x] + dict[0]['emotions'][x]
    print(detector.detect_emotions(img))
    plt.imshow(img)


def mainWindow(name):
    sg.theme('Black')

    layout = [[sg.Text("Hello " + name, size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('Record', size=(10, 1), font='Helvetica 14'),
               sg.Button('Stop', size=(10, 1), font='Helvetica 14'), ]]

    window = sg.Window('Emotion reader',
                       layout, location=(800, 400))

    cap = cv2.VideoCapture(0)
    recording = False
    takePicture = False
    x = 0

    while True:
        event, values = window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            return
        elif event == 'Record':
            recording = True
        elif event == 'Stop':
            emotiePredominanta = emotii();
            sg.Popup(emotiePredominanta, keep_on_top=True)
            return
        if recording:
            ret, frame = cap.read()

            if (x == 20):
                medie_emotii(frame)
                x = 0

            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            if (takePicture):
                takePicture = False
            x = x + 1

            window['image'].update(data=imgbytes)


def emotii():
    max1 = 0
    emotie1 = ''
    emotie2 = ''
    emotie3 = ''
    max2 = 0
    max3 = 0
    emotions['neutral'] = 0
    for x in emotions:
        if emotions[x] > max1:
            emotie1 = x
            max1 = emotions[x]
    emotions[emotie1]=0

    for x in emotions:
        if emotions[x] > max2:
            emotie2 = x
            max2 = emotions[x]
    emotions[emotie2]=0

    for x in emotions:
        if emotions[x] > max3:
            emotie3 = x
            max3 = emotions[x]
    strMax1 = str(max1)
    strMax2 = str(max2)
    strMax3 = str(max3)
    emotiiPrincipale = "The most dominant emotion presented by the child during the activity was: "+emotie1 + "(" + strMax1 + ")" + "\n" + \
                       "The second most dominant emotion presented by the child during the activity was: " +emotie2 + "(" + strMax2 + ")" + "\n" + \
                       "The third most dominant emotion presented by the child during the activity was: "+ emotie3 + "(" + strMax3 + ")"
    return emotiiPrincipale
