import streamlit as st
import pytesseract
from PIL import ImageGrab, Image, ImageEnhance
import io
import re

# Tesseract 실행 파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\tesseract file\tesseract.exe'

def preprocess_image(image):
    # 이미지를 그레이스케일로 변환
    gray = image.convert('L')
    # 대비 향상
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(2.0)
    return enhanced

def extract_text_from_image(image):
    # 이미지 전처리
    preprocessed = preprocess_image(image)
    
    # Tesseract 설정 최적화
    custom_config = r'--oem 3 --psm 6 -l kor+eng'
    
    # 텍스트 추출
    text = pytesseract.image_to_string(preprocessed, config=custom_config)
    
    # 후처리
    text = post_process_text(text)
    
    return text

def post_process_text(text):
    # 줄바꿈 정리
    text = re.sub(r'\n+', '\n', text).strip()
    
    # 자주 발생하는 오류 수정 (예시)
    text = text.replace('Baz', '또한')
    text = text.replace('mc', '')
    
    return text

def get_clipboard_image():
    try:
        img = ImageGrab.grabclipboard()
        if img is None:
            return None
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr
    except Exception as e:
        st.error(f"클립보드에서 이미지를 가져오는 중 오류 발생: {e}")
        return None

def main():
    st.title("클립보드 이미지 텍스트 추출기")

    st.write("1. 원하는 영역을 캡처하세요 (예: 윈도우의 경우 Win + Shift + S)")
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

if __name__ == "__main__":
    main()