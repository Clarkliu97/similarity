import pandas as pd
import base64

def main():
    authors = ['Peicheng']
    write_to_html(authors)


def write_to_html(authors): 
    author = "Author: "
    for i in authors:
        author += i + ", "
    author = author[:-2]

    author_tag = "<p>Author: " + author + "</p>"

    table = pd.read_csv('Output\Ginger_Error_Stats.csv')
    table.to_html('Output\Ginger_Error_Stats.html')

    table_html = table.to_html()

    img = base64.b64encode(open('Output\Ginger_Error_Stats.png', 'rb').read()).decode('utf-8')
    img_tag = '<img src="data:image/png;base64,{0}">'.format(img)
    print(img_tag)

    html = author_tag + table_html + img_tag
    with open('Output\Ginger_Error_Stats.html', 'w') as f:
        f.write(html)
        f.close()


if __name__ == '__main__':
    main()