import json

attr_LIGHT= {
    "background-color": "white",
    "color": "black", 
    "border-radius": "25px",
    "margin": "0px",
    "float": "center",
    "font": "Arial",
    "padding": "10px",
    "justify-content": "center"
}

attr_DARK = {
    "background-color": "black",
    "color": "white", 
    "border-radius": "25px",
    "margin": "0px",
    "float": "center",
    "font-family": "Arial",
    "padding": "10px",
    "justify-content": "center"
}

attr_APPLE_DARK = {
    "background-color": "#080808",
    "color": "white", 
    "border-radius": "25px",
    "margin": "0px",
    "float": "center",
    "font-family": "Cursive",
    "padding": "10px",
    "justify-content": "right",
}

attr_LEFT = {
    "background-color": "white",
    "color": "black", 
    "border-radius": "25px",
    "margin": "0px",
    "float": "center",
    "font-family": "Arial",
    "padding": "10px",
    "justify-content": "left"
}

attr_REDDIT = {
    "background-color": "#FFFFFF",
    "padding-top": "0px",
    "padding-left": "0px",
    "padding-right": "0px",
    "border": "1px solid rgb(137, 137, 137)",
    "font-family": "IBMPlexSans, Arial, sans-serif",
    "border-radius": "2px",
    "justify-content": "right"
}

attr_SLIDE1 = {
    "background-color": "#FFFFFF",
    "padding-top": "0px",
    "padding-left": "0px",
    "padding-right": "0px",
    "padding": "5px",
    "border": "4px solid rgb(0, 0, 0)",
    "font-family": "IBMPlexSans, Arial, sans-serif",
    "border-radius": "2px",
    "float": "center",
    
    "display": "flex",
    "flex-direction": "column"

}

attr_SLIDE2 = {
    "background-color": "#000000aa",
    "color": "white",
    "secondary-color": "rgb(189, 161, 255)",
    "padding-top": "0px",
    "padding-left": "0px",
    "padding-right": "0px",
    "padding": "15px",
    "justify-content": "center",
    "font-family": "IBMPlexSans, Arial, sans-serif",
    "border-radius": "2px",
    "float": "center",
    "border-radius": "25px"
}

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


slide1 = {"site": attr_SLIDE1, "card": card_col, "flags": flags1}
slide2 = {"site": attr_SLIDE2, "card": card_col, "flags": flags2}
reddit = {"site": attr_REDDIT, "card": card_col, "flags": flags3}
apple_dark = {"site": attr_APPLE_DARK, "card": card_col, "flags": flags2}
def dump(data):
    # change this and reload server
    # next: TODO: requests from fontend
    y = json.dumps(data)
    print(y , file=open('attr.json', 'w'))
if __name__ == '__main__':
    dump(apple_dark)
