from pynput import keyboard
import pynput.keyboard._win32 as w32
import _thread
import time

LST = w32.Listener(None, None)
stupid_global = False

def on_press(key):
    try:
        pass
        # print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        pass
        # print('special key {0} pressed'.format(key))

def on_release(key):
    pass
    # print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def preprocess_keys(msg, data):
    global l, stupid_global, LST
    if stupid_global:
        is_packet = data.vkCode == LST._VK_PACKET
        if is_packet:
            tup = (msg | LST._UTF16_FLAG, data.scanCode)
        else:
            tup = (msg, data.vkCode)
        key_send = LST._event_to_key(tup[0], tup[1])
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
        win32_event_filter = preprocess_keys
        )

l.start()
_thread.start_new_thread(timer_please,())
l.join()


