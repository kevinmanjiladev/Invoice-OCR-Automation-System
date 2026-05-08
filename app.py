# pip install paddlepaddle==2.6.2
# pip install paddleocr==2.9.1
# pip install opencv-python==4.8.1.78
# pip install matplotlib==3.7.2
# pip install mysql-connector-python
# pip install streamlit==1.32.0

from paddleocr import PaddleOCR

ocr=PaddleOCR(use_angle_cls=True,lang='en')
results=ocr.ocr('images/invoice.jpg')
for line in results[0]:
    text=line[1][0]
    confidence=line[1][1]
    print(f'Text:{text}')
    print(f'Confidence:{confidence}')
    print("-"*30)