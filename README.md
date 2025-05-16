# 📝 Optical Answer Sheet Reader using OpenCV

A Python script to **automatically detect filled bubbles on MCQ-style optical answer sheets** using image processing techniques. This tool identifies the **most darkened bubble** for each question and determines the corresponding answer (A–E).

## 📸 Use Case

Ideal for scanning and evaluating OMR (Optical Mark Recognition) sheets used in quizzes, exams, or surveys where responses are marked using bubbles.
Instead of the standard procedure of using a dedicated omr scanner which needs all sheets to be arranged, this can be an alternative to quickly assess the papers and display marks using camera footage.

---

## 🔧 Features

- Converts input images to grayscale and applies Gaussian blur
- Thresholds the image using Otsu's binarization
- Detects circular contours that match answer bubbles
- Groups bubbles based on vertical positions to identify questions
- Determines marked answers by analyzing the fill ratio
- Supports options from A to E based on x-axis positioning

---

## 🛠️ Requirements

    Python 3.7+

    OpenCV

    NumPy

Install dependencies:
```
pip install opencv-python numpy```
