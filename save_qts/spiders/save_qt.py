import json
import os
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import scrapy
from scrapy_splash import SplashRequest, SplashResponse


SPLASH_TOKEN = os.getenv('SPLASH_TOKEN', '')


class SaveQtSpider(scrapy.Spider):
    name = 'save_qt'
    allowed_domains = ['quicktopic.com']
    start_urls = ['http://quicktopic.com/']

    out_dir: Path

    def __init__(
        self,
        urls=None,
        out_dir='/tmp',
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        lines = (s.strip() for s in Path(urls).read_text().splitlines())
        urls = {
            self.canonicalize_qt_url(s)
            for s in lines
            if s and not s.startswith('#')
        }
        self.start_urls = sorted(urls)
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def canonicalize_qt_url(s: str) -> str:
        url = urlparse(s)
        return f'https://quicktopic.com{url.path}?m1=-1&mN=-1'

    def start_requests(self):
        splash_meta = dict(
            magic_response=False,
            splash_headers={},
        )
        if SPLASH_TOKEN:
            splash_meta['splash_headers']['X-Token'] = SPLASH_TOKEN

        for url in self.start_urls:
            yield SplashRequest(
                url,
                endpoint='render.json',
                callback=self.save_body,
                method='GET',
                args=dict(har='1', html='1'),
                meta=dict(splash=splash_meta),
            )

    def parse(self, response):
        return response

    @staticmethod
    def clean_qt_url(s: str):
        url = urlparse(s)
        return url.path.lstrip('/').replace('/', '+')

    def save_body(self, response):
        url = getattr(response, 'data', {}).get('url', response.url)
        path = self.out_dir / self.clean_qt_url(url)

        path.with_suffix('.json').write_bytes(response.body)

        if html := response.data.get('html'):
            path.with_suffix('.html').write_text(html)

        if har := response.data.get('har'):
            with path.with_suffix('.har').open('wt') as f:
                json.dump(har, f)
