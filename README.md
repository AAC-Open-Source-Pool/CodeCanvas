# CodeCanvas: Flowchart-to-Code Translator

## Table of Contents
- [Introduction](#introduction) <br>
- [Requirements](#requirements) <br>
- [How to use](#installation-and-usage) <br>
- [Preview](#previews) <br>
- [Team](#team-details) <br>
- [Contribution](#contribution) <br>
- [Improvements](#improvements) 

## Abstract
<p align="left">
CodeCanvas is a definitive solution for converting visual flowchart logic into executable code, distinguished by its innovative Structured Logic Compiler approach that goes far beyond generic image-to-text translation. Our core differentiation is the elimination of ambiguity in the flowchart's flow, providing Structural Certainty vs. Guesswork. Instead of guessing the order based on visual proximity, CodeCanvas uses a custom YOLOv8 model to identify the structural grammar—the shapes and the arrows. This structure is compiled into a formal JSON Graph (Nodes & Edges), explicitly defining connections like "Node 5 connects to Node 7," which guarantees the final code follows the intended logic. We ensure Robust, High-Accuracy Multimodal Grounding by tackling messy handwriting directly. We run a hybrid vision pipeline that pairs Customized EasyOCR for optimal text extraction with the Gemini 2.5 Flash model, which acts as an AI Proofreader to autonomously correct potential OCR typos (e.g., fixing "Leave hom" to "Leave home") and interpret complex mathematical symbols using its vision. Finally, CodeCanvas delivers a Complete, Deployable Engineering Product. This includes Instant Language Translation in real-time, allowing users to dynamically switch the output code between Python, Java, C++, and C without rerunning the heavy analysis. Furthermore, the integrated Code Assistant Chat provides Interactive Refinement, guiding users to modify the code (e.g., "add error handling" or "optimize the loop"), transforming the tool into an interactive, guided learning experience. CodeCanvas doesn't merely translate; it digitizes logic, autonomously corrects errors, and guides the user to a production-ready solution, establishing itself as a necessary educational and prototyping platform.
</p>

## Requirements
| Package/Language | Version/Link |
|---|---|
| **Python** | [3.11.x](https://www.python.org/)|
| **Streamlit** | [1.27.x](https://streamlit.io)|
| **ultralytics (YOLOv8)** | [Any recent version](https://docs.ultralytics.com) |
| **easyocr** | [Any recent version](https://www.jaided.ai/easyocr/) |
| **google-genai** | [Any recent version](https://ai.google.dev/gemini-api/docs/api-key) |
| **opencv-python** | [Any recent version](https://opencv.org/) |

## Installation and usage
### **1. Clone the repository**
git clone [https://github.com/AAC-Open-Source-Pool/25AACL03](https://github.com/AAC-Open-Source-Pool/25AACL03)
cd 25AACL03

### **2. Install dependencies**
pip install -r requirements.txt

### **3. Run the application**
Run the main entry point to start the Streamlit application:
streamlit run Home.py

## Preview
Screenshots of the project
![Capture1](https://github.com/user-attachments/assets/c66de048-f208-4933-8ced-75a2b7abe2f8)

![Capture2](https://github.com/user-attachments/assets/f421da28-94ce-4c55-a98a-51c414593bda)

![Capture5](https://github.com/user-attachments/assets/3581fc9f-ff03-477a-ab98-79c62d0a2401)

![Capture3](https://github.com/user-attachments/assets/7f93b7a3-53b4-492d-8298-06f553f2c167)

![Capture4](https://github.com/user-attachments/assets/e25f9f92-4948-430d-9aa1-188d9da3173a)

## Team details
<b>Team Number: </b><p>25AACL03</p> <b>Senior Mentor:</b><p> Meghana</p> <b>Junior Mentor:</b><p> Lahari</p> <b>Team Member 1:</b><p> S L P Srinishpa Gandhalu</p> <b>Team Member 2:</b><p> Varnika Mishra</p>

## Contribution 
This section provides instructions and details on how to submit a contribution via a pull request. It is important to follow these guidelines to make sure your pull request is accepted.

1. Before choosing to propose changes to this project, it is advisable to go through the readme.md file of the project to get the philosophy and the motive that went behind this project. The pull request should align with the philosophy and the motive of the original poster of this project.
2. To add your changes, make sure that the programming language in which you are proposing the changes should be the same as the programming language that has been used in the project. The versions of the programming language and the libraries(if any) used should also match with the original code.
3. Write a documentation on the changes that you are proposing. The documentation should include the problems you have noticed in the code(if any), the changes you would like to propose, the reason for these changes, and sample test cases. Remember that the topics in the documentation are strictly not limited to the topics aforementioned, but are just an inclusion.
4. Submit a pull request via Git etiquettes


## Improvements
1. YOLO Model Generalization: Expand the custom YOLO dataset to include highly variable inputs, such as complex intersections, rough hand-drawn shapes, and flowcharts with varying line thicknesses.
2. Graph Topology Validation: Implement explicit graph-theory algorithms (e.g., cycle detection, connectivity checks) to confirm the flow logic derived from the arrows before passing it to the LLM.
3. Improved OCR Error Handling: Introduce conditional image processing (e.g., dynamic contrast adjustment) specifically on failed OCR regions to enhance text extraction from poor-quality images.
4. Code Assistant Features: Add context-aware capabilities to the chat assistant, such as suggesting unit tests based on the extracted flowchart logic.
5. Webcam Stabilization: Enhance the live camera input feature to include image stabilization or capture multiple frames to improve clarity for detection and OCR.
