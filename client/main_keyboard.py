from pynput import keyboard
import _thread
import time

stupid_global = False


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def ret_false(msg, data):
    global l, stupid_global
    if stupid_global:
        l.suppress_event()
    return True

def timer_please():
    global stupid_global
    while True:
        time_now = time.time()
        while (time.time() - time_now < 5):
            pass
        stupid_global = not stupid_global
        print(stupid_global)

l = keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        win32_event_filter = ret_false
        )

l.start()
_thread.start_new_thread(timer_please,())
l.join()


