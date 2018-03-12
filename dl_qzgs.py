from ebooklib import epub
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

uks_root = 'https://www.uukanshu.com'

options = Options()
options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=options)
browser.get('https://www.uukanshu.com/b/167/')

soup = BeautifulSoup(browser.page_source, 'lxml')
chapter_div = soup.find(id='chapterList')
chapter_links = [a['href'] for a in chapter_div.find_all('a')][::-1]

book = epub.EpubBook()
book.set_identifier('0922ce20-24fa-11e8-b566-0800200c9a66')
book.set_title('全职高手')
book.add_author('蝴蝶蓝')
book.set_language('zh')

chapters = []

with open('rejects.txt', 'w') as rejects:

    i = 0
    while i < len(chapter_links):
        link = chapter_links[i]
        try:
            time.sleep(5)
            browser.get(uks_root + link)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            title = soup.find(id='timu').string
            content = soup.find(id='contentbox')
            ads = content.find_all(class_='ad_content')
            [a.decompose() for a in ads]
            text = str(content)

            pos = text.find('UU看书')
            if pos < 0:
                pos = text.find('UＵ看书')
            if pos < 0:
                pos = text.find('ＵU看书')
            if pos < 0:
                pos = text.find('ＵＵ看书')

            length = 22
            if text[pos + 21] == '\n':
                length = 21
            while ord(text[pos + length - 1]) > 127:
                length -= 1

            rejects.write(title + ': ' + text[pos:pos + length] + '\n')

            with open('txt/' + title + '.txt', 'w') as f:
                f.write(text)

            chapter = epub.EpubHtml(title=title, file_name=title+'.xhtml', lang='zh')
            chapter.content = '<center><h3>' + title + '</h3></center>' + text[:pos] + text[pos + length:]

            book.add_item(chapter)
            chapters.append(chapter)
        except:
            browser.quit()
            browser = webdriver.Chrome(chrome_options=options)
            continue
        i += 1
        print(str(i) + ' / ' + str(len(chapter_links)))

browser.quit()

book.toc = (tuple([c.title for c in chapters]))
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
book.spine = chapters

epub.write_epub('quanzhigaoshou.epub', book, {})
