import os
import pyhtml
import re



######## FUNCTIONS ########################################
def regex_parser(line, regex_parsing_list):
    for regex in regex_parsing_list:
        hr = ''
        m = re.match(regex['pattern'], line)
        if m:
            if re.match('^hr_.*', regex['match']):
                hr = 'pre'
            if re.match('.*_hr$', regex['match']):
                hr = 'post'

            html_args = regex.get('html_args')
            if not html_args:
                html_args = {}

            if re.match(r'.*match\[0\].*', regex['match']):
                return (m[0], html_args, hr)
            if re.match(r'.*match\[1\].*', regex['match']):
                return (m[1], html_args, hr)
            if re.match(r'.*match\[2\].*', regex['match']):
                return (m[2], html_args, hr)
            if re.match(r'.*match\[3\].*', regex['match']):
                return (m[3], html_args, hr)
            if re.match(r'.*match\[4\].*', regex['match']):
                return (m[4], html_args, hr)
            if re.match(r'.*match\[5\].*', regex['match']):
                return (m[5], html_args, hr)
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


def generate_html_body(input_file_path, regex_parsing_list):
    body_parts = [pyhtml.br]
    current_part = ''
    empty_lines_count = 0

    with open(input_file_path, 'r', encoding='utf-8') as book:
        for line in book:
            if len(current_part.strip()) == 0:
                current_part = line
                continue

            parsed_element = regex_parser(current_part, regex_parsing_list)
            if len(parsed_element[0]) > 0:
                empty_lines_count = 0
                if parsed_element[1].get('tag'):
                    if parsed_element[2] == 'pre':
                        body_parts.append(pyhtml.br)
                        body_parts.append(pyhtml.hr)
                    body_parts = append_body_part(parsed_element, body_parts)
                    if parsed_element[2] == 'post':
                        body_parts.append(pyhtml.br)
                        body_parts.append(pyhtml.hr)
                    current_part = ''
                else:
                    current_part += parsed_element[0]

            if len(line.strip()) == 0:
                empty_lines_count += 1
                continue

            if empty_lines_count > 0:
                parsed_element = regex_parser(line, regex_parsing_list)
                if len(parsed_element[0]) > 0:
                    empty_lines_count = 0
                    if parsed_element[1].get('tag'):
                        body_parts = append_body_part(current_part, body_parts)
                        if parsed_element[2] == 'pre':
                            body_parts.append(pyhtml.br)
                            body_parts.append(pyhtml.hr)
                        body_parts = append_body_part(parsed_element, body_parts)
                        if parsed_element[2] == 'post':
                            body_parts.append(pyhtml.br)
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

    return out_file_path


def main(main_config):
    output_files = []
    input_file_path = main_config['scraper_output_file']
    regex_parsing_list = main_config['parser_config'].get('regex_parsing_list')
    if not regex_parsing_list:
        regex_parsing_list = {}

    ## html body
    print('Generating html body')
    body = generate_html_body(input_file_path, regex_parsing_list)

    ## normal html
    print('Generating html head')
    book_title = re.sub(r'\.\w+$', '', os.path.split(input_file_path)[1])
    head = generate_html_head(book_title, main_config['stylesheet'])
    html = pyhtml.html(head, body)
    output_files.append((dump_html(html, input_file_path), main_config['stylesheet_filepath']))

    ## mobile-friendly html
    print('Generating html head (mobile)')
    book_title = book_title + ' (mobile)'
    head = generate_html_head(book_title, main_config['stylesheet_mobile'])
    html = pyhtml.html(head, body)
    output_files.append((dump_html(html, input_file_path, mobile=True), main_config['stylesheet_mobile_filepath']))

    return output_files



######## MAIN #############################################
if __name__ == '__main__':
    main({})
