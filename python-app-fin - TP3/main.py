from flask import Flask, request, redirect, url_for, jsonify
import time
import logging
import requests
import re
from collections import Counter
import matplotlib.pyplot as plt
import io
import base64
from pytrends.request import TrendReq
 
 
 

 
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


@app.route('/google-trends', methods=['GET'])

def google_trends():

    # Create a pytrends client

    pytrends = TrendReq(hl='en-US', tz=360, geo='FR')

 

    # Define your keywords and timeframe

    keywords = ['Deloitte', 'CapGemini']

    timeframe = 'today 3-m'  # You can customize the timeframe

 

    # Get Google Trends data

    pytrends.build_payload(keywords, timeframe=timeframe)

    interest_over_time_df = pytrends.interest_over_time()

 

    # Process the data or return it as JSON, HTML, etc.

    # For example, you can return the data as JSON:

    data = interest_over_time_df.to_json(orient='split')

 

    return data

 

 @app.route('/chart-image')

def chart_image():

    # Create a pytrends client and fetch data as previously mentioned

    pytrends = TrendReq(hl='en-US', tz=360, geo='FR')

    keywords = ['Deloitte', 'CapGemini']

    timeframe = 'today 3-m'

    pytrends.build_payload(keywords, timeframe=timeframe)

    interest_over_time_df = pytrends.interest_over_time()

 

    # Create a time series chart

    plt.figure(figsize=(10, 6))

    for keyword in keywords:

        plt.plot(interest_over_time_df.index, interest_over_time_df[keyword], label=keyword)

    plt.xlabel('Date')

    plt.ylabel('Interest Over Time')

    plt.title('Google Trends Comparison')

    plt.legend()


    # Save the chart as an image

    img_buffer = io.BytesIO()

    plt.savefig(img_buffer, format='png')

    img_buffer.seek(0)

    img_data = base64.b64encode(img_buffer.read()).decode()

 

    return f'<img src="data:image/png;base64,{img_data}" alt="Google Trends Chart">'

def count_words_with_dict(text):
    word_count = {}
    words = re.findall(r'\w+', text)
    for word in words:
        word = word.lower()
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def count_words_with_counter(text):
    words = re.findall(r'\w+', text)
    word_count = Counter(word.lower() for word in words)
    return word_count

# Example usage:
shakespeare_text = "Your Shakespeare text goes here..."
word_count = count_words_with_counter(shakespeare_text)
print(word_count)

@app.route('/count_words_and_chart')
def count_words_and_chart():
    # Download Shakespeare's text
    shakespeare_url = "https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt"
    response = requests.get(shakespeare_url)
    shakespeare_text = response.text

    # Count word frequency using a dictionary
    word_count_dict = count_words_with_dict(shakespeare_text)

    # Count word frequency using Counters
    word_count_counter = count_words_with_counter(shakespeare_text)

    # Create the chart image
    plt.figure(figsize=(10, 6))
    plt.plot(word_count_dict.keys(), word_count_dict.values(), label='Word Count (Dictionary)')
    plt.plot(word_count_counter.keys(), word_count_counter.values(), label='Word Count (Counter)')
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.title('Word Count Comparison')
    plt.legend()

    # Save the chart as an image
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_data = base64.b64encode(img_buffer.read()).decode()

    return f'<img src="data:image/png;base64,{img_data}" alt="Word Count Chart">'


def execution_time_logger(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.chart_image()}' took {execution_time:.6f} seconds to execute.")
        return result
    return wrapper

# Apply the decorator to a specific route
@app.route('/time')
@execution_time_logger
def route_to_measure_time():
    # code 
    return "Response"

@app.route('/root')

def root():

    return "Hello from Space! 🚀"

 

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8080)
     