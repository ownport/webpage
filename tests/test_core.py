TEST_CONTENT = '''
<html>
    <head>
        <link rel="image_src" href="http://example.com/img1.jpg" />
        <meta property="og:image" content="http://example.com/img2.jpg" />
        <link rel="canonical" href="http://example.com/index1.html">
    </head>
    <body>
        <a href="http://example.com/index.html">Home</a>
        <a href="http://example.com/articles.html">Articles</a>
        <img src="http://localhost:8888/logo.jpg" />
    </body>
</html>
'''

TEST_URL_LIST = [
    'http://example.com/img1.jpg', 'http://example.com/index1.html', 
    'http://example.com/index.html', 'http://example.com/articles.html', 
    'http://localhost:8888/logo.jpg',
]

TEST_OFFLINE_URL_LIST = [
    'files/example.com-img1.jpg', 'files/example.com-index1.html', 
    'files/example.com-index.html', 'files/example.com-articles.html',
    'files/localhost-8888-logo.jpg',
]
