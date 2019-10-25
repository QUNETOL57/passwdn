from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
from models.models import LoginModel,StoreModel
from views.views import LoginView


def demo(screen, scene):
    scenes = [
        Scene([LoginView(screen, login)], -1, name='Login'),
        # Scene([ListView(screen, contacts)], -1, name="Main"),
        # Scene([ContactView(screen, contacts)], -1, name="Edit Contact")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


login = LoginModel()
# contacts = ContactModel()
last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene