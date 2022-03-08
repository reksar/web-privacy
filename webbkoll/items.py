from dataclasses import dataclass


# TODO: split first- and third-party cookies
# TODO: split requests and hosts count
@dataclass(frozen=True)
class SummaryItem:
    summary_url: str
    checked_url: str
    final_url: str
    ip: str
    default_https: bool
    cookies: str
    aside_requests: str
    csp: bool
    referrer_policy: bool
