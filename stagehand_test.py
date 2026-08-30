import asyncio

from pydantic import BaseModel
from stagehand_test import Stagehand, local_browser


class Story(BaseModel):
    title: str
    points: int


class Stories(BaseModel):
    stories: list[Story]


async def main() -> None:
    browser = await local_browser.launch()
    sh = await Stagehand.create(browser=browser)

    page = await browser.context.active_page()
    if page is None:
        raise RuntimeError("Stagehand initialized without an active page")

    await page.goto("https://news.ycombinator.com")

    result = await sh.extract(
        "Extract the top 5 stories",
        Stories,
    )

    print(result.data.stories)

    await sh.close()
    await browser.close()


asyncio.run(main())