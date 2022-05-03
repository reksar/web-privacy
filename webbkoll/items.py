from dataclasses import dataclass


@dataclass(frozen=True)
class AsideRequests:
    requests: int
    hosts: int

@dataclass(frozen=True)
class Cookies:
    first_party: int
    third_party: int
    total: int

@dataclass(frozen=True)
class Summary:
    summary_url: str
    checked_url: str
    final_url: str
    ip: str
    default_https: bool
    cookies: Cookies
    aside_requests: AsideRequests
    csp: bool
    referrer_policy: bool

@dataclass(frozen=True)
class WebbkollError:
    error: str
