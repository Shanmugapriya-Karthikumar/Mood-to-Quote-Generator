import streamlit as st
import random
import json
from datetime import datetime
from textblob import TextBlob
from PIL import Image, ImageDraw, ImageFont
import io
from transformers import pipeline

# Initialize emotion classification pipeline (caches automatically)
@st.cache_resource
def load_emotion_model():
    """Load the HuggingFace emotion classification model"""
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

# Comprehensive quotes dataset with intensity, emotion, and theme
QUOTES_DATABASE = {
    "happy": [
        {"text": "Happiness is not something ready made. It comes from your own actions.", "author": "Dalai Lama", "intensity": "medium", "theme": "life"},
        {"text": "The best way to cheer yourself is to try to cheer someone else up.", "author": "Mark Twain", "intensity": "high", "theme": "self-growth"},
        {"text": "Happiness is a direction, not a place.", "author": "Sydney J. Harris", "intensity": "medium", "theme": "life"},
        {"text": "Be happy for this moment. This moment is your life.", "author": "Omar Khayyam", "intensity": "high", "theme": "life"},
        {"text": "Happiness depends upon ourselves.", "author": "Aristotle", "intensity": "medium", "theme": "self-growth"},
        {"text": "The greatest happiness you can have is knowing that the one you love is happy because of you.", "author": "Unknown", "intensity": "high", "theme": "love"},
        {"text": "Success is getting what you want; happiness is wanting what you get.", "author": "W. H. Auden", "intensity": "medium", "theme": "career"},
        {"text": "For every minute you are angry you lose sixty seconds of happiness.", "author": "Ralph Waldo Emerson", "intensity": "medium", "theme": "life"}
    ],
    "sad": [
        {"text": "The only way the pain stops is if you learn to live with it.", "author": "Unknown", "intensity": "high", "theme": "life"},
        {"text": "Tears come from the heart and not from the brain.", "author": "Leonardo da Vinci", "intensity": "high", "theme": "love"},
        {"text": "Sadness is but a wall between two gardens.", "author": "Khalil Gibran", "intensity": "medium", "theme": "life"},
        {"text": "It's okay to feel sad sometimes. It's part of being human.", "author": "Unknown", "intensity": "low", "theme": "self-growth"},
        {"text": "After a storm comes a calm.", "author": "Matthew Henry", "intensity": "low", "theme": "life"},
        {"text": "This too shall pass.", "author": "Persian Proverb", "intensity": "low", "theme": "life"},
        {"text": "Deep grief is like the mountains, the older it becomes, the easier it is to see its beauty.", "author": "Unknown", "intensity": "high", "theme": "life"}
    ],
    "angry": [
        {"text": "Anger is an acid that can do more harm to the vessel in which it is stored than to anything on which it is poured.", "author": "Mark Twain", "intensity": "high", "theme": "life"},
        {"text": "For every minute you remain angry, you give up sixty seconds of peace of mind.", "author": "Ralph Waldo Emerson", "intensity": "high", "theme": "self-growth"},
        {"text": "Holding onto anger is like drinking poison and expecting the other person to die.", "author": "Buddha", "intensity": "high", "theme": "life"},
        {"text": "Anger makes you smaller, while forgiveness forces you to grow.", "author": "Cherie Carter-Scott", "intensity": "medium", "theme": "self-growth"},
        {"text": "The greatest remedy for anger is delay.", "author": "Seneca", "intensity": "medium", "theme": "self-growth"},
        {"text": "In anger we should do nothing which we would not do in cold blood.", "author": "Thomas Jefferson", "intensity": "medium", "theme": "life"}
    ],
    "anxious": [
        {"text": "Anxiety is the dizziness of freedom.", "author": "Søren Kierkegaard", "intensity": "high", "theme": "life"},
        {"text": "The way out of anxiety is to go through it, not around it.", "author": "Unknown", "intensity": "high", "theme": "self-growth"},
        {"text": "You don't have to control your thoughts. You just have to stop letting them control you.", "author": "Dan Millman", "intensity": "medium", "theme": "self-growth"},
        {"text": "Breathe. You are going to be okay.", "author": "Unknown", "intensity": "low", "theme": "life"},
        {"text": "Anxiety is like a rocking chair. It gives you something to do but gets you nowhere.", "author": "Jodi Picoult", "intensity": "medium", "theme": "life"},
        {"text": "Everything you want is on the other side of fear.", "author": "George Addair", "intensity": "high", "theme": "career"}
    ],
    "calm": [
        {"text": "Calmness is the cradle of power.", "author": "Josiah Gilbert Holland", "intensity": "high", "theme": "self-growth"},
        {"text": "Peace begins with a smile.", "author": "Mother Teresa", "intensity": "medium", "theme": "life"},
        {"text": "The quieter you become, the more you can hear.", "author": "Ram Dass", "intensity": "medium", "theme": "self-growth"},
        {"text": "In the midst of movement and chaos, keep stillness inside of you.", "author": "Deepak Chopra", "intensity": "medium", "theme": "life"},
        {"text": "Serenity is not freedom from the storm, but peace amid the storm.", "author": "Unknown", "intensity": "high", "theme": "life"},
        {"text": "Calm is a superpower.", "author": "Unknown", "intensity": "low", "theme": "self-growth"}
    ],
    "lonely": [
        {"text": "Loneliness is a sign you need to cultivate relationships.", "author": "Unknown", "intensity": "medium", "theme": "life"},
        {"text": "The cure for loneliness is not to be alone, but to be connected.", "author": "Dr. David Hawkins", "intensity": "high", "theme": "love"},
        {"text": "Remember you are not alone in this world; reach out.", "author": "Unknown", "intensity": "low", "theme": "self-growth"},
        {"text": "Loneliness is about feeling disconnected. Connection is the cure.", "author": "Unknown", "intensity": "medium", "theme": "life"},
        {"text": "You are never too broken to be loved.", "author": "Unknown", "intensity": "high", "theme": "love"},
        {"text": "Being alone is fine. Feeling lonely is not.", "author": "Unknown", "intensity": "medium", "theme": "self-growth"}
    ],
    "motivated": [
        {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "intensity": "high", "theme": "career"},
        {"text": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson", "intensity": "high", "theme": "career"},
        {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt", "intensity": "high", "theme": "self-growth"},
        {"text": "You are capable of amazing things.", "author": "Unknown", "intensity": "high", "theme": "self-growth"},
        {"text": "Progress is progress, no matter how small.", "author": "Unknown", "intensity": "medium", "theme": "life"},
        {"text": "Every expert was once a beginner.", "author": "Unknown", "intensity": "medium", "theme": "career"},
        {"text": "Your potential is endless. Your imagination is the only limit.", "author": "Unknown", "intensity": "high", "theme": "self-growth"}
    ]
}

# Keyword overrides for specific emotions
KEYWORD_OVERRIDES = {
    "sad": ["lonely", "heartbroken", "depressed", "devastated", "broken", "lost", "grieving"],
    "anxious": ["overthinking", "panicking", "nervous", "worried", "afraid", "tense", "on edge"],
    "lonely": ["isolated", "alone", "disconnected", "abandoned", "unwanted", "forgotten", "friendless"],
    "motivated": ["energized", "pumped", "inspired", "driven", "ambitious", "determined", "fired up"],
    "angry": ["furious", "livid", "outraged", "enraged", "seething", "fuming"],
    "burnt_out": ["exhausted", "drained", "burnt out", "overwhelmed", "fatigued", "wiped out"]
}

# Advanced emotion configuration with themes
EMOTION_CONFIG = {
    "happy": {
        "colors": ["#FFD93D", "#6BCB77"],
        "text_color": "#2D3436",
        "emoji": "😊",
        "gradient": "linear-gradient(135deg, #FFD93D 0%, #6BCB77 100%)",
        "accent": "#F39C12"
    },
    "sad": {
        "colors": ["#2C3E50", "#34495E"],
        "text_color": "#ECF0F1",
        "emoji": "😔",
        "gradient": "linear-gradient(135deg, #2C3E50 0%, #34495E 100%)",
        "accent": "#3498DB"
    },
    "angry": {
        "colors": ["#E74C3C", "#C0392B"],
        "text_color": "#FFFFFF",
        "emoji": "😠",
        "gradient": "linear-gradient(135deg, #E74C3C 0%, #C0392B 100%)",
        "accent": "#E67E22"
    },
    "anxious": {
        "colors": ["#9B59B6", "#8E44AD"],
        "text_color": "#FFFFFF",
        "emoji": "😰",
        "gradient": "linear-gradient(135deg, #9B59B6 0%, #8E44AD 100%)",
        "accent": "#AF7AC5"
    },
    "calm": {
        "colors": ["#3498DB", "#85C1E9"],
        "text_color": "#FFFFFF",
        "emoji": "😌",
        "gradient": "linear-gradient(135deg, #3498DB 0%, #85C1E9 100%)",
        "accent": "#5DADE2"
    },
    "lonely": {
        "colors": ["#1A237E", "#311B92"],
        "text_color": "#E1F5FE",
        "emoji": "🌙",
        "gradient": "linear-gradient(135deg, #1A237E 0%, #311B92 100%)",
        "accent": "#7986CB"
    },
    "motivated": {
        "colors": ["#FF6B35", "#FF8C42"],
        "text_color": "#FFFFFF",
        "emoji": "🚀",
        "gradient": "linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%)",
        "accent": "#FFB347"
    }
}


def keyword_override(text):
    """
    Check if text contains specific keywords that override emotion detection.
    Returns emotion if keyword found, None otherwise.
    """
    text_lower = text.lower()
    for emotion, keywords in KEYWORD_OVERRIDES.items():
        for keyword in keywords:
            if keyword in text_lower:
                return emotion
    return None

def get_textblob_sentiment(text):
    """
    Analyze sentiment using TextBlob.
    Returns polarity score (-1 to 1) and subjectivity.
    """
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def get_transformer_emotion(text):
    """
    Get emotion classification from HuggingFace transformer model.
    Returns emotion label and confidence score.
    """
    try:
        emotion_model = load_emotion_model()
        result = emotion_model(text[:512])  # Limit to 512 chars (model limit)
        emotion = result[0][0]['label'].lower()
        score = result[0][0]['score']
        return emotion, score
    except Exception as e:
        st.warning(f"Transformer model error: {e}. Using sentiment analysis only.")
        return None, 0

def get_final_emotion(text):
    """
    Combine multiple emotion detection methods:
    1. Check keyword overrides first (highest priority)
    2. Use transformer model output
    3. Fall back to TextBlob sentiment analysis
    Returns final emotion classification.
    """
    # Priority 1: Keyword overrides
    keyword_emotion = keyword_override(text)
    if keyword_emotion:
        return keyword_emotion
    
    # Priority 2: Transformer model
    transformer_emotion, confidence = get_transformer_emotion(text)
    if transformer_emotion and confidence > 0.5:
        # Map transformer emotions to our emotion set
        emotion_mapping = {
            "joy": "happy",
            "sadness": "sad",
            "anger": "angry",
            "fear": "anxious",
            "surprise": "motivated",
            "neutral": "calm",
            "disgust": "angry"
        }
        detected = emotion_mapping.get(transformer_emotion, transformer_emotion)
        if detected in EMOTION_CONFIG:
            return detected
    
    # Priority 3: TextBlob sentiment analysis
    polarity, subjectivity = get_textblob_sentiment(text)
    
    if polarity > 0.1:
        return "happy"
    elif polarity < -0.1:
        return "sad"
    else:
        return "calm"

def get_quote(emotion):
    """
    Get a random quote for the detected emotion.
    Ensures variation by avoiding recent quotes.
    """
    if emotion not in QUOTES_DATABASE:
        emotion = "calm"
    
    quotes_list = QUOTES_DATABASE[emotion]
    if not quotes_list:
        return {"text": "You are stronger than you think.", "author": "Unknown", "intensity": "high", "theme": "self-growth"}
    
    # Get last quote to avoid repetition
    if "last_quote" in st.session_state and st.session_state.last_quote:
        last_text = st.session_state.last_quote.get("text", "")
        available_quotes = [q for q in quotes_list if q["text"] != last_text]
        if available_quotes:
            return random.choice(available_quotes)
    
    return random.choice(quotes_list)

def generate_image(quote_data, emotion):
    """
    Generate an Instagram-ready quote image with emotion-specific styling.
    Returns PNG image as bytes.
    """
    width, height = 1080, 1350
    config = EMOTION_CONFIG.get(emotion, EMOTION_CONFIG["calm"])
    colors = config["colors"]
    
    # Create gradient background
    img = Image.new('RGB', (width, height), color=colors[0])
    draw = ImageDraw.Draw(img)
    
    # Draw smooth gradient
    for y in range(height):
        ratio = y / height
        r = int(int(colors[1][1:3], 16) * ratio + int(colors[0][1:3], 16) * (1 - ratio))
        g = int(int(colors[1][3:5], 16) * ratio + int(colors[0][3:5], 16) * (1 - ratio))
        b = int(int(colors[1][5:7], 16) * ratio + int(colors[0][5:7], 16) * (1 - ratio))
        draw.line((0, y, width, y), fill=(r, g, b))
    
    # Add decorative elements
    draw.ellipse([80, 40, 280, 240], outline=colors[0], width=4)
    draw.ellipse([width-280, height-240, width-80, height-40], outline=colors[0], width=4)
    
    # Load fonts
    try:
        quote_font = ImageFont.truetype("arial.ttf", 56)
        author_font = ImageFont.truetype("arial.ttf", 40)
        emotion_font = ImageFont.truetype("arial.ttf", 48)
    except:
        quote_font = ImageFont.load_default()
        author_font = ImageFont.load_default()
        emotion_font = ImageFont.load_default()
    
    # Format quote text with word wrapping
    quote_text = f'"{quote_data["text"]}"'
    words = quote_text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=quote_font)
        if bbox[2] - bbox[0] < width - 100:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    # Calculate positioning
    total_height = len(lines) * 70 + 100
    start_y = (height - total_height) // 2
    
    # Draw quote
    y_pos = start_y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=quote_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_pos), line, font=quote_font, fill=config["text_color"])
        y_pos += 70
    
    # Draw author
    author_text = f"— {quote_data['author']}"
    bbox = draw.textbbox((0, 0), author_text, font=author_font)
    auth_x = (width - (bbox[2] - bbox[0])) // 2
    draw.text((auth_x, y_pos + 40), author_text, font=author_font, fill=config["text_color"])
    
    # Draw emotion and intensity at bottom
    emotion_badge = f"{config['emoji']} {emotion.upper()}"
    bbox = draw.textbbox((0, 0), emotion_badge, font=emotion_font)
    badge_x = (width - (bbox[2] - bbox[0])) // 2
    draw.text((badge_x, height - 100), emotion_badge, font=emotion_font, fill=config["text_color"])
    
    # Save to bytes
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

def add_to_history(emotion, quote_data):
    """Add current quote to session history (max 5)"""
    if "history" not in st.session_state:
        st.session_state.history = []
    
    history_entry = {
        "emotion": emotion,
        "quote": quote_data["text"],
        "author": quote_data["author"],
        "timestamp": datetime.now().strftime("%H:%M"),
        "theme": quote_data.get("theme", "life")
    }
    
    st.session_state.history.insert(0, history_entry)
    st.session_state.history = st.session_state.history[:5]  # Keep only last 5

def initialize_session():
    """Initialize session state variables"""
    if "history" not in st.session_state:
        st.session_state.history = []
    if "last_quote" not in st.session_state:
        st.session_state.last_quote = None

def main():
    # Page configuration
    st.set_page_config(
        page_title="Mood-to-Quote Generator Pro",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    initialize_session()
    
    # Advanced CSS styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header Styles */
    .pro-header {
        text-align: center;
        padding: 50px 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 25px;
        color: white;
        margin-bottom: 40px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .pro-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 300px;
        height: 300px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .pro-header h1 {
        margin: 0;
        font-size: 3.5em;
        font-weight: 800;
        letter-spacing: -1px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        font-family: 'Playfair Display', serif;
    }
    
    .pro-header .subtitle {
        font-size: 1.3em;
        color: rgba(255,255,255,0.95);
        margin-top: 12px;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Input Container */
    .input-wrapper {
        background: white;
        padding: 35px;
        border-radius: 20px;
        box-shadow: 0 10px 35px rgba(0,0,0,0.08);
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
    }
    
    .input-label {
        font-size: 1.2em;
        font-weight: 600;
        color: #2d3436;
        margin-bottom: 15px;
        display: block;
    }
    
    .stTextInput > div > div > input {
        font-size: 17px !important;
        padding: 18px 20px !important;
        border-radius: 15px !important;
        border: 2.5px solid #e0e0e0 !important;
        transition: all 0.4s cubic-bezier(0.4,0,0.2,1) !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15) !important;
    }
    
    /* Button Styles */
    .button-wrapper {
        text-align: center;
        margin: 40px 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 18px 60px !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        border-radius: 50px !important;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.35) !important;
        transition: all 0.4s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Emotion Badge */
    .emotion-badge {
        display: inline-block;
        padding: 16px 32px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.3em;
        margin: 25px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        animation: slideInDown 0.6s ease;
    }
    
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Quote Container */
    .quote-container {
        background: white;
        padding: 50px;
        border-radius: 25px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.1);
        text-align: center;
        margin: 35px 0;
        animation: fadeInUp 0.8s ease;
        border-left: 8px solid;
        position: relative;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .quote-text {
        font-size: 2.8em !important;
        font-weight: 600;
        line-height: 1.7;
        color: #2d3436;
        font-style: italic;
        margin: 30px 0 20px 0;
        font-family: 'Playfair Display', serif;
    }
    
    .quote-author {
        font-size: 1.2em;
        color: #95a5a6;
        font-style: normal;
        margin-bottom: 0;
    }
    
    .quote-meta {
        font-size: 0.95em;
        color: #bdc3c7;
        margin-top: 15px;
        display: flex;
        justify-content: center;
        gap: 20px;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border: none !important;
        padding: 16px 50px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        border-radius: 50px !important;
        box-shadow: 0 8px 25px rgba(245, 87, 108, 0.35) !important;
        transition: all 0.4s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 40px rgba(245, 87, 108, 0.5) !important;
    }
    
    /* History Section */
    .history-container {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        margin-top: 40px;
    }
    
    .history-title {
        font-size: 1.4em;
        font-weight: 700;
        color: #2d3436;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .history-item {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 15px 20px;
        border-radius: 12px;
        margin: 12px 0;
        border-left: 5px solid;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .history-emotion {
        font-weight: 700;
        font-size: 1.05em;
        margin-bottom: 5px;
    }
    
    .history-quote {
        font-size: 0.95em;
        color: #555;
        font-style: italic;
        margin-bottom: 8px;
    }
    
    .history-meta {
        font-size: 0.85em;
        color: #999;
        display: flex;
        justify-content: space-between;
    }
    
    /* No Data Message */
    .no-data {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.15em;
        padding: 50px;
        background: white;
        border-radius: 20px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #95a5a6;
        font-size: 0.95em;
        margin-top: 60px;
        padding-bottom: 30px;
        border-top: 2px solid rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="pro-header">
        <h1>✨ Mood-to-Quote Generator Pro</h1>
        <p class="subtitle">AI-Powered Mood Analysis • Personalized Wisdom • Instagram-Ready Content</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions
    st.markdown("""
    <div style="text-align: center; color: #2d3436; font-size: 1.1em; margin-bottom: 35px;">
        🧠 Advanced AI emotion detection powered by TextBlob + HuggingFace Transformers<br>
        📱 Share authentic moments with perfectly matched quotes
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
    st.markdown('<label class="input-label">💭 How are you feeling today?</label>', unsafe_allow_html=True)
    mood_text = st.text_input(
        "",
        placeholder="e.g., I'm feeling overwhelmed and burnt out... or I'm so motivated today!",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate button
    st.markdown('<div class="button-wrapper">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button("🚀 GENERATE QUOTE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main logic
    if generate_button:
        if mood_text.strip():
            with st.spinner("🤖 Analyzing your mood..."):
                emotion = get_final_emotion(mood_text)
                quote_data = get_quote(emotion)
                
                # Store last quote for history
                st.session_state.last_quote = quote_data
                add_to_history(emotion, quote_data)
                
                config = EMOTION_CONFIG[emotion]
                
                # Emotion badge
                st.markdown(f"""
                <div style="text-align: center;">
                    <div class="emotion-badge" style="background: {config['gradient']}; color: {config['text_color']};">
                        {config['emoji']} {emotion.upper()} • AI DETECTED
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Quote display
                st.markdown(f"""
                <div class="quote-container" style="border-left-color: {config['colors'][0]};">
                    <div class="quote-text">"{quote_data['text']}"</div>
                    <div class="quote-author">— {quote_data['author']}</div>
                    <div class="quote-meta">
                        <span>📚 Theme: {quote_data['theme'].capitalize()}</span>
                        <span>💪 Intensity: {quote_data['intensity'].capitalize()}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Download button
                img_buf = generate_image(quote_data, emotion)
                st.download_button(
                    label=f"📥 DOWNLOAD QUOTE IMAGE",
                    data=img_buf,
                    file_name=f"quote_{emotion}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png",
                    use_container_width=True
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="no-data">
                💭 Please share how you're feeling to get started!<br>
                <span style="font-size: 0.9em; color: #bdc3c7;">Be authentic and specific for better AI analysis</span>
            </div>
            """, unsafe_allow_html=True)
    
    # History section
    if st.session_state.history:
        st.markdown("""
        <div class="history-container">
            <div class="history-title">📜 Recent Moods (Last 5)</div>
        </div>
        """, unsafe_allow_html=True)
        
        for i, entry in enumerate(st.session_state.history):
            config = EMOTION_CONFIG.get(entry["emotion"], EMOTION_CONFIG["calm"])
            st.markdown(f"""
            <div class="history-item" style="border-left-color: {config['colors'][0]};">
                <div class="history-emotion">{config['emoji']} {entry['emotion'].upper()}</div>
                <div class="history-quote">"{entry['quote']}"</div>
                <div class="history-meta">
                    <span>{entry['theme'].capitalize()}</span>
                    <span>{entry['timestamp']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <hr style="border: none; border-top: 1px solid rgba(0,0,0,0.1); margin: 30px 0;">
        Made with 💜 by Mood-to-Quote Generator Pro | Powered by AI • 2026
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()