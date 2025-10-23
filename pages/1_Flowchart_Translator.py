# pages/1_Flowchart_Translator.py
import streamlit as st
import numpy as np
import cv2
from google import genai
from ultralytics import YOLO
import easyocr
from PIL import Image as PILImage
import json
import math
import os
import time
import base64

st.set_page_config(
    page_title="CodeCanvas: Flowchart Translator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Base64 Encoding Function ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        return ""

BG_BASE64 = get_base64_image("static/blackpurple.jpg")

# --- STUNNING PROFESSIONAL STYLE ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    -webkit-font-smoothing: antialiased;
}}

.stApp {{
    background: linear-gradient(135deg, #0a0e27 0%, #1a1d3a 50%, #0f0a1e 100%);
    background-image: url("data:image/jpg;base64,{BG_BASE64}");
    background-size: cover;
    background-attachment: fixed;
    background-blend-mode: overlay;
    color: #FFFFFF;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

.stApp::before {{
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    z-index: 0;
    pointer-events: none;
}}

#MainMenu, footer, header {{visibility: hidden; height: 0;}}
[data-testid="stToolbar"] {{display: none;}}

.main .block-container {{
    padding: 24px 48px !important;
    max-width: 1600px;
    position: relative;
    z-index: 1;
}}

/* HERO */
.hero {{
    text-align: center;
    padding: 18px 0 16px;
    position: relative;
}}

.hero-title {{
    font-size: 5.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #FFFFFF 0%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -3px;
    margin-bottom: 12px;
    line-height: 1;
    text-shadow: none;
    animation: titleGlow 3s ease-in-out infinite;
}}

@keyframes titleGlow {{
    0%, 100% {{ filter: drop-shadow(0 4px 20px rgba(167, 139, 250, 0.3)); }}
    50% {{ filter: drop-shadow(0 4px 40px rgba(167, 139, 250, 0.6)); }}
}}

.hero-sub {{
    font-size: 1.15rem;
    color: rgba(255, 255, 255, 0.85);
    font-weight: 400;
    letter-spacing: 0.5px;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}}

/* CLEAN SECTION STYLING */
.section-container {{
    padding: 20px 0;
    margin: 16px 0;
}}

.label {{
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: rgba(167, 139, 250, 0.8);
    margin-bottom: 12px;
    display: block;
}}

/* SELECTBOX - Premium Enhanced Style */
.stSelectbox > div {{
    margin-top: 12px;
}}

.stSelectbox div[data-baseweb="select"] {{
    background: rgba(167, 139, 250, 0.1);
    backdrop-filter: blur(40px);
    border: 2px solid rgba(167, 139, 250, 0.25);
    border-radius: 24px;
    color: #FFFFFF;
    font-size: 1.2rem;
    font-weight: 500;
    transition: all 0.4s ease;
    padding: 12px 20px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}}

.stSelectbox div[data-baseweb="select"]:hover {{
    border-color: rgba(167, 139, 250, 0.5);
    background: rgba(167, 139, 250, 0.15);
    box-shadow: 0 8px 32px rgba(167, 139, 250, 0.3);
    transform: translateY(-2px);
}}

.stSelectbox div[data-baseweb="select"] > div {{
    color: #FFFFFF;
}}

/* Dropdown menu styling */
.stSelectbox [role="listbox"] {{
    background: rgba(30, 30, 50, 0.95) !important;
    backdrop-filter: blur(40px);
    border: 2px solid rgba(167, 139, 250, 0.3) !important;
    border-radius: 20px !important;
    padding: 8px !important;
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.5);
}}

.stSelectbox [role="option"] {{
    background: transparent !important;
    color: rgba(255, 255, 255, 0.8) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    margin: 4px 0 !important;
    transition: all 0.2s ease !important;
    font-weight: 500 !important;
}}

.stSelectbox [role="option"]:hover {{
    background: rgba(167, 139, 250, 0.2) !important;
    color: #FFFFFF !important;
    transform: translateX(4px);
}}

.stSelectbox [aria-selected="true"] {{
    background: rgba(167, 139, 250, 0.25) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}}

/* RADIO BUTTONS - Enhanced Pills */
div[data-testid="stRadio"] {{
    display: flex;
    gap: 16px;
    justify-content: flex-start;
    margin-top: 12px;
}}

div[data-testid="stRadio"] > div {{
    display: flex;
    gap: 16px;
    width: 100%;
}}

div[data-testid="stRadio"] > div > label {{
    display: flex !important;
    background: rgba(167, 139, 250, 0.08) !important;
    backdrop-filter: blur(40px);
    color: #FFFFFF !important;
    font-size: 1.05rem;
    font-weight: 500;
    border: 2px solid rgba(167, 139, 250, 0.2) !important;
    border-radius: 999px;
    padding: 20px 40px !important;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    flex: 1;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden;
}}

div[data-testid="stRadio"] > div > label:hover {{
    background: rgba(167, 139, 250, 0.15) !important;
    border-color: rgba(167, 139, 250, 0.5) !important;
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 16px 48px rgba(167, 139, 250, 0.3);
}}

/* Hide radio circles */
div[data-testid="stRadio"] input[type="radio"] {{
    display: none;
}}

/* FILE UPLOADER - Epic Enhanced Style */
[data-testid="stFileUploader"] {{
    background: rgba(167, 139, 250, 0.06);
    backdrop-filter: blur(40px);
    border: 3px dashed rgba(167, 139, 250, 0.3);
    border-radius: 28px;
    padding: 60px;
    transition: all 0.5s ease;
    margin-top: 12px;
    text-align: center;
    position: relative;
}}

[data-testid="stFileUploader"]::before {{
    content: '📤';
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 2rem;
    opacity: 0.3;
}}

[data-testid="stFileUploader"]:hover {{
    border-color: rgba(167, 139, 250, 0.6);
    background: rgba(167, 139, 250, 0.12);
    transform: scale(1.01);
    box-shadow: 0 12px 48px rgba(167, 139, 250, 0.3);
}}

[data-testid="stFileUploader"] section {{
    border: none !important;
    background: transparent !important;
}}

[data-testid="stFileUploader"] button {{
    background: rgba(167, 139, 250, 0.15);
    border: 2px solid rgba(167, 139, 250, 0.3);
    border-radius: 999px;
    color: #FFFFFF;
    padding: 14px 32px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
}}

[data-testid="stFileUploader"] button:hover {{
    background: rgba(167, 139, 250, 0.25);
    border-color: rgba(167, 139, 250, 0.5);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(167, 139, 250, 0.4);
}}

/* CODE CONTAINER */
.code-box {{
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(139, 92, 246, 0.2);
    border-radius: 20px;
    padding: 24px;
    margin: 20px 0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}}

.code-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(139, 92, 246, 0.15);
}}

.code-title {{
    font-size: 0.85rem;
    font-weight: 700;
    color: rgba(167, 139, 250, 0.9);
    text-transform: uppercase;
    letter-spacing: 1.5px;
}}

.stCodeBlock {{
    background: transparent !important;
    border: none !important;
    margin: 0 !important;
}}

/* BUTTONS */
.stButton button {{
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(99, 102, 241, 0.15));
    border: 1.5px solid rgba(139, 92, 246, 0.3);
    border-radius: 12px;
    color: #FFFFFF;
    padding: 11px 24px;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.2);
}}

.stButton button:hover {{
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.25), rgba(99, 102, 241, 0.25));
    border-color: rgba(139, 92, 246, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.35);
}}

.stDownloadButton button {{
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.15));
    border: 1.5px solid rgba(16, 185, 129, 0.4);
    border-radius: 12px;
    color: #FFFFFF;
    font-weight: 600;
    padding: 11px 24px;
    transition: all 0.3s ease;
}}

.stDownloadButton button:hover {{
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.25), rgba(5, 150, 105, 0.25));
    border-color: rgba(16, 185, 129, 0.6);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}}

/* CHAT SECTION */
.chat-box {{
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.02) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(139, 92, 246, 0.2);
    border-radius: 24px;
    padding: 28px 32px;
    margin-top: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}}

.chat-title {{
    font-size: 1.4rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.chat-desc {{
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.5);
    margin-bottom: 20px;
}}

.stChatMessage {{
    background: rgba(255, 255, 255, 0.03) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 16px !important;
    margin-bottom: 12px !important;
}}

.stChatMessage[data-testid="user-message"] {{
    background: rgba(139, 92, 246, 0.08) !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
}}

.stChatInput textarea {{
    background: rgba(139, 92, 246, 0.08) !important;
    border: 1.5px solid rgba(139, 92, 246, 0.25) !important;
    border-radius: 14px !important;
    color: #FFFFFF !important;
    font-size: 0.95rem !important;
    padding: 14px 18px !important;
    transition: all 0.3s ease;
}}

.stChatInput textarea:focus {{
    border-color: rgba(139, 92, 246, 0.5) !important;
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.25) !important;
}}

/* ALERTS */
.stSuccess {{
    background: rgba(16, 185, 129, 0.12);
    border-left: 4px solid #10b981;
    border-radius: 12px;
    color: #FFFFFF;
    padding: 14px 18px;
    backdrop-filter: blur(10px);
}}

.stError {{
    background: rgba(239, 68, 68, 0.12);
    border-left: 4px solid #ef4444;
    border-radius: 12px;
    color: #FFFFFF;
    padding: 14px 18px;
    backdrop-filter: blur(10px);
}}

.stInfo {{
    background: rgba(59, 130, 246, 0.12);
    border-left: 4px solid #3b82f6;
    border-radius: 12px;
    color: #FFFFFF;
    padding: 14px 18px;
    backdrop-filter: blur(10px);
}}

.stWarning {{
    background: rgba(245, 158, 11, 0.12);
    border-left: 4px solid #f59e0b;
    border-radius: 12px;
    color: #FFFFFF;
    padding: 14px 18px;
    backdrop-filter: blur(10px);
}}

.stSpinner > div {{
    border-color: rgba(139, 92, 246, 0.3) transparent transparent transparent !important;
}}

::-webkit-scrollbar {{width: 10px;}}
::-webkit-scrollbar-track {{background: rgba(0, 0, 0, 0.3);}}
::-webkit-scrollbar-thumb {{background: rgba(139, 92, 246, 0.4); border-radius: 5px;}}
::-webkit-scrollbar-thumb:hover {{background: rgba(139, 92, 246, 0.6);}}

label {{display: none !important;}}

@media (max-width: 768px) {{
    .hero-title {{font-size: 2.8rem;}}
    .main .block-container {{padding: 16px 24px !important;}}
}}
</style>
""", unsafe_allow_html=True)


# --- SESSION STATE ---
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'flowchart_context' not in st.session_state:
    st.session_state.flowchart_context = None
if 'current_language' not in st.session_state:
    st.session_state.current_language = "Python"
if 'last_modification' not in st.session_state:
    st.session_state.last_modification = None
if 'original_image' not in st.session_state:
    st.session_state.original_image = None


# --- LOAD MODELS ---
@st.cache_resource
def load_models_and_client():
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key: raise ValueError("GEMINI_API_KEY not found in secrets.")
        client = genai.Client(api_key=api_key)
        yolo_model = YOLO('models/best.pt')
        reader = easyocr.Reader(['en'])
        return client, yolo_model, reader
    except Exception as e:
        st.error(f"Failed to load resources: {e}")
        return None, None, None

client, yolo_model, reader = load_models_and_client()
if not all([client, yolo_model, reader]): st.stop()


# --- UTILITY FUNCTIONS ---
def validate_flowchart(yolo_results, _yolo_model):
    class_names = _yolo_model.names
    flowchart_classes = ['process', 'decision', 'start_end', 'arrow', 'scan']
    detected_shapes = []
    for r in yolo_results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            shape_type = class_names[class_id]
            if shape_type in flowchart_classes:
                detected_shapes.append(shape_type)
    
    if len(detected_shapes) == 0:
        return False, "❌ No flowchart detected. Please upload a clear flowchart image."
    elif len(detected_shapes) < 2:
        return False, "⚠️ Incomplete flowchart. Please ensure all elements are visible."
    else:
        return True, f"✅ Flowchart validated! Detected {len(detected_shapes)} elements."

def analyze_flowchart(yolo_results, reader, img_np, _yolo_model):
    shapes_data = []
    arrows_data = []
    class_names = _yolo_model.names
    for r in yolo_results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            shape_type = class_names[class_id]
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()
            bbox = (x1, y1, x2, y2)
            if 'arrow' in shape_type:
                arrows_data.append({'type': shape_type, 'bbox': bbox})
            else:
                roi = img_np[y1:y2, x1:x2]
                try:
                    text_result = reader.readtext(roi, detail=0, paragraph=True)
                    extracted_text = " ".join(text_result).strip()
                except Exception:
                    extracted_text = ""
                shapes_data.append({
                    'id': len(shapes_data),
                    'type': shape_type,
                    'bbox': bbox,
                    'text': extracted_text
                })
    return {"shapes": shapes_data, "arrows": arrows_data}

def create_dynamic_prompt_flow(graph, target_language):
    shapes = {s['id']: s for s in graph['shapes']}
    flow_instructions = []
    for shape_id in sorted(shapes.keys()):
        node = shapes[shape_id]
        current_text = node['text'].strip()
        current_type = node['type']
        if current_text.lower() in ['start', 'end', 'stop']: continue
        if current_type == 'process' or current_type == 'scan':
            flow_instructions.append(f"ACTION: {current_text}")
        elif current_type == 'decision':
            flow_instructions.append(f"DECISION: {current_text}")
    prompt_text = f"""You are an expert {target_language} programmer. 

Convert this flowchart logic into clean, executable {target_language} code:

{chr(10).join(flow_instructions)}

Requirements:
- Write complete, runnable code
- Include proper comments
- Use best practices for {target_language}
- Output ONLY the code, no explanations

{target_language} Code:"""
    return prompt_text

def is_casual_query(prompt):
    """Check if the prompt is a casual conversation query"""
    prompt_lower = prompt.lower().strip()
    
    # Short casual responses (acknowledgments, greetings, etc.)
    short_casual = [
        'ok', 'okay', 'thanks', 'thx', 'thank you', 'got it', 'cool', 
        'nice', 'great', 'awesome', 'perfect', 'yes', 'no', 'yep', 'nope',
        'sure', 'alright', 'k', 'kk', 'ty', 'understood', 'got it',
        'hi', 'hello', 'hey', 'bye', 'goodbye'
    ]
    
    # Check if it's a short casual response (exact match or very short)
    if prompt_lower in short_casual or len(prompt.split()) <= 2 and any(word in prompt_lower for word in short_casual):
        return True
    
    # Question words and conversational patterns
    casual_patterns = [
        'what', 'why', 'how', 'explain', 'tell me', 'can you', 
        'what did', 'what changes', 'what have you', 'describe',
        'show me', 'which', 'where', 'when', 'who', 'difference',
        'compare', 'is there', 'are there', 'does it', 'do you'
    ]
    
    return any(pattern in prompt_lower for pattern in casual_patterns)

def handle_conversational_query(prompt, current_code, last_modification, target_language, _client):
    """Handle conversational queries about the code"""
    prompt_lower = prompt.lower().strip()
    
    # Handle short acknowledgments without calling API
    short_responses = {
        'ok': "👍 Great! Let me know if you need anything else.",
        'okay': "👍 Perfect! Feel free to ask if you need more help.",
        'thanks': "You're welcome! 😊 Happy to help anytime.",
        'thx': "You're welcome! 😊",
        'thank you': "You're very welcome! 😊 Glad I could help.",
        'got it': "Awesome! 👍 Let me know if you need anything else.",
        'cool': "😎 Glad you like it!",
        'nice': "😊 Thanks! Anything else I can help with?",
        'great': "🎉 Glad it works for you!",
        'perfect': "✨ Perfect! Let me know if you need more changes.",
        'yes': "👍 Got it!",
        'no': "👍 No problem!",
        'sure': "👍 Sounds good!",
        'alright': "👍 Great!",
        'k': "👍",
        'kk': "👍👍",
        'ty': "You're welcome! 😊"
    }
    
    if prompt_lower in short_responses:
        return short_responses[prompt_lower]
    
    # For actual questions, use AI with retry logic
    context = f"""You are a helpful coding assistant. The user has {target_language} code and is asking a question about it.

Current Code:
```{target_language.lower()}
{current_code}
```

Last Modification Made: {last_modification if last_modification else "Initial code generation from flowchart"}

User Question: {prompt}

Provide a friendly, conversational response. Explain clearly what was changed, why it was changed, or answer their question about the code. Keep it natural and helpful, like a real conversation."""

    # Retry logic for API calls
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = _client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[context]
            )
            return response.text.strip()
        except Exception as e:
            if "503" in str(e) or "overloaded" in str(e).lower():
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    return "⏳ The AI service is busy right now. Please wait a moment and try again."
            raise e

def regenerate_code_with_customization(original_code, user_request, target_language, _client):
    """Regenerate code based on user request with retry logic"""
    prompt = f"""You are an expert {target_language} programmer.

Original Code:
```{target_language.lower()}
{original_code}
```

User Request: {user_request}

Task: Modify the code according to the user's request. Output ONLY the modified {target_language} code, no explanations.

Modified Code:"""

    # Retry logic for API calls
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = _client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[prompt]
            )
            return response.text.strip()
        except Exception as e:
            if "503" in str(e) or "overloaded" in str(e).lower():
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    raise Exception("⏳ The AI service is busy right now. Please wait 30 seconds and try again.")
            raise e

def run_codecanvas_pipeline(image_np, target_language, _client, _yolo_model, _reader):
    time.sleep(1)
    yolo_results = _yolo_model.predict(source=image_np, save=False, conf=0.5, verbose=False)
    is_valid, validation_msg = validate_flowchart(yolo_results, _yolo_model)
    if not is_valid:
        return None, None, validation_msg
    flowchart_graph = analyze_flowchart(yolo_results, _reader, image_np, _yolo_model)
    final_prompt_text = create_dynamic_prompt_flow(flowchart_graph, target_language)
    original_image_pil = PILImage.fromarray(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
    response = _client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[final_prompt_text, original_image_pil]
    )
    generated_code = response.text.strip()
    return generated_code, flowchart_graph, validation_msg


# --- HERO ---
st.markdown("""
<div class="hero">
    <div class="hero-title">CodeCanvas</div>
    <div class="hero-sub">Transform flowcharts into production-ready code with AI</div>
</div>
""", unsafe_allow_html=True)

# --- INPUT SECTION ---
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<span class="label">🎯 Target Language</span>', unsafe_allow_html=True)
    target_language = st.selectbox(
        "lang",
        ("Python", "Java", "C++", "C", "JavaScript"),
        index=0,
        label_visibility="collapsed",
        key="language_selector"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<span class="label">📤 Input Method</span>', unsafe_allow_html=True)
    input_method = st.radio(
        "input",
        ("🖼️ Upload Image", "📸 Live Camera"),
        horizontal=True,
        label_visibility="collapsed"
    )
    
    uploaded_file = None
    camera_image = None
    
    if input_method == "🖼️ Upload Image":
        uploaded_file = st.file_uploader("upload", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    else:
        camera_image = st.camera_input("capture", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)


# --- DETECT LANGUAGE CHANGE ---
if target_language != st.session_state.current_language:
    if st.session_state.flowchart_context and st.session_state.original_image is not None:
        with st.spinner(f'🔄 Converting to {target_language}...'):
            try:
                # Regenerate code in new language
                final_prompt_text = create_dynamic_prompt_flow(
                    st.session_state.flowchart_context, 
                    target_language
                )
                original_image_pil = PILImage.fromarray(
                    cv2.cvtColor(st.session_state.original_image, cv2.COLOR_BGR2RGB)
                )
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[final_prompt_text, original_image_pil]
                )
                # UPDATE THE MAIN CODE (not chat)
                st.session_state.generated_code = response.text.strip()
                st.session_state.current_language = target_language
                st.session_state.last_modification = f"Converted to {target_language}"
                
                # Clear chat history when language changes
                st.session_state.chat_history = []
                
                # Force rerun to update display
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error converting language: {e}")
                st.session_state.current_language = target_language

# --- PROCESSING ---
image_np = None

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image_np = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
elif camera_image is not None:
    file_bytes = np.asarray(bytearray(camera_image.read()), dtype=np.uint8)
    image_np = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

if image_np is not None and st.session_state.generated_code is None:
    with st.spinner('✨ Analyzing flowchart and generating code...'):
        try:
            result = run_codecanvas_pipeline(image_np, target_language, client, yolo_model, reader)
            generated_code, flowchart_context, validation_msg = result
            
            if generated_code is None:
                st.error(validation_msg)
                st.info("💡 **Tips:** Ensure the flowchart is clear, well-lit, and all elements are visible.")
            else:
                st.session_state.generated_code = generated_code
                st.session_state.flowchart_context = flowchart_context
                st.session_state.original_image = image_np
                st.session_state.current_language = target_language
                st.session_state.chat_history = []
                st.session_state.last_modification = None
                st.success(validation_msg)
                st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- CODE DISPLAY ---
if st.session_state.generated_code:
    st.markdown('<div class="code-box">', unsafe_allow_html=True)
    
    col_label, col_download = st.columns([3, 1])
    with col_label:
        st.markdown(f'<div class="code-title">💻 Generated {st.session_state.current_language} Code</div>', unsafe_allow_html=True)
    with col_download:
        file_extensions = {
            "Python": "py",
            "Java": "java",
            "C++": "cpp",
            "C": "c",
            "JavaScript": "js"
        }
        st.download_button(
            label="⬇️ Download",
            data=st.session_state.generated_code.encode("utf-8"),
            file_name=f"codecanvas_output.{file_extensions.get(st.session_state.current_language, 'txt')}",
            mime="text/plain",
            use_container_width=True
        )
    
    # Proper syntax highlighting language mapping
    syntax_languages = {
        "Python": "python",
        "Java": "java",
        "C++": "cpp",
        "C": "c",
        "JavaScript": "javascript"
    }
    
    # Get the correct syntax language identifier
    syntax_lang = syntax_languages.get(st.session_state.current_language, "text")
    
    # Display code with proper syntax highlighting
    st.code(
        st.session_state.generated_code, 
        language=syntax_lang,
        line_numbers=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- CHAT INTERFACE ---
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    st.markdown('<div class="chat-title">💬 AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-desc">Chat with me to modify your code, ask questions, or understand changes</div>', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # If message contains code, display it in a code block
            if "code" in message:
                msg_syntax_lang = syntax_languages.get(message.get("language", st.session_state.current_language), "text")
                st.code(message["code"], language=msg_syntax_lang, line_numbers=True)
    
    # Chat input
    if prompt := st.chat_input("💭 Ask me anything: 'add error handling', 'what did you change?', 'make it shorter'"):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                try:
                    # Check if it's a conversational query or code modification request
                    if is_casual_query(prompt):
                        # Handle as conversation
                        response_text = handle_conversational_query(
                            prompt,
                            st.session_state.generated_code,
                            st.session_state.last_modification,
                            st.session_state.current_language,
                            client
                        )
                        st.markdown(response_text)
                        st.session_state.chat_history.append({
                            "role": "assistant", 
                            "content": response_text
                        })
                    else:
                        # Handle as code modification request - Generate NEW code in chat
                        new_code = regenerate_code_with_customization(
                            st.session_state.generated_code,
                            prompt,
                            st.session_state.current_language,
                            client
                        )
                        
                        # Update last modification tracking (but DON'T update main code)
                        st.session_state.last_modification = prompt
                        
                        # Display response with new code in chat
                        response_text = f"✅ I've updated the code based on your request. Here's the new version:"
                        st.markdown(response_text)
                        
                        # Get syntax language for display
                        msg_syntax_lang = syntax_languages.get(st.session_state.current_language, "text")
                        st.code(new_code, language=msg_syntax_lang, line_numbers=True)
                        
                        # Add to chat history with code
                        st.session_state.chat_history.append({
                            "role": "assistant", 
                            "content": response_text,
                            "code": new_code,
                            "language": st.session_state.current_language
                        })
                        
                except Exception as e:
                    error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
                    st.markdown(error_msg)
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
    
    st.markdown('</div>', unsafe_allow_html=True)