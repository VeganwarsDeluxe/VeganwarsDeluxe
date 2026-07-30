from __future__ import annotations

from typing import TYPE_CHECKING, Any

from VegansDeluxe.core.Translator.LocalizedString import LocalizedString

if TYPE_CHECKING:
    from VegansDeluxe.core.Session import Session


class LogEntry:
    """A structured message produced during a session.

    ``text`` is deliberately kept as a template instead of being rendered when
    the entry is created. This leaves room for a source entity's custom text to
    replace it before the log is delivered.
    """

    def __init__(
        self,
        message_id: str | None,
        text: str | LocalizedString,
        args: tuple[Any, ...] = (),
        kwargs: dict[str, Any] | None = None,
        source_id: str | None = None,
        target_id: str | None = None,
        custom_text_role: str = "source",
        suffix: str = "\n",
    ):
        self.message_id = message_id
        self.text = text
        self.args = tuple(args)
        self.kwargs = dict(kwargs or {})
        self.source_id = source_id
        self.target_id = target_id
        self.custom_text_role = custom_text_role
        self.suffix = suffix

    @staticmethod
    def _localized_custom_text(value, code: str) -> str | None:
        if isinstance(value, str):
            return value
        if not isinstance(value, dict):
            return None
        if code and isinstance(value.get(code), str):
            return value[code]
        for fallback in ("en", "default"):
            if isinstance(value.get(fallback), str):
                return value[fallback]
        return next((text for text in value.values() if isinstance(text, str)), None)

    def _custom_text(self, session: Session, code: str = "") -> str | None:
        if not self.message_id:
            return None

        owner_id = self.source_id if self.custom_text_role == "source" else self.target_id
        if not owner_id:
            return None

        owner = session.get_entity(owner_id)
        if owner is None:
            return None

        custom_texts = owner.custom_texts
        role_texts = custom_texts.get(self.custom_text_role)
        if isinstance(role_texts, dict) and self.message_id in role_texts:
            return self._localized_custom_text(role_texts[self.message_id], code)

        custom_text = custom_texts.get(self.message_id)
        if isinstance(custom_text, dict) and self.custom_text_role in custom_text:
            custom_text = custom_text[self.custom_text_role]
        return self._localized_custom_text(custom_text, code)

    def render(self, session: Session, code: str = "") -> str:
        """Render this entry, applying the source entity's custom text first."""
        custom_text = self._custom_text(session, code)
        if custom_text is not None:
            if isinstance(self.text, LocalizedString):
                rendered = self.text.apply_format_queue(custom_text, code)
                if self.args or self.kwargs:
                    rendered = rendered.format(*self.args, **self.kwargs)
            else:
                rendered = custom_text.format(*self.args, **self.kwargs) \
                    if self.args or self.kwargs else custom_text
            return rendered + self.suffix

        text = self.text

        if isinstance(text, LocalizedString):
            if self.args or self.kwargs:
                text = text.format(*self.args, **self.kwargs)
            rendered = text.localize(code)
        else:
            rendered = text.format(*self.args, **self.kwargs) if self.args or self.kwargs else text

        return rendered + self.suffix

    def __str__(self) -> str:
        """Provide a useful fallback for log consumers without a Session."""
        if isinstance(self.text, LocalizedString):
            text = self.text.format(*self.args, **self.kwargs) if self.args or self.kwargs else self.text
            return str(text) + self.suffix
        return self.text.format(*self.args, **self.kwargs) + self.suffix \
            if self.args or self.kwargs else self.text + self.suffix
