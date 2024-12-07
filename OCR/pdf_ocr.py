from pdf2image import convert_from_path
from paddleocr import PaddleOCR
# pororo도 후보 -> 버전 문제로 제외
import os

pdf_file = ".raw/2024 학사제도 안내.pdf"
output_file = ".data/2024 학사제도 안내.txt"
def ocr_pdf_with_paddleocr(pdf_path, output_dir="output_images", lang="korean"):
    ocr = PaddleOCR(use_gpu=False, use_angle_cls=True, lang=lang)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    images = convert_from_path(pdf_path, dpi=600)

    ocr_results = []

    for page_num, image in enumerate(images, start=1):
        print(f"Processing page {page_num}...")
        image_path = os.path.join(output_dir, f"page_{page_num}.jpg")
        image.save(image_path, "JPEG", quality=100)
        result = ocr.ocr(image_path, cls=True)

        print(f"OCR raw result for page {page_num}: {result}")

        if not result or not result[0]:
            print(f"No text detected on page {page_num}.")
            continue

        page_text = "\n".join([line[1][0] for line in result[0]])
        ocr_results.append(f"Page {page_num}:\n{page_text}")

    full_text = "\n\n".join(ocr_results)
    return full_text

ocr_text = ocr_pdf_with_paddleocr(pdf_file, output_dir="./output_images", lang="korean")

if not os.path.exists(os.path.dirname(output_file)):
    os.makedirs(os.path.dirname(output_file))

with open(output_file, "w", encoding="utf-8") as f:
    f.write(ocr_text)

print("OCR 처리 완료. 결과가 저장되었습니다.")