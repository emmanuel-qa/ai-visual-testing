"""
Local test that doesn't require internet access
Tests the visual AI tool using local HTML files
"""
from visual_ai_test import VisualAITester
from pathlib import Path

# Create simple test HTML files
def create_test_html():
    """Create test HTML files locally"""
    
    html1 = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page 1</title>
        <style>
            body { 
                font-family: Arial; 
                padding: 50px;
                background: #f0f0f0;
            }
            h1 { color: #333; }
            .box {
                width: 300px;
                height: 200px;
                background: #4CAF50;
                margin: 20px;
                padding: 20px;
                color: white;
            }
        </style>
    </head>
    <body>
        <h1>Visual Regression Test Page</h1>
        <div class="box">
            <h2>Test Box</h2>
            <p>This is a test element for visual regression testing.</p>
        </div>
    </body>
    </html>
    """
    
    html2 = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page 2</title>
        <style>
            body { 
                font-family: Arial; 
                padding: 50px;
                background: #e0e0e0;
            }
            h1 { color: #666; }
            .box {
                width: 350px;
                height: 220px;
                background: #2196F3;
                margin: 25px;
                padding: 25px;
                color: white;
            }
        </style>
    </head>
    <body>
        <h1>Visual Regression Test Page - MODIFIED</h1>
        <div class="box">
            <h2>Test Box - Changed!</h2>
            <p>This box has different dimensions and colors.</p>
        </div>
    </body>
    </html>
    """
    
    # Save HTML files
    Path("test_page1.html").write_text(html1)
    Path("test_page2.html").write_text(html2)
    print("✓ Test HTML files created\n")

def run_local_test():
    """Run tests using local HTML files"""
    
    # Create test files
    create_test_html()
    
    # Initialize tester
    tester = VisualAITester()
    tester.print_banner()
    
    print("\n📚 LOCAL TEST: Testing with local HTML files\n")
    print("This test doesn't require internet access!\n")
    
    # Get absolute paths
    test1_path = Path("test_page1.html").absolute()
    test2_path = Path("test_page2.html").absolute()
    
    # Test 1: Create baseline with first page
    print("\n--- TEST 1: Creating Baseline ---")
    result1 = tester.run_test(
        url=f"file://{test1_path}",
        test_name="local_test_page",
        threshold=0.95
    )
    
    # Test 2: Compare with same page (should PASS - 100% similar)
    print("\n--- TEST 2: Testing Identical Page (Should PASS) ---")
    result2 = tester.run_test(
        url=f"file://{test1_path}",
        test_name="local_test_page",
        threshold=0.95
    )
    
    # Test 3: Compare with modified page (should FAIL - different)
    print("\n--- TEST 3: Testing Modified Page (Should FAIL) ---")
    result3 = tester.run_test(
        url=f"file://{test2_path}",
        test_name="local_test_page",
        threshold=0.95
    )
    
    # Generate report
    summary = tester.generate_report()
    
    print("\n" + "="*70)
    print("📊 LOCAL TEST SUMMARY")
    print("="*70)
    print(f"Test 1 Status: {result1.get('status', 'ERROR')}")
    print(f"Test 2 Status: {result2.get('status', 'ERROR')}")
    print(f"Test 3 Status: {result3.get('status', 'ERROR')}")
    print("="*70)
    
    print("\n✅ LOCAL TEST COMPLETE!")
    print("\nCheck the following:")
    print("  📁 baselines/  - Contains baseline image")
    print("  📁 results/    - Contains test report and diff images")
    print("  📄 current_*.png - Current screenshots")
    
    return summary

if __name__ == "__main__":
    run_local_test()