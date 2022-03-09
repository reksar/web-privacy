from dataclasses import dataclass


@dataclass(frozen=True)
class CookiesItem:
    first_party: int
    third_party: int
    total: int


# TODO: split requests and hosts count
@dataclass(frozen=True)
class SummaryItem:
    summary_url: str
    checked_url: str
    final_url: str
    ip: str
    default_https: bool
    cookies: CookiesItem
    aside_requests: str
    csp: bool
    referrer_policy: bool
