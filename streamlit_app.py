import streamlit as st
import pytesseract
from PIL import Image
import io
import platform
import base64

# Tesseract 설정
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
else:
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def get_image_from_clipboard_windows():
    import win32clipboard
    
    win32clipboard.OpenClipboard()
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
            return Image.open(io.BytesIO(data[14:]))  # Skip the BITMAPINFO header
    finally:
        win32clipboard.CloseClipboard()
    return None

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang='kor+eng')
    return text

def main():
    st.title("이미지 텍스트 추출기")

    if platform.system() == "Windows":
        st.write("1. 원하는 영역을 캡처하세요 (예: Win + Shift + S)")
        st.write("2. '클립보드에서 이미지 가져오기' 버튼을 클릭하세요")
        
        if st.button("클립보드에서 이미지 가져오기"):
            image = get_image_from_clipboard_windows()
            if image:
                st.image(image, caption="클립보드에서 가져온 이미지", use_column_width=True)
                if st.button("텍스트 추출"):
                    text = extract_text_from_image(image)
                    st.write("추출된 텍스트:")
                    st.text_area("", value=text, height=300)
            else:
                st.warning("클립보드에 이미지가 없거나 이미지를 가져오는데 실패했습니다.")
    else:
        st.write("이 기능은 Windows에서만 사용 가능합니다.")
        st.write("대신 이미지 파일을 직접 업로드해주세요.")
    
    st.write("또는 이미지 파일을 직접 업로드하세요:")
    uploaded_file = st.file_uploader("이미지 파일 선택", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)
        if st.button("업로드된 이미지에서 텍스트 추출"):
            text = extract_text_from_image(image)
            st.write("추출된 텍스트:")
            st.text_area("", value=text, height=300)

if __name__ == "__main__":
    main()