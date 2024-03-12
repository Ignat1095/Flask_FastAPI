"""Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое
изображение должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg — Программа должна использовать
многопоточный, многопроцессорный и асинхронный подходы. — Программа должна иметь возможность задавать список
URL-адресов через аргументы командной строки. — Программа должна выводить в консоль информацию о времени скачивания
каждого изображения и общем времени выполнения программы. """

import os
from pathlib import Path
import requests
import time
import argparse
import threading
from multiprocessing import Process
import asyncio
import aiohttp

images = []
with open('./images.txt') as file:
    for image in file.readlines():
        images.append(image.strip())

PATH = Path('images')


def download_img(url, dir_path=PATH):
    start_time = time.time()
    response = requests.get(url)
    filename = url.split('/')[-1]
    with open(os.path.join(dir_path, filename), 'wb') as f:
        for data in response.iter_content(1024):
            f.write(data)
    end_time = time.time() - start_time
    print(f'Загрузка {filename} заняла {end_time:.2f} сек')


def parse():
    parser = argparse.ArgumentParser(description='Парсер изображений по URL-адресам')
    parser.add_argument('-u', '--urls', default=images, nargs='+', type=str, help='Список URL-адресов')
    return parser.parse_args()


async def download_img_as(url, dir_path=PATH):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            item = await response.read()
            filename = url.split('/')[-1]
            with open(os.path.join(dir_path, filename), 'wb') as f:
                f.write(item)
    end_time = time.time() - start_time
    print(f'Загрузка {filename} заняла {end_time:.2f} сек')


def download_img_thread(urls):
    threads = []
    start_time = time.time()

    for url in urls:
        thread = threading.Thread(target=download_img, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time() - start_time
    print(f'{"-"*7}> Общее время: {end_time:.2f} сек')


def download_img_process(url):
    processes = []
    start_time = time.time()

    for url in urls:
        process = Process(target=download_img, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time() - start_time
    print(f'{"-"*7}> Общее время: {end_time:.2f} сек')


async def download_img_async(urls):
    tasks = []
    start_time = time.time()

    for url in urls:
        task = asyncio.create_task(download_img_as(url))
        tasks.append(task)

    await asyncio.gather(*tasks)

    end_time = time.time() - start_time
    print(f'{"-"*7}> Общее время: {end_time:.2f} сек')


if __name__ == '__main__':
    urls = parse().urls

    if not os.path.exists(PATH):
        os.mkdir(PATH)

    print(f"{len(urls)} фото")

    print(f'\n\n-> Многопоточный подход'
          f'\n {"_" * 30}')
    download_img_thread(urls)

    print(f'\n\n-> Многопроцессорный подход'
          f'\n {"_" * 30}')
    download_img_process(urls)

    print(f'\n\n-> Асинхронный подход'
          f'\n {"_" * 30}')
    asyncio.run(download_img_async(urls))
