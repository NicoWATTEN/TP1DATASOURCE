from flask import Flask, request, jsonify

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
   return prefix_google + "Hello World"

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
   
if __name__ == "__main__":
     app.run()