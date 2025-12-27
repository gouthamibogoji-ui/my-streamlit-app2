import streamlit as st 
import numpy as np 
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="Flower Image Processor", layout="wide")

# Title
st.title("Flower Image - Multi-Color Channel Visualizer")

# Load image from URL
@st.cache_data(show_spinner=False)
def load_image():
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Sacred_lotus_Nelumbo_nucifera.jpg/960px-Sacred_lotus_Nelumbo_nucifera.jpg"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    return Image.open(BytesIO(response.content)).convert("RGB")

# Load and display image
Flower = load_image()
st.image(Flower, caption="Original Image", use_container_width=True)

# Convert to NumPy array
Flower_np = np.array(Flower)
R, G, B = Flower_np[:, :, 0], Flower_np[:, :, 1], Flower_np[:, :, 2]

# Create channel images
red_img = np.zeros_like(Flower_np)
green_img = np.zeros_like(Flower_np)
blue_img = np.zeros_like(Flower_np)

red_img[:, :, 0] = R
green_img[:, :, 1] = G
blue_img[:, :, 2] = B

# Display RGB channels
st.subheader("RGB Channel Visualization")
col1, col2, col3 = st.columns(3)

with col1:
    st.image(red_img, caption="Red Channel", use_container_width=True)

with col2:
    st.image(green_img, caption="Green Channel", use_container_width=True)

with col3:
    st.image(blue_img, caption="Blue Channel", use_container_width=True)

# Grayscale + Colormap
st.subheader("Colormapped Grayscale Image")

colormap = st.selectbox(
    "Choose a Matplotlib colormap",
    ["viridis", "plasma", "inferno", "magma", "cividis", "hot", "cool", "gray"]
)

Flower_gray = Flower.convert("L")
Flower_gray_np = np.array(Flower_gray)

# Plot using matplotlib
fig, ax = plt.subplots(figsize=(6, 4))
ax.imshow(Flower_gray_np, cmap=colormap)
ax.axis("off")

st.pyplot(fig)
