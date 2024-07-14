import streamlit as st
import pytesseract
from PIL import ImageGrab, Image
import io
import os

# Streamlit Cloud에서 Tesseract 설치 (필요한 경우)
if not os.path.exists("/usr/bin/tesseract"):
    os.system("apt-get install -y tesseract-ocr")
    os.system("apt-get install -y libtesseract-dev")
    os.system("apt-get install -y tesseract-ocr-kor")

# Tesseract 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows 경로
if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Streamlit Cloud 경로

def get_clipboard_image():
    try:
        image = ImageGrab.grabclipboard()
        if image is not None:
            # PIL Image를 bytes로 변환
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()
        else:
            return None
    except Exception as e:
        st.error(f"클립보드에서 이미지를 가져오는 중 오류 발생: {e}")
        return None

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang='kor+eng')
    return text

def main():
    st.title("Windows 클립보드 이미지 텍스트 추출기")

    st.write("1. 원하는 영역을 캡처하세요 (예: Win + Shift + S)")
    st.write("2. 아래 '클립보드에서 이미지 가져오기' 버튼을 클릭하세요")

    if st.button("클립보드에서 이미지 가져오기"):
        img_bytes = get_clipboard_image()
        if img_bytes is not None:
            image = Image.open(io.BytesIO(img_bytes))
            st.image(image, caption="클립보드에서 가져온 이미지", use_column_width=True)
            
            text = extract_text_from_image(image)
            
            st.write("추출된 텍스트:")
            st.text_area("", value=text, height=300)
        else:
            st.warning("클립보드에 이미지가 없거나 이미지를 가져오는데 실패했습니다.")

    st.write("참고: 이 앱은 Windows에서 최적화되어 있습니다. 다른 운영 체제에서는 제대로 작동하지 않을 수 있습니다.")

if __name__ == "__main__":
    main()