"""
Test URLs for validating the ingestion pipeline.
These can be used for testing the pipeline with real documentation sites.
"""

# Example documentation sites that can be used for testing
TEST_DOC_SITES = [
    # Add documentation sites here for testing
    # "https://docusaurus.io/docs",  # Docusaurus documentation itself
    # "https://reactjs.org/docs",    # React documentation
    # "https://docs.python.org/3/",  # Python documentation
]

# For testing purposes, we can also create a simple test document
TEST_DOCUMENTATION_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Documentation Page</title>
</head>
<body>
    <nav class="navbar">
        <ul>
            <li>Home</li>
            <li>Docs</li>
            <li>API</li>
        </ul>
    </nav>

    <div class="main-wrapper">
        <div class="doc-page">
            <h1>Test Documentation</h1>
            <p>This is a test documentation page for validating the ingestion pipeline.</p>
            <p>The pipeline should extract this content and ignore navigation elements.</p>

            <h2>Section 1: Introduction</h2>
            <p>This section provides an introduction to the test documentation.</p>

            <h2>Section 2: Features</h2>
            <p>This section describes the features of the test system.</p>

            <div class="code-block">
                <pre>code example</pre>
            </div>

            <footer class="footer">
                <p>Footer content should be ignored</p>
            </footer>
        </div>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    print("Test documentation URLs for the ingestion pipeline:")
    for url in TEST_DOC_SITES:
        print(f"  - {url}")