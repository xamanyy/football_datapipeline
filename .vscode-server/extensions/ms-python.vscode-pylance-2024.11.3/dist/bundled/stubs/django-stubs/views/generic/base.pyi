from collections.abc import Callable
from typing import Any

from django import http

class ContextMixin:
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...

class View:
    http_method_names: list[str] = ...
    request: http.HttpRequest = ...
    args: Any = ...
    kwargs: Any = ...
    def __init__(self, **kwargs: Any) -> None: ...
    @classmethod
    def as_view(cls, **initkwargs: Any) -> Callable[..., http.HttpResponse]: ...
    def setup(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> None: ...
    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...
    def http_method_not_allowed(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...
    def options(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...

class TemplateResponseMixin:
    template_name: str = ...
    template_engine: str | None = ...
    response_class: type[http.HttpResponse] = ...
    content_type: str | None = ...
    request: http.HttpRequest = ...
    def render_to_response(
        self, context: dict[str, Any], **response_kwargs: Any
    ) -> http.HttpResponse: ...
    def get_template_names(self) -> list[str]: ...

class TemplateView(TemplateResponseMixin, ContextMixin, View):
    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...

class RedirectView(View):
    permanent: bool = ...
    url: str | None = ...
    pattern_name: str | None = ...
    query_string: bool = ...
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None: ...
    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...
    def head(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...
    def post(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...
    def delete(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...
    def put(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...
    def patch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...