import pickle

from pynput.keyboard import Listener, Key, KeyCode
import win32api
import PIL
from PIL import ImageGrab
from PIL import Image
import socket
import cv2
import numpy

store = set()

HOT_KEYS = {
    'runBreakingCaptcha': set([Key.alt_l, KeyCode(char='1')])
}


def runBreakingCaptcha():
    captureScreenShot()
    sendScreenShot()
    mask = getInferenceResult()


def captureScreenShot():
    img = ImageGrab.grab()
    saveas = "screenshot.png"
    img.save(saveas)


def sendScreenShot():
    pil_image = PIL.Image.open('screenshot.png').convert('RGB')
    frame = numpy.array(pil_image)
    frame = frame[:, :, ::-1].copy()

    encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), 0]
    result, imgencode = cv2.imencode('.png', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tobytes()
    """
    # Image Test Code
    decimg = cv2.imdecode(data, 1)
    cv2.imshow('CLIENT', decimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
    TCP_IP = '15.164.211.141'
    TCP_PORT = 9999
    sock = socket.socket()
    sock.connect((TCP_IP, TCP_PORT))
    sock.send(str(len(stringData)).ljust(16).encode('utf-8'))
    sock.send(stringData)
    sock.close()


def getInferenceResult():
    HOST = '127.0.0.1'
    PORT = 9999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen(True)
    print('9999port waiting')

    conn, addr = s.accept()
    print('Connected by', addr)

    data = conn.recv(4096)
    data_variable = pickle.loads(data)
    conn.close()
    print(data_variable)
    # Access the information by doing data_variable.process_id or data_variable.task_id etc..,
    print('Data received from client')
    return data_variable


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
