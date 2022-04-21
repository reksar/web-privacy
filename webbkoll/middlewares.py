# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import re
import time
from http import HTTPStatus
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware as ScrapyRetry
from webbkoll.settings import WEBBKOLL_URL


class WebbkollSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ResultsRetry(ScrapyRetry):

    INTERVAL_SECONDS = 7

    def process_response(self, request, response, spider):
        """
        Override from base class. Must either:
        - return a Response object
        - return a Request object
        - or raise IgnoreRequest

        After submitting the Webbkoll form to check an URL, it redirects to a
        `status` resourse "https://webbkoll.dataskydd.net/en/status?id=<...>".

        Then, you will get either HTTP status 200 or 302 redirect.

        It takes some time (10-20 sec) to check the URL, and while the check
        is incomplete, the Webbkoll `status` will respond with HTTP 200.
        Once the check is complete, you will get 302 redirect to `results`
        "https://webbkoll.dataskydd.net/en/results?url=<...>".

        A `results` will be cached, so you may get 302 redirect immediately.
        """
        if request.meta.get('dont_retry', False):
            return response

        if still_status(response):
            # Retry if response is a `status` resource and redirect to a
            # `results` is not ready. This prevents the spider from parsing
            # the `status` page instead of `results`.
            reason = 'Redirect to results is not ready.'
            time.sleep(self.INTERVAL_SECONDS)
            return self._retry(request, reason, spider) or response

        return response


def still_status(response):
    # When redirect to results is not ready.
    return is_status_url(response.url) and HTTPStatus.OK == response.status

def is_status_url(url):
    # "https://webbkoll.dataskydd.net/en/status?id=<...>"
    return re.match(rf'{WEBBKOLL_URL}/\w+/status', url)
