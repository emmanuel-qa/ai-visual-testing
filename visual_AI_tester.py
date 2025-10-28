"""
Visual AI Testing Tool
A simple, powerful tool for automated visual regression testing using AI/computer vision.

Author: Emmanuel Kuye
License: MIT
"""

from playwright.sync_api import sync_playwright
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime
from skimage.metrics import structural_similarity as ssim
import json

class VisualAITester:
    """
    Main class for visual regression testing using structural similarity (SSIM)
    """
    
    def __init__(self, baselines_dir="baselines", results_dir="results"):
        """
        Initialize the tester
        
        Args:
            baselines_dir: Directory to store baseline images
            results_dir: Directory to store test results and diffs
        """
        self.baselines_dir = Path(baselines_dir)
        self.results_dir = Path(results_dir)
        self.baselines_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)
        self.test_results = []
    
    def _capture_screenshot(self, url, output_path):
        """Capture screenshot of a webpage using Playwright"""
        with sync_playwright() as p:
            # Try browsers in order: Chromium, Firefox, WebKit
            browsers = [
                ('firefox', p.firefox),
                ('chromium', p.chromium),
                ('webkit', p.webkit)
            ]
            
            for browser_name, browser_type in browsers:
                try:
                    browser = browser_type.launch(headless=True)
                    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
                    page.goto(url)
                    page.screenshot(path=str(output_path), full_page=True)
                    browser.close()
                    return True
                except Exception:
                    continue
            
            raise Exception("Could not launch any browser (tried Chromium, Firefox, WebKit)")
    
    def run_test(self, url, test_name, threshold=0.95):
        """
        Run visual regression test
        
        Args:
            url: URL to test
            test_name: Name for this test
            threshold: Similarity threshold (0.0-1.0), default 0.95 (95%)
        
        Returns:
            dict: Test result with status, similarity score, etc.
        """
        # Capture current screenshot
        current_path = self.results_dir / f"current_{test_name}.png"
        self._capture_screenshot(url, current_path)
        
        # Load current image
        current_img = cv2.imread(str(current_path))
        
        # Check if baseline exists
        baseline_path = self.baselines_dir / f"{test_name}_baseline.png"
        
        if not baseline_path.exists():
            # Create new baseline
            cv2.imwrite(str(baseline_path), current_img)
            
            result = {
                "test_name": test_name,
                "status": "BASELINE_CREATED",
                "similarity_score": 1.0,
                "timestamp": datetime.now().isoformat(),
                "message": "Baseline created and validated"
            }
            self.test_results.append(result)
            return result
        
        # Load baseline
        baseline_img = cv2.imread(str(baseline_path))

         # Resize images to match if dimensions differ (for full-page screenshots)
        if baseline_img.shape != current_img.shape:
            # Get dimensions
            h1, w1 = baseline_img.shape[:2]
            h2, w2 = current_img.shape[:2]
            
            # Use the larger dimensions to avoid losing content
            max_height = max(h1, h2)
            max_width = max(w1, w2)
            
            # Resize both to match
            if baseline_img.shape[:2] != (max_height, max_width):
                baseline_img = cv2.resize(baseline_img, (max_width, max_height))
            if current_img.shape[:2] != (max_height, max_width):
                current_img = cv2.resize(current_img, (max_width, max_height))
        
        # Convert to grayscale for SSIM
        gray_baseline = cv2.cvtColor(baseline_img, cv2.COLOR_BGR2GRAY)
        gray_current = cv2.cvtColor(current_img, cv2.COLOR_BGR2GRAY)
        
        # Calculate similarity
        similarity_score, diff_image = ssim(gray_baseline, gray_current, full=True)
        
        # Compare with threshold
        if similarity_score >= threshold:
            result = {
                "test_name": test_name,
                "status": "PASSED",
                "similarity_score": similarity_score,
                "timestamp": datetime.now().isoformat(),
                "message": f"Images are {similarity_score*100:.2f}% similar (threshold: {threshold*100}%)"
            }
        else:
            # Generate visual diff
            diff_path = self._generate_diff_image(
                current_img, baseline_img, diff_image, test_name
            )
            
            result = {
                "test_name": test_name,
                "status": "FAILED",
                "similarity_score": similarity_score,
                "diff_image": str(diff_path),
                "timestamp": datetime.now().isoformat(),
                "message": f"Images are {similarity_score*100:.2f}% similar (threshold: {threshold*100}%)"
            }
        
        self.test_results.append(result)
        return result
    
    def _generate_diff_image(self, current_img, baseline_img, diff_image, test_name):
        """Generate visual diff with red boxes around differences"""
        # Convert SSIM diff to usable format
        diff_image = (diff_image * 255).astype("uint8")
        
        # Threshold to find significant differences
        thresh = cv2.threshold(diff_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        
        # Find contours of differences
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw red boxes on current image (preserves color)
        diff_highlighted = current_img.copy()
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Minimum 100 pixels to ignore tiny variations
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(diff_highlighted, (x, y), (x + w, y + h),
                            (0, 0, 255), 2)  # Red box
        
        # Create side-by-side comparison
        comparison = self._create_comparison_image(baseline_img, current_img, diff_highlighted)
        
        # Save diff image
        diff_path = self.results_dir / f"{test_name}_diff_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        cv2.imwrite(str(diff_path), comparison)
        
        return diff_path
    
    def _create_comparison_image(self, baseline, current, diff):
        """Create side-by-side comparison image"""
        # Add labels
        baseline_labeled = baseline.copy()
        current_labeled = current.copy()
        diff_labeled = diff.copy()
        
        cv2.putText(baseline_labeled, 'BASELINE', (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        cv2.putText(current_labeled, 'CURRENT', (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 165, 255), 4)
        cv2.putText(diff_labeled, 'DIFFERENCES', (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        
        # Stack horizontally
        comparison = np.hstack([baseline_labeled, current_labeled, diff_labeled])
        return comparison
    
    def generate_report(self):
        """Generate JSON report of all test results"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(self.test_results),
            "passed": sum(1 for r in self.test_results if r['status'] == 'PASSED'),
            "failed": sum(1 for r in self.test_results if r['status'] == 'FAILED'),
            "baselines_created": sum(1 for r in self.test_results if r['status'] == 'BASELINE_CREATED'),
            "results": self.test_results
        }
        
        report_path = self.results_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report


# NOTE: All print statements are commented out for clean output
# Uncomment any print() lines below if you want detailed logging

# Example print statements you can uncomment:
# print(f"📸 Capturing screenshot: {test_name}")
# print(f"✅ Test passed: {similarity_score*100:.2f}%")
# print(f"❌ Test failed: {similarity_score*100:.2f}%")
# print(f"🎨 Generated diff: {diff_path}")