from playwright.sync_api import sync_playwright, ViewportSize
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_viewport_size(ViewportSize(width = 1080*2, height=1920*2))



    page.goto('https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=760766942734-7b92qqmu8p6dpeb7hhfqb15batdp1sba.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.upload&state=aLvhK11JTVtOoXF9Wc4RILWsDnC1jY&prompt=consent&access_type=offline')  #navigate to URL
    
