from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication


class ContactView(Frame):
    def __init__(self, screen, model):
        super(ContactView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Contact Details",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Name:", "name"))
        layout.add_widget(Text("Address:", "address"))
        layout.add_widget(Text("Phone number:", "phone"))
        layout.add_widget(Text("Email address:", "email"))
        layout.add_widget(
            TextBox(Widget.FILL_FRAME,
                    "Notes:",
                    "notes",
                    as_string=True,
                    line_wrap=True))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(ContactView, self).reset()
        self.data = self._model.get_current_contact()

    def _ok(self):
        self.save()
        self._model.update_current_contact(self.data)
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")


class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       on_load=self._reload_list,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="Contact List")
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(Widget.FILL_FRAME,
                                  model.get_summary(),
                                  name="contacts",
                                  add_scroll_bar=True,
                                  on_change=self._on_pick,
                                  on_select=self._edit)
        self._edit_button = Button("Edit", self._edit)
        self._delete_button = Button("Delete", self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", self._add), 0)
        layout2.add_widget(self._edit_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        self._edit_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit Contact")

    def _edit(self):
        self.save()
        self._model.current_id = self.data["contacts"]
        raise NextScene("Edit Contact")

    def _delete(self):
        self.save()
        self._model.delete_contact(self.data["contacts"])
        self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class LoginView(Frame):
    def __init__(self, screen, model):
        super(LoginView, self).__init__(screen,
                                        # screen.height * 2 // 6,
                                        15,
                                        # screen.width * 2 // 7,
                                        50,
                                        hover_focus=True,
                                        can_scroll=False,
                                        title="Sign in")
        # Save off the model that accesses the contacts database.
        self._model = model
        self.set_theme("bright")

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Login:", "login"))
        # layout.add_widget(Text("Password:", "password"))
        # layout.add_widget(Text("Password", name="password", on_change=self._on_change, hide_char="*"), 1)
        layout.add_widget(Text("Password", name="password", hide_char="*"))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(LoginView, self).reset()
        # self.data = self._model.get_current_contact()

    def _ok(self):
        # self.save()
        # self._model.update_current_contact(self.data)
        # raise NextScene("Main")
        pass

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")
