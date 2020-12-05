import pickle
from pynput.keyboard import Listener, Key, KeyCode
import PIL
from PIL import ImageGrab
from PIL import Image
import socket
import cv2
import numpy
import windowHandler

store = set()

HOT_KEYS = {
    'runBreakingCaptcha': set([Key.alt_l, KeyCode(char='1')])
}


# socket recive buffer
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def runBreakingCaptcha():
    captureScreenShot()
    info = sendImageAndGetInfo()
    w_handler = windowHandler.windowHandler()
    w_handler.click(w_handler.checkCell(w_handler.findObjectsXY(info)))



def captureScreenShot():
    img = ImageGrab.grab()
    saveas = "screenshot.png"
    img.save(saveas)


def imageToBytes():
    pil_image = PIL.Image.open('screenshot.png').convert('RGB')
    frame = numpy.array(pil_image)
    frame = frame[:, :, ::-1].copy()

    encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), 0]
    result, imgencode = cv2.imencode('.png', frame, encode_param)
    data = numpy.array(imgencode)
    return data.tobytes()


def getTitleInfo():
    import pyautogui as pg
    from os import listdir
    from os.path import isfile, join

    titleCategories = {'tauto': 0, 'tbus': 1, 'tcar': 2, 'tcw': 3, 'tgdd': 4, 'tlight': 5, 'tshj': 6, 'tstair': 7}

    path = '.\\Titles\\'
    for f in listdir(path):
        if isfile(join(path, f)):
            titleImageBox = pg.locateOnScreen(join(path, f), confidence=0.7)
            if titleImageBox is not None:
                leftBottomOffset = (titleImageBox[0], titleImageBox[1] + titleImageBox[3])

                for name, category in titleCategories.items():
                    if f.__contains__(name):
                        print('return title:', name, category, 'offset', leftBottomOffset)
                        return category, leftBottomOffset

    raise Exception('could not find title category')


def sendImageAndGetInfo():
    category, leftBottomOffset = getTitleInfo()
    data = imageToBytes()

    TCP_IP = '15.164.211.141'
    TCP_PORT = 1234

    s = socket.socket()
    s.connect((TCP_IP, TCP_PORT))

    s.send(str(len(data)).ljust(16).encode('utf-8'))
    s.send(data)

    length = recvall(s, 16)
    r = recvall(s, int(length))

    r_variable = pickle.loads(r)

    s.close()

    print(r_variable)
    # Access the information by doing data_variable.process_id or data_variable.task_id etc..,
    print('Data received from client')
    return r_variable


def handleKeyPress(key):
    store.add(key)

    for action, trigger in HOT_KEYS.items():
        CHECK = all([True if triggerKey in store else False for triggerKey in trigger])

        if CHECK:
            try:
                action = eval(action)
                if callable(action):
                    action()
            except NameError as err:
                print(err)


def handleKeyRelease(key):
    if key in store:
        store.remove(key)

    # exit
    if key == Key.esc:
        return False


with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
    listener.join()
