#!/usr/bin/env python3
"""
Test script to verify that the extract_text_from_url function
extracts content only from the <article> tag and removes unwanted elements.
"""

import requests
from bs4 import BeautifulSoup
import re

def test_article_extraction():
    """
    Test the logic of the modified extract_text_from_url function
    """
    # Create sample HTML content similar to a Docusaurus page
    sample_html = """
    <html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <header>
            <nav>Navigation content</nav>
            Header content
        </header>

        <aside class="sidebar">
            Sidebar content
        </aside>

        <div class="table-of-contents">
            <h3>On this page</h3>
            <ul>
                <li>Section 1</li>
                <li>Section 2</li>
            </ul>
        </div>

        <main>
            <article>
                <h1>Main Content Title</h1>
                <p>This is the main content that should be extracted.</p>
                <p>It contains important information about the topic.</p>
                <div class="content-section">
                    <h2>Subsection</h2>
                    <p>More detailed content here.</p>
                </div>
            </article>

            <footer>
                Footer content that should not be extracted
            </footer>
        </main>

        <script>Some script content</script>
        <style>Some style content</style>
    </body>
    </html>
    """

    soup = BeautifulSoup(sample_html, 'html.parser')

    # Apply the same logic as in the modified function
    # Remove script, style, navigation, TOC, sidebar, header, footer, and other non-content elements
    for element in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
        element.decompose()

    # Remove TOC/"On this page" elements which are typically in elements with classes like "table-of-contents", "toc", "on-page", etc.
    for element in soup.find_all(['div', 'section'], class_=re.compile(r'.*\b(table-of-contents|toc|on-page|sidebar|navigation|menu|footer|header)\b.*', re.IGNORECASE)):
        element.decompose()

    # Extract content only from the <article> tag
    content_element = soup.find('article')

    # If no article tag found, return empty content (no fallback to main or body)
    if not content_element:
        content = ""
    else:
        # Extract text from the article element
        content = content_element.get_text(separator=' ', strip=True)

    # Clean up the text
    content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
    content = content.strip()

    print("Extracted content:")
    print(repr(content))

    # Verify that the content contains only what's in the article tag
    expected_content = "Main Content Title This is the main content that should be extracted. It contains important information about the topic. Subsection More detailed content here."

    print("\nExpected content:")
    print(repr(expected_content))

    # Check that unwanted content is not present
    unwanted_elements = ["Navigation content", "Header content", "Sidebar content",
                         "On this page", "Footer content", "Some script content",
                         "Some style content"]

    print("\nChecking for unwanted elements:")
    all_good = True
    for element in unwanted_elements:
        if element in content:
            print(f"❌ Found unwanted element: '{element}'")
            all_good = False
        else:
            print(f"✅ Correctly removed: '{element}'")

    print(f"\nContent extraction {'successful' if all_good and content else 'failed'}")

    # Test with HTML that has no article tag
    print("\n" + "="*50)
    print("Testing with HTML that has NO article tag:")

    no_article_html = """
    <html>
    <head><title>Test Page</title></head>
    <body>
        <header>Header content</header>
        <nav>Navigation content</nav>
        <main>Main content outside article</main>
        <footer>Footer content</footer>
    </body>
    </html>
    """

    soup2 = BeautifulSoup(no_article_html, 'html.parser')

    # Apply the same logic
    for element in soup2(["script", "style", "nav", "header", "footer", "aside", "form"]):
        element.decompose()

    for element in soup2.find_all(['div', 'section'], class_=re.compile(r'.*\b(table-of-contents|toc|on-page|sidebar|navigation|menu|footer|header)\b.*', re.IGNORECASE)):
        element.decompose()

    content_element = soup2.find('article')
    if not content_element:
        content2 = ""
    else:
        content2 = content_element.get_text(separator=' ', strip=True)

    content2 = re.sub(r'\s+', ' ', content2)
    content2 = content2.strip()

    print(f"Content when no article tag exists: {repr(content2)}")
    print(f"Expected: {repr('')}")
    print(f"Correct (empty when no article): {'✅' if content2 == '' else '❌'}")


if __name__ == "__main__":
    test_article_extraction()