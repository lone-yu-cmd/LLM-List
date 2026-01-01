import sys
import time
from urllib.parse import urlparse, urljoin
from playwright.sync_api import sync_playwright

def crawl_dynamic_docs(url, wait_selector=None):
    """
    Crawl documentation using Playwright to handle dynamic content (SPA).
    It extracts all links from the rendered page.
    """
    print(f"Starting crawl for: {url}")
    print("Initializing Playwright (headless Chromium)...")
    
    unique_links = set()
    base_domain = urlparse(url).netloc
    
    try:
        with sync_playwright() as p:
            # Launch browser with stealthier options
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars",
                    "--window-position=0,0",
                    "--ignore-certifcate-errors",
                    "--ignore-certifcate-errors-spki-list",
                    "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                ignore_https_errors=True,
                viewport={'width': 1920, 'height': 1080}
            )
            
            # Inject stealth script to hide webdriver property
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            page = context.new_page()
            
            # Navigate
            print("Navigating to page...")
            try:
                # Use a shorter timeout to fail fast if blocked, but enough for a normal load
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                
                # Try to wait for something that looks like a link or sidebar
                # If we don't know the selector, just wait a bit
                time.sleep(5)
                
            except Exception as e:
                print(f"Navigation warning: {e}")
            
            # Extract all links
            print("Extracting links...")
            elements = page.query_selector_all("a")
            
            found_count = 0
            for el in elements:
                try:
                    href = el.get_attribute("href")
                    if not href:
                        continue
                    
                    # Normalize URL
                    full_url = urljoin(url, href)
                    parsed = urlparse(full_url)
                    
                    # Filter: Keep only links within the same domain
                    if parsed.netloc == base_domain:
                        clean_url = full_url.split('#')[0].split('?')[0]
                        if clean_url not in unique_links:
                            unique_links.add(clean_url)
                            found_count += 1
                except Exception as e:
                    continue
            
            print(f"Found {found_count} links on the page (after filtering).")
            browser.close()
            
    except Exception as e:
        print(f"Error during crawl: {e}")
        if "Executable doesn't exist" in str(e):
            print("\nError: Playwright browsers are not installed.")
            print("Please run: playwright install chromium")
        return []

    return sorted(list(unique_links))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/crawl_api_docs.py <url>")
        sys.exit(1)
    
    target_url = sys.argv[1]
    links = crawl_dynamic_docs(target_url)
    
    print(f"\nSuccessfully extracted {len(links)} unique links:")
    print("-" * 50)
    for link in links:
        print(link)
    print("-" * 50)
    print(f"Total: {len(links)} pages")
