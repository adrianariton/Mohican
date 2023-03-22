from color_sorting import get_colorcoeff
from scraper import get_heuristics
from colorfulness import get_category
PARSED_DATA=["background-color",
    "color",
    "secondary-color",
    "padding-top",
    "padding-left",
    "padding-right",
    "padding",
    "justify-content",
    "font-family",
    "border-radius",
    "float",
    "border-radius",
    "margin-top",
    "border-top",
    "font-weight"]

DEFAULTS = [
    'white',
    '#fff',
    '#FFF',
    '#FFFFFF',
    'inherit',
    'unset',
    '#ffffff',
    'transparent',
    '#000',
    '#000000',
    'black',
    'FontAwesome',
    'inherit !important',
    'currentColor'
]

TRANSPARENT = [

    'transparent',

    'inherit !important',
    'currentColor',
    'inherit'
]


card_col = {
    "display": "flex",
    "flex-direction": "column",
    "justify-content": "center"
}

card_row = {
    "display": "flex",
    "flex-direction": "row",
    "justify-content": "center"
}

card_none = {
    "overflow":"hidden",
    "justify-content": "center"
}

flags1 = ["simplistic", "big_logo"]
flags2 = ["simplistic"]
flags3 = ["s"]

def parse_features(url, ss):
    ft = get_heuristics(url)
    # print(ft)
    ret = {}
    color = []
    bgcolor = []
    for data in PARSED_DATA:
        if data in ft:
            dex = ft[data]
            k = list(dex.keys())
            if len(k) == 0:
                continue
            i = 1
            while i < len(k) and k[i] in DEFAULTS:
                i = i + 1
            if i >= len(k):
                i = len(k) - 1
            # print(f'{data}: {k[0]}, {k[i]}')
            
            e = k[i]
            if (i + 1) < len(k) and k[i + 1] not in DEFAULTS:
                e = k[i + 1]
            # ret[data] = {k[0], k[i], e}
            if data == 'background-color':
                bgcolor = k
                print(k)
            if data == 'color':
                color = k
                print(k)
            
            else:
                ret[data] = k[0]
    category = []
    if ss == 'on' or ss == True:
        category = get_category(url)

    for c in color:
        for g in bgcolor:
            if c!=g and c not in TRANSPARENT and g not in TRANSPARENT:
                ret['color'] = c
                ret['background-color'] = g
                print(c, g)
                if "simplistic" not in category:
                    return {'site':ret, 'card':card_col, 'flags': flags3}
                if category == "simplistic_none":
                    return {'site':ret, 'card':card_col, 'flags': flags2}
                return {'site':ret, 'card':card_col, 'flags': flags1}

    return {'site':ret, 'card':card_col, 'flags': flags3}


    

