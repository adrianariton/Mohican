/**
 * Frontend_script to be added inside page for it to scrape
 * color schemes
 * 
 */

document.addEventListener('DOMContentLoaded', () => {
    var queue = []
    var wanted = ['color', 'background-color']
    var dex = {'emp': 0}
    var body = document.querySelector('body');

    const st = getComputedStyle(body)
    console.log(st['background-color'])
    console.log(st)
    queue.push(body)


   
    // TODO: build tree that counts the number of all descendants once for a node
    // HOW-TO example: test_website_page.html
    var children_tree = [];
    queue = []
    queue.push(body)

    while(queue.length != 0) {
        var elem = queue[0];
        queue.pop();

        const st = getComputedStyle(elem)

        var children = elem.children;

        for (var i = 0 ; i < wanted.length; ++i) {
            if(`${wanted[i]}` in dex) {

                
                if (`${st[wanted[i]]}` in dex[wanted[i]]) {
                    dex[wanted[i]][st[`${wanted[i]}`]] += children.length + 1

                } else {
                    dex[wanted[i]][st[`${wanted[i]}`]] = children.length + 1

                }
                
            } else {

                dex[wanted[i]] = {};
                dex[wanted[i]][st[`${wanted[i]}`]] = children.length + 1

            }
        }

        for (var i = 0 ; i < children.length; ++i) {
            queue.push(children[i]);
        }
    }
    console.log("HEYA")
    console.log(dex)
})

