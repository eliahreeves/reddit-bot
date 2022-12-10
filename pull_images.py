import Errors
import constants as c
from playwright.sync_api import sync_playwright, ViewportSize
import time

def GetAuthToken(url):
    times = 0
    auth_code = Errors.BotError(Errors.ErrorType.UPLOAD_ERROR, "GetAuthToken")
    while True:
        try:
            times += 1
            with sync_playwright() as p:
                browser = p.firefox.launch()
                page = browser.new_page()
                page.set_viewport_size(ViewportSize(width = 1080*2, height=1920*2))

                page.goto(url)  #navigate to URL
                page.fill('input[type="email"]', c.GOOGLE_EMAIL)
                page.locator('text=Next').click()
                page.fill('input[type="password"]', c.GOOGLE_PASSWORD)
                page.locator('text=Next').click()
                time.sleep(2)
                page.locator('button').nth(2).click()
                page.locator('id=submit_approve_access').click()
                auth_code = page.locator("textarea").text_content()
                browser.close()
                break
        except Exception as e: 
            print(f"Tried {times} times")
            if times < c.MAX_GET_AUTH_TRIES: continue
            break

    return auth_code

def ScreenShotForLong(id, url):
    '''
    This function is called by main and uses the url passed by main.py to get screenshots of the post.
    this function is only called if "B" is passed to main and is written to get screenshots of long form posts
    without comments.
    '''
    
    with sync_playwright() as p:
        #launches chromium and sets screen size
        browser = p.firefox.launch()
        page = browser.new_page()
        page.set_viewport_size(ViewportSize(width = 1080*2, height=1920*2))
    
        page.goto(url)  #navigate to URL
        page.locator('[data-test-id="post-content"]').screenshot(path=(f"image_temp/{id}.png")) #gets title screenshot
    
        browser.close()

def ScreenShotForShort(id, url, comments_used):
    '''
    inputs given are the post id, url, and a list of comment ids to be used in the post
    This function is called if a value other then 'B' ('C') is passed to main.
    '''
    with sync_playwright() as p:
        #launches chromium and sets screen size
        browser = p.firefox.launch()
        page = browser.new_page()
        page.set_viewport_size(ViewportSize(width = 1080*2, height=1920*2))

        page.goto(url)  #navigate to URL

        time.sleep(3)

        #page.screenshot(path="a.png")
        page.locator('[data-test-id="post-content"]').screenshot(path=(f"image_temp/{id}.png")) #gets title screenshot
        #gets screenshots for comments
        for i in comments_used:
            instances = page.locator(f'.t1_{i}')    #finds instances of .t1_{comment_id}
            '''
            from the instances found in the previous step the second is screenshoted. The second instace is
            consistantly the desired comment. The reason this method of searching must be used instead of looking at
            ".comment" tags is beacuse it seems there is no way to defferentiate between parent and child comments
            through html code with the playwright module.
            '''
            instances.nth(1).screenshot(path=(f"image_temp/{id}_{i}.png"))
    
        browser.close()

def main(type, id, url, comments_used):
    '''
    Function is called from main.py determines whether to call ScreenShotForLong() or ScreenShotForShort()
    based on if "B" is passed or not
    '''
    if type == "B":
        ScreenShotForLong(id, url)
    else:
        ScreenShotForShort(id, url, comments_used)
#print(GetAuthToken('https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=760766942734-7b92qqmu8p6dpeb7hhfqb15batdp1sba.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.upload&state=aLvhK11JTVtOoXF9Wc4RILWsDnC1jY&prompt=consent&access_type=offline'))