import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from pathlib import Path
import json
from datetime import datetime
from playwright.sync_api import sync_playwright
import sys



class VisualAITester:
    """
    AI-powered visual regression testing using Computer Vision
    Key AI Feature: SSIM (Structural Similarity Index Measure)
    - Analyzes structure, luminance, and contrast
    - Mimics human visual perception
    - More intelligent than pixel-by-pixel comparison
    """
    
    def __init__(self, baseline_dir='baselines', results_dir="results"):
        """Initilise the tester with directories for baselines and results."""
        self.baseline_dir = Path(baseline_dir)
        self.baseline_dir.mkdir(parents=True, exist_ok=True)

        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

        self.test_results = []
        
        print("🤖 AI Visual Testing Tool Initialized")
        print(f"📁 Baseline directory: {self.baseline_dir.absolute()}")
        print(f"📁 Results directory: {self.results_dir.absolute()}\n")

    def capture_screenshot(self, url, test_name):
        """ Capture screenshot of a webpage using sync_playwright

        Args:
            url: The URL to capture
            test_name: Name for this test (used for file naming)

        Returns:
            Path to the saved screenshot
        """
        print(f"📸 Capturing screenshot: {test_name}")
        print(f"🌐 URL: {url}")
        
        with sync_playwright() as p:
            # lauch a headless browser
            browser = p.chromium.launch(headless=True)

            #create a page with standard desktop viewport
            page = browser.new_page(viewport={'width': 1920, 'height': 1080})

            try:
                # navigate to URL
                page.goto(url, wait_until='domcontentloaded', timeout=30000)

                # wait for everything to load
                page.wait_for_timeout(2000)

                # take screenshots
                screenshot_path = f"current_{test_name}.png"
                page.screenshot(path=screenshot_path, full_page=False)

                print(f"📸 Screenshot saved: {screenshot_path}")
                return screenshot_path

            except Exception as e:
                print(f"❌ Error capturing screenshot: {e}")
                return None

            finally:
                browser.close()

    def compare_with_baseline(self, current_screenshot, test_name, threshold=0.95):
        """ 
        compare current screenshot with baseline using AI (SSIM algorithm)    
        this is where the magic actually happens
        Args: 
            current_screenshot: path to current screenshot
            test_name: Test Name
            threshold: similarity threshold (0.0 to 1.0, default 0.95 = 95% similarity)

        Returns:
            dictionary with test results
        """
        baseline_path = self.baseline_dir / f"{test_name}_baseline.png"

        # if first run, create baseline
        if not baseline_path.exists():
            import shutil
            shutil.copy(current_screenshot, baseline_path)
    
            result = {
                "test_name": test_name,
                "status": "BASELINE_CREATED",
                "timestamp": datetime.now().isoformat(),
                "message": "Baseline image created. Future tests will compare against this image."
            }

            print(f"🆕 BASELINE CREATED")
            print(f"   Baseline saved: {baseline_path}")
            print(f"   Run test again to compare!\n")
        
            self.test_results.append(result)
            return result
        
        # load images
        print(f"🔍 Comparing with baseline: {baseline_path}")
        print(f"  Algorithm: SSIM (Structural Similarity Index Measure)")
        print(f"    Threshold: {threshold*100:.2f}% similarity\n")

        current_img = cv2.imread(current_screenshot)
        baseline_img = cv2.imread(str(baseline_path))

        # now we need to ensure the images are both the same size
        if current_img.shape != baseline_img.shape:
            print(f"⚠️ Image size mismatch. ⚙️ Resizing current image to match baseline.")
            baseline_img = cv2.resize(baseline_img, (current_img.shape[1], current_img.shape[0]))

        # now convert to grayscale as SSIM works on single channel images
        gray_current = cv2.ccvtColor(current_img, cv2.COLOR_BGR2GRAY)
        gray_baseline = cv2.cvtColor(baseline_img, cv2.COLOR_BGR2GRAY)
            
        # 🧠 THE actual AI PART: Calculate SSIM by mimicing human visual perception
        similarity_score, diff_image = ssim(gray_baseline, gray_current, full=True)

        print(f"   📊 AI Similarity Score: {similarity_score:.4f}")
        print(f"   📊 Percentage: {similarity_score*100:.2f}%")

        # determin pass or fail based on the threshold set earlier
        passed = similarity_score >= threshold

        if passed:
            print(f"✅ TEST PASSED\n")
            print(f"   images are {similarity_score*100:.2f}% similar (threshold: {threshold*100}%)\n")

            result = {
                "test_name": test_name,
                "status": "PASSED",
                "timestamp": datetime.now().isoformat(),
                "message": f"Images are {similarity_score*100:.2f}% similar (threshold: {threshold*100}%)"
            }
        else:
            print(f"❌ TEST FAILED\n")
            print(f"   Images only {similarity_score*100:.2f}% similar (threshold: {threshold*100}%)")

            # generate visual diff showing where changes/differences are
            diff_path = self._generate_diff_image(
                current_img, baseline_img, diff_image, test_name
        )

            result = {
                "test_name": test_name,
                "status": "FAILED",
                "timestamp": datetime.now().isoformat(),
                'diff_image': str(diff_path),
                "message": f"Images are {similarity_score*100:.2f}% similar (threshold: {threshold*100}%)"
            }

            print(f"  🎨 Visual diff generated: {diff_path}\n")

        self.test_results.append(result)
        return result

        self.test_results.append(result)
        return result
