from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
from models import LoginModel, StoreModel
from controllers import MainAction
from views import LoginView, DetailView, ListView


class PasswdnMain(object):

    def __init__(self):
        self.login_model = LoginModel()
        self.store_model = StoreModel()
        self.main_action = MainAction(self.login_model, self.store_model)
        self.last_scene = None

    def screens(self, screen, scene):
        scenes = [
            Scene([LoginView(screen, self.main_action, self.login_model)], -1, name='Login'),
            Scene([ListView(screen, self.main_action, self.store_model)], -1, name="List"),
            Scene([DetailView(screen, self.main_action, self.store_model)], -1, name="Detail")

        ]

        screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

    def start_prog(self):
        while True:
            try:
                Screen.wrapper(self.screens, catch_interrupt=True, arguments=[self.last_scene], )
                sys.exit(0)
            except ResizeScreenError as e:
                self.last_scene = e.scene


if __name__ == '__main__':
    PasswdnMain().start_prog()