"""
DEMO 
Shows AI catching bugs humans would miss during manual review
"""
from visual_ai_test import VisualAITester
from pathlib import Path

def create_original_page():
    """Create original e-commerce page"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TechMart - Premium Electronics</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #f5f5f5;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px 50px;
                color: white;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .logo { font-size: 28px; font-weight: bold; }
            .nav { display: flex; gap: 30px; }
            .nav a { 
                color: white; 
                text-decoration: none; 
                font-size: 16px;
                transition: opacity 0.3s;
            }
            .nav a:hover { opacity: 0.8; }
            
            .hero {
                background: white;
                margin: 30px auto;
                max-width: 1200px;
                padding: 60px;
                text-align: center;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }
            .hero h1 {
                font-size: 48px;
                color: #333;
                margin-bottom: 20px;
            }
            .hero p {
                font-size: 20px;
                color: #666;
                margin-bottom: 40px;
            }
            .cta-button {
                background: #667eea;
                color: white;
                padding: 18px 45px;
                font-size: 18px;
                border: none;
                border-radius: 50px;
                cursor: pointer;
                font-weight: 600;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                transition: transform 0.2s;
            }
            .cta-button:hover { transform: translateY(-2px); }
            
            .products {
                max-width: 1200px;
                margin: 0 auto 50px;
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 30px;
                padding: 0 30px;
            }
            .product {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                text-align: center;
                transition: transform 0.3s;
            }
            .product:hover { transform: translateY(-5px); }
            .product img {
                width: 100%;
                height: 200px;
                object-fit: contain;
                margin-bottom: 20px;
            }
            .product h3 {
                font-size: 22px;
                color: #333;
                margin-bottom: 15px;
            }
            .product .price {
                font-size: 28px;
                color: #667eea;
                font-weight: bold;
                margin: 15px 0;
            }
            .product .old-price {
                font-size: 18px;
                color: #999;
                text-decoration: line-through;
                margin-right: 10px;
            }
            .product button {
                background: #667eea;
                color: white;
                border: none;
                padding: 12px 35px;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 15px;
            }
            
            .trust-badges {
                max-width: 1200px;
                margin: 50px auto;
                padding: 40px;
                background: white;
                border-radius: 10px;
                display: flex;
                justify-content: space-around;
                align-items: center;
            }
            .badge {
                text-align: center;
                padding: 20px;
            }
            .badge-icon {
                font-size: 48px;
                margin-bottom: 10px;
            }
            .badge-text {
                font-size: 16px;
                color: #666;
                font-weight: 600;
            }
            
            .footer {
                background: #2c3e50;
                color: white;
                padding: 40px;
                text-align: center;
                margin-top: 50px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">🛒 TechMart</div>
            <div class="nav">
                <a href="#products">Products</a>
                <a href="#deals">Deals</a>
                <a href="#support">Support</a>
                <a href="#cart">Cart (0)</a>
            </div>
        </div>
        
        <div class="hero">
            <h1>Summer Electronics Sale</h1>
            <p>Save up to 40% on premium electronics</p>
            <button class="cta-button">Shop Now</button>
        </div>
        
        <div class="products">
            <div class="product">
                <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Crect fill='%23667eea' width='200' height='120'/%3E%3Crect fill='%23333' y='120' width='200' height='80'/%3E%3C/svg%3E" alt="Laptop">
                <h3>UltraBook Pro</h3>
                <p>16GB RAM, 512GB SSD, Intel i7</p>
                <div>
                    <span class="old-price">$1,499</span>
                    <span class="price">$1,199</span>
                </div>
                <button>Add to Cart</button>
            </div>
            
            <div class="product">
                <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Ccircle cx='100' cy='100' r='80' fill='%23667eea'/%3E%3Ccircle cx='100' cy='100' r='50' fill='%23764ba2'/%3E%3C/svg%3E" alt="Headphones">
                <h3>NoiseCancel Pro</h3>
                <p>Active noise cancellation, 40hr battery</p>
                <div>
                    <span class="old-price">$349</span>
                    <span class="price">$279</span>
                </div>
                <button>Add to Cart</button>
            </div>
            
            <div class="product">
                <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Crect fill='%23667eea' x='30' y='20' width='140' height='160' rx='20'/%3E%3Crect fill='%23764ba2' x='50' y='40' width='100' height='120'/%3E%3C/svg%3E" alt="Phone">
                <h3>SmartPhone X</h3>
                <p>5G, 128GB, Triple camera system</p>
                <div>
                    <span class="old-price">$999</span>
                    <span class="price">$799</span>
                </div>
                <button>Add to Cart</button>
            </div>
        </div>
        
        <div class="trust-badges">
            <div class="badge">
                <div class="badge-icon">🚚</div>
                <div class="badge-text">Free Shipping</div>
            </div>
            <div class="badge">
                <div class="badge-icon">🔒</div>
                <div class="badge-text">Secure Payment</div>
            </div>
            <div class="badge">
                <div class="badge-icon">↩️</div>
                <div class="badge-text">30-Day Returns</div>
            </div>
            <div class="badge">
                <div class="badge-icon">⭐</div>
                <div class="badge-text">5-Star Rated</div>
            </div>
        </div>
        
        <div class="footer">
            <p>&copy; 2025 TechMart Electronics. All rights reserved.</p>
            <p>support@techmart.com | 1-800-555-TECH</p>
        </div>
    </body>
    </html>
    """
    return html

def create_subtle_bugs_page():
    """Create page with SUBTLE but CRITICAL bugs that look almost identical"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TechMart - Premium Electronics</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #f5f5f5;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px 50px;
                color: white;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .logo { font-size: 28px; font-weight: bold; }
            .nav { display: flex; gap: 30px; }
            .nav a { 
                color: white; 
                text-decoration: none; 
                font-size: 16px;
                transition: opacity 0.3s;
            }
            .nav a:hover { opacity: 0.8; }
            
            .hero {
                background: white;
                margin: 30px auto;
                max-width: 1200px;
                padding: 60px;
                text-align: center;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            }
            .hero h1 {
                font-size: 48px;
                color: #333;
                margin-bottom: 20px;
            }
            .hero p {
                font-size: 20px;
                color: #666;
                margin-bottom: 40px;
            }
            .cta-button {
                background: #667eea;
                color: white;
                padding: 18px 45px;
                font-size: 18px;
                border: none;
                border-radius: 50px;
                cursor: pointer;
                font-weight: 600;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                transition: transform 0.2s;
                /* BUG #1: Button shifted 10px to the right */
                margin-left: 10px;
            }
            .cta-button:hover { transform: translateY(-2px); }
            
            .products {
                max-width: 1200px;
                margin: 0 auto 50px;
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 30px;
                padding: 0 30px;
            }
            .product {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                text-align: center;
                transition: transform 0.3s;
            }
            .product:hover { transform: translateY(-5px); }
            .product img {
                width: 100%;
                height: 200px;
                object-fit: contain;
                margin-bottom: 20px;
            }
            .product h3 {
                font-size: 22px;
                color: #333;
                margin-bottom: 15px;
            }
            .product .price {
                font-size: 28px;
                /* BUG #2: Wrong color - should be #667eea (purple) but is #e74c3c (red) */
                color: #e74c3c;
                font-weight: bold;
                margin: 15px 0;
            }
            .product .old-price {
                font-size: 18px;
                color: #999;
                text-decoration: line-through;
                margin-right: 10px;
            }
            .product button {
                background: #667eea;
                color: white;
                border: none;
                padding: 12px 35px;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 15px;
            }
            
            .trust-badges {
                max-width: 1200px;
                margin: 50px auto;
                padding: 40px;
                background: white;
                border-radius: 10px;
                display: flex;
                justify-content: space-around;
                align-items: center;
            }
            .badge {
                text-align: center;
                padding: 20px;
            }
            .badge-icon {
                font-size: 48px;
                margin-bottom: 10px;
            }
            .badge-text {
                font-size: 16px;
                color: #666;
                font-weight: 600;
            }
            
            .footer {
                background: #2c3e50;
                color: white;
                padding: 40px;
                text-align: center;
                margin-top: 50px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">🛒 TechMart</div>
            <div class="nav">
                <a href="#products">Products</a>
                <a href="#deals">Deals</a>
                <a href="#support">Support</a>
                <a href="#cart">Cart (0)</a>
            </div>
        </div>
        
        <div class="hero">
            <h1>Summer Electronics Sale</h1>
            <p>Save up to 40% on premium electronics</p>
            <button class="cta-button">Shop Now</button>
        </div>
        
        <div class="products">
            <div class="product">
                <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Crect fill='%23667eea' width='200' height='120'/%3E%3Crect fill='%23333' y='120' width='200' height='80'/%3E%3C/svg%3E" alt="Laptop">
                <h3>UltraBook Pro</h3>
                <p>16GB RAM, 512GB SSD, Intel i7</p>
                <div>
                    <span class="old-price">$1,499</span>
                    <span class="price">$1,199</span>
                </div>
                <button>Add to Cart</button>
            </div>
            
            <div class="product">
                <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Ccircle cx='100' cy='100' r='80' fill='%23667eea'/%3E%3Ccircle cx='100' cy='100' r='50' fill='%23764ba2'/%3E%3C/svg%3E" alt="Headphones">
                <h3>NoiseCancel Pro</h3>
                <p>Active noise cancellation, 40hr battery</p>
                <div>
                    <span class="old-price">$349</span>
                    <span class="price">$279</span>
                </div>
                <!-- BUG #3: Missing "Add to Cart" button -->
            </div>
            
            <div class="product">
                <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Crect fill='%23667eea' x='30' y='20' width='140' height='160' rx='20'/%3E%3Crect fill='%23764ba2' x='50' y='40' width='100' height='120'/%3E%3C/svg%3E" alt="Phone">
                <h3>SmartPhone X</h3>
                <p>5G, 128GB, Triple camera system</p>
                <div>
                    <span class="old-price">$999</span>
                    <span class="price">$799</span>
                </div>
                <button>Add to Cart</button>
            </div>
        </div>
        
        <div class="trust-badges">
            <div class="badge">
                <div class="badge-icon">🚚</div>
                <div class="badge-text">Free Shipping</div>
            </div>
            <div class="badge">
                <div class="badge-icon">🔒</div>
                <div class="badge-text">Secure Payment</div>
            </div>
            <div class="badge">
                <div class="badge-icon">↩️</div>
                <div class="badge-text">30-Day Returns</div>
            </div>
            <!-- BUG #4: Missing 5-star badge -->
        </div>
        
        <div class="footer">
            <p>&copy; 2025 TechMart Electronics. All rights reserved.</p>
            <p>support@techmart.com | 1-800-555-TECH</p>
        </div>
    </body>
    </html>
    """
    return html

def save_demo_files():
    """Save HTML files"""
    Path("dmo_original.html").write_text(create_original_page())
    Path("demo_with_bugs.html").write_text(create_subtle_bugs_page())
    print("✅ Demo files created\n")

def run_demo():
    """Run the impressive demo"""
    
    save_demo_files()
    
    tester = VisualAITester()
    tester.print_banner()
    
    print("\n" + "="*80)
    print("🎯 IMPRESSIVE DEMO - Catching Subtle Visual Bugs")
    print("="*80)
    print("\n💡 THE CHALLENGE:")
    print("   Two pages that look NEARLY IDENTICAL to the human eye")
    print("   But contain CRITICAL bugs that would break the user experience")
    print("\n🤖 Can the AI catch what humans miss?\n")
    
    original_path = Path("impressive_demo_original.html").absolute()
    buggy_path = Path("impressive_demo_with_bugs.html").absolute()
    
    print("="*80)
    print("STEP 1: Capture Baseline (Original Page)")
    print("="*80)
    result1 = tester.run_test(
        url=f"file://{original_path}",
        test_name="techmart_homepage",
        threshold=0.95
    )
    
    print("\n" + "="*80)
    print("STEP 2: Test Updated Page (Looks The Same... Or Does It?)")
    print("="*80)
    print("\n🔍 BUGS HIDDEN IN THIS PAGE:")
    print("   Bug #1: CTA button shifted 10px right (off-center)")
    print("   Bug #2: Price color changed to red (should be purple)")
    print("   Bug #3: Missing 'Add to Cart' button on middle product")
    print("   Bug #4: Missing '5-Star Rated' trust badge")
    print("\n⚠️  These bugs are VERY subtle - easy to miss in manual review!")
    print("   Let's see if the AI catches them...\n")
    
    result2 = tester.run_test(
        url=f"file://{buggy_path}",
        test_name="techmart_homepage",
        threshold=0.95
    )
    
    # Generate report
    summary = tester.generate_report()
    
  
    
    return summary

if __name__ == "__main__":
    run_demo()