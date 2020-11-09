import asyncio
import time
from pyppeteer import launch


async def screenshot(url, js, path):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    time.sleep(10)
    if js:
        for script in js:
            await page.evaluate(script)
    await page.screenshot({'path': path})

    await browser.close()

def main():
    # os.system("webkit2png https://www.geoguessr.com/game/eX1OXKEPFA1sG9me "
    #           "--selector=.game-layout__panorama "
    #           "--delay=10 "
    #           "--js='document.querySelector('.game-layout__controls').remove();'")

    # url = "https://www.geoguessr.com/game/eX1OXKEPFA1sG9me"
    url = "https://www.google.com/maps/@35.0955185,-89.7506739,3a,75y,267h,83.59t/data=!3m7!1e1!3m5!1sZHBhGVcp6tN8AcsHnh4oLw!2e0!6s%2F%2Fgeo2.ggpht.com%2Fcbk%3Fpanoid%3DZHBhGVcp6tN8AcsHnh4oLw%26output%3Dthumbnail%26cb_client%3Dsearch.revgeo_and_fetch.gps%26thumb%3D2%26w%3D96%26h%3D64%26yaw%3D38.664722%26pitch%3D0%26thumbfov%3D100!7i13312!8i6656"
    # script = ["document.querySelector('.game-layout__controls').remove();",
    #           "document.querySelector('.layout__header').remove();",
    #           "document.querySelector('.game-layout__status').remove();",
    #           "document.querySelector('.game-layout').style.paddingTop = 0"]
    script = None
    path = "example1.png"

    asyncio.get_event_loop().run_until_complete(
        screenshot(url, script, path)
    )


    return 0


if __name__ == "__main__":
    main()