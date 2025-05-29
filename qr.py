import streamlit as st
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import io

st.set_page_config(page_title="QR Code Generator & Reader", layout="centered")
st.title("🔳 QR Code Generator & Reader")

tab1, tab2 = st.tabs(["Generate QR", "Decode QR"])

with tab1:
    st.header("Generate a QR Code")
    url = st.text_input("Enter URL or text to encode:")

    if url:
        # 1) Make the QR
        qr_pil: Image.Image = qrcode.make(url)

        # 2) Save it to an in-memory buffer
        buf = io.BytesIO()
        qr_pil.save(buf, format="PNG")
        buf.seek(0)

        # 3) DISPLAY it via the buffer
        st.image(buf, caption="Your QR Code", use_container_width=True)

        # 4) DOWNLOAD button (uses same buffer)
        st.download_button(
            label="Download QR Code",
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
            st.warning("No QR code found in the image. Please try another image.")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & Python")