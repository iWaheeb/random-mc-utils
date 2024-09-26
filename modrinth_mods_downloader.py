from argparse import ArgumentParser
from urllib.parse import unquote
import json
import os

import requests


def main():
    modpack_path = get_modpack_path()
    modpack_data = get_modpack_data(modpack_path)
    download_urls = get_download_urls(modpack_data)

    modpack_name: str = modpack_data["name"]

    download_mods(download_urls, modpack_name)


def get_modpack_path() -> str:
    parser = ArgumentParser(
        description="This tool is used to download mods from a modrinth.index.json file"
    )
    parser.add_argument("path", help="the path of a modrinth mods file")
    return parser.parse_args().path


def get_modpack_data(modpack_path) -> dict:
    with open(modpack_path, "r") as file:
        modpack_data = json.load(file)
    return modpack_data


def get_download_urls(modpack_data) -> list[str]:
    download_urls = []
    for mod in modpack_data["files"]:
        for url in mod["downloads"]:
            download_urls.append(url)
    return download_urls


def download_mods(download_urls, modpack_name):
    if not os.path.exists(modpack_name):
        os.makedirs(modpack_name)

    count = 0
    for url in download_urls:
        mod_name = get_mod_name(url)
        download_path = f"{modpack_name}/{mod_name}"
        download_one_mod(url, download_path)
        count = count + 1

    print(f"{count} mods has been downloaded out of {len(download_urls)}")


def get_mod_name(url) -> str:
    encoded_name = url.split("/")[-1]
    return unquote(encoded_name)


def download_one_mod(url, download_path):
    response = requests.get(url)

    if response.status_code == 200:
        with open(download_path, "wb") as file:
            file.write(response.content)
        print(f"Successed: {url}")
    else:
        error_code = response.status_code
        print(f"Failed, error {error_code}: {url}")


if __name__ == "__main__":
    main()
