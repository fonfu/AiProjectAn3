import PySimpleGUI as sg
import cv2
import mainWindow
import face_recognition
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import sys


class Notepad(qtw.QWidget):

    def __init__(self):
        super(Notepad, self).__init__()
        self.text = qtw.QTextEdit(self, placeholderText="Enter your name here")
        self.clr_btn = qtw.QPushButton('Save')
        self.name = ""

        self.init_ui()

    def init_ui(self):
        layout = qtw.QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.clr_btn)
        self.clr_btn.clicked.connect(self.clear_text)

        self.setLayout(layout)
        self.setWindowTitle('PyQt5 TextEdit')

        self.show()

    def clear_text(self):
        self.name = self.text.toPlainText()
        self.text.clear()
        self.close()


def verifyFacialRecogn(frame):
    cv2.imwrite('Frame2' + '.jpg', frame)
    picture_of_me = face_recognition.load_image_file("Frame2.jpg")
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

    f = open("people.txt", "r")
    for x in f:
        x = x[:-1]
        print(x)
        picture = face_recognition.load_image_file(x)
        encoding = face_recognition.face_encodings(picture)[0]
        results = face_recognition.compare_faces([my_face_encoding], encoding)
        if results[0] == True:
            x = x[:-1]
            x = x[:-1]
            x = x[:-1]
            x = x[:-1]
            return x;
    return 0
    """encodingM = face_recognition.face_encodings(pictureM)[0]"""

    """pictureI = face_recognition.load_image_file("iustin1.png")
    encodingI = face_recognition.face_encodings(pictureI)[0]

    resultsM = face_recognition.compare_faces([my_face_encoding], encodingM)
    resultsI = face_recognition.compare_faces([my_face_encoding], encodingI)

    if resultsM[0] == True:
        return "Mihai"
    elif resultsI[0] == True:
        return "Iustin"
    else:
        return 0"""


def registerEncoding(frame):
    app = qtw.QApplication(sys.argv)
    writer = Notepad()
    app.exec_()
    print(writer.name)
    cv2.imwrite(writer.name + '.jpg', frame)
    f = open("people.txt", "a")
    f.write(writer.name + ".jpg" + "\n")
    """picture_of_me = face_recognition.load_image_file("Frame2.jpg")
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

    print(my_face_encoding)"""


def main():
    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('InsideOut', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('Record', size=(10, 1), font='Helvetica 14'),
               sg.Button('Login', size=(10, 1), font='Helvetica 14'),
               sg.Button('Register', size=(10, 1), font='Helvetica 14')]]

    # create the window and show it without the plot
    window = sg.Window('Emotion reader',
                       layout, location=(800, 400))

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    recording = False
    takePicture = False
    register = False
    while True:
        event, values = window.read(timeout=20)
        if event == 'Login':
            takePicture = True
        if event == sg.WIN_CLOSED:
            return
        elif event == 'Record':
            recording = True

        if event == 'Register':
            register = True

        if recording:
            ret, frame = cap.read()
            img = cv2.imencode('.png', frame)[1]
            imgbytes = img.tobytes()  # ditto
            if (register):
                registerEncoding(frame)
                register = False
            if (takePicture):
                takePicture = False
                ret = verifyFacialRecogn(frame)
                if ret == 0:
                    sg.PopupOK('User necunoscut', keep_on_top=True)
                else:
                    sg.PopupOK(ret + ' ai fost logat, Welcome', keep_on_top=True)
                    window.close()
                    return ret

            window['image'].update(data=imgbytes)


name = main()
if (name != 0):
    mainWindow.mainWindow(name)
