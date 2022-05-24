"""
A `Spider*` class - is a spider middleware.
See https://docs.scrapy.org/en/latest/topics/spider-middleware.html

A `Downloader*` class - is a downloader middleware.
See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
"""

import re
import time
from http import HTTPStatus
from scrapy.http import Request, Response, FormRequest
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from webbkoll.settings import WEBBKOLL_URL, RETRY_AFTER_SECONDS


class SpiderCheckUrlRequest:

    def process_start_requests(self, start_requests, spider):
        """
        Gets `start_requests` based on the `start_urls` from `spider`.
        Transforms these requests to Webbkoll <form> requests.

        See https://docs.scrapy.org/en/latest/topics/spider-middleware.html#scrapy.spidermiddlewares.SpiderMiddleware.process_start_requests
        """
        yield from map(preload_webbkoll_form, start_requests)


class DownloaderRetryResults(RetryMiddleware):

    def process_response(self, request, response, spider):
        """
        After submitting the Webbkoll form to check an URL, it redirects to a
        *status* resourse "https://webbkoll.dataskydd.net/en/status?id=<...>".

        Then, you will get either HTTP status 200 or 302 redirect.

        It takes some time (10-20 sec) to check the URL, and while the check
        is incomplete, the Webbkoll *status* will respond with HTTP 200.
        Once the check is complete, you will get 302 redirect to *results*
        "https://webbkoll.dataskydd.net/en/results?url=<...>".

        You may get 302 redirect immediately if *results* is cached.
        """
        if still_status(response):
            # Retry if response is a *status* resource and redirect to a
            # *results* is not ready. This prevents the spider from parsing
            # the *status* page instead of *results*.
            reason = 'Redirect to results is not ready.'
            time.sleep(RETRY_AFTER_SECONDS)
            return self._retry(request, reason, spider) or response

        return response


def still_status(response):
    # When redirect to *results* is not ready.
    return is_status_url(response.url) and HTTPStatus.OK == response.status


def is_status_url(url):
    # URL like "https://webbkoll.dataskydd.net/en/status?id=<...>"
    # Matches "https://webbkoll.dataskydd.net/<word>/status"
    return re.match(rf'{WEBBKOLL_URL}/\w+/status', url)


def preload_webbkoll_form(request):
    """
    Instead of making the `request`, gets `WEBBKOLL_URL` to load the <form>
    with the actual CSRF token. Then submits this <form> with the given
    `request.url`.

    See https://docs.scrapy.org/en/latest/topics/request-response.html#scrapy.http.Request.replace
    """
    return request.replace(
        url=WEBBKOLL_URL,
        callback=submit_webbkoll_form,
        cb_kwargs={'url': request.url},
        dont_filter=True)


def submit_webbkoll_form(webbkoll_form: Response, **formdata: dict) -> Request:
    # Submits preloaded Webbkoll <form> with the given `formdata`.
    return FormRequest.from_response(
        webbkoll_form,
        formdata=formdata,
        dont_filter=True)
