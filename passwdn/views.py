from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, PopUpDialog
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication


class LoginView(Frame):
    def __init__(self, screen, controller, model):
        super(LoginView, self).__init__(screen,
                                        # screen.height * 2 // 6,
                                        15,
                                        # screen.width * 2 // 7,
                                        50,
                                        hover_focus=True,
                                        can_scroll=False,
                                        title='Sign in')
        # Save off the model that accesses the contacts database.
        self._model = model
        self._controller = controller
        self.set_theme('bright')

        layout = Layout([1, 3, 1], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text('Login:', name='login'), 1)
        # layout.add_widget(Divider(height=3), 1)
        layout.add_widget(Text('Password', name='password', hide_char='*'), 1)
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button('OK', self._ok), 0)
        layout2.add_widget(Button('Quit', self._quit), 3)
        self.fix()

    def reset(self):
        super(LoginView, self).reset()
        # self.data = self._model.select_all()

    def _ok(self):
        self.save()
        usl = self._controller.login_in(self.data['login'], self.data['password'])
        if usl is True:
            raise NextScene('List')
        pass

    @staticmethod
    def _quit():
        raise StopApplication('User pressed quit')


class DetailView(Frame):
    def __init__(self, screen, controller, model):
        super(DetailView, self).__init__(screen,
                                         screen.height * 2 // 5,
                                         screen.width * 2 // 5,
                                         hover_focus=True,
                                         can_scroll=False,
                                         reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model
        self._controller = controller
        self.set_theme('bright')

        # Create the form for displaying the list of contacts.
        layout = Layout([1, 10, 1], fill_frame=True)
        self.add_layout(layout)
        # TODO сделать регулярки для валидации
        layout.add_widget(Text('Name:', 'name'), 1)
        layout.add_widget(Text('Address:', 'address'), 1)
        layout.add_widget(Text('Nick name:', 'nickname'), 1)
        layout.add_widget(Text('Email address:', 'email'), 1)
        layout.add_widget(Text('Phone number:', 'telnumber', validator='^[+]?[0-9]*$'), 1)
        layout.add_widget(Text('Secret question:', 'secretquest'), 1)
        layout.add_widget(Text('Password:', 'password'), 1)
        # layout.add_widget(Button('gen', self._gen_pass), 2)
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button('OK', self._ok), 0)
        layout2.add_widget(Button('Cancel', self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(DetailView, self).reset()
        self.data = self._controller.get_current()

    def _ok(self):
        self.save()
        self._controller.update_current(self.data)
        raise NextScene('List')

    @staticmethod
    def _cancel():
        raise NextScene('List')


class ListView(Frame):
    def __init__(self, screen, controller, model):
        super(ListView, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       on_load=self._reload_list,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title='Passwdn')
        # Save off the model that accesses the contacts database.
        self._model = model
        self._controller = controller
        self.set_theme('bright')
        self.palette['selected_focus_field'] = (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_GREEN)

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(Widget.FILL_FRAME,
                                  self._controller.get_list(),
                                  # model.get_summary(),
                                  name='store',
                                  add_scroll_bar=True,
                                  on_change=self._on_pick,
                                  on_select=self._edit)
        self._edit_button = Button('Edit', self._edit)
        self._delete_button = Button('Delete', self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button('Add', self._add), 0)
        layout2.add_widget(self._edit_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button('Quit', self._quit), 3)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        self._edit_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        # self._list_view.options = self._model.get_summary()
        self._list_view.options = self._controller.get_list()
        self._list_view.value = new_value

    def _add(self):
        self._model.current_id = None
        raise NextScene('Detail')

    def _edit(self):
        self.save()
        self._model.current_id = self.data['store']
        raise NextScene('Detail')

    def _delete(self):
        self.save()
        self._model.current_id = self.data['store']
        # self._model.delete(self.data['store'])
        self._controller.delete_current()
        self._reload_list()

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Are you sure?",
                        ["Yes", "No"],
                        has_shadow=True,
                        on_close=self._quit_on_yes))

    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")
