"""Render docs/cover.jpg (1600x2400) and docs/social.jpg (1200x630) from
illustrations/cover.svg and social.svg with headless Chromium (Playwright).
Run after replacing illustrations/cover_medallion.jpg; then rebuild the
print wrap with python tools/build_wrap.py."""
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent

def render():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Render cover.jpg (1600x2400)
        page = browser.new_page(viewport={"width": 800, "height": 1200}, device_scale_factor=2)
        cover_svg = (ROOT / "illustrations" / "cover.svg").resolve().as_uri()
        page.goto(cover_svg)
        page.wait_for_timeout(1000)
        out_cover = ROOT / "docs" / "cover.jpg"
        page.screenshot(path=str(out_cover), type="jpeg", quality=88)
        print("Rendered docs/cover.jpg:", Image.open(out_cover).size)

        # Render social.jpg (1200x630)
        page2 = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        social_svg = (ROOT / "illustrations" / "social.svg").resolve().as_uri()
        page2.goto(social_svg)
        page2.wait_for_timeout(1000)
        out_social = ROOT / "docs" / "social.jpg"
        page2.screenshot(path=str(out_social), type="jpeg", quality=88)
        print("Rendered docs/social.jpg:", Image.open(out_social).size)

        browser.close()

if __name__ == "__main__":
    render()
