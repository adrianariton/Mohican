### Copyright Horia Mercan 


import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from lxml import etree
import re
import os
import multiprocessing as mp
import time
class Heuristics:
    def __init__(self, margins, border, height, width, outline, font):
        self.margins = margins
        self.border = border
        self.height = height
        self.width = width
        self.outline = outline
        self.font = font

def get_extension(url):
    return url.split(".")[-1].split("?")[0]

def get_themes_params(theme, css_file):
    text = "." + theme + '.*\{.*\}'
    result = re.search(text, css_file)
    print (text)
    print(result)
    # print("___________________________")
    if result != None:
        alpha = str(result)
        try:
            alpha = alpha.split('=')[-1]
            alpha = alpha.split("{")[1].split("}")[0]
        except Exception as e:
            return ""
        
        print(alpha)
        return alpha
    return ""

# beautiful soup parameter

# def DFS(pageElement):
#     elements = pageElement.find_all()

#     if len(elements) > 0:
#         for element in elements:
#             print(element.name)
#             print("----------------------")
#             DFS(element)

def findRegExInText():
    None

def getClasses(elements, css_files):
    
    
    css_dictionary = {}
    for css in css_files:
            r = requests.get(css, allow_redirects = True)
            print(str(r.content).replace("\\n", " "), file = open("response.txt", "a"))    # print(soup)


    dictionary = {}
    interes = ["width", "height", "bgcolor", "border", "text-color", "font-family", "text-align"
                , "outline-style", "background-color", "onclick", "margin-bottom", "border-radius"
                , "padding", "margin"]
    for element in elements:
        attributes = element.attrs
        for atr in attributes:
            atr = atr.strip(" ")
            if atr not in dictionary:
                dictionary[atr] = [element[atr]]
            else:
                dictionary[atr].append(element[atr])
    if "style" in dictionary:
        for description in dictionary["style"]:
            characteristics = description.split(";")
            for charact in characteristics:
                if ':' in charact:
                    name = charact.split(':')[0]
                    value = charact.split(':')[1]
                    name = name.strip(" ")
                    if name not in dictionary:
                        dictionary[name] = [value]
                    else:
                        dictionary[name].append(value)

    return dictionary["class"]

def getFrequency(class_array):
    frequency = {}
    for class_element in class_array:
        # print(class_element)
        for every_class in class_element:
            if not every_class in frequency:
                frequency[every_class] = 1
            else:
                frequency[every_class] += 1
    return frequency

def value_getter(item):
    return item[1]
def get_params_from_file(text):
    cmd = 'cat response.txt | grep -E -o "' + text +':[A-Z#()a-z0-9]*(}|;)" > ' + text + ".txt"
    # print(cmd)
    os.system(cmd)
    # time.sleep(0.1)
    file = open(text + ".txt", "r")
    dictionary = {}

    for line in file:
        line = line[:-2]
        # print(line)
        tupleLine = line.split(":")
        # print("HERE")
        # print(tupleLine)
        if tupleLine[1] in dictionary:
            dictionary[tupleLine[1]] += 1
        else:
            dictionary[tupleLine[1]] = 1

    # max_key = max(dictionary, key = dictionary.get)
    return sorted(dictionary.items(), key=value_getter, reverse = True)

def writeInFile(text, file):
    print(text, end = " = ", file = file)
    print(get_params_from_file(text), file = file)
    
def get_heuristics(url):
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    html = session.get(url).content

    soup = bs(html, "html.parser")

    # get the CSS files
    css_files = []

    for css in soup.find_all("link"):
        if css.attrs.get("href"):
            # if the link tag has the 'href' attribute
            css_url = urljoin(url, css.attrs.get("href"))
            if get_extension(css_url) == "css":
                # print(get_extension(css_url))
                css_files.append(css_url) 

    # print(css_files)
    elements = soup.find_all()

    class_array = list(getClasses(elements, css_files))
    
    # print(class_array)
    # print("--------------------------")
    # print(getFrequency(class_array))

    file = open("Heuristics.txt", "w")
    interes = ["width", "height", "bgcolor", "border", "text-color", "font-family", "text-align"
                , "outline-style", "background-color", "onclick", "padding", "border-radius"]
    
    # for one in interes:
    #     print(one)
        # file = open(one + ".txt", "r")
    print (mp.cpu_count())
    processes = []
    for one in interes:
        p = mp.Process(target = writeInFile, args =(one, file))
        processes.append(p)
        p.start()
        writeInFile(one, file)
    for p in processes:
        p.join()
        None
    
if __name__ == "__main__":
    
    get_heuristics("http://www.compjour.org/warmups/govt-text-releases/intro-to-bs4-lxml-parsing-wh-press-briefings/")
    # print(get_params_from_file("text-align"))
    