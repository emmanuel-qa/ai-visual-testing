# 🤖 AI-Powered Visual Regression Testing

**Intelligent screenshot comparison using Computer Vision and Machine Learning**

by [Emmanuel Kuye](https://github.com/emmanuel-qa)

---

## 🌟 What Makes This "AI"?

Instead of simple pixel-by-pixel comparison, this tool uses **SSIM (Structural Similarity Index Measure)** - a computer vision algorithm that mimics how humans perceive visual differences.

### Traditional Approach:
```
if pixel[x,y] != pixel[x,y]: FAIL
❌ Too strict - fails on minor rendering differences
❌ Can't distinguish significant vs insignificant changes
❌ Breaks on anti-aliasing, font rendering, etc.
```

### AI Approach (SSIM):
```
similarity = analyze_structure(img1, img2)
✅ Understands visual patterns like humans
✅ Ignores insignificant differences
✅ Focuses on structural changes
✅ Returns similarity score (0-100%)
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Install browsers (tries all, installs what works)
playwright install chromium firefox webkit
```

**Note:** The tool automatically uses whichever browser is available (Chromium → Firefox → WebKit), so you don't need all three!

### 2. Run the Demo

```bash
# Simple demo (no internet required)
python simple_demo.py

# Local HTML test
python local_test.py

# Test real websites (requires internet)
python example_usage.py
```

---

## 🎯 Features

✅ **Smart Browser Detection** - Automatically uses Chromium, Firefox, or WebKit (whichever works)  
✅ **AI-Powered Comparison** - SSIM algorithm mimics human visual perception  
✅ **Visual Diff Generation** - Highlights exactly what changed  
✅ **Baseline Management** - Automatic baseline creation and updates  
✅ **Organized File Structure** - All screenshots in results/ folder  
✅ **JSON Reports** - Detailed test results with timestamps  
✅ **Configurable Thresholds** - Set custom similarity requirements  
✅ **No Internet Required** - Works with local HTML files and data URLs  

---

## 📁 Project Structure

```
ai-visual-testing/
├── visual_ai_test.py      # Main tool
├── example_usage.py       # Demo with external websites
├── local_test.py          # Demo with local HTML files
├── simple_demo.py         # Simple demo using data URLs
├── requirements.txt       # Dependencies
├── baselines/            # Baseline images (auto-created)
├── results/              # Test results, diffs, and screenshots
└── README.md            # This file
```

---

## 💻 Usage

### Basic Example

```python
from visual_ai_test import VisualAITester

# Initialize
tester = VisualAITester()

# Run test
result = tester.run_test(
    url="https://example.com",
    test_name="homepage",
    threshold=0.95  # 95% similarity required
)

# Generate report
tester.generate_report()
```

### Custom Thresholds

```python
# Strict comparison (99% similar required)
tester.run_test(url="...", test_name="checkout", threshold=0.99)

# Lenient comparison (90% similar is okay)
tester.run_test(url="...", test_name="feed", threshold=0.90)
```

### Batch Testing

```python
test_cases = [
    {"name": "homepage", "url": "https://example.com", "threshold": 0.95},
    {"name": "about", "url": "https://example.com/about", "threshold": 0.95},
    {"name": "contact", "url": "https://example.com/contact", "threshold": 0.95}
]

for test in test_cases:
    tester.run_test(**test)

tester.generate_report()
```

---

## 🔧 How It Works

### 1. First Run - Create Baseline
```
📸 Capture screenshot
💾 Save as baseline
🆕 Status: BASELINE_CREATED
```

### 2. Subsequent Runs - Compare with AI
```
📸 Capture new screenshot
🤖 AI analyzes both images using SSIM
📊 Calculate similarity score (0-100%)
✅ Pass if score ≥ threshold
❌ Fail if score < threshold
🎨 Generate visual diff (if failed)
```

### 3. Visual Diff Generation
```
🔍 Find differences using computer vision
🎯 Detect significant changes (ignoring noise)
📦 Draw red boxes around changes
🖼️ Create side-by-side comparison:
   [Baseline] [Current] [Differences Highlighted]
```

---

## 🎨 Understanding SSIM

**SSIM = Structural Similarity Index Measure**

The algorithm analyzes three components:

1. **Luminance**: How bright are the images?
2. **Contrast**: How much variation is there?
3. **Structure**: How similar are the patterns?

**Similarity Scores:**
- `1.00` (100%): Perfect match
- `0.99` (99%): Virtually identical
- `0.95` (95%): Very similar (default threshold)
- `0.90` (90%): Similar but noticeable differences
- `< 0.85` (85%): Significant visual changes

---

## 🛠️ Troubleshooting

### Browser Issues

**Problem:** `net::ERR_ABORTED` or browser crashes  
**Solution:** The tool automatically tries multiple browsers. If all fail:

```bash
# Reinstall browsers
playwright install chromium firefox webkit

# Or install just one that works
playwright install firefox
```

**Problem:** Firewall/antivirus blocking  
**Solution:** 
- Temporarily disable firewall/antivirus
- Or use `headless=False` to see browser window
- Or use the `simple_demo.py` which doesn't need internet

### Network Issues

**Problem:** `net::ERR_TUNNEL_CONNECTION_FAILED`  
**Solution:** Use local tests instead:

```bash
# These work without internet
python simple_demo.py
python local_test.py
```

### Installation Issues

**Problem:** `pip install` fails  
**Solution:**

```bash
# Update pip
python -m pip install --upgrade pip

# Install with specific versions
pip install playwright==1.40.0
```

---

## 📊 Example Test Report

```json
{
  "timestamp": "2025-10-22T12:00:00",
  "total_tests": 3,
  "passed": 2,
  "failed": 1,
  "baselines_created": 0,
  "results": [
    {
      "test_name": "homepage",
      "status": "PASSED",
      "similarity": 0.9987,
      "timestamp": "2025-10-22T12:00:01"
    },
    {
      "test_name": "checkout",
      "status": "FAILED",
      "similarity": 0.8734,
      "diff_image": "results/checkout_diff_20251022_120002.png",
      "timestamp": "2025-10-22T12:00:02"
    }
  ]
}
```

---

## 🎓 Learn More

**Understanding SSIM:**
- [Original SSIM Paper](https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf)
- [Why SSIM for Visual Testing](https://ece.uwaterloo.ca/~z70wang/research/ssim/)

**Computer Vision Basics:**
- [OpenCV Tutorials](https://docs.opencv.org/master/d9/df8/tutorial_root.html)
- [Image Processing Fundamentals](https://scikit-image.org/docs/stable/user_guide.html)

---

## 📝 License

MIT License - feel free to use in your projects!

---

## 👨‍💻 Author

**Emmanuel Kuye**  
Senior QA Engineer specializing in test automation and AI-powered testing

📧 Email: kuyeemmanuel@rocketmail.com  
💼 LinkedIn: [emmanuel-kuye](https://linkedin.com/in/emmanuel-kuye)  
🐙 GitHub: [emmanuel-qa](https://github.com/emmanuel-qa)

---

## 🙏 Acknowledgments

- **scikit-image** for SSIM implementation
- **OpenCV** for computer vision capabilities
- **Playwright** for browser automation
- The QA community for inspiration

---

## ⭐ If you find this useful, please star the repo!

---

## 🔄 Recent Updates

### v1.1.0 (Latest)
- ✅ **Smart browser detection** - Auto-fallback from Chromium → Firefox → WebKit
- ✅ **Clean file structure** - Screenshots now saved to `results/` folder
- ✅ **Better error messages** - Clear guidance when browsers unavailable
- ✅ **Improved stability** - Fixed browser crashes on macOS
- ✅ **Data URL support** - Works completely offline with simple_demo.py

### v1.0.0
- Initial release with AI-powered visual regression testing