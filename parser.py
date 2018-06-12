import urllib.request
import asyncio
import aiohttp
import os
import time
from random import randint
from html_parser import MyHTMLParser

URL = "https://news.ycombinator.com/"
PATCH = "/home/igor/mnt/tmp/"


def save_html(html):
	new_dir = PATCH + "/" + time.strftime("%Y%m%d-%H%M%S") + str(randint(0, 1000)) + "/"
	try:
		os.mkdir(new_dir)
	except Exception as e:
		print(e)
	else:
		path = os.path.join(new_dir, "index.html")
		with open(path, "w+") as index:
			index.write(html)


def get_url():
	parser = MyHTMLParser()
	with urllib.request.urlopen(URL) as response:
		parser.feed(response.read().decode('utf-8'))
	return parser.links


async def async_get_url(session, url):
	async with session.get(url) as response:
		return response.status, await response.text()


async def async_fetch(url):
	async with aiohttp.ClientSession() as session:
		try:
			status, html = await async_get_url(session, url)
		except Exception as e:
			return 500, e
		else:
			return status, html


async def make_tasks(urls):
	loop = asyncio.get_event_loop()
	tasks = [asyncio.ensure_future(async_fetch(url)) for url in urls]
	for i, task in enumerate(asyncio.as_completed(tasks)):
		status, html = await task
		if status == 200:
			loop.run_in_executor(None, save_html, html)


def main():
	links = get_url()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(make_tasks(links))
	loop.close()


if __name__ == '__main__':
	main()
