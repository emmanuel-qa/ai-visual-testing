from visual_ai_test import VisualAITester

def demo():
    """
    Demo showing the AI visual testing tool in action
    """
    # initialize the tester from the visual_ai_test module
    tester = VisualAITester()
    
    tester.print_banner()


    print("\n📚 DEMO: Testing multiple websites\n")
    print("First run: Creates baselines")
    print("Second run: Compares with AI and shows differences\n")

    
    

    # lets define the test cases
    test_cases = [
        {
            'name': 'playwright_homepage',
            'url': 'https://playwright.dev',
            'threshold': 0.95
        },
        {
            'name': 'python_homepage',
            'url': 'https://www.python.org',
            'threshold': 0.95
        },
        {
            'name': 'github_homepage',
            'url': 'https://github.com',
            'threshold': 0.95
        }
    ]

    # run all tests
    for test in test_cases:
        result = tester.run_test(
            url=test['url'],
            test_name=test['name'],
            threshold=test['threshold']
        )

    # generate report
    summary = tester.generate_report()

    # print instructions
    print("\n📖 WHAT TO DO NEXT:")
    print("   1. Check the 'baselines' folder - you'll see baseline images")
    print("   2. Check the 'results' folder - you'll see test reports")
    print("   3. Run this script AGAIN to see AI comparison in action")
    print("   4. If any differences are found, check results folder for visual diffs image\n")

    return summary



def custom_test_example():
    """
    Example of testing your own website
    """
    print("\n🎯 CUSTOM TEST EXAMPLE\n")
    tester = VisualAITester()

    # Test your own website!
    result = tester.run_test(
        url="https://example.com",  # Change this to your website
        test_name="my_website_test",
        threshold=0.95  # 95% similarity required
    )

    tester.generate_report()

    return result

def advanced_example():
    """
    Advanced example with different thresholds
    """
    print("\n🔬 ADVANCED EXAMPLE: Different Thresholds\n")
    tester = VisualAITester()

    # Strict comparison (99% similar required)
    tester.run_test(
        url="https://playwright.dev",
        test_name="strict_test",
        threshold=0.99
    )

    # Lenient comparison (90% similar is okay)
    tester.run_test(
        url="https://www.python.org",
        test_name="lenient_test",
        threshold=0.90
    )

    tester.generate_report()
    
    
if __name__ == "__main__":
    # run demo
    demo()

        # Uncomment to try custom test
        # custom_test_example()

        # Uncomment to try advanced example
    # advanced_example()