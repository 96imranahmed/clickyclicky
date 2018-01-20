from pynput import mouse
from pynput.mouse import Button, Controller

import time

controller = Controller()

while True:
    x,y = controller.position
    if x > 1000:
        controller.position = (500,y)


# class Mouse:
#     def __init__(self):
#         self.last_position = None
#         self.mouse = mouse.Controller()
#         self.listener = mouse.Listener(on_move=self.on_move,on_click=self.on_click, on_scroll=self.on_scroll)

#     def on_move(self, x, y):
#         if self.last_position is None:
#             self.last_position = (x, y)
#         else:
#             if x > 1000:
#                 self.listener.stop() 
#                 self.mouse.position = (500, 500)
#                 self.last_position = (500,500)
#                 self.listener = mouse.Listener(on_move=self.on_move,on_click=self.on_click, on_scroll=self.on_scroll)
#                 self.listener.start()
#                 self.listener.join()

#     def on_click(self, x, y, button, pressed):
#         print("I clicked")

#     def on_scroll(self, x, y, dx, dy):
#         pass

#     def run(self):
#         self.last_position = self.mouse.position
#         try:
#             self.listener.start()
#             self.listener.join()
#         except Exception as e:
#             print("listener died: {}".format(e))
# if __name__ == '__main__':
#     p = Mouse()
#     p.run()