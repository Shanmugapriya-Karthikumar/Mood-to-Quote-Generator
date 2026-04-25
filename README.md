# Mood-to-Quote Generator Pro ✨

A sophisticated AI-powered Streamlit application that generates deeply personalized inspirational quotes based on advanced emotion analysis. Create Instagram-ready content with one click.

## 🎯 Features

### 🧠 Advanced Dual-Engine Emotion Detection
- **TextBlob Sentiment Analysis**: Analyzes polarity and subjectivity for baseline emotion
- **HuggingFace Transformer Model**: Uses pre-trained `distilroberta-base` for accurate emotion classification
- **Keyword-Based Override System**: Special keywords trigger specific emotions (e.g., "burnt out" → anxious/sad)
- **Intelligent Combination**: Multi-layer decision tree for final emotion classification

### 💭 7 Emotion Categories
- 😊 **Happy** - Celebratory, joyful, uplifting quotes
- 😔 **Sad** - Compassionate, healing, acceptance quotes
- 😠 **Angry** - Empowering, boundary-setting quotes
- 😰 **Anxious** - Calming, perspective-shifting quotes
- 😌 **Calm** - Peaceful, meditative, serene quotes
- 🌙 **Lonely** - Connection-focused, reassuring quotes
- 🚀 **Motivated** - Inspiring, achievement-driven quotes

### 📚 Intelligent Quote Engine
Each quote includes:
- **Text**: The actual quote
- **Author**: Original source
- **Intensity**: Low / Medium / High emotional intensity
- **Theme**: Life | Love | Career | Self-Growth
- **Variety System**: Avoids repeating the same quote consecutively

Over **50+ curated quotes** spanning all emotions and themes.

### 🎨 Stunning Visual Design
- **Modern UI/UX** with smooth animations and transitions
- **Glassmorphism Design**: Frosted glass effects and depth
- **Dynamic Gradients**: Emotion-specific color palettes
- **Responsive Layout**: Perfect on desktop and mobile
- **Typography**: Professional fonts (Playfair Display + Poppins)

### 📸 Instagram-Ready Image Generation
- **1080x1350px dimensions**: Perfect for Instagram stories/feed
- **Emotion-Specific Styling**: Unique gradients and colors per emotion
- **Decorative Elements**: Elegant circular frames
- **Professional Typography**: Multi-line text wrapping
- **Author Attribution**: Full quote citation included
- **Metadata**: Emotion badge and intensity marker

### 📜 History Tracking
- **Last 5 Moods**: Persistent session history
- **Emotion Timeline**: See your emotional journey
- **Quote Reference**: Quick access to past quotes
- **Timestamps**: Track when each mood was recorded

### 🎯 Code Architecture

```
emotion_detection_pro/
├── load_emotion_model()          # Cache HuggingFace transformer
├── keyword_override()             # Priority keyword matching
├── get_textblob_sentiment()       # Sentiment analysis
├── get_transformer_emotion()      # AI emotion classification
├── get_final_emotion()            # Intelligent combination logic
├── get_quote()                    # Smart quote selection
├── generate_image()               # PIL image generation
├── add_to_history()               # Session history management
├── initialize_session()           # State initialization
└── main()                         # Streamlit UI orchestration
```

## 🚀 Installation

### Requirements
- Python 3.8+
- Streamlit
- TextBlob
- Transformers (HuggingFace)
- PyTorch
- Pillow
- NumPy

### Setup

1. **Clone/Download project**
   ```bash
   cd mood-quote-generator-pro
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **First run setup** (downloads HuggingFace model on first use)
   ```bash
   streamlit run app.py
   ```

## 💻 Usage

### Starting the App
```bash
streamlit run app.py
```
The app will launch at `http://localhost:8501`

### Workflow

1. **Express Your Feeling**
   - Type how you're feeling in the input box
   - Be specific for better AI analysis
   - Example: "I'm feeling burnt out and overwhelmed"

2. **Get AI Analysis**
   - App analyzes mood using dual-engine system
   - Detects emotion + keywords
   - Shows confidence level

3. **View Your Quote**
   - See emotion badge with emoji
   - Read perfectly matched quote
   - View theme and intensity metadata

4. **Share on Social**
   - Click "DOWNLOAD QUOTE IMAGE"
   - Get Instagram-ready 1080x1350px image
   - Share instantly to social media

5. **Track Your Journey**
   - View recent moods in history section
   - See emotional patterns over time
   - Quick reference to past quotes

## 🎨 Emotion & Color Mapping

| Emotion | Emoji | Primary Color | Gradient | Theme |
|---------|-------|---------------|----------|-------|
| Happy | 😊 | #FFD93D | Yellow → Green | Warm & Energetic |
| Sad | 😔 | #2C3E50 | Dark Blue | Calm & Reflective |
| Angry | 😠 | #E74C3C | Red | Bold & Intense |
| Anxious | 😰 | #9B59B6 | Purple | Ethereal & Complex |
| Calm | 😌 | #3498DB | Sky Blue | Serene & Peaceful |
| Lonely | 🌙 | #1A237E | Deep Blue | Night & Solitude |
| Motivated | 🚀 | #FF6B35 | Orange | Bright & Energetic |

## 🔧 Customization

### Add More Quotes
Edit the `QUOTES_DATABASE` dictionary in `app.py`:
```python
"happy": [
    {
        "text": "Your quote here",
        "author": "Author Name",
        "intensity": "high",
        "theme": "life"
    },
    ...
]
```

### Add Keyword Triggers
Edit `KEYWORD_OVERRIDES`:
```python
KEYWORD_OVERRIDES = {
    "anxious": ["specific_word", "another_keyword", ...],
    ...
}
```

### Adjust Colors
Modify`EMOTION_CONFIG` gradient colors and text colors.

## 📊 How AI Works

### Dual-Engine Logic

```
User Input
    ↓
[Phase 1: Keyword Check]
  └─ Found? → Return emotion
    ↓ (No)
[Phase 2: Transformer Analysis]
  └─ Confidence > 50%? → Return emotion
    ↓ (No/Low confidence)
[Phase 3: Sentiment Analysis]
  └─ Polarity > 0.1? → Happy
  └─ Polarity < -0.1? → Sad
  └─ Else → Calm
```

## 🖼️ Sample Flows

### Flow 1: Keyword Override
- Input: "I'm burnt out and exhausted"
- Keyword Match: "burnt out" → Anxious
- Result: Anxious quote displayed immediately

### Flow 2: Transformer Model
- Input: "Such an amazing day, feeling so alive!"
- Keywords: No match
- Transformer: Classifies as JOY (94% confidence)
- Result: Happy quotes displayed

### Flow 3: Sentiment Fallback
- Input: "I don't really know how I feel"
- Keywords: No match
- Transformer: Low confidence (42%)
- Sentiment: Polarity = -0.05 (neutral)
- Result: Calm quotes displayed

## 📱 Mobile Responsive

The app is fully mobile-friendly with:
- Touch-optimized buttons
- Responsive text sizing
- Mobile-appropriate gradient layouts
- Finger-friendly input fields

## 🎯 Perfect For

- **Self-Reflection**: Understand your emotional state
- **Mental Health**: Daily mood tracking & journaling
- **Social Media**: Generate authentic Instagram content
- **Content Creators**: Endless quote material for posts
- **Personal Growth**: Motivational content tailored to you
- **Teams**: Share wellness quotes with colleagues

## 🔐 Privacy

- All processing is local
- No data collected or stored server-side
- History stored only in session memory
- Completely anonymous usage

## 📚 Technologies Stack

| Technology | Purpose |
|-----------|---------|
| **Streamlit** | Web framework & UI |
| **TextBlob** | Sentiment analysis |
| **Transformers** (HuggingFace) | Emotion classification |
| **PyTorch** | Deep learning inference |
| **Pillow (PIL)** | Image generation |
| **NumPy** | Numerical computing |

## 🚀 Performance

- **First Load**: ~5-10 seconds (downloads 300MB model once)
- **Subsequent Loads**: <1 second (model cached)
- **Quote Generation**: Instant (<100ms)
- **Image Generation**: ~500ms per image

## 🐛 Troubleshooting

### "Could not find PyAudio" error
- Voice input is not available; use text input instead

### Model doesn't download
```bash
pip install --upgrade transformers torch
```

### Slow performance
- Ensure you have 4GB+ RAM
- First run downloads ~300MB model (one-time)
- Run on stable internet connection initially

## 📝 Sample Prompts

Try these inputs to see how the AI responds:

```
Happy: "I just got promoted! Living my best life!"
Sad: "Going through a breakup, feeling heartbroken"
Angry: "This is infuriating! I can't believe this happened"
Anxious: "I'm overthinking everything and can't sleep"
Calm: "Taking a meditation break, feeling peaceful"
Lonely: "I feel so isolated and disconnected"
Motivated: "Time to crush my goals and make it happen!"
```

## 📄 License

Free for personal and commercial use.

## 👨‍💻 Authors

Created with 💜 by AI Development Team
Mood-to-Quote Generator Pro | 2026

## 🙏 Acknowledgments

- HuggingFace Transformers team for emotion model
- TextBlob for sentiment analysis
- Streamlit for the amazing framework
- Quote authors for timeless wisdom

---

**Transform your emotions into wisdom. One quote at a time.** ✨