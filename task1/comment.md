Парсится страница [obrazovaka.ru](https://obrazovaka.ru/books). <br>
С помощью библиотеки `BeautifulSoup` достаются ссылки на страницы произведений.
На основе этих ссылок в методе `generate_index_file` генерируется файл `index.txt`. А дальше в методе `download_page` скачиваются страницы произведений.