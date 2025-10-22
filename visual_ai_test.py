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