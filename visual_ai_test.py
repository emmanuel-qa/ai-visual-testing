import shutil
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
            # Try each browser until one successfully captures the screenshot
            # This handles both launch failures AND navigation failures
            browsers_to_try = [
                (p.firefox, 'Firefox'),
                (p.chromium, 'Chromium'),
                (p.webkit, 'WebKit')
            ]
            
            last_error = None
            
            for browser_type, browser_name in browsers_to_try:
                try:
                    # Try to launch browser
                    browser = browser_type.launch(headless=True)
                    print(f"   ✓ Launched {browser_name} browser")
                    
                    # Create page with standard desktop viewport
                    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
                    
                    # Try to navigate to URL
                    page.goto(url, wait_until='domcontentloaded', timeout=30000)
                    
                    # Wait for everything to load
                    page.wait_for_timeout(2000)
                    
                    # Take screenshot - save to results folder
                    screenshot_path = self.results_dir / f"current_{test_name}.png"
                    page.screenshot(path=str(screenshot_path), full_page=False)
                    
                    print(f"   ✓ Screenshot captured successfully with {browser_name}")
                    print(f"📸 Screenshot saved: {screenshot_path}")
                    
                    browser.close()
                    return str(screenshot_path)
                    
                except Exception as e:
                    last_error = e
                    print(f"   ✗ {browser_name} failed: {str(e)[:100]}")
                    try:
                        browser.close()
                    except:
                        pass
                    continue
            
            # If we got here, all browsers failed
            print(f"❌ All browsers failed. Last error: {last_error}")
            return None

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
        gray_current = cv2.cvtColor(current_img, cv2.COLOR_BGR2GRAY)
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

    def _generate_diff_image(self, current_img, baseline_img, diff_image, test_name):
        """ generate a visual difference image highlighting where changes occured
        This uses computer vision to find and highlight differences
        """
        print(f"   🎨 Generating visual diff...")

        # convert ssim difference to a usable format
        diff_image = (diff_image * 255).astype("uint8")

        # threshold to find significant differences
        thresh = cv2.threshold(diff_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        # find boundaries (contours) of differences 
        countours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # draw red boxes around the differences
        diff_highlighted = current_img.copy()

        significant_changes = 0
        total_area = 0

        for contour in countours:
            area = cv2.contourArea(contour)

            # only highlight significant differneces and should ignore tiny variations
            if area > 100: # minimum of 100 pixels
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(diff_highlighted, (x, y), (x + w, y + h),
                              (0, 0, 255), 2) # red box, 2 px thick
                significant_changes += 1
                total_area += area

        print(f"     ⚠️ Significant changes detected: {significant_changes} areas, Total changed area: {total_area} pixels")

        # create a side-by-side comparison image
        comparison = self._create_comparison_image(baseline_img, current_img, diff_highlighted)

        # Save diff image
        diff_path = self.results_dir / f"{test_name}_diff_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png" 
        cv2.imwrite(str(diff_path), comparison)
    
        return diff_path

    def _create_comparison_image(self, baseline, current, diff):
        """ Create a side-by-side comparison image showing baseline, current, and diff """
        # Add labels to each image
        baseline_labeled = baseline.copy()
        current_labeled = current.copy()
        diff_labeled = diff.copy()

        # add text labels i.e font, position, size, thickness and color
        cv2.putText(baseline_labeled, 'BASELINE', (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        cv2.putText(current_labeled, 'CURRENT', (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 165, 0), 4)
        cv2.putText(diff_labeled, 'DIFFERENCES', (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)

        # Stack images horizontally
        comparison = np.hstack((baseline_labeled, current_labeled, diff_labeled))

        return comparison
    
    def run_test(self, url, test_name, threshold=0.95):
        """
            Run complete visual regression test
            
            Args:
                url: URL to test
                test_name: Unique name for this test
                threshold: Similarity threshold (0.95 = 95%)
                
            Returns:
                Test result dictionary
        """
        print(f"\n{'='*70}")
        print(f"🤖 AI VISUAL REGRESSION TEST: {test_name}")
        print(f"{'='*70}\n")

        try:
            # Step 1: Capture screenshot
            screenshot = self.capture_screenshot(url, test_name)

            # Step 2: Compare with baseline using AI
            result = self.compare_with_baseline(screenshot, test_name, threshold)

            return result

        except Exception as e:
            print(f"❌ TEST ERROR: {e}\n")
            result = {
                'test_name': test_name,
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            self.test_results.append(result)
            return result

    def generate_report(self, report_name="visual_test_report.json"):
        """ Generate a JSON report of all test results """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.results_dir / f"test_report_{timestamp}.json"

        summary = {
        'timestamp': datetime.now().isoformat(),
        'total_tests': len(self.test_results),
        'passed': sum(1 for r in self.test_results if r['status'] == 'PASS'),
        'failed': sum(1 for r in self.test_results if r['status'] == 'FAIL'),
        'baselines_created': sum(1 for r in self.test_results if r['status'] == 'BASELINE_CREATED'),
        'errors': sum(1 for r in self.test_results if r['status'] == 'ERROR'),
        'results': self.test_results
    }
        
        with open(report_path, 'w') as f:
            json.dump(summary, f, indent=2)
    
        print(f"\n{'='*70}")
        print(f"📊 TEST REPORT GENERATED")
        print(f"{'='*70}")
        print(f"📁 Report: {report_path}")
        print(f"📈 Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"🆕 Baselines Created: {summary['baselines_created']}")
        if summary['errors'] > 0:
            print(f"⚠️  Errors: {summary['errors']}")
        print(f"{'='*70}\n")
    
        return summary

    def print_banner(self):
        """Print banner"""
        banner = """
        ╔═══════════════════════════════════════════════════════════╗
        ║                                                           ║
        ║        🤖 AI-POWERED VISUAL REGRESSION TESTING 🤖         ║
        ║                                                           ║
        ║              Using Computer Vision & SSIM                 ║
        ║                 By Emmanuel Kuye                          ║
        ║                                                           ║
        ╚═══════════════════════════════════════════════════════════╝
        """
        print(banner)

    
    if __name__ == "__main__":
        print_banner()
        print("\n⚡ Quick Demo Mode")
        print("Run example_usage.py for full demo\n")