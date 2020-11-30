import os
import re
import pyhtml
from .html_builder_data import regex_parsing_list as rplist
from .html_builder_data import stylesheet, stylesheet_mobile



######## FUNCTIONS ########################################
def regex_parser(line):
    for regex in rplist:
        hr = ''
        m = re.match(regex[0], line)
        if m:
            if re.match('^hr_.*', regex[1]):
                hr = 'pre'
            if re.match('.*_hr$', regex[1]):
                hr = 'post'

            if re.match(r'.*match\[0\].*', regex[1]):
                return (m[0], regex[2], hr)
            if re.match(r'.*match\[1\].*', regex[1]):
                return (m[1], regex[2], hr)
            # more regex options here

    return '', {'tag': 'p'}, None


def generate_html_element(tag='p', text=None, div=False, div_style=None, **attibutes):
    html_element = None
    html_tag = getattr(pyhtml, tag)

    if attibutes:
        html_tag = html_tag(**attibutes)

    if text or tag == 'p': 
        html_tag = html_tag(text.strip())

    if div:
        div_tag = getattr(pyhtml, 'div')
        if div_style:
            div_tag = div_tag(class_=div_style)
        html_element = div_tag(html_tag)

    if not html_element:
        html_element = html_tag

    return html_element


def append_body_part(part, body_parts):
    html_element = None

    if isinstance(part, str):
        if len(part.strip()) > 0:
            html_element = generate_html_element(
                tag='p',
                text=part,
                div=True
            )
    else:
        html_element = generate_html_element(
            text=part[0],
            **part[1]
        )

    if html_element:
        body_parts.append(html_element)

    return body_parts


def generate_html_body(input_file_path):
    body_parts = [pyhtml.br]
    current_part = ''
    empty_lines_count = 0

    with open(input_file_path, 'r', encoding='utf-8') as book:
        for line in book:
            if len(current_part.strip()) == 0:
                current_part = line
                continue

            parsed_element = regex_parser(current_part)
            if len(parsed_element[0]) > 0:
                empty_lines_count = 0
                if parsed_element[1].get('tag'):
                    if parsed_element[2] == 'pre':
                        body_parts.append(pyhtml.hr)
                    body_parts = append_body_part(parsed_element, body_parts)
                    if parsed_element[2] == 'post':
                        body_parts.append(pyhtml.hr)
                    current_part = ''
                else:
                    current_part += parsed_element[0]

            if len(line.strip()) == 0:
                empty_lines_count += 1
                continue

            if empty_lines_count > 0:
                parsed_element = regex_parser(line)
                if len(parsed_element[0]) > 0:
                    empty_lines_count = 0
                    if parsed_element[1].get('tag'):
                        body_parts = append_body_part(current_part, body_parts)
                        if parsed_element[2] == 'pre':
                            body_parts.append(pyhtml.hr)
                        body_parts = append_body_part(parsed_element, body_parts)
                        if parsed_element[2] == 'post':
                            body_parts.append(pyhtml.hr)
                        current_part = ''
                    else:
                        current_part += parsed_element[0]
                    continue

                current_part = current_part.replace('\n','') + line
                empty_lines_count = 0
                continue

            body_parts = append_body_part(current_part.replace('\n',''), body_parts)
            current_part = line

    body_parts = append_body_part(current_part.replace('\n',''), body_parts)

    body = pyhtml.body(body_parts)
    return body


def generate_html_head(title, stylesheet):
    head = pyhtml.head(
        pyhtml.title(title),
        pyhtml.style(stylesheet)
    )
    return head


def dump_html(html, input_file_path, mobile=False):
    output_file_split = os.path.split(input_file_path)
    
    if mobile:
        out_file = output_file_split[1].replace('.txt','') + ' (mobile).html'
    else:
        out_file = output_file_split[1].replace('.txt','') + '.html'

    out_file_path = os.path.join(output_file_split[0], out_file)
    print(f"Saving html into file: '{out_file_path}'")
    
    with open(out_file_path,'w', encoding="utf-8") as book:
        book.write(html.render())


def main(input_file_path):
    print('Generating html')
    body = generate_html_body(input_file_path)

    ## normal html
    print('Generating html head')
    book_title = re.sub(r'\.\w+$', '', os.path.split(input_file_path)[1])
    head = generate_html_head(book_title, stylesheet)
    html = pyhtml.html(head, body)
    dump_html(html, input_file_path)

    ## mobile-friendly html
    print('Generating html head (mobile)')
    book_title = book_title + ' (mobile)'
    head = generate_html_head(book_title, stylesheet_mobile)
    html = pyhtml.html(head, body)
    dump_html(html, input_file_path, mobile=True)



######## MAIN #############################################
if __name__ == '__main__':
    #TODO remove
    #main(r'E:\WORKSHOP\Python\BookScraper\Габриэль Гарсиа Маркес @ Сто лет одиночества.txt')
    main('not_defined')
