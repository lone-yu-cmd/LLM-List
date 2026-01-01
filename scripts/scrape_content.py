import sys
import json
import os
import time
import argparse
import re
from urllib.parse import urlparse
import html2text
from playwright.sync_api import sync_playwright

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = str(value)
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def scrape_urls(urls, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Starting scrape for {len(urls)} URLs...")
    
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    converter.ignore_emphasis = False
    converter.body_width = 0 # No wrapping
    
    with sync_playwright() as p:
        # Launch browser with stealthier options (copied from crawl_api_docs.py)
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
        
        for i, url in enumerate(urls):
            print(f"[{i+1}/{len(urls)}] Processing: {url}")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                # Wait for some content stability
                time.sleep(3)
                
                # Extract title for filename
                title = page.title()
                if not title:
                    title = "untitled"
                
                # Slugify url path for filename to ensure uniqueness
                path = urlparse(url).path
                filename = slugify(f"{title}-{path}")
                if not filename:
                    filename = slugify(url)
                
                # Truncate filename if too long
                if len(filename) > 200:
                    filename = filename[:200]
                    
                filepath = os.path.join(output_dir, f"{filename}.md")
                
                # Get content
                # Try to get the main content if possible, otherwise body
                # Common selectors for documentation content
                selectors = ["article", "main", ".markdown-body", "#content", ".content", "body"]
                content_html = ""
                
                for selector in selectors:
                    if page.locator(selector).count() > 0:
                        # Check if it's visible
                        if page.locator(selector).first.is_visible():
                            content_html = page.locator(selector).first.inner_html()
                            print(f"  Found content using selector: {selector}")
                            break
                
                if not content_html:
                    content_html = page.content()
                    print("  Using full page content")
                
                markdown = converter.handle(content_html)
                
                # Add metadata header
                header = f"---\ntitle: {title}\nurl: {url}\n---\n\n"
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(header + markdown)
                    
                print(f"  Saved to: {filepath}")
                
            except Exception as e:
                print(f"  Error processing {url}: {e}")
        
        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape content from a list of URLs")
    parser.add_argument("inputs", nargs="+", help="One or more URLs, or JSON files containing a list of URLs")
    parser.add_argument("--output", "-o", default="docs_dump", help="Output directory")
    
    args = parser.parse_args()
    
    urls = []
    for input_arg in args.inputs:
        if input_arg.endswith(".json"):
            try:
                with open(input_arg, "r") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        urls.extend(data)
                    else:
                        print(f"Warning: JSON file {input_arg} must contain a list of URLs, skipping.")
            except Exception as e:
                print(f"Error reading JSON file {input_arg}: {e}")
        else:
            # Assume it's a direct URL
            urls.append(input_arg)
        
    if not urls:
        print("No URLs found to scrape.")
        sys.exit(1)

    scrape_urls(urls, args.output)
