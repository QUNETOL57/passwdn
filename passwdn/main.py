from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
from models import LoginModel, StoreModel
from controllers import MainAction
from views import ContactView,ListView,LoginView


class PasswdnMain(object):

    def __init__(self):
        self.l_model = LoginModel()
        self.m_action = MainAction()
        self.last_scene = None

    def screens(self, screen, scene):
        scenes = [
            Scene([LoginView(screen, self.m_action, self.l_model)], -1, name='Login'),
            # Scene([ListView(screen, contacts)], -1, name="Main"),
            # Scene([ContactView(screen, contacts)], -1, name="Edit Contact")
        ]

        screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

    def start_prog(self):
        while True:
            try:
                Screen.wrapper(self.screens, catch_interrupt=True, arguments=[self.last_scene])
                sys.exit(0)
            except ResizeScreenError as e:
                self.last_scene = e.scene


if __name__ == '__main__':
    PasswdnMain().start_prog()