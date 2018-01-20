from pymouse import PyMouse
from pynput import mouse as PynputMouse
import _thread
import time

stupid_global = False

def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))

def ret_false(msg, data):
    global l, stupid_global
    if stupid_global:
        if msg == 514 or msg == 513:
            l.suppress_event()
    return False

def timer_please():
    global stupid_global
    while True:
        time_now = time.time()
        while (time.time() - time_now < 5):
            pass
        stupid_global = not stupid_global
        print(stupid_global)

l = PynputMouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll,
        win32_event_filter = ret_false)

l.start()
_thread.start_new_thread(timer_please,())
l.join()


