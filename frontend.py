import streamlit as st
from app import get_all_packages as get_packages
from versions import get_package_versions  # returns list of versions
from vulnerability import check_vulnerabilities  # returns vulnerability data

st.set_page_config(page_title="Poetry Dependency Analyzer", layout="wide")

st.title("📦 Poetry Dependency Analyzer")

# Sidebar for navigation
mode = st.sidebar.radio("Choose Action", ["📋 List Packages", "📜 View Versions", "🛡 Check Vulnerabilities"])



if mode == "📋 List Packages":
    if st.button("List Installed Packages"):
        packages = get_packages()  # should return a list
        st.write("### Installed Packages:")
        st.write(packages)

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