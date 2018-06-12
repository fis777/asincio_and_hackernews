from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    links = []

    def handle_starttag(self, tag, attrs):
        attr_dict = {}
        if tag == "a":
            for attr in attrs:
                (attr_name, attr_body) = attr
                attr_dict[attr_name] = attr_body
            try:
                if attr_dict['class'] == 'storylink':
                    self.links.append(attr_dict['href'])
            except Exception:
                pass
