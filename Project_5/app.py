
import subprocess
import sys
import importlib.util

# Install missing packages automatically
for module in ["streamlit", "pandas", "plotly"]:
    if importlib.util.find_spec(module) is None:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", module
        ])

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page setup
st.set_page_config(
    page_title="PacketScope",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 PacketScope")
st.subheader("Network Traffic Analysis Dashboard")

# Load datasets
DATA_DIR = Path(__file__).parent / "data" / "dashboard"

@st.cache_data
def load_data(filename):
    path = DATA_DIR / filename
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

tls_df = load_data("tls_domains.csv")
domain_df = load_data("domain_summary.csv")
dns_df = load_data("dns_summary.csv")
quic_df = load_data("quic_summary.csv")
destination_df = load_data("destination_summary.csv")
protocol_df = load_data("protocol_comparison.csv")
timeline_df = load_data("traffic_timeline.csv")
packet_size_df = load_data("packet_size_summary.csv")

# Navigation
page = st.sidebar.radio(
    "Choose Analysis",
    [
        "Overview",
        "Domain Analysis",
        "Protocol Analysis",
        "Network Destinations",
        "Traffic Timeline",
        "Packet Size Analysis"
    ]
)

if page == "Overview":
    st.header("Network Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("TLS Observations", len(tls_df))
    col2.metric(
        "DNS Requests",
        int(dns_df["DNS_Requests"].sum())
        if "DNS_Requests" in dns_df.columns else 0
    )
    col3.metric("Remote IPs", len(destination_df))

    if not protocol_df.empty:
        fig = px.pie(
            protocol_df,
            names="Protocol",
            values="Packets",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "Domain Analysis":
    st.header("Domain Analysis")

    if not domain_df.empty:
        fig = px.bar(
            domain_df.head(15),
            x="Observations",
            y="Domain",
            orientation="h"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(domain_df)

elif page == "Protocol Analysis":
    st.header("Protocol Analysis")

    if not protocol_df.empty:
        fig = px.pie(
            protocol_df,
            names="Protocol",
            values="Packets",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(protocol_df)

elif page == "Network Destinations":
    st.header("Network Destinations")

    if not destination_df.empty:
        destination_df["Display"] = (
            destination_df["Domain"].fillna("Domain not detected")
            + " (" + destination_df["Remote IP"].astype(str) + ")"
        )

        fig = px.bar(
            destination_df.head(15),
            x="Total_Packets",
            y="Display",
            orientation="h"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(destination_df)

elif page == "Traffic Timeline":
    st.header("Traffic Timeline")

    if not timeline_df.empty:
        timeline_df["Second"] = pd.to_datetime(
            timeline_df["Second"]
        )

        fig = px.line(
            timeline_df,
            x="Second",
            y="Packets",
            color="Direction"
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "Packet Size Analysis":
    st.header("Packet Size Analysis")

    if not packet_size_df.empty:
        fig = px.bar(
            packet_size_df,
            x="Average_Size",
            y="Domain",
            orientation="h"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(packet_size_df)
