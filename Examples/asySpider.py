#!/usr/bin/env python
# coding: utf-8
# Asynchronous Spider Example
from datetime import timedelta
from tornado import httpclient, gen, ioloop, queues


class AsySpider(object):
    """A simple class of asynchronous spider."""
    def __init__(self, urls, concurrency=10, **kwargs):
        urls.reverse()
        self.urls = urls
        self.concurrency = concurrency
        self._q = queues.Queue()
        self._fetching = set()
        self._fetched = set()

    def fetch(self, url, **kwargs):
        fetch = getattr(httpclient.AsyncHTTPClient(), 'fetch')
        return fetch(url, **kwargs)

    def handle_html(self, url, html):
        """handle html page"""
        print(url)

    def handle_response(self, url, response):
        if response.code == 200:
            self.handle_html(url, response.body)
        elif response.code == 599:
            self._fetching.remove(url)
            self._q.put(url)

    @gen.coroutine
    def get_page(self, url):
        try:
            response = yield self.fetch(url)
            print('######fetched {}'.format(url))
        except Exception as e:
            print('Exception: {} {}'.format(e, url))
            raise gen.Return(e)
        raise gen.Return(response)

    @gen.coroutine
    def _run(self):
        @gen.coroutine
        def fetch_url():
            current_url = yield self._q.get()
            try:
                if current_url in self._fetching:
                    return
                print('Fetching****** {}'.format(current_url))
                self._fetching.add(current_url)

                response = yield self.get_page(current_url)
                self.handle_response(current_url, response)

                self._fetched.add(current_url)

                for i in range(self.concurrency):
                    if self.urls:
                        yield self._q.put(self.urls.pop())
            finally:
                self._q.task_done()

        @gen.coroutine
        def worker():
            while True:
                yield fetch_url()

        self._q.put(self.urls.pop())

        for _ in range(self.concurrency):
            worker()

        yield self._q.join(timeout=timedelta(seconds=300000))
        assert self._fetching == self._fetched

    def run(self):
        io_loop = ioloop.IOLoop.current()
        io_loop.run_sync(self._run)


class MySpider(AsySpider):
    def fetch(self, url, **kwargs):
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
        }
        return super(MySpider, self).fetch(url, headers=headers, request_timeout=1)

    def handle_html(self, url, html):
        print(url, html)


def main():
    urls = []
    for page in range(1, 100):
        urls.append('https://www.baidu.com?page={}'.format(page))
    s = MySpider(urls)
    s.run()

if __name__ == '__main__':
    main()
