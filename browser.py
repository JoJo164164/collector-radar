from playwright.sync_api import sync_playwright

def fetch_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(url, timeout=60000)

        page.wait_for_timeout(2000)

        html = page.content()

        browser.close()

        return html


def fetch_page(page, url):
    page.goto(url, timeout=60000)
    page.wait_for_timeout(2000)
    return page.content()
