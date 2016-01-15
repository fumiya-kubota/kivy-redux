
ADD_TODO = 'ADD_TODO'
COMPLETE_TODO = 'COMPLETE_TODO'


def add_todo(text):
    return {
        'type': ADD_TODO,
        'text': text
    }


def complete_todo(index):
    return {
        'type': COMPLETE_TODO,
        'index': index
    }


def todo_app(action, state=None):
    if state is None:
        state = {
            'todos': []
        }

    type_ = action.get('type')
    if type_ == ADD_TODO:
        state['todos'].append(action['text'])
    elif type_ == COMPLETE_TODO:
        state['todos'].pop(action['index'])

    return state
