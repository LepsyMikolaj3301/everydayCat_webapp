from flask import Flask, render_template  
import schedule
import os
from datetime import datetime
import requests
from dotenv import load_dotenv
import json


# creating a Flask application 

app = Flask(__name__) 
load_dotenv()


# GLOBAL STATIC VARS

IMAGE_DIR = "static/cat_info/"
API_KEY_CATS = os.getenv('API_KEY_CATS')
 

def get_posts() -> list:
    # API KEY IS ENCRYPTED
    
    endpoint_url = f'https://api.thecatapi.com/v1/images/search?limit={limit}&api_key={API_KEY_CATS}'
    try:
        # MAKE GET REQUEST TO THE API
        response = requests.get(endpoint_url)
        
        # Is the request successful:
        if response.status_code == 200:
            return response.json()
        else:
            print(f'ERROR: {response.status_code}')
            return None
    except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions
        print('ERROR - OTHER:', e)
        return None
   

class CurrentPhotos():
    def __init__(self):
        self._current_day_cats: list = json.load(IMAGE_DIR + 'current_day_cats.json')
        self._cur_cat_index = 1
        self._current_cat = self._current_day_cats[0]  
        
    def update_images_dir(self):
    
        with open(IMAGE_DIR + 'current_day_cats.json', 'w') as file_current_cats, open(IMAGE_DIR + 'last_day_cats.json', 'w') as file_last_cats:
            # loading in the info of last cats (last day)
            cat_photos_to_be_changed = json.load(file_current_cats)
            
            try:
                # get the json object from api (for today)
                current_day_cats = get_posts()
                
                # saving the last cats to the last json
                json.dump(cat_photos_to_be_changed, file_last_cats, indent=6)
                
                if current_day_cats:
                    json.dump(current_day_cats, file_current_cats, indent=6)
                    print(f'CATS SUCCESSFULLY UPDATED AT {datetime.now()}')
                else:
                    raise Exception("Error with API")
            except Exception as e:
                print(f'Something went wrong :( - {e}')
                # if something gets wrong - stay with old photos
                json.dump(cat_photos_to_be_changed, file_current_cats, indent=6)

        # IN the end - update the index
        self._cur_cat_index = 0
        
        
    def update_cur_image(self):
        """This functions is called to update the currently displayed image to a new one 
        """
        # get the next cat info and image
        with open(IMAGE_DIR + 'current_day_cats.json') as file_current_cats:
            self._current_day_cats = json.load(file_current_cats)
            
        
        if self._current_day_cats:
            
            # UPDATE CURRENT CAT
            self._current_cat = self._current_day_cats[self._cur_cat_index]
            
            # log print
            print(f"[ {datetime.now()} ] Image updated to (cat ID): {self._current_cat['id']}")
            
            # update the index
            self._cur_cat_index += 1
            
    def get_curr_cat(self) -> dict:
        return self._current_cat

# Schedule all tasks:
cur_ph = CurrentPhotos()
schedule.every().hour.do(cur_ph.update_cur_image())
# Get 24 random cat images at midnight
schedule.every().day.at('23:55').do(cur_ph.update_images_dir())
 
    
@app.route("/") 
def home(): 
    
    cat = cur_ph.get_curr_cat()
    cat_description = 
    
    return render_template('home.html',  
                           cat_foto=cat['url']) 
  
def test():
    # update_images_dir()
    pass
    
    
# run the application 
if __name__ == "__main__": 
    # app.run(debug=True)
    test()