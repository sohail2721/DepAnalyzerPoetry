import streamlit as st
from app import get_all_packages as get_packages, get_package_metadata, extract_package_data
from versions import get_package_versions  # returns list of versions
from vulnerability import check_vulnerabilities  # returns vulnerability data

st.set_page_config(page_title="Poetry Dependency Analyzer", layout="wide")

st.title("📦 Poetry Dependency Analyzer")

PACKAGES_PER_PAGE = 50

# Sidebar for navigation
mode = st.sidebar.radio("Choose Action", ["📋 List Packages", "📜 View Versions", "🛡 Check Vulnerabilities"])

# Function to display installed packages and their metadata
def list_installed_packages():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0

    if 'packages' not in st.session_state:
        st.session_state.packages = get_packages()  # Fetch all packages once and store in session state

    # Calculate the start and end indices for the current page
    start_index = st.session_state.current_page * PACKAGES_PER_PAGE
    end_index = start_index + PACKAGES_PER_PAGE
    packages_to_display = st.session_state.packages[start_index:end_index]

    st.write("### Installed Packages:")
    
    # Display package names as buttons with unique keys
    for idx, package in enumerate(packages_to_display):
        package_key = f"package_{idx}_{package}"  # Unique key for each package button
        if st.button(package, key=package_key):  # When a package is clicked
            st.write(f"Fetching metadata for {package}...")
            metadata = get_package_metadata(package)
            if metadata:
                pkg_data = extract_package_data(metadata)
                st.write("### Package Metadata")
                st.write(f"**Name**: {pkg_data['name']}")
                st.write(f"**Version**: {pkg_data['version']}")
                st.write(f"**Summary**: {pkg_data['summary']}")
                st.write(f"**Author**: {pkg_data['author']}")
                st.write(f"**License**: {pkg_data['license']}")
                st.write(f"**Upload Date**: {pkg_data['upload_date']}")
                st.write(f"**Download URL**: [{pkg_data['download_url']}]({pkg_data['download_url']})")
                st.write(f"**Homepage URL**: [{pkg_data['homepage_url']}]({pkg_data['homepage_url']})")
            else:
                st.error(f"Failed to fetch metadata for package {package}")

    # Add a 'Load More' button with a unique key
    if end_index < len(st.session_state.packages):
        load_more_key = "load_more_button"  # Unique key for "Load More" button
        if st.button("Load More", key=load_more_key):
            st.session_state.current_page += 1
            list_installed_packages()  # Reload the function to show the next set of packages

# Displaying different modes
if mode == "📋 List Packages":
    list_installed_packages()

elif mode == "📜 View Versions":
    # Shared input
    package_name = st.text_input("Enter Package Name (from PyPI)", "")
    if package_name:
        versions = get_package_versions(package_name)
        if versions:
            st.write(f"### Versions of `{package_name}`:")
            st.write(versions)
        else:
            st.warning("No versions found.")

elif mode == "🛡 Check Vulnerabilities":
    # Shared input
    package_name = st.text_input("Enter Package Name (from PyPI)", "")
    version = st.text_input("Enter Version", "")
    if package_name and version:
        st.write(f"### Checking vulnerabilities for {package_name}=={version}")
        vulns = check_vulnerabilities(package_name, version)
        
        if vulns:
            for v in vulns:
                if "error" in v:
                    st.error(f"🔴 {v['error']}")
                elif "message" in v:
                    st.success(f"✅ {v['message']}")
                else:
                    st.error(f"🔴 {v['id']}: {v['summary']}")
                    st.write(f"Details: {v.get('details', 'N/A')}")
                    st.write(f"More Info: {v.get('more_info', 'N/A')}")
                    st.markdown("---")
        else:
            st.success("✅ No vulnerabilities found.")
