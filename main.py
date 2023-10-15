from flask import Flask, request, redirect, url_for, jsonify

import logging

import requests

 

 
app = Flask(__name__)

@app.route("/")

def hello_world():
   prefix_google = """
   <!-- Google tag (gtag.js) -->
   <script async
   src="https://www.googletagmanager.com/gtag/js?id=G-9TRYDPP9GX"></script>
   <script>
   window.dataLayer = window.dataLayer || [];
   function gtag(){dataLayer.push(arguments);}
   gtag('js', new Date());
   gtag('config', 'G-9TRYDPP9GX');
   </script>
   """
   message = "Hello World 🚀"

   button_google = '''

    <form action="/make_google_request" method="get">

        <input type="submit" value="Fetch Google Cookies">

    </form>

    '''

   button_ganalytics = '''

    <form action="/make_ganalytics_request" method="get">

        <input type="submit" value="Fetch Google Analytics Data">

    </form>

    '''

   button_ganalytics_data = '''

    <form action="/get_ganalytics_data" method="get">

        <input type="submit" value="Obtenir le nombre de visiteurs depuis Google Analytics">

    </form>

    '''

   return prefix_google + message + "<br>" + button_google + button_ganalytics + button_ganalytics_data

   logging.basicConfig(level=logging.DEBUG)

 

@app.route('/logger')
def logger():
    # Print a log in the Python console
    print("This is a Python log message")

    # Print a log in the browser console using JavaScript
    return """
    <script>
         console.log("This is a browser log message");
     </script>
     """
   
     
@app.route('/make_google_request')

def make_google_request():

    req = requests.get("https://www.google.com/")

    cookies = req.cookies._cookies

    cookies_str = "\n".join([f"{i} {j} {k} {cookies[i][j][k].value}" for i in cookies for j in cookies[i] for k in cookies[i][j]])

    return cookies_str

 

@app.route('/make_ganalytics_request')

def make_ganalytics_request():
   ganalytics_url = "https://analytics.google.com/analytics/web/#/p407803949/reports/intelligenthome?params=_u..nav%3Dmaui"

   req = requests.get(ganalytics_url)

   

    # Display the status code

   status_code = req.status_code

   

    # Display the response text

   response_text = req.text

   

   return jsonify(status_code=status_code, text=response_text)


 

@app.route('/root')

def root():

    return "Hello from Space! 🚀"

 

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8080)
     