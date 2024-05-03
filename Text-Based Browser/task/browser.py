#import typing
import os
import sys
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

class Browser:
    def __init__(self, storagePath):
        self.storagePath = storagePath
        self.history = deque()

    def mainInterface(self):
        self.createStorage(self.storagePath)
        while True:  # do-while
            now = input()
            if now == 'exit':
                break
            elif now == 'back':
                if len(self.history) >= 2: self.browse(self.history[-2]) # prints the content of the prev article
            else:
                self.browse(now)

    def browse(self, url: str):
        modified_url = url.strip()
        if modified_url.find('http') == -1:
            modified_url = 'https://'+modified_url
        if self.checkURL(modified_url):
            try:
                response = requests.get(modified_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a') # !note: find_all returnes links to the elements, not copies
                for link in links:
                    if link.string is not None:
                        link.string.replace_with(Fore.BLUE + str(link.string) + Style.RESET_ALL)
                    else:
                        pass
                    # print(link)
                text_content = soup.get_text()
                print(text_content)
                self.saveToStorage(modified_url, text_content) # url with no https://
                self.history.append(modified_url)
            except KeyError:
                print('Invalid URL')
        else:
            print("Invalid URL")

    def saveToStorage(self, url: str, response: str):
        articlesPath = url[:url.find('.')]
        articlesPath = articlesPath.replace('https://', '')
        file_path = os.path.join(self.storagePath, articlesPath)
        with open(file_path, 'w', encoding='utf-8') as m_storage:
            m_storage.write(response)

    def createStorage(self, path: str):
        self.path = path
        if not os.access(self.path, os.F_OK):
            os.mkdir(self.path)
        else:
            pass

    def checkURL(self, url: str):
        if url.find('.') >= 0 and url[-1] != '.':
            return True
        else:
            return False

# todo: highlight all the links in output text with blue color (Fore.BLUE)
# links start with <a> tag
def main():
    storagePath = sys.argv[1] # check if it's fine
    browser = Browser(storagePath)
    browser.mainInterface()

if __name__ == "__main__":
    main()