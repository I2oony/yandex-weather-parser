from requests_html import HTMLSession

def save_page(url, path_to_file):
    session = HTMLSession()

    response = session.get(url)
    response.html.render()

    # error during rendering process, it seems like env to render can't be downloaded
    # OSError: Chromium downloadable not found
    
    with open(path_to_file, "w") as output_file:
        output_file.write(response.html)
