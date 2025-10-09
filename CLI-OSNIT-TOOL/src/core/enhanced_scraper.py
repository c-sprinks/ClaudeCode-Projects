#!/usr/bin/env python3
"""
Enhanced Web Scraper - Advanced OSINT Collection

High-performance web scraping module with Brotli compression, JavaScript rendering,
user agent rotation, and stealth capabilities for comprehensive OSINT collection.

Features:
- Brotli compression support for faster downloads
- JavaScript-enabled scraping with requests-html
- Intelligent user agent rotation
- Rate limiting and stealth mode
- Content decompression and parsing
- Session management and cookie handling
"""

import asyncio
import logging
import time
import random
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import json
import hashlib

import requests
import aiohttp
import brotli
from requests_html import HTMLSession, AsyncHTMLSession
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import lxml.html

logger = logging.getLogger(__name__)


@dataclass
class ScrapingResult:
    """Result of web scraping operation"""
    url: str
    status_code: int
    content: str
    headers: Dict[str, str]
    response_time: float
    encoding: str
    compression: Optional[str]
    javascript_executed: bool
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class ScrapingConfig:
    """Configuration for web scraping operations"""
    enable_javascript: bool = True
    enable_brotli: bool = True
    rotate_user_agents: bool = True
    stealth_mode: bool = True
    max_retries: int = 3
    timeout: int = 30
    rate_limit: float = 1.0  # Seconds between requests
    custom_headers: Optional[Dict[str, str]] = None
    proxy_list: Optional[List[str]] = None


class EnhancedScraper:
    """
    Enhanced Web Scraper with Advanced Capabilities

    Provides high-performance web scraping with Brotli compression,
    JavaScript rendering, and intelligent stealth features.
    """

    def __init__(self, config: Optional[ScrapingConfig] = None):
        self.config = config or ScrapingConfig()

        # Initialize user agent rotation
        self.ua = UserAgent() if self.config.rotate_user_agents else None

        # Session management
        self.session = None
        self.async_session = None

        # Request tracking
        self.request_history = []
        self.last_request_time = 0

        # Cache for repeated requests
        self.cache_dir = Path.home() / ".inspector-g" / "scraper_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        logger.info("🌐 Enhanced Scraper initialized with advanced capabilities")

    def _get_session(self) -> HTMLSession:
        """Get or create HTML session with optimal configuration"""
        if self.session is None:
            self.session = HTMLSession()

            # Configure session headers
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br' if self.config.enable_brotli else 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }

            if self.config.custom_headers:
                headers.update(self.config.custom_headers)

            self.session.headers.update(headers)

        return self.session

    async def _get_async_session(self) -> AsyncHTMLSession:
        """Get or create async HTML session"""
        if self.async_session is None:
            self.async_session = AsyncHTMLSession()

        return self.async_session

    def _get_user_agent(self) -> str:
        """Get random user agent string"""
        if self.ua and self.config.rotate_user_agents:
            try:
                return self.ua.random
            except Exception as e:
                logger.warning(f"Failed to get random user agent: {e}")

        # Fallback user agents
        fallback_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        return random.choice(fallback_agents)

    def _apply_rate_limiting(self):
        """Apply rate limiting between requests"""
        if self.config.rate_limit > 0:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time

            if time_since_last < self.config.rate_limit:
                sleep_time = self.config.rate_limit - time_since_last
                logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)

            self.last_request_time = time.time()

    def _get_cache_key(self, url: str, headers: Dict[str, str]) -> str:
        """Generate cache key for request"""
        content = f"{url}:{json.dumps(headers, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()

    def _get_cached_result(self, cache_key: str) -> Optional[ScrapingResult]:
        """Get cached scraping result if available and fresh"""
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)

                # Check if cache is fresh (1 hour)
                cached_time = datetime.fromisoformat(data['timestamp'])
                if datetime.now() - cached_time < timedelta(hours=1):
                    logger.debug(f"Using cached result for {data['url']}")
                    return ScrapingResult(
                        url=data['url'],
                        status_code=data['status_code'],
                        content=data['content'],
                        headers=data['headers'],
                        response_time=data['response_time'],
                        encoding=data['encoding'],
                        compression=data['compression'],
                        javascript_executed=data['javascript_executed'],
                        timestamp=datetime.fromisoformat(data['timestamp']),
                        metadata=data['metadata']
                    )
            except Exception as e:
                logger.warning(f"Failed to load cached result: {e}")

        return None

    def _cache_result(self, cache_key: str, result: ScrapingResult):
        """Cache scraping result"""
        try:
            cache_file = self.cache_dir / f"{cache_key}.json"

            data = {
                'url': result.url,
                'status_code': result.status_code,
                'content': result.content,
                'headers': result.headers,
                'response_time': result.response_time,
                'encoding': result.encoding,
                'compression': result.compression,
                'javascript_executed': result.javascript_executed,
                'timestamp': result.timestamp.isoformat(),
                'metadata': result.metadata
            }

            with open(cache_file, 'w') as f:
                json.dump(data, f)

        except Exception as e:
            logger.warning(f"Failed to cache result: {e}")

    def _decompress_content(self, content: bytes, encoding: str) -> str:
        """Decompress content based on encoding"""
        try:
            if encoding == 'br':
                # Brotli decompression
                decompressed = brotli.decompress(content)
                return decompressed.decode('utf-8', errors='ignore')
            elif encoding == 'gzip':
                import gzip
                decompressed = gzip.decompress(content)
                return decompressed.decode('utf-8', errors='ignore')
            elif encoding == 'deflate':
                import zlib
                decompressed = zlib.decompress(content)
                return decompressed.decode('utf-8', errors='ignore')
            else:
                return content.decode('utf-8', errors='ignore')
        except Exception as e:
            logger.warning(f"Decompression failed: {e}")
            return content.decode('utf-8', errors='ignore')

    def scrape_url(self, url: str, javascript: bool = None) -> ScrapingResult:
        """
        Scrape a single URL with enhanced capabilities
        """
        start_time = time.time()

        # Override config if specified
        use_javascript = javascript if javascript is not None else self.config.enable_javascript

        # Apply rate limiting
        self._apply_rate_limiting()

        # Prepare headers
        headers = {}
        if self.config.rotate_user_agents:
            headers['User-Agent'] = self._get_user_agent()

        # Check cache
        cache_key = self._get_cache_key(url, headers)
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result

        logger.info(f"🌐 Scraping URL: {url}")

        # Attempt scraping with retries
        last_exception = None
        for attempt in range(self.config.max_retries):
            try:
                if use_javascript:
                    result = self._scrape_with_javascript(url, headers, start_time)
                else:
                    result = self._scrape_without_javascript(url, headers, start_time)

                # Cache successful result
                self._cache_result(cache_key, result)
                return result

            except Exception as e:
                last_exception = e
                logger.warning(f"Scraping attempt {attempt + 1} failed: {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff

        # All attempts failed
        logger.error(f"All scraping attempts failed for {url}: {last_exception}")
        raise last_exception

    def _scrape_with_javascript(self, url: str, headers: Dict[str, str], start_time: float) -> ScrapingResult:
        """Scrape URL with JavaScript execution"""
        session = self._get_session()

        # Update headers for this request
        session.headers.update(headers)

        response = session.get(url, timeout=self.config.timeout)
        response.raise_for_status()

        # Execute JavaScript if page has it
        if response.html.raw_html and b'<script' in response.html.raw_html:
            logger.debug("Executing JavaScript...")
            response.html.render(timeout=20, keep_page=True)

        response_time = time.time() - start_time

        # Determine compression
        compression = None
        if 'content-encoding' in response.headers:
            compression = response.headers['content-encoding']

        # Get final content
        content = response.html.html or response.text

        return ScrapingResult(
            url=url,
            status_code=response.status_code,
            content=content,
            headers=dict(response.headers),
            response_time=response_time,
            encoding=response.encoding or 'utf-8',
            compression=compression,
            javascript_executed=True,
            timestamp=datetime.now(),
            metadata={
                'page_title': self._extract_title(content),
                'links_found': len(response.html.links),
                'images_found': len([img for img in response.html.find('img')]),
                'forms_found': len([form for form in response.html.find('form')])
            }
        )

    def _scrape_without_javascript(self, url: str, headers: Dict[str, str], start_time: float) -> ScrapingResult:
        """Scrape URL without JavaScript execution (faster)"""
        response = requests.get(
            url,
            headers=headers,
            timeout=self.config.timeout,
            allow_redirects=True
        )
        response.raise_for_status()

        response_time = time.time() - start_time

        # Handle compressed content
        compression = None
        content = response.text

        if 'content-encoding' in response.headers:
            compression = response.headers['content-encoding']
            if compression in ['br', 'gzip', 'deflate']:
                content = self._decompress_content(response.content, compression)

        # Parse with BeautifulSoup for metadata
        soup = BeautifulSoup(content, 'lxml')

        return ScrapingResult(
            url=url,
            status_code=response.status_code,
            content=content,
            headers=dict(response.headers),
            response_time=response_time,
            encoding=response.encoding or 'utf-8',
            compression=compression,
            javascript_executed=False,
            timestamp=datetime.now(),
            metadata={
                'page_title': self._extract_title_from_soup(soup),
                'links_found': len(soup.find_all('a')),
                'images_found': len(soup.find_all('img')),
                'forms_found': len(soup.find_all('form'))
            }
        )

    def _extract_title(self, html_content: str) -> str:
        """Extract page title from HTML content"""
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            title_tag = soup.find('title')
            return title_tag.get_text().strip() if title_tag else "No title"
        except Exception:
            return "Title extraction failed"

    def _extract_title_from_soup(self, soup: BeautifulSoup) -> str:
        """Extract page title from BeautifulSoup object"""
        try:
            title_tag = soup.find('title')
            return title_tag.get_text().strip() if title_tag else "No title"
        except Exception:
            return "Title extraction failed"

    async def scrape_urls_async(self, urls: List[str], javascript: bool = None) -> List[ScrapingResult]:
        """
        Scrape multiple URLs asynchronously
        """
        use_javascript = javascript if javascript is not None else self.config.enable_javascript

        logger.info(f"🌐 Starting async scraping of {len(urls)} URLs")

        semaphore = asyncio.Semaphore(5)  # Limit concurrent requests

        async def scrape_single(url: str) -> ScrapingResult:
            async with semaphore:
                # Apply rate limiting
                if self.config.rate_limit > 0:
                    await asyncio.sleep(self.config.rate_limit)

                try:
                    return await self._scrape_url_async(url, use_javascript)
                except Exception as e:
                    logger.error(f"Failed to scrape {url}: {e}")
                    # Return error result
                    return ScrapingResult(
                        url=url,
                        status_code=0,
                        content="",
                        headers={},
                        response_time=0.0,
                        encoding="utf-8",
                        compression=None,
                        javascript_executed=False,
                        timestamp=datetime.now(),
                        metadata={"error": str(e)}
                    )

        tasks = [scrape_single(url) for url in urls]
        results = await asyncio.gather(*tasks)

        logger.info(f"✅ Completed async scraping of {len(urls)} URLs")
        return results

    async def _scrape_url_async(self, url: str, use_javascript: bool) -> ScrapingResult:
        """Async version of URL scraping"""
        start_time = time.time()

        headers = {}
        if self.config.rotate_user_agents:
            headers['User-Agent'] = self._get_user_agent()

        if use_javascript:
            # Use requests-html async session
            session = await self._get_async_session()
            response = await session.get(url)
            await response.html.arender(timeout=20)

            content = response.html.html or response.text

            return ScrapingResult(
                url=url,
                status_code=response.status_code,
                content=content,
                headers=dict(response.headers),
                response_time=time.time() - start_time,
                encoding=response.encoding or 'utf-8',
                compression=response.headers.get('content-encoding'),
                javascript_executed=True,
                timestamp=datetime.now(),
                metadata={
                    'page_title': self._extract_title(content),
                    'links_found': len(response.html.links),
                }
            )
        else:
            # Use aiohttp for faster non-JS scraping
            async with aiohttp.ClientSession(
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            ) as session:
                async with session.get(url) as response:
                    content = await response.text()

                    return ScrapingResult(
                        url=url,
                        status_code=response.status,
                        content=content,
                        headers=dict(response.headers),
                        response_time=time.time() - start_time,
                        encoding=response.charset or 'utf-8',
                        compression=response.headers.get('content-encoding'),
                        javascript_executed=False,
                        timestamp=datetime.now(),
                        metadata={
                            'page_title': self._extract_title(content),
                        }
                    )

    def extract_osint_data(self, result: ScrapingResult) -> Dict[str, Any]:
        """
        Extract OSINT-relevant data from scraping result
        """
        soup = BeautifulSoup(result.content, 'lxml')

        osint_data = {
            'url': result.url,
            'title': result.metadata.get('page_title', ''),
            'emails': self._extract_emails(result.content),
            'phone_numbers': self._extract_phone_numbers(result.content),
            'social_links': self._extract_social_links(soup),
            'external_links': self._extract_external_links(soup, result.url),
            'technologies': self._detect_technologies(result),
            'meta_data': self._extract_meta_data(soup),
            'forms': self._analyze_forms(soup),
            'response_headers': result.headers,
            'performance': {
                'response_time': result.response_time,
                'compression': result.compression,
                'javascript_executed': result.javascript_executed
            }
        }

        return osint_data

    def _extract_emails(self, content: str) -> List[str]:
        """Extract email addresses from content"""
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, content)
        return list(set(emails))  # Remove duplicates

    def _extract_phone_numbers(self, content: str) -> List[str]:
        """Extract phone numbers from content"""
        import re
        # Simple phone number patterns
        phone_patterns = [
            r'\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',  # US format
            r'\+?[0-9]{1,4}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}',  # International
        ]

        phones = []
        for pattern in phone_patterns:
            phones.extend(re.findall(pattern, content))

        return list(set(phones))

    def _extract_social_links(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract social media links"""
        social_domains = {
            'twitter': ['twitter.com', 'x.com'],
            'facebook': ['facebook.com', 'fb.com'],
            'linkedin': ['linkedin.com'],
            'instagram': ['instagram.com'],
            'youtube': ['youtube.com', 'youtu.be'],
            'github': ['github.com'],
            'tiktok': ['tiktok.com'],
            'telegram': ['t.me', 'telegram.me']
        }

        social_links = {platform: [] for platform in social_domains.keys()}

        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            for platform, domains in social_domains.items():
                if any(domain in href for domain in domains):
                    social_links[platform].append(link['href'])

        return {k: list(set(v)) for k, v in social_links.items() if v}

    def _extract_external_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract external links"""
        from urllib.parse import urljoin, urlparse

        base_domain = urlparse(base_url).netloc
        external_links = []

        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            parsed = urlparse(full_url)

            if parsed.netloc and parsed.netloc != base_domain:
                external_links.append(full_url)

        return list(set(external_links))

    def _detect_technologies(self, result: ScrapingResult) -> Dict[str, Any]:
        """Detect technologies used by the website"""
        technologies = {
            'server': result.headers.get('server', 'Unknown'),
            'framework': None,
            'cms': None,
            'javascript_libraries': [],
            'analytics': []
        }

        content_lower = result.content.lower()

        # Detect frameworks and CMSs
        if 'wordpress' in content_lower or 'wp-content' in content_lower:
            technologies['cms'] = 'WordPress'
        elif 'drupal' in content_lower:
            technologies['cms'] = 'Drupal'
        elif 'joomla' in content_lower:
            technologies['cms'] = 'Joomla'

        # Detect JavaScript libraries
        js_libraries = {
            'jquery': 'jquery',
            'react': 'react',
            'angular': 'angular',
            'vue': 'vue',
            'bootstrap': 'bootstrap'
        }

        for lib_name, pattern in js_libraries.items():
            if pattern in content_lower:
                technologies['javascript_libraries'].append(lib_name)

        # Detect analytics
        analytics_patterns = {
            'google-analytics': 'Google Analytics',
            'gtag': 'Google Analytics',
            'facebook.com/tr': 'Facebook Pixel',
            'hotjar': 'Hotjar'
        }

        for pattern, service in analytics_patterns.items():
            if pattern in content_lower:
                technologies['analytics'].append(service)

        return technologies

    def _extract_meta_data(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract meta data from HTML"""
        meta_data = {}

        # Standard meta tags
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            if tag.get('name'):
                meta_data[tag['name']] = tag.get('content', '')
            elif tag.get('property'):
                meta_data[tag['property']] = tag.get('content', '')

        return meta_data

    def _analyze_forms(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Analyze forms on the page"""
        forms = []

        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'GET').upper(),
                'inputs': [],
                'has_file_upload': False
            }

            for input_tag in form.find_all(['input', 'textarea', 'select']):
                input_data = {
                    'type': input_tag.get('type', 'text'),
                    'name': input_tag.get('name', ''),
                    'required': input_tag.has_attr('required')
                }

                if input_data['type'] == 'file':
                    form_data['has_file_upload'] = True

                form_data['inputs'].append(input_data)

            forms.append(form_data)

        return forms

    def get_scraping_stats(self) -> Dict[str, Any]:
        """Get scraping statistics"""
        return {
            'total_requests': len(self.request_history),
            'cache_size': len(list(self.cache_dir.glob('*.json'))),
            'config': {
                'javascript_enabled': self.config.enable_javascript,
                'brotli_enabled': self.config.enable_brotli,
                'user_agent_rotation': self.config.rotate_user_agents,
                'rate_limit': self.config.rate_limit
            }
        }

    def clear_cache(self):
        """Clear scraping cache"""
        try:
            for cache_file in self.cache_dir.glob('*.json'):
                cache_file.unlink()
            logger.info("🗑️ Scraping cache cleared")
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")

    def close(self):
        """Clean up resources"""
        if self.session:
            self.session.close()
        if self.async_session:
            asyncio.create_task(self.async_session.close())


# Global enhanced scraper instance
enhanced_scraper = EnhancedScraper()