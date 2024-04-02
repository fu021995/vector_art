from bs4 import BeautifulSoup
import requests, os, time

base_url = "https://svgsilh.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def get_image_src(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="card mb-3 box-shadow h-100")
    links = [card.find("img", class_="card-img-top")["src"] for card in cards]
    return links


def get_classes(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    card_body = soup.find("div", class_="card-body")
    classes = card_body.find_all("a")
    classes = [c["href"] for c in classes]
    return classes


def get_max_page(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    page = soup.find("ul", class_="pagination")
    max_page = page.find_all("li")[-1]
    latest_page = max_page.find("a")["href"]
    return latest_page


CLASS_INDEX = 187
classes = get_classes(base_url)
classes = classes[CLASS_INDEX:]

for index, cls_path in enumerate(classes):
    latest_page = get_max_page(base_url + cls_path)
    cls_name = cls_path.split("/")[2].split(".")[0].split("-")[0]

    max_page = int(latest_page.split("-")[-1].split(".")[0])
    if max_page > 5:
        max_page = 5
    for i in range(1, max_page + 1):
        if i % 2 == 0:
            time.sleep(3)
        imgs = get_image_src(base_url + "/tag/" + cls_name + f"-{i}.html")
        download_folder = (
            "./download_svg/" + str(index + CLASS_INDEX) + "-" + cls_name + "/"
        )
        os.makedirs(download_folder, exist_ok=True)
        for j, src in enumerate(imgs):
            response = requests.get(base_url + src, headers=headers)
            with open(
                os.path.join(download_folder, f"image_{i}_{j}.svg"), "wb"
            ) as file:
                # 将响应的内容写入到文件中
                file.write(response.content)
