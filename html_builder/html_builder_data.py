stylesheet = '''
    div {
        width: auto
    }

    div.quote {
        text-align: right;
        font-style: italic;
        font-size: 90%;
    }

    body {
        font-size: 110%;
    }
'''

stylesheet_mobile = '''
    div {
        width: auto
    }

    div.quote {
        text-align: right;
        font-style: italic;
        font-size: 90%;
    }

    body {
        font-size: 175%;
    }
'''

    # div {
    #     max-width: 400px;
    #     min-width: 100px;
    # }


regex_parsing_list = [
    # example: (r'\[\d+\]', 'match[0]', {'tag': 'h1', 'class_': 'tag_style_value', 'div_style': 'div_style_value'})
    (r'@@title\:(.*)','match[1]', {'tag': 'h1', 'class_': 'title', 'div': True, 'div_style': 'title'}),
    (r'@@author\:(.*)','match[1]_hr', {'tag': 'h3', 'class_': 'title', 'div': True, 'div_style': 'title'}),
    (r'\[\d+\]', 'match[0]', {}),
    (r'@@(FOOTNOTES)@@','hr_match[1]', {'tag': 'h2', 'div': True, 'div_style': 'ftnotes_header'}),
    (r'\d+\..*','hr_match[0]', {'tag': 'h3', 'class_': 'chapter', 'div': True, 'div_style': 'chapter'}),
    (r'\d+','match[0]', {'tag': 'h6', 'div': True, 'div_style': 'ftnotes'})
]
