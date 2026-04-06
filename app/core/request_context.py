from contextvars import ContextVar


_client_ip_ctx: ContextVar[str | None] = ContextVar("client_ip", default=None)
_user_agent_ctx: ContextVar[str | None] = ContextVar("user_agent", default=None)


def set_request_identity(client_ip: str | None, user_agent: str | None) -> tuple:
    token_ip = _client_ip_ctx.set(client_ip)
    token_ua = _user_agent_ctx.set(user_agent)
    return token_ip, token_ua


def reset_request_identity(tokens: tuple) -> None:
    token_ip, token_ua = tokens
    _client_ip_ctx.reset(token_ip)
    _user_agent_ctx.reset(token_ua)


def get_request_client_ip() -> str | None:
    return _client_ip_ctx.get()


def get_request_user_agent() -> str | None:
    return _user_agent_ctx.get()
