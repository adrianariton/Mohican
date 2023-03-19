### Copyright Horia Mercan 


import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import re
import os
import multiprocessing as mp
from PIL import Image

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
    # print (text)
    # print(result)
    # print("___________________________")
    if result != None:
        alpha = str(result)
        try:
            alpha = alpha.split('=')[-1]
            alpha = alpha.split("{")[1].split("}")[0]
        except Exception as e:
            return ""
        
        # print(alpha)
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
    # print(elements)
    if elements == None:
        print("eu", file = open("response.txt", "w"))
        return None
        
    css_dictionary = {}
    for css in css_files:
            r = requests.get(css, allow_redirects = True)
            # open("response.txt", "a")
            # os.system("rm response.txt")
            
            print(str(r.content).replace("\\n", " "), file = open("response.txt", "a"))    # print(soup)


    dictionary = {}
    # interes = ["width", "height", "bgcolor", "border", "text-color", "font-family", "text-align"
    #             , "outline-style", "background-color", "onclick", "margin-bottom", "border-radius"
    #             , "padding", "margin", "color"]
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

    return dictionary["class"] if "class" in dictionary else None

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
def get_params_from_file(text, dict_final):
    cmd = 'cat response.txt | grep -E -o "' + text +':[A-Z#()a-z0-9]*(}|;)" > ' + text + ".txt"
    print(cmd)
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
    new_dict = dict(sorted(dictionary.items(), key=value_getter, reverse = True))
    # print (text, end = " : ");print(new_dict)
    dict_final.append(
        {"attribute" : text,
         "objects" : new_dict}
    )

    cmdRm = "rm " + text + ".txt"
    # os.system(cmdRm)
    return new_dict

def writeInFile(text, file, dict_final):
    print(text, end = " = ", file = file)
    print(get_params_from_file(text = text, dict_final= dict_final), file = file)
    
def get_heuristics(url):
    fileToClose = open("response.txt", "w")
    print("\n", file = fileToClose)
    fileToClose.flush()
    fileToClose.close()
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    html = session.get(url).content

    soup = bs(html, "html.parser")
    print(html, file = open("html.txt", "w"))
    # get the CSS files
    css_files = []
    img_files = []
    for css in soup.find_all("link"):
        if css.attrs.get("href"):
            # if the link tag has the 'href' attribute
            css_url = urljoin(url, css.attrs.get("href"))
            if get_extension(css_url) == "css":
                # print(get_extension(css_url))
                css_files.append(css_url)
            elif get_extension(css_url) in ["png", "jpeg", "ico", "jpeg"]:
                img_files.append(css_url)

    print("css_files", end = " : "); print(css_files)
    print("img_files", end = " : "); print(img_files)
    elements = soup.find_all()
    aux = getClasses(elements, css_files)
    # aux_html = getCla
    class_array = (list(getClasses(elements, css_files)) if not aux == None else [])
    # print(css_files)
    # print(class_array)
    # print("--------------------------")
    print(getFrequency(class_array))

    file = open("Heuristics.txt", "a")
    interes = ["width", "height", "bgcolor", "border", "text-color", "font-family", "text-align"
                , "outline-style", "background-color", "onclick", "padding", "border-radius",
                "color", "text-color"]
    
    # for one in interes:
    #     print(one)
        # file = open(one + ".txt", "r")
    print (mp.cpu_count())
    dict_final = mp.Manager().list()
    processes = []
    for one in interes:
        p = mp.Process(target = writeInFile, args =(one, file, dict_final))
        p.start()
        processes.append(p)
        
        # writeInFile(one, file, dict_final)
    for p in processes:
        p.join()
        
        None
    # args = []
    # for elem in interes:
    #     args.append(tuple([elem, file, dict_final]))
    # with mp.Pool() as pool:
    #     map_result = pool.starmap_async(writeInFile, args)
    #     result = map_result.get(timeout = 0.3)
    items = {}
    for key in dict_final : 
        items[key["attribute"]] = key["objects"]
    # print(items)

    interes.append("Heuristics")
    for one in interes:
        print("\n", file = open(one + ".txt" , "w"))


    return items

''' 
if __name__ == "__main__":
    url1 = "http://www.compjour.org/warmups/govt-text-releases/intro-to-bs4-lxml-parsing-wh-press-briefings/"
    url2 = "https://pbinfo.ro"
    url3 = "https://www.geeksforgeeks.org/python-split-dictionary-keys-and-values-into-separate-lists/"
    url4 = "https://github.com/"
    url5 = "https://www.innovationlabs.ro/"
    url6 = "https://eestec.ro"
    url7 = "https://www.hrs-bg.com/"
    url8 = "https://www.vodafone.ro/"
    print(get_heuristics(url8))

'''
if __name__ == "__main__":

    url1 = "http://www.compjour.org/warmups/govt-text-releases/intro-to-bs4-lxml-parsing-wh-press-briefings/"
    url2 = "https://pbinfo.ro"
    url3 = "https://www.geeksforgeeks.org/python-split-dictionary-keys-and-values-into-separate-lists/"
    url4 = "https://github.com/"
    url5 = "https://www.innovationlabs.ro/"
    url6 = "https://eestec.ro"
    url7 = "https://www.hrs-bg.com/"
    url8 = "https://www.vodafone.ro/"
    url9 = "https://pizzahut.ro"
    print(get_heuristics(url9))