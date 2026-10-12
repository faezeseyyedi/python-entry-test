
import json
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote


def get_pypi_data(url):
    try:
        with urlopen(url, timeout=10) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code == 404:
            return None
        raise


def check_dependencies(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    dependencies_checked = len(lines)
    packages_not_found = 0
    versions_not_found = 0

    oldest_package = None
    oldest_date = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if "==" in line:
            name, version = line.split("==", 1)
            name = name.strip()
            version = version.strip()
        else:
            name = line
            version = None

        package_url = f"https://pypi.org/pypi/{quote(name, safe='')}/json"
        package_data = get_pypi_data(package_url)

        if package_data is None:
            packages_not_found += 1
            continue

        if version is None:
            continue

        version_url = (
            f"https://pypi.org/pypi/"
            f"{quote(name, safe='')}/{quote(version, safe='')}/json"
        )

        version_data = get_pypi_data(version_url)

        if version_data is None:
            versions_not_found += 1
            continue

        files = version_data.get("urls", [])

        if files:
            upload_time = files[0]["upload_time"]

            if oldest_date is None or upload_time < oldest_date:
                oldest_date = upload_time
                oldest_package = f"{name}=={version}"

    print("Dependencies checked:", dependencies_checked)
    print("Packages not on PyPI:", packages_not_found)
    print("Versions not on PyPI:", versions_not_found)

    if oldest_package:
        year = oldest_date[:4]
        print(f"Oldest pinned release: {oldest_package} ({year})")
    else:
        print("Oldest pinned release: None")


check_dependencies("requirements.txt")
