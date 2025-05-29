import streamlit as st
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import io

# --- App Config ---
st.set_page_config(page_title="QR Code Generator & Reader", layout="centered")
st.title("🔳 QR Code Generator & Reader")
st.write("Generate styled QR codes or decode any QR image instantly.")

# --- Tabs ---
tab1, tab2 = st.tabs(["Generate QR", "Decode QR"])

with tab1:
    st.header("Generate a QR Code")
    text = st.text_input("Enter URL or text to encode:")
    style = st.selectbox(
        "Choose a design style:",
        [
            "Default (Black & White)",
            "Professional (Dark Blue)",
            "Personal - Heart (Red)",
            "Personal - Wife (Purple)"
        ]
    )

    if text:
        # Configure QR parameters
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        # Determine colors
        if style.startswith("Default"):
            fill_color, back_color = 'black', 'white'
        elif style.startswith("Professional"):
            fill_color, back_color = '#003366', 'white'
        elif style.startswith("Personal - Heart"):
            fill_color, back_color = 'red', 'white'
        else:  # Personal - Wife
            fill_color, back_color = 'purple', '#ffe6f2'

        # Generate styled image
        qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

        # Overlay heart icon for "Personal - Heart"
        if style == "Personal - Heart (Red)":
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(qr_img)
            w, h = qr_img.size
            # Draw a simple heart in center
            draw.text(
                (w/2 - 20, h/2 - 20),
                "❤",
                fill="red",
                # fallback font
            )

        # Prepare buffer
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        buf.seek(0)

        # Display & Download
        st.image(buf, caption=f"Your QR Code: {style}", use_container_width=True)
        st.download_button(
            "Download QR Code",
            data=buf,
            file_name="qr_code.png",
            mime="image/png"
        )

with tab2:
    st.header("Decode a QR Code")
    uploaded_file = st.file_uploader("Upload a QR code image:", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded QR Image", use_container_width=True)
        decoded = decode(image)
        if decoded:
            content = decoded[0].data.decode("utf-8")
            st.success("Decoded content:")
            st.code(content)
        else:
            st.warning("No QR code found. Try another image.")

# --- Footer ---
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & Python")
