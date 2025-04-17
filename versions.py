import requests

def get_package_versions(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        versions = list(data.get("releases", {}).keys())
        versions.sort(reverse=True)  # Latest first
        return versions
    else:
        raise Exception(f"Package '{package_name}' not found on PyPI.")

# Example usage
# if __name__ == "__main__":
#     pkg = input("Enter a package name: ")
#     try:
#         versions = get_package_versions(pkg)
#         print(f"\nAvailable versions of '{pkg}':")
#         for v in versions:
#             print(f" - {v}")
#     except Exception as e:
#         print(e)
