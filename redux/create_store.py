class Store(object):
    def __init__(self, state, reducer):
        super(Store, self).__init__()
        self._state = state
        self._reducer = reducer
        self._listeners = []

    @property
    def state(self):
        return self._state

    def subscribe(self, listener):
        self._listeners.append(listener)

        is_unsubscribed = False

        def unsubscribe():
            if not is_unsubscribed:
                self._listeners.remove(listener)

        return unsubscribe

    def dispatch(self, action):
        self._state = self._reducer(action, self._state)
        for listener in self._listeners:
            listener()

    def replace_reducer(self, reducer):
        self._reducer = reducer


def create_store(reducer, initial_state=None):
    state = initial_state
    if state is None:
        state = reducer({})

    return Store(state, reducer)

