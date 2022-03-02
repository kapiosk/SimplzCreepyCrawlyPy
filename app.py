from flask import Flask, make_response, request
from playwright.sync_api import sync_playwright

#playwright install
#playwright install-deps 
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'PostMe! PDF!!'

@app.route('/PDFURL', methods=['GET'])
def pdfFromURL():
    dataUrl = request.args.get('dataUrl')
    if dataUrl is not None:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("https://playwright.dev")
            print(page.title())
            browser.close()
    resp = make_response()
    return resp

# def CreateResponse(html, fileName):
#     resp = make_response()
#     if fileName is None:
#         fileName = 'temp.pdf'
#     pdf = weasyprint.HTML(string=html)
#     resp.data = pdf.write_pdf()
#     resp.headers['Content-Disposition'] = f'attachment; filename="{fileName}"'
#     resp.headers['Content-Type'] = 'application/pdf'
#     return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)