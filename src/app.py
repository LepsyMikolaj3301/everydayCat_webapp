from flask import Flask 
from flask import render_template 
  
  

# creates a Flask application 
app = Flask(__name__) 
  
  
@app.route("/") 
def home_cat(): 
    
    
    cat_description = 'cat cat cat'
    return render_template('home.html',  
                           cat_description=cat_description) 
  
# run the application 
if __name__ == "__main__": 
    app.run(debug=True)