# Assembles add-parts 
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import json as JSON
from PIL import Image
from colorthief import ColorThief
from collections import Counter
import math
from simplicity import parse_features

url1 = "http://pbinfo.ro"
url2 = 'https://lsacbucuresti.ro/'
url3 = "https://www.innovationlabs.ro/"
url4 = "https://www.celticfc.com/"
url5 = "https://www.yahoo.com/?guccounter=1"
url6 = "https://regex101.com/"

SITE_URL =  url3

EMPTY_STYLE = {}
FREEDOM = "__freedom__"
TEXT_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'a', 'p', 'span', 'ul', 'li']
EMBEDED_TAGS = ['img', 'embeded']
CONTAINER_TAGS = ['div']
SMALLCINTAINER_TAGS = ['button']

NEED_DEFINING = ['background-color']
EMBEDED_STYLE = ['border-radius']
TEXT_STYLE = ['float' ,'color', 'font', 'font-family', 'font-weight', 'font-size', 'margin', 'margin-right', 'margin-left', 'margin-top', 'margin-bottom']

CONTAINER_STYLE = ['border-radius' ,'justify-content', 'align-items', 'flex-direction', 'background-color', 'background', 'display']
EINZELKIND_CONTAINER_STYLE = ['border-radius', 'margin-right', 'margin-left', 'margin-top', 'margin-bottom']
GRANDPA_STYLE = ['border', 'padding', 'padding-left', 'padding-right', 'padding-top', 'padding-bottom', 'margin']
def siblings(elem):
    h = []
    for element in elem.next_siblings:
        h = h + [element]
    for element in elem.previous_siblings:
        h = h + [element]
    return h

def is_einzelkind(elem):
    if not elem.parent or elem.parent == elem:
        return True
    return len(siblings(elem)) == 0

class Image:
    def __init__(self, content, style=EMPTY_STYLE, type=0):
        self.content = content
        self.style = style
        self.type = type
        
    def lightness(self):
        im = Image.open(self.content)
        width, height = im.size

        color_thief = ColorThief(self.content)
        # get the dominant color
        dominant_color = color_thief.get_color(quality=1)
        # build a color palette
        palette = color_thief.get_palette(color_count=6)
        print(palette)



        colortuples = Counter(im.getdata())   # dict: color -> number

        pix = im.load()
        sum = 0
        for x in range(0, width):
            for y in range(0, height):
                sum += pix[x, y][0] + pix[x, y][1] + pix[x, y][2]
        
        dev = 0
        mean = sum / (width * height * 3)
        for x in range(0, width):
            for y in range(0, height):
                dev += (pix[x, y][0] + pix[x, y][1] + pix[x, y][2] - mean) ** 2
        
        return mean, math.sqrt(dev/(width * height * 3 - 1))
                

class Text:
    def __init__(self, content, style=EMPTY_STYLE, type='span', color='primary'):
        self.content = content
        self.style = style
        self.type = type
        self.color = color

class Raw:
    def __init__(self, content):
        self.content = content
       
# Default div for style_scraping will be body 
class WebDiv:
    def __init__(self, style, depth):
        self.style = style
        self.depth = depth

    
class Advertisment:
    '''
        Title: company title
        Parts: dictionary
    '''
    def __init__(self, title, parts, html, rigidity):
        self.title = title
        self.parts = parts
        self.rigidity = rigidity
        self.html = html
    
    def assemble(self, json=None, features=None):
        if json == None:
            site_features = features
        else:
            site_features = JSON.loads(json)
        keys = list(self.parts.keys())
        
        card_features = site_features['card']
        flags = site_features['flags']

        site_features = site_features['site']
        
        print(site_features)

        final = self.html
        
        for key in keys:
            val = self.parts[key]

            keystr = f'$${key}$$'
            
            if type(val) is Image:
                style = ""
                for key, value in val.style.items():
                    style = style + f'{key}:{val.style[key]}  !important;'
                if 'simplistic' in flags:
                    print('simple')
                if 'simplistic' in flags and val.type != 'logo':
                    style = style + 'display: none;'
                if 'big_logo' in flags and val.type == 'logo':
                    style = style + 'height: 150px !important; width: auto !important;'
                final = final.replace(keystr, f"<img data-mohican='true' src='{val.content}' style='{style}'>")
            if type(val) is Text:
                style = ""
                for key, value in val.style.items():
                    style = style + f'{key}:{val.style[key]} !important;'
                if keystr == '$$motto$$' and "secondary-color" in site_features:
                    style = style + f'color:{site_features["secondary-color"]} !important;'
                    
                final = final.replace(keystr, f"<{val.type} data-mohican='true' style='padding: 0; margin: 0; {style}'>{val.content}</{val.type}>")
            if type(val) is Raw:
                final = final.replace(keystr, f"'{val.content}'")

        soup = bs(final, "html.parser")
        markup = bs(final, "html.parser")
        
        taglist = markup.find_all()
        
        for elem in taglist:
            if elem.parent == None or elem.parent == elem or str(elem.parent).strip() == str(elem).strip():
                # print(f"parent: {elem}")
                for key_, value_ in card_features.items():
                    if elem.has_attr('style'):
                        elem['style'] = elem['style'] + f'; {key_}: {value_} !important;'
                        elem['style'] += f'; overflow: hidden !important;'
                for key_, value_ in site_features.items():
                    if elem.has_attr('style'):
                        elem['style'] = elem['style'] + f'; {key_}: {value_} !important;'
                        elem['style'] += f'; overflow: hidden !important;'
                        
     
            if (elem.has_attr('data-mohican') and elem['data-mohican'] == 'true'):
                while elem:
                    st = ""
                    if(elem.has_attr('style')):
                        st = elem['style']
                    
                    while str(st).count("$$$") > 0:
                        dd = st.split("$$$")
                        half = dd[1]
                        
                        m_attr = dd[1].split(":")[0]
                        m_val = dd[1].split(":")[1]
                        
                        if m_attr in site_features:
                            st.replace(f'{m_attr}: {m_val};', f'{m_attr}: {site_features[m_attr]};')
                    
                    for key_, value_ in site_features.items():
                        
                        
                        if is_einzelkind(elem) and elem.name in CONTAINER_TAGS:
                            #print("Einz!")
                            if str(key_) in EINZELKIND_CONTAINER_STYLE:
                                #print("Cont!")

                                elem['style'] = elem['style'] + f'; {key_}: {value_} !important;'
                                elem['style'] += f'; overflow: hidden !important;'

                            
                        # Chack if attr needs defining
                        sw = 0
                        if str(key_) in NEED_DEFINING:
                            #print(f"def!")
                            if elem.has_attr('style'):
                                if str(elem['style']).count(str(key_)) > 0:
                                    #print(f"{str(elem['style'])} found!")
                                    sw = 1
                        else:
                            sw = 1
                        if sw == 0:
                            continue
                        
                        elif elem.has_attr('style'):
                                
                            if elem.name in TEXT_TAGS and str(key_) in TEXT_STYLE:
                                elem['style'] =  f'; {key_}: {value_} !important;;' + elem['style']
                                elem['style'] = elem['style'] + f'; margin-left: 5px'
                            if elem.name in EMBEDED_TAGS and str(key_) in EMBEDED_STYLE:
                                elem['style'] = elem['style'] + f'; {key_}: {value_} !important;;'
                            if elem.name in CONTAINER_TAGS and str(key_) in CONTAINER_STYLE:
                                elem['style'] = elem['style'] + f'; {key_}: {value_} !important;;'
                    elem = elem.parent
        final = str(markup)
        
        return final
            

from test_scraper import dump

def run_mohican():
    parts = {
        "head": Text(content="Mohican", style=EMPTY_STYLE, type='h1'),
        "img" : Image(content="static/mohican.png", style={"width": "auto", "height": "70px", "padding": "10px"}, type='logo'),
        "motto": Text("flawless ads .", style={"font-family": "cursive"}, type='h2'),
        "bcg" : Raw(content='https://forum.zorin.com/uploads/default/original/2X/7/7fee1cd44a7b3f949550bd4d57a10a3946468a60.jpeg'),
        "bcgimg" : Image(content='https://forum.zorin.com/uploads/default/original/2X/7/7fee1cd44a7b3f949550bd4d57a10a3946468a60.jpeg')
    }

    ad_file = 'adslide1.html'

    ad = Advertisment(title='Randomadd', parts=parts, rigidity=0, html=open(f'{ad_file}', 'r').read())

    
    # Alter HTML file to see the changes done
    # Read in the file
    with open('adver.html', 'r') as file :
        filedata = file.read()

    dump()
    features = open('attr.json', 'r').read()
    # ft = parse_features(SITE_URL)
    # print(ft)
    # Replace the target string
    # testing
    filedata = filedata.replace('@@', ad.assemble(json=features))

    # Write the file out again
    with open('adver.html', 'w') as file:
        file.write(filedata)


run_mohican()
