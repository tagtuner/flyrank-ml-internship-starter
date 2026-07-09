import os
import asyncio
from playwright.async_api import async_playwright

async def main():
    # Paths to local HTML mockups
    work_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "work"))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "charts"))
    
    os.makedirs(output_dir, exist_ok=True)
    
    files_to_capture = [
        ("sitemap_sketch.html", "sitemap_sketch.png", (920, 720)),
        ("claude_project_v2_mockup.html", "claude_project_v2_config.png", (1200, 800)),
        ("claude_chat_pressure_test.html", "claude_pressure_test_chat.png", (1200, 800)),
        ("identity_kit.html", "identity_kit.png", (920, 850)),
        ("../index.html", "empty_but_live.png", (920, 720)),
        ("mcp_showcase_mockup.html", "mcp_evidence.png", (920, 900)),
        ("../pfsense_audit.html", "case_study.png", (1200, 1000)),
        ("../audit_booking.html", "booking_page.png", (1200, 800))
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for html_name, png_name, viewport in files_to_capture:
            page = await browser.new_page(viewport={"width": viewport[0], "height": viewport[1]})
            file_url = f"file:///{os.path.join(work_dir, html_name).replace(os.sep, '/')}"
            print(f"Loading {file_url}...")
            await page.goto(file_url, wait_until="networkidle")
            # Wait a split second to ensure Google Fonts render properly
            await asyncio.sleep(1.0)
            
            output_path = os.path.join(output_dir, png_name)
            await page.screenshot(path=output_path, full_page=False)
            print(f"Captured screenshot: {output_path}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
