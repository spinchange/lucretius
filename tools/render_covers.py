"""Render docs/cover.jpg (1600x2400) from illustrations/cover.svg, and every
link-preview card illustrations/social*.svg to docs/<name>.jpg (1200x630:
social.jpg for the site, social-essay.jpg and social-margin.jpg for their
pages), with headless Chromium (Playwright). Run after changing a card or
replacing illustrations/cover_medallion.jpg; then rebuild the site (the
preview URLs are versioned by content) and, for the cover, the print wrap
with python tools/build_wrap.py."""
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

        # Render the link-preview cards (1200x630)
        page2 = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        for svg in sorted((ROOT / "illustrations").glob("social*.svg")):
            page2.goto(svg.resolve().as_uri())
            page2.wait_for_timeout(1000)
            out = ROOT / "docs" / f"{svg.stem}.jpg"
            page2.screenshot(path=str(out), type="jpeg", quality=88)
            print(f"Rendered docs/{out.name}:", Image.open(out).size)

        browser.close()

if __name__ == "__main__":
    render()
