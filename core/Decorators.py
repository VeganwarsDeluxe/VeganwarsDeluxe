from typing import Callable

from core.Events.EventManager import event_manager
from core.Events.Events import AttachStateEvent, Event
from core.SessionManager import session_manager
from core.States import State
from core.Context import StateContext, EventContext


def ExperimentalRegisterState():
    def decorator_func(state: type[State]):
        def callback_wrapper(message):
            callback = state.register

            context = StateContext[state](message, session_manager.get_session(message.session_id))
            return callback(context)

        event_manager.at_event(event=AttachStateEvent, unique_type=state, callback_wrapper=callback_wrapper)

    return decorator_func


def RegisterState(state: type[State]):
    def decorator_func(callback: Callable):
        def callback_wrapper(message):
            context = StateContext[state](message, session_manager.get_session(message.session_id))
            return callback(context)

        event_manager.at_event(event=AttachStateEvent, unique_type=state, callback_wrapper=callback_wrapper)

    return decorator_func


def RegisterEvent(session_id: str = None, event: type[Event] = Event, unique_type=None, priority=0, filters=None):
    def decorator_func(callback: Callable):
        def callback_wrapper(message):
            context = EventContext[event](message, session_manager.get_session(message.session_id))
            return callback(context)

        event_manager.at_event(event=event, session_id=session_id, unique_type=unique_type,
                               priority=priority, filters=filters, callback_wrapper=callback_wrapper)

    return decorator_func


def At(session_id: str, turn: int, event: type[Event] = Event, priority: int = 0, filters=None):
    def decorator_func(callback: Callable):
        def callback_wrapper(message):
            context = EventContext[event](message, session_manager.get_session(message.session_id))
            return callback(context)

        event_manager.at(callback_wrapper, session_id, turn, event, priority=priority, filters=filters)

    return decorator_func


def Nearest(session_id: str, event: type[Event] = Event, priority=0, filters=None):
    def decorator_func(callback: Callable):
        def callback_wrapper(message):
            context = EventContext[event](message, session_manager.get_session(message.session_id))
            return callback(context)

        event_manager.nearest(callback_wrapper, session_id, event=event, priority=priority, filters=filters)

    return decorator_func


def Every(session_id: str, turns: int, start: int = 1, event: type[Event] = Event, filters=None):
    def decorator_func(callback: Callable):
        def callback_wrapper(message):
            context = EventContext[event](message, session_manager.get_session(message.session_id))
            return callback(context)

        event_manager.every(callback_wrapper, session_id, turns, start, event, filters)

    return decorator_func


def After(session_id: str, turns: int, event: type[Event] = Event, repeats: int = 1, filters=None):
    def decorator_func(callback: Callable):
        def callback_wrapper(message):
            context = EventContext[event](message, session_manager.get_session(message.session_id))
            return callback(context)

        event_manager.after(event=event, session_id=session_id, turns=turns, repeats=repeats,
                            filters=filters, callback_wrapper=callback_wrapper)

    return decorator_func
