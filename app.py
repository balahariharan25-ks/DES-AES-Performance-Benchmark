import streamlit as st
import pandas as pd

# -------------------------------
# Page Setup
# -------------------------------
st.set_page_config(page_title="DES vs AES Dashboard", layout="wide")

# -------------------------------
# Title
# -------------------------------
st.title("🔐 DES vs AES-256 Performance Dashboard")
st.markdown("### Cryptography Benchmarking Project")

# -------------------------------
# Load Data
# -------------------------------
df = pd.read_csv("results.csv")

# -------------------------------
# Sidebar Filter (VERY IMPRESSIVE ⭐)
# -------------------------------
st.sidebar.header("Filter Options")
selected_sizes = st.sidebar.multiselect(
    "Select File Sizes (MB)",
    df["Size (MB)"],
    default=df["Size (MB)"]
)

filtered_df = df[df["Size (MB)"].isin(selected_sizes)]

# -------------------------------
# Show Data
# -------------------------------
st.subheader("📊 Benchmark Data")
st.dataframe(filtered_df, use_container_width=True)

# -------------------------------
# Key Insights
# -------------------------------
st.subheader("📈 Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.metric("Faster Algorithm", "DES")

with col2:
    st.metric("More Secure", "AES-256")

# -------------------------------
# Charts
# -------------------------------
st.subheader("⏱️ Encryption Time")
st.markdown("**X-axis:** File Size (MB) | **Y-axis:** Time (seconds)")
st.line_chart(filtered_df.set_index("Size (MB)")[["AES Time (s)", "DES Time (s)"]])

st.subheader("🧠 Memory Usage")
st.markdown("**X-axis:** File Size (MB) | **Y-axis:** Memory (bytes)")
st.line_chart(filtered_df.set_index("Size (MB)")[["AES Memory (bytes)", "DES Memory (bytes)"]])

st.subheader("CPU Usage")
st.markdown("**X-axis:** File Size (MB) | **Y-axis:** CPU Time (seconds)")
st.line_chart(filtered_df.set_index("Size (MB)")[["AES CPU", "DES CPU"]])

# -------------------------------
# Download Option 
# -------------------------------
st.subheader("⬇️ Download Results")
st.download_button(
    label="Download CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_results.csv",
    mime="text/csv"
)

# -------------------------------
# Conclusion
# -------------------------------
st.subheader("📌 Conclusion")

st.write("""
- AES-256 is more secure but computationally intensive.
- DES is faster but outdated and insecure.
- Performance gap increases with file size.
""")