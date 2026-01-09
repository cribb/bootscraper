import unittest
from crawl import *

class TestCrawl(unittest.TestCase):
    def test_normalize_url_1(self):
        input_url = ""
        expected_output = ""                    
        actual = normalize_url(input_url)
        self.assertEqual(actual, expected_output)

    def test_normalize_url_2(self):
        input_url = "/"                     
        expected_output = ""                    
        actual = normalize_url(input_url)
        self.assertEqual(actual, expected_output)

    def test_normalize_url_3(self):
        input_url = "https://blog.boot.dev/path"
        expected_output = "blog.boot.dev/path"
        actual = normalize_url(input_url)
        self.assertEqual(actual, expected_output)

    def test_normalize_url_4(self):
        input_url = "http://blog.boot.dev/path/"
        expected_output = "blog.boot.dev/path"
        actual = normalize_url(input_url)
        self.assertEqual(actual, expected_output)

    def test_get_h1_from_html_1(self):
        input = ""
        result = ""        
        actual = get_h1_from_html(input)
        self.assertEqual(actual, result)

    def test_get_h1_from_html_2(self):
        input = "<h1>Header 1 Text</h1>" # testing for actual content
        result = "Header 1 Text"        
        actual = get_h1_from_html(input)
        self.assertEqual(actual, result)

    def test_get_h1_from_html_3(self):
        input = "<h2>Header 2 Text</h2>" # testing for absent content
        result = ""
        actual = get_h1_from_html(input)
        self.assertEqual(actual, result)

    def test_get_h1_from_html_4(self):
        input = "<html><body><h1>Test Title</h1></body></html>" # nested content
        result = "Test Title"
        actual = get_h1_from_html(input)
        self.assertEqual(actual, result)

    def test_get_h1_from_html_5(self):
        input = """ <html>
                        <body>
                            <h1>Welcome to Boot.dev</h1>
                            <main>
                            <p>Learn to code by building real projects.</p>
                            <p>This is the second paragraph.</p>
                            </main>
                        </body>
                    </html> """
        result = "Welcome to Boot.dev"
        actual = get_h1_from_html(input)
        self.assertEqual(actual, result)

    def test_get_first_paragraph_from_html_1(self):
        input = "<p></p>"
        result = ""           
        actual = get_first_paragraph_from_html(input)
        self.assertEqual(actual, result)

    def test_get_first_paragraph_from_html_2(self):
        input = "<p> When in the course of human events </p>"
        result = "When in the course of human events"           
        actual = get_first_paragraph_from_html(input)
        self.assertEqual(actual, result)

    def test_get_first_paragraph_from_html_3(self):
        input = "<p id='foo'>To be or not to be</p>"
        result = "To be or not to be"        
        actual = get_first_paragraph_from_html(input)
        self.assertEqual(actual, result)

    def test_get_first_paragraph_from_html_4(self):
        input = "<p> Excelsior!"
        result = "Excelsior!"          
        actual = get_first_paragraph_from_html(input)
        self.assertEqual(actual, result)

    def test_get_first_paragraph_from_html_5(self):
        input = "<p>This is the first paragraph.</p><p id='bar'>This is the second paragraph.<p>"
        result = "This is the first paragraph."         
        actual = get_first_paragraph_from_html(input)
        self.assertEqual(actual, result)

    def test_get_first_paragraph_from_html_6(self):
        input = "<html><body><p>Test paragraph.</p></body></html>"
        result = "Test paragraph."           
        actual = get_first_paragraph_from_html(input)
        self.assertEqual(actual, result)

    def test_get_first_paragraph_from_html_7(self):
        input = '''<html><body>
                        <p>Outside paragraph.</p>
                        <main>
                            <p>Main paragraph.</p>
                        </main>
                    </body></html>'''
        result = "Main paragraph."         
        actual = get_first_paragraph_from_html(input)
        self.assertEqual(actual, result)

    def test_get_urls_from_html_1(self):
        input_url = "https://blog.boot.dev"
        input_body = ''
        expected = []
        actual = get_urls_from_html(input_body, input_url)
        self.assertListEqual(actual, expected)

    def test_get_urls_from_html_2(self):
        input_url = "https://blog.boot.dev"
        input_body = '<a/>'
        expected = ['https://blog.boot.dev']
        actual = get_urls_from_html(input_body, input_url)
        self.assertListEqual(actual, expected)
    
    def test_get_urls_from_html_3(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'                      
        expected = ['https://blog.boot.dev']
        actual = get_urls_from_html(input_body, input_url)
        self.assertListEqual(actual, expected)

    def test_get_urls_from_html_4(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="/foobar"><span>Boot.dev</span></a></body></html>'
        expected = ['https://blog.boot.dev/foobar']
        actual = get_urls_from_html(input_body, input_url)
        self.assertListEqual(actual, expected)
    
    def test_get_urls_from_html_5(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="/foobar/"><span>Boot.dev</span></a></body></html>'
        expected = ['https://blog.boot.dev/foobar/']
        actual = get_urls_from_html(input_body, input_url)
        self.assertListEqual(actual, expected)

    def test_get_images_from_html(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)
    
    def test_extract_page_data_basic(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
                            <h1>Test Title</h1>
                            <p>This is the first paragraph.</p>
                            <a href="/link1">Link 1</a>
                            <img src="/image1.jpg" alt="Image 1">
                        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)
            
if __name__ == "__main__":
    unittest.main()

