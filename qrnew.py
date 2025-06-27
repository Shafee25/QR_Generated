# Advanced QR Code Generator (Python/Streamlit Version)
#
# To run this app:
# 1. Make sure you have Python installed.
# 2. Install the required libraries by running the following command in your terminal:
#    pip install streamlit qrcode[pil] pillow
# 3. Save this code as a Python file (e.g., app.py).
# 4. Run the app from your terminal with the command:
#    streamlit run app.py

import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# --- Helper Functions ---

def hex_to_rgb(hex_color):
    """Converts a hex color string to an (R, G, B) tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_qr_with_logo(data, logo_image, qr_color, bg_color):
    """Generates a QR code with a logo in the center."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H, # High error correction for logo
        box_size=12,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create QR image with specified colors
    qr_img = qr.make_image(
        fill_color=qr_color, 
        back_color=bg_color
    ).convert('RGBA')

    if logo_image:
        logo = Image.open(logo_image).convert("RGBA")
        
        # Calculate size and position for the logo
        qr_width, qr_height = qr_img.size
        logo_max_size = qr_height // 4
        logo.thumbnail((logo_max_size, logo_max_size))

        # Create a white background for the logo for better visibility
        logo_bg_size = logo.size[0] + 8, logo.size[1] + 8
        logo_bg = Image.new("RGBA", logo_bg_size, bg_color)

        # Paste logo onto its background
        logo_bg.paste(logo, (4, 4), logo)
        
        # Position for logo background
        pos = ((qr_width - logo_bg.size[0]) // 2, (qr_height - logo_bg.size[1]) // 2)
        
        # Paste the logo with its background onto the QR code
        qr_img.paste(logo_bg, pos, logo_bg)

    return qr_img


def add_frame_to_image(image, frame_text, frame_color, text_color):
    """Adds a colored frame with text below an image."""
    if not frame_text:
        return image
        
    qr_width, qr_height = image.size
    frame_height = 80  # Height of the bottom frame
    
    # Create a new image with space for the frame
    final_image = Image.new('RGBA', (qr_width, qr_height + frame_height), frame_color)
    
    # Paste the QR code onto the new canvas
    final_image.paste(image, (0, 0))
    
    # Add text to the frame
    draw = ImageDraw.Draw(final_image)
    
    # Use a basic font; for custom fonts, provide a .ttf file path
    try:
        font = ImageFont.truetype("arialbd.ttf", 40)
    except IOError:
        font = ImageFont.load_default() # Fallback font
        
    text_bbox = draw.textbbox((0, 0), frame_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (qr_width - text_width) // 2
    text_y = qr_height + (frame_height - text_height) // 2
    
    draw.text((text_x, text_y), frame_text, font=font, fill=text_color)
    
    return final_image


# --- Streamlit App UI ---
st.set_page_config(layout="wide", page_title="Advanced QR Code Generator")

# Main title
st.title("Advanced QR Code Generator")
st.markdown("Create beautiful, branded QR codes in seconds. Customize everything from the logo to the frame.")

# Two-column layout: Controls on the left, Preview on the right
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🎨 Customization Panel")

    # Section 1: Content
    with st.expander("1. Content & Logo", expanded=True):
        data_input = st.text_input("URL or Text to Encode", "https://www.streamlit.io")
        logo_upload = st.file_uploader("Upload Your Logo (Optional)", type=['png', 'jpg', 'jpeg'])

    # Section 2: Colors
    with st.expander("2. QR Colors", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            dot_color_hex = st.color_picker('Dot Color', '#000000')
        with c2:
            bg_color_hex = st.color_picker('Background Color', '#FFFFFF')

    # Section 3: Frame
    with st.expander("3. Frame & Text (Optional)", expanded=True):
        frame_text_input = st.text_input("Frame Text (e.g., 'SCAN ME!')", "")
        c1, c2 = st.columns(2)
        with c1:
            frame_color_hex = st.color_picker('Frame Color', '#000000')
        with c2:
            frame_text_color_hex = st.color_picker('Frame Text Color', '#FFFFFF')


# --- Logic for Generating and Displaying QR Code ---
with col2:
    st.header("🖼️ Live Preview")

    # Convert hex colors to RGB tuples for PIL
    dot_color_rgb = hex_to_rgb(dot_color_hex)
    bg_color_rgb = hex_to_rgb(bg_color_hex)
    frame_color_rgb = hex_to_rgb(frame_color_hex)
    frame_text_color_rgb = hex_to_rgb(frame_text_color_hex)

    if data_input:
        try:
            # Generate QR code with logo
            final_qr = create_qr_with_logo(data_input, logo_upload, dot_color_rgb, bg_color_rgb)

            # Add frame if text is provided
            final_image = add_frame_to_image(final_qr, frame_text_input, frame_color_rgb, frame_text_color_rgb)

            # Display the final image
            st.image(final_image, use_container_width=True, caption="Your Custom QR Code")

            # Prepare image for download
            buffered = io.BytesIO()
            final_image.save(buffered, format="PNG")
            img_byte = buffered.getvalue()

            # Add a download button
            st.download_button(
                label="⬇️ Download QR Code",
                data=img_byte,
                file_name="custom_qr_code.png",
                mime="image/png",
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text or a URL to generate a QR code.")

# --- Footer ---
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & Python")

