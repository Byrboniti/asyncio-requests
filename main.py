import datetime
import json
import time
from bs4 import BeautifulSoup
import csv
# import requests
import asyncio
import aiohttp

books_data_list = []
start_time = time.time()


async def get_page_data(session, page):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    url = f"https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page={page}"

    async with session.get(url=url, headers=header) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, "lxml")

        books_items = soup.find("tbody", class_="products-table__body").find_all("tr")

        for items in books_items:
            book_data = items.find_all("td")
            try:
                book_title = book_data[0].find("a").text.strip()
            except:
                book_title = "Net_nazvaniya"
            try:
                book_author = book_data[1].find("a").text.strip()
            except:
                book_author = "net_author"
            try:
                # book_publishing = book!!!!!s_data[2].find("a").text.strip()
                book_publishing = book_data[2].find_all("a")

                book_publishing = ":".join([bp.text for bp in book_publishing])
            except:
                book_publishing = "net_publishing"
            try:
                book_new_price = int(book_data[3].find("div", class_="price").find("span").find("span"
                                                                                                ).text.strip().replace(
                    " ", ""))
            except:
                book_new_price = "No_new_price"
            try:
                book_old_price = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))
            except:
                book_old_price = "no_old_price"

            try:
                book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)
            except:
                book_sale = "no_sale"
            try:
                book_status = book_data[-1].text.strip()
            except:
                book_status = "net_statusa"

            books_data_list.append(
                {
                    "book_title": book_title,
                    "book_author": book_author,
                    "book_publishing": book_publishing,
                    "book_new_price": book_new_price,
                    "book_old_price": book_old_price,
                    "book_sale": book_sale,
                    "book_status": book_status
                }
            )
        print(f" Complit {page}")


async def gather_data():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    url = "https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table"
    async with aiohttp.ClientSession() as session:
        tasks = []
        response = await session.get(url=url, headers=header)

        soup = BeautifulSoup(await response.text(), "lxml")
        pages_count = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(gather_data())
    cur_time = datetime.datetime.now().strftime("%d_%M_%Y_%H_%M")

    with open(f"labirint_{cur_time}.json", "w", encoding="utf-8") as file:
        json.dump(books_data_list, file, indent=4, ensure_ascii=False)

    with open(f"labirint_{cur_time}_asyncio.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Title",
                "Author",
                "Publisher",
                "Prise with sale",
                "Prise without sale",
                "Sale percent",
                "Store availability"
            )
        )
    for book in books_data_list:
        with open(f"labirint_{cur_time}_asyncio.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    book["book_title"],
                    book["book_author"],
                    book["book_publishing"],
                    book["book_new_price"],
                    book["book_old_price"],
                    book["book_sale"],
                    book["book_status"]
                )
            )
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")


if __name__ == '__main__':
    main()

# start_time = time.time()
#
#
# def get_data():
#     cur_time = datetime.datetime.now().strftime("%d_%M_%Y_%H_%M")
#     with open(f"labirint_{cur_time}.csv", "w", encoding="utf-8") as file:
#         writer = csv.writer(file)
#         writer.writerow(
#             (
#                 "Title",
#                 "Author",
#                 "Publisher",
#                 "Prise with sale",
#                 "Prise without sale",
#                 "Sale percent",
#                 "Store availability"
#             )
#         )
#     books_data = []
#     header = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
#     }
#     url = "https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table"
#     response = requests.get(url=url, headers=header)
#     soup = BeautifulSoup(response.text, "lxml")
#     pages_count = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)
#
#     for page in range(1, pages_count + 1):
#         url = f"https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page={page}"
#
#         response = requests.get(url=url, headers=header)
#
#         soup = BeautifulSoup(response.text, "lxml")
#         books_items = soup.find("tbody", class_="products-table__body").find_all("tr")
#         for items in books_items:
#             book_data = items.find_all("td")
#             try:
#                 book_title = book_data[0].find("a").text.strip()
#             except:
#                 book_title = "Net_nazvaniya"
#             try:
#                 book_author = book_data[1].find("a").text.strip()
#             except:
#                 book_author = "net_author"
#             try:
#                 # book_publishing = book!!!!!s_data[2].find("a").text.strip()
#                 book_publishing = book_data[2].find_all("a")
#
#                 book_publishing = ":".join([bp.text for bp in book_publishing])
#             except:
#                 book_publishing = "net_publishing"
#             try:
#                 book_new_price = int(book_data[3].find("div", class_="price").find("span").find("span"
#                                                                                                 ).text.strip().replace(
#                     " ", ""))
#             except:
#                 book_new_price = "No_new_price"
#             try:
#                 book_old_price = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))
#             except:
#                 book_old_price = "no_old_price"
#
#             try:
#                 book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)
#             except:
#                 book_sale = "no_sale"
#             try:
#                 book_status = book_data[-1].text.strip()
#             except:
#                 book_status = "net_statusa"
#             # print(book_title)
#             # print(book_author)
#             # print(book_publishing)
#             # print(book_new_price)
#             # print(book_old_price)
#             # print(book_sale)
#             # print(book_status)
#             # print("#"* 10)
#             books_data.append(
#                 {
#                     "book_title": book_title,
#                     "book_author": book_author,
#                     "book_publishing": book_publishing,
#                     "book_new_price": book_new_price,
#                     "book_old_price": book_old_price,
#                     "book_sale": book_sale,
#                     "book_status": book_status
#                 }
#             )
#             with open(f"labirint_{cur_time}.csv", "a", encoding="utf-8") as file:
#                 writer = csv.writer(file)
#                 writer.writerow(
#                     (
#                         book_title,
#                         book_author,
#                         book_publishing,
#                         book_new_price,
#                         book_old_price,
#                         book_sale,
#                         book_status
#                     )
#                 )
#         print(f"Ending {page}/{pages_count}")
#         time.sleep(1)
#
#     with open(f"labirint_{cur_time}.json", "w", encoding="utf-8") as file:
#         json.dump(books_data, file, indent=4, ensure_ascii=False)
#
#
# def main():
#     get_data()
#     finish_time = time.time() - start_time
#     print(f"spent{finish_time}")
#
#
# if __name__ == '__main__':
#     main()
