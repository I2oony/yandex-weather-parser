import requests

def save_page(url, path_to_file):
    # headers from web browser to avoid captcha
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Content-Type": "text/plain;charset=UTF-8"
    }
    
    response = requests.post(url, headers=headers)
    print(f"Status code of getting page: {response.status_code}")

    with open(path_to_file, "w", encoding="utf-8") as output_file:
        output_file.write(response.text)

    # should contain parsing next, but i found out, 
    # that yandex returns script, not the static page
