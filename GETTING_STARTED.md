# Getting Started with Mood-to-Quote Generator Pro

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

**First-time setup note**: The app will automatically download the HuggingFace emotion model (~300MB) on first run. This is a one-time download.

### 2. Run the App
```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB recommended (model inference uses ~1-2GB)
- **Disk Space**: ~300MB for HuggingFace model cache
- **Internet**: Required for first run (model download)

---

## Features Overview

### 🧠 Smart Emotion Detection

The app uses a **3-layer intelligent system** to detect your emotion:

1. **Layer 1: Keyword Override (Highest Priority)**
   - Checks if your text contains specific emotion keywords
   - Examples: "burnt out" → anxious, "heartbroken" → sad
   - Returns immediately if keyword found

2. **Layer 2: AI Transformer Model (Medium Priority)**
   - Uses HuggingFace's `distilroberta-base` language model
   - Pre-trained on emotion classification
   - Returns if confidence > 50%

3. **Layer 3: Sentiment Analysis (Fallback)**
   - TextBlob analyzes text polarity
   - Positive → Happy, Negative → Sad, Neutral → Calm

### 💬 Quote Selection

Each emotion has 6-8 unique quotes with:
- **Intensity**: Low / Medium / High emotional weight
- **Theme**: Life | Love | Career | Self-Growth
- **Variety**: Avoids repeating the same quote consecutively

### 🎨 Image Generation

Download Instagram-ready images:
- **Size**: 1080x1350px (perfect for Instagram)
- **Design**: Emotion-specific gradients and styling
- **Metadata**: Quote author and emotion badge included
- **Format**: PNG with high quality

### 📜 History Tracking

See your last 5 moods:
- Emotion detected
- Quote displayed
- Time recorded
- Theme category

---

## Usage Examples

### Example 1: Keyword Override
```
Input: "I'm burnt out and exhausted"
Process: Keyword "burnt out" detected
Result: Anxious emotion → Get anxious quotes
```

### Example 2: AI Model Recognition
```
Input: "Such an amazing day! Feeling so alive and inspired!"
Process: 
  - No keyword match
  - Transformer classifies as JOY (96% confidence)
Result: Happy emotion → Get happy quotes
```

### Example 3: Sentiment Analysis Fallback
```
Input: "I don't know, just feeling meh"
Process:
  - No keyword match
  - Transformer uncertain (38% confidence)
  - Polarity = -0.02 (neutral)
Result: Calm emotion → Get calm quotes
```

---

## Configuration

### Add Custom Emotions

Edit the `EMOTION_CONFIG` dictionary in `app.py`:

```python
EMOTION_CONFIG = {
    "your_emotion": {
        "colors": ["#HEX1", "#HEX2"],
        "text_color": "#HEXTEXT",
        "emoji": "😊",
        "gradient": "linear-gradient(...)",
        "accent": "#HEXACCENT"
    }
}
```

### Add Custom Keywords

Edit `KEYWORD_OVERRIDES`:

```python
KEYWORD_OVERRIDES = {
    "anxious": ["new_keyword", "another_keyword"],
    ...
}
```

### Add Custom Quotes

Edit `QUOTES_DATABASE`:

```python
"happy": [
    {
        "text": "Your quote here",
        "author": "Author Name",
        "intensity": "high",  # low, medium, or high
        "theme": "life"       # life, love, career, self-growth
    }
]
```

---

## Troubleshooting

### Issue: App runs slowly on first load
**Solution**: First run downloads the emotion model (~300MB). This is normal and only happens once. Subsequent runs are instant.

### Issue: "torch not found" error
**Solution**: Reinstall torch:
```bash
pip install --upgrade torch
```

### Issue: Model download fails
**Solution**: Check internet connection and retry. Or manually download:
```python
from transformers import pipeline
pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
```

### Issue: Out of memory
**Solution**: 
- Ensure 4GB+ RAM available
- Close other applications
- Restart Streamlit server

### Issue: Images not downloading
**Solution**:
- Try a different browser
- Clear browser cache
- Check file permissions

---

## Performance Tips

1. **First load**: 5-10 seconds (normal, downloads model)
2. **Subsequent loads**: <1 second
3. **Quote generation**: <100ms
4. **Image generation**: ~500ms

To speed up:
- Use a modern browser (Chrome, Firefox, Safari)
- Ensure stable internet
- Run on a machine with 4GB+ RAM

---

## Advanced Usage

### Batch Processing (Coming Soon)

Process multiple moods at once:
```python
moods = [
    "I feel great today",
    "Feeling anxious about tomorrow",
    "Just got promoted!"
]

for mood in moods:
    emotion = get_final_emotion(mood)
    quote = get_quote(emotion)
    print(f"{emotion}: {quote}")
```

### Custom Model Integration

Use a different emotion model:
```python
@st.cache_resource
def load_emotion_model():
    return pipeline(
        "text-classification",
        model="your-model-name",
        top_k=1
    )
```

### Export History

Save your history as JSON:
```python
import json

history_json = json.dumps(st.session_state.history, indent=2)
with open("mood_history.json", "w") as f:
    f.write(history_json)
```

---

## Project Structure

```
mood-quote-generator-pro/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Full documentation
├── GETTING_STARTED.md    # This file
└── .venv/               # Virtual environment (auto-created)
```

---

## Key Code Functions

| Function | Purpose |
|----------|---------|
| `get_final_emotion(text)` | 3-layer emotion detection |
| `keyword_override(text)` | Check keyword triggers |
| `get_textblob_sentiment(text)` | Sentiment polarity analysis |
| `get_transformer_emotion(text)` | AI emotion classification |
| `get_quote(emotion)` | Select random quote |
| `generate_image(quote_data, emotion)` | Create downloadable image |
| `add_to_history(emotion, quote_data)` | Track recent moods |

---

## Contributing

Want to improve the app?

1. **Add quotes**: Edit `QUOTES_DATABASE` with more quotes
2. **Improve detection**: Add keywords to `KEYWORD_OVERRIDES`
3. **Custom colors**: Modify `EMOTION_CONFIG` gradients
4. **Bug fixes**: Test thoroughly and document changes

---

## Privacy & Security

✅ **All processing is local**
- No data sent to external servers
- No login or authentication required
- History stored only in session memory
- Completely anonymous usage

---

## Updates & Maintenance

### Check for updates:
```bash
pip list --outdated
```

### Update packages:
```bash
pip install --upgrade -r requirements.txt
```

### Update HuggingFace model:
```bash
pip install --upgrade transformers
```

---

## Support

For issues or questions:
1. Check the README.md for documentation
2. Review GETTING_STARTED.md (this file)
3. Check troubleshooting section above
4. Verify all dependencies are installed: `pip list`

---

## License

Free for personal and commercial use.

---

**Ready to transform your mood into wisdom? Run the app now!** ✨

```bash
streamlit run app.py
```
