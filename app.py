from flask import Flask, request, Response
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return 'PostMe! PDF!!'

@app.route('/Test', methods = ['GET'])
def test():
    with sync_playwright() as p:
        with p.chromium.launch() as browser:
            with browser.new_context(ignore_https_errors = True) as context:
                page = context.new_page()
                page.set_content('<p>Test</p>')
                data = page.pdf(format = 'A4', print_background = True)
                return Response(response = data, status = 200, mimetype = 'application/pdf')

@app.route('/PDFURL', methods = ['GET'])
def pdfFromURL():
    dataUrl = request.args['dataUrl']
    if dataUrl is not None:
        with sync_playwright() as p:
            with p.chromium.launch() as browser:
                with browser.new_context(ignore_https_errors = True) as context:
                    page = context.new_page()
                    if 'Authorization' in request.headers:
                        authorization = request.headers['Authorization']
                        page.set_extra_http_headers({'Authorization': f'Bearer {authorization}'})
                    page.goto(dataUrl)
                    page.wait_for_load_state('networkidle')
                    data = page.pdf(format = 'A4', print_background = True)
                    return Response(response = data, status = 200, mimetype = 'application/pdf')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001)
