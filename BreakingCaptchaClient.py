import pickle
from pynput.keyboard import Listener, Key, KeyCode
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


def sendImageAndGetInfo():
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
