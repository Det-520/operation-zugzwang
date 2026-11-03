import os, sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
    pg = b.new_page(viewport={"width":1580,"height":1140}, device_scale_factor=float(sys.argv[3]) if len(sys.argv)>3 else 1)
    pg.goto("file://"+sys.argv[1]); pg.wait_for_timeout(600)
    pg.screenshot(path=sys.argv[2]); b.close()
