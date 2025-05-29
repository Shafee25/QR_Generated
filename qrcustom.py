import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer
)
from qrcode.image.styles.colormasks import SolidFillColorMask
from pyzbar.pyzbar import decode
from PIL import Image
import io

# --- App Config ---
st.set_page_config(page_title="QR Code Generator & Reader", layout="centered")
st.title("🔳 QR Code Generator & Reader")
st.write("Generate fully styled QR codes with custom shapes or decode any QR image instantly.")

# --- Ensure required extras ---
# Make sure qrcode[pil] is installed: pip install qrcode[pil]

# --- Tabs ---
tab1, tab2 = st.tabs(["Generate QR", "Decode QR"])

with tab1:
    st.header("Generate a QR Code with Custom Shape")
    text = st.text_input("Enter URL or text to encode:")

    shape = st.selectbox(
        "Choose QR module shape:",
        [
            "Square (Classic)",
            "Gapped Square",
            "Circle",
            "Rounded",
            "Vertical Bars"
        ]
    )

    if text:
        # Build QR object
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        # Select module drawer
        drawers = {
            "Square (Classic)": SquareModuleDrawer(),
            "Gapped Square": GappedSquareModuleDrawer(),
            "Circle": CircleModuleDrawer(),
            "Rounded": RoundedModuleDrawer(),
            "Vertical Bars": VerticalBarsDrawer()
        }
        module_drawer = drawers.get(shape)

        # Define a solid fill color mask (black on white)
        color_mask = SolidFillColorMask(front_color=(0, 0, 0), back_color=(255, 255, 255))

        # Generate the styled QR image
        try:
            qr_img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=module_drawer,
                color_mask=color_mask
            ).convert("RGB")
        except Exception as e:
            st.error(f"Failed to generate styled QR: {e}")
            st.stop()

        # Display and download
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        buf.seek(0)

        st.image(buf, caption=f"Your QR Code: {shape}", use_container_width=True)
        st.download_button(
            label="Download QR Code",
            data=buf,
            file_name="styled_qr.png",
            mime="image/png"
        )

with tab2:
    st.header("Decode a QR Code")
    uploaded_file = st.file_uploader("Upload a QR code image:", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded QR Image", use_container_width=True)
            decoded = decode(image)
            if decoded:
                content = decoded[0].data.decode("utf-8")
                st.success("Decoded content:")
                st.code(content)
            else:
                st.warning("No QR code found. Try another image.")
        except Exception as e:
            st.error(f"Error decoding image: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & Python")
