from typing import Callable

from core.Events.EventManager import event_manager
from core.Events.Events import AttachStateEvent, Event
from core.SessionManager import session_manager
from core.States import State
from core.Context import Context


def RegisterState(state: type[State]):
    def decorator_func(callback: Callable):
        def callback_wrapper(message):
            context = Context[state](message, session_manager.get_session(message.session_id))
            return callback(context)

        return event_manager.at_event(event=AttachStateEvent, unique_type=state, callback_wrapper=callback_wrapper)

    return decorator_func


def RegisterEvent(session_id: str = None, event: type[Event] = Event, unique_type=None, priority=0, filters=None):
    def decorator_func(callback: Callable):
        def callback_wrapper(message):
            context = Context[event](message, session_manager.get_session(message.session_id))
            return callback(context)

        return event_manager.at_event(event=event, session_id=session_id, unique_type=unique_type,
                                      priority=priority, filters=filters, callback_wrapper=callback_wrapper)

    return decorator_func
