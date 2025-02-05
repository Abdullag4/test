import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
from pyzbar.pyzbar import decode
import av
import pandas as pd
import datetime

# -----------------------------
# 1) STREAMLIT PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Barcode Scanner", layout="centered")

st.title("Barcode Scanner App")

st.markdown(
    """
    This app scans item barcodes via your webcam and logs them.  
    Use the button below to start your camera, and hold barcodes in front of it.
    """
)

# -----------------------------
# 2) GLOBAL STORAGE FOR SCANNED CODES
# -----------------------------
# We use Streamlit's session state to store scanned barcodes.
if "scanned_codes" not in st.session_state:
    st.session_state.scanned_codes = []

# -----------------------------
# 3) WEBCAM BARCODE DECODER
# -----------------------------
def video_frame_callback(frame):
    """Callback function that receives each frame from the webcam,
    decodes barcodes, and updates the session_state list."""
    img = frame.to_ndarray(format="bgr24")

    # Decode barcodes using pyzbar
    decoded_objects = decode(img)
    for obj in decoded_objects:
        barcode_data = obj.data.decode("utf-8")  # the actual barcode string

        # If not already in the list, append
        if barcode_data not in st.session_state.scanned_codes:
            st.session_state.scanned_codes.append(barcode_data)

    # Return the original frame (no real-time overlay needed, can add if desired)
    return av.VideoFrame.from_ndarray(img, format="bgr24")


# ---------------------------------
# 4) CREATE THE WEBRTC STREAMER
# ---------------------------------
webrtc_ctx = webrtc_streamer(
    key="barcode-scanner",
    mode=WebRtcMode.SENDRECV,
    client_settings=ClientSettings(
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": False},
    ),
    video_frame_callback=video_frame_callback,
    async_processing=True,
)

# ---------------------------------
# 5) DISPLAY AND DOWNLOAD BARCODE LOG
# ---------------------------------
st.subheader("Scanned Barcodes:")

# Convert the scanned codes to a DataFrame for convenience
scanned_df = pd.DataFrame({"Barcode": st.session_state.scanned_codes})

# Show table in Streamlit
st.table(scanned_df)

# Provide a download button for CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

csv_data = convert_df_to_csv(scanned_df)

st.download_button(
    label="Download barcodes as CSV",
    data=csv_data,
    file_name=f"scanned_barcodes_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv",
)
