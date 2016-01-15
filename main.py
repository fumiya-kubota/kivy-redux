from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from todo.todo_app import todo_app, add_todo, complete_todo
from redux.create_store import create_store


Builder.load_string('''
<TodoButton>:
    width: 400
    size_hint: None, 0.1

<TodoWidget>
    text_field: text_field
    add_button: add_button
    todo_layout: todo_layout
    id: todos

    canvas.before:
        Color:
            rgb: 1, 1, 0.552
        Rectangle:
            pos: self.pos
            size: self.size

    TodoLayout:
        id: todo_layout
        todos: root.todos
        anchor_y: 'top'
        anchor_x: 'center'
        center_x: self.parent.center_x
        width: 400

        orientation: 'lr-tb'
        height: root.height - 60
        y: root.top - self.height - 15
        canvas.before:
            Color:
                rgb: 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size

    Widget:
        center_x: self.parent.center_x
        height: 30
        width: 400
        anchor_y: 'center'

        TextInput:
            id: text_field
            x: self.parent.x
            width: 350
            height: self.parent.height

        Button:
            id: add_button
            right: self.parent.right
            width: 50
            height: self.parent.height
            text: 'Add'
            on_press: root.add_todo(root.text_field.text)
''')


class TodoButton(Button):
    number = 0


class TodoLayout(StackLayout):
    __events__ = ('on_complete', )

    todos = ListProperty([])

    complete_callback = None

    def on_todos(self, instance, value):
        self.clear_widgets()
        for idx, text in enumerate(value):
            button = TodoButton(text=text)
            button.number = idx

            def on_press(btn):
                self.dispatch('on_complete', btn.number)
            button.bind(on_press=on_press)

            self.add_widget(button)

    def on_complete(self, *args):
        pass


class TodoWidget(Widget):
    add_button = ObjectProperty(None)
    text_field = ObjectProperty(None)
    todos = ListProperty([])
    todo_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TodoWidget, self).__init__(**kwargs)
        self.state = create_store(todo_app)
        # 状態の更新を見張る。
        self.state.subscribe(self.update_todo)
        self.todo_layout.bind(on_complete=self.on_complete)

    def update_todo(self):
        self.todos = self.state.state['todos']

    def add_todo(self, text):
        self.state.dispatch(add_todo(text))
        self.text_field.text = ''

    def on_complete(self, instance, value):
        self.state.dispatch(complete_todo(value))


class MyApp(App):
    def build(self):
        return TodoWidget()


if __name__ == '__main__':
    MyApp().run()
