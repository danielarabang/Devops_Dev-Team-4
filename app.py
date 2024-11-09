# Save this file as `ip_address_app.py`
import streamlit as st
import pandas as pd
import requests
from matplotlib import pyplot as plt

# Function to get user's public IP addresses and additional geolocation information
def get_ip_info():
    ipv4_address = "Unavailable"
    ipv6_address = "Unavailable"
    ipv4_info = {}
    ipv6_info = {}

    # Try to get IPv4 info
    try:
        ipv4_response = requests.get('https://api64.ipify.org?format=json', timeout=5)
        ipv4_address = ipv4_response.json().get('ip', 'Unavailable')
        ipv4_info = requests.get(f'https://ipinfo.io/{ipv4_address}/json', timeout=5).json()
    except requests.RequestException:
        ipv4_address = "Unavailable"
        ipv4_info = {}

    # Try to get IPv6 info
    try:
        ipv6_response = requests.get('https://api6.ipify.org?format=json', timeout=5)
        ipv6_address = ipv6_response.json().get('ip', 'Unavailable')
        ipv6_info = requests.get(f'https://ipinfo.io/{ipv6_address}/json', timeout=5).json()
    except requests.RequestException:
        ipv6_address = "Unavailable"
        ipv6_info = {}

    return ipv4_address, ipv6_address, ipv4_info, ipv6_info

# Display IPs and additional info in a pandas DataFrame
def display_ip_addresses(ipv4, ipv6, ipv4_info, ipv6_info):
    data = {
        "IP Type": ["IPv4", "IPv6"],
        "IP Address": [ipv4, ipv6],
        "Country": [ipv4_info.get('country', 'Unavailable'), ipv6_info.get('country', 'Unavailable')],
        "ASN": [ipv4_info.get('org', 'Unavailable'), ipv6_info.get('org', 'Unavailable')],
        "ISP": [ipv4_info.get('org', 'Unavailable'), ipv6_info.get('org', 'Unavailable')],
    }
    df = pd.DataFrame(data)
    st.write("### Your IP Addresses and Geolocation Info")
    st.dataframe(df)
    return df

# Visualize IP requests using Matplotlib
def plot_ip_requests(count_ipv4, count_ipv6):
    plt.figure(figsize=(5, 5))
    plt.bar(['IPv4', 'IPv6'], [count_ipv4, count_ipv6], color=['blue', 'green'])
    plt.title("Frequency of IP Requests")
    plt.xlabel("IP Type")
    plt.ylabel("Number of Requests")
    st.pyplot(plt)

# Streamlit app layout
def main():
    st.title("Public IP Address Fetcher with Geolocation")

    # Retrieve and display IP addresses and additional information
    ipv4, ipv6, ipv4_info, ipv6_info = get_ip_info()
    df = display_ip_addresses(ipv4, ipv6, ipv4_info, ipv6_info)

    # Initialize or update request counters
    if 'ipv4_count' not in st.session_state:
        st.session_state['ipv4_count'] = 0
    if 'ipv6_count' not in st.session_state:
        st.session_state['ipv6_count'] = 0

    # Increment request counts based on availability
    if ipv4 != "Unavailable":
        st.session_state['ipv4_count'] += 1
    if ipv6 != "Unavailable":
        st.session_state['ipv6_count'] += 1

    # Display request counts and plot
    st.write("### IP Request Frequency")
    plot_ip_requests(st.session_state['ipv4_count'], st.session_state['ipv6_count'])

if __name__ == "__main__":
    main()
