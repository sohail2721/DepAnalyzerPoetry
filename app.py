import requests
from bs4 import BeautifulSoup
import time
import json

PYPI_SIMPLE_URL = "https://pypi.org/simple/"
PYPI_JSON_URL_TEMPLATE = "https://pypi.org/pypi/{package}/json"
LIMIT = 30  # Adjust as needed

def get_all_packages():
    response = requests.get(PYPI_SIMPLE_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch package list: {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')
    packages = [a.text for a in soup.find_all('a')]
    return packages

def get_package_metadata(package_name):
    url = PYPI_JSON_URL_TEMPLATE.format(package=package_name)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def extract_package_data(metadata):
    info = metadata.get("info", {})
    version = info.get("version")
    releases = metadata.get("releases", {})
    urls = metadata.get("urls", [])

    # 11.2 Date Published
    upload_time = None
    if version in releases and releases[version]:
        upload_time = releases[version][0].get("upload_time_iso_8601")

    # 11.3 Download URL (wheel or tar.gz)
    download_url = None
    for file in urls:
        if file['packagetype'] in ['bdist_wheel', 'sdist']:
            download_url = file.get("url")
            break

    return {
        "name": info.get("name"),
        "version": version,
        "summary": info.get("summary"),
        "author": info.get("author"),
        "license": info.get("license"),
        "upload_date": upload_time,
        "download_url": download_url,
        "homepage_url": info.get("home_page") or info.get("project_url")
    }

def main():
    print("Fetching package list from PyPI...")
    all_packages = get_all_packages()
    print(f"Found {len(all_packages)} packages.")
    
    print(f"Fetching metadata for {LIMIT} packages...\n")
    results = []

    for pkg in all_packages[:LIMIT]:
        metadata = get_package_metadata(pkg)
        if metadata:
            pkg_data = extract_package_data(metadata)
            print(f"✔ {pkg_data['name']} ({pkg_data['version']})")
            results.append(pkg_data)
        else:
            print(f"✘ Failed for {pkg}")
        time.sleep(0.3)

    with open("pypi_packages_extended.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nSaved to pypi_packages_extended.json")

if __name__ == "__main__":
    main()
