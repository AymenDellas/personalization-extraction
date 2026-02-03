from __future__ import annotations

import time
from playwright.sync_api import Page, sync_playwright


def _scroll_page(page, steps: int = 6, delay_s: float = 0.6) -> None:
    for _ in range(steps):
        page.mouse.wheel(0, 800)
        time.sleep(delay_s)


def _follow_linkedin_redirect(page: Page) -> None:
    warning_header = page.locator(
        "h1",
        has_text="not on LinkedIn",
    )
    if warning_header.count() == 0 or not warning_header.first.is_visible():
        return

    print("Detected LinkedIn redirect warning. Attempting to follow link...")
    redirect_link = page.locator("main a[href]").first
    if not redirect_link.is_visible():
        return

    actual_url = redirect_link.get_attribute("href")
    if not actual_url:
        return

    print(f"Found actual URL: {actual_url}")
    page.goto(actual_url, timeout=45000, wait_until="domcontentloaded")
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        print("Network idle timeout after LinkedIn redirect.")


def _extract_visible_text(page: Page) -> str:
    content_locator = page.locator("main")
    if content_locator.count() == 0:
        content_locator = page.locator("body")

    text = content_locator.inner_text().strip()
    if not text:
        text = page.locator("body").inner_text().strip()
    if not text:
        text = page.evaluate("() => document.body ? document.body.innerText : ''").strip()
    return text


def scrape_generic_website(url: str, headless: bool = True) -> str | None:
    """
    Opens a generic website and extracts the visible text from the rendered page.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/121.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 720},
        )

        page = context.new_page()

        try:
            print(f"Navigating to {url}...")
            page.goto(url, timeout=45000, wait_until="domcontentloaded")

            try:
                page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                print("Network idle timeout, continuing with rendered content.")

            try:
                page.wait_for_selector("body", timeout=5000)
            except Exception:
                print("Body selector not ready, continuing with rendered content.")

            try:
                _follow_linkedin_redirect(page)
            except Exception as e:
                print(f"LinkedIn redirect handling warning: {e}")

            _scroll_page(page)

            text = _extract_visible_text(page)

            return text or None

        except Exception as e:
            print(f"Website scrape error: {e}")
            return None
        finally:
            browser.close()
