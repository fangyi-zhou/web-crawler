from web_crawler.link_processor import find_links

BASIC_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
    {head}
</head>
<body>
    {body}
</body>
</html>
"""


def test_link_processor_can_find_a_single_link():
    # Produce a basic HTML document with a single link
    html = BASIC_HTML.format(head="", body='<a href="https://example.com">Example</a>')
    links = find_links(html, base_url="https://example.com")
    assert links == {"https://example.com"}


def test_link_processor_can_find_multiple_links():
    # Produce a basic HTML document with multiple links
    html = BASIC_HTML.format(
        head="",
        body="\n".join(
            [f'<a href="https://example.com/{id}">Example</a>' for id in range(5)]
        ),
    )
    links = find_links(html, base_url="https://example.com")
    assert "https://example.com/0" in links
    assert "https://example.com/1" in links
    assert "https://example.com/2" in links
    assert "https://example.com/3" in links
    assert "https://example.com/4" in links


def test_link_processor_can_find_multiple_links_ignores_fragments():
    # Produce a basic HTML document with multiple links
    html = BASIC_HTML.format(
        head="",
        body="\n".join(
            [f'<a href="https://example.com/#{id}">Example</a>' for id in range(5)]
        ),
    )
    links = find_links(html, base_url="https://example.com")
    assert "https://example.com/" in links


def test_link_processor_can_find_a_single_relative_link_without_base_html():
    # Produce a basic HTML document with a single relative link
    # When no base tag is present, the base URL should be used.
    html = BASIC_HTML.format(head="", body='<a href="/page">Example</a>')
    links = find_links(html, base_url="https://example.com/")
    assert links == {"https://example.com/page"}


def test_link_processor_can_find_a_single_relative_link_with_base_html():
    # Produce a basic HTML document with a single relative link
    # When a base tag is present, the base URL in the base tag should be used.
    html = BASIC_HTML.format(
        head='<base href="https://example2.com">', body='<a href="/page">Example</a>'
    )
    links = find_links(html, base_url="https://example.com/")
    assert links == {"https://example2.com/page"}
