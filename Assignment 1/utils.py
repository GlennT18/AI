import hashlib
import shutil
import sys
from collections import OrderedDict
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse, urlunparse

import lxml.html
import requests
from lxml import etree

_VERBOSE = True


def visit_url(url: str) -> List[str]:
    url = _normalize_url(url)
    if _VERBOSE:
        print(f"Visiting URL: {url}", file=sys.stderr)

    links = list()

    cache = _check_cache(url)
    if cache is not None:
        if len(cache) > 0:
            links = cache.split('\n')
    else:
        try:
            r = requests.get(url)
            if (200 <= r.status_code < 300 and
                    r.headers.get('content-type', '').startswith('text/html')):
                content = r.text

                tree = lxml.html.document_fromstring(content)
                raw_links = tree.xpath('//a[@href]/@href')
                normalized_links = map(
                    lambda u: _normalize_url(u, url),
                    raw_links
                )
                same_origin_links = filter(
                    lambda u: _is_same_origin(u, url),
                    normalized_links
                )
                # Exclude current URL from links
                out_links = filter(lambda u: u != url, same_origin_links)
                unique_links = list(OrderedDict.fromkeys(out_links))
                links = unique_links

                _write_cache(url, '\n'.join(links))
        except (requests.exceptions.RequestException, lxml.etree.ParserError):
            pass

    return links


def clean_cache_dir() -> None:
    cache_dir = _get_cache_dir()
    if cache_dir.is_dir():
        shutil.rmtree(cache_dir)


def _check_cache(url: str) -> Optional[str]:
    if not _cache_available():
        return None

    cache_path = _get_cache_dir() / _get_cache_key(url)
    if cache_path.is_file():
        try:
            cache_file = open(cache_path, 'r')
            try:
                return cache_file.read()
            finally:
                cache_file.close()
        except OSError:
            return None


def _write_cache(url: str, content: str) -> None:
    if not _cache_available():
        return

    cache_path = _get_cache_dir() / _get_cache_key(url)
    try:
        cache_file = open(cache_path, 'w')
        try:
            cache_file.write(content)
        finally:
            cache_file.close()
    except OSError:
        pass


def _get_cache_key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()


def _cache_available() -> bool:
    if not hasattr(_cache_available, 'available'):
        try:
            _get_cache_dir().mkdir(parents=True, exist_ok=True)
            _cache_available.available = True
        except OSError:
            _cache_available.available = False
    return _cache_available.available


def _get_cache_dir() -> Path:
    home_dir = Path.home()
    platform = sys.platform
    if platform == 'win32':
        return home_dir / 'AppData' / 'Local' / 'Temp' / 'CrawlerCache'
    elif platform == 'darwin':
        return home_dir / 'Library' / 'Caches' / 'CrawlerCache'
    else:
        return home_dir / '.cache' / 'crawler-cache'


def _is_relative_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == '' and parsed.netloc == ''


def _is_same_origin(url: str, origin_url: str) -> bool:
    parsed = urlparse(url)

    if _is_relative_url(url):
        return True
    else:
        return parsed.netloc == urlparse(origin_url).netloc


def _normalize_url(url: str, context_url: str = '') -> str:
    parsed = urlparse(url)._replace(scheme='https', fragment='', query='')
    trailing_slash_stripped = False
    if parsed.path.endswith('/'):
        parsed = parsed._replace(path=parsed.path.rstrip('/'))
        trailing_slash_stripped = True
    context_parsed = urlparse(context_url)

    if _is_relative_url(url):
        parsed = parsed._replace(netloc=context_parsed.netloc)

    path = parsed.path
    if path == '':
        new_path = context_parsed.path
    elif not path.startswith('/'):
        # Partially implement relative URL handling according to
        # https://www.w3.org/TR/WD-html40-970917/htmlweb.html#h-5.1.2
        if trailing_slash_stripped:
            parent = context_parsed.path
        else:
            parent = context_parsed.path.rsplit('/', 1)[0]
        new_path = f'{parent}/{parsed.path}'
    else:
        new_path = path

    parsed = parsed._replace(path=new_path)

    return str(urlunparse(parsed))
