from flask import Flask, render_template  
from apscheduler.schedulers.background import BackgroundScheduler
import os
import shutil
from datetime import datetime
import requests

# creating a Flask application 
app = Flask(__name__) 

# GLOBAL VARS
IMAGE_DIR = "static/images"
CURRENT_IMAGE = os.path.join(IMAGE_DIR, "current.jpg")


# SCHEDULE USING SCHEDULER
# Schedule the actions
scheduler = BackgroundScheduler()

def get_posts(api_key):
    # API KEY IS ENCRYPTED
    limit = 24
    endpoint_url = f'https://api.thecatapi.com/v1/images/search?limit={limit}&api_key={api_key}'
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
    

# Get 24 random cat images at midnight (before a bit, not to confuse the algorithm below)
@scheduler.scheduled_job('cron', hour=23, minute=57)
def update_images_dir():
    # all the images as paths (for use later, to delete)
    all_old_images_paths = [os.path.join(IMAGE_DIR, img) for img in os.listdir(IMAGE_DIR)]
    
    # get the json object from api
    list_of_img_info = get_posts()
        
        
    
    
    
    pass


# Updating the image

@scheduler.scheduled_job('interval', hour=1)
def update_cur_image(used_images) -> str:
    """This functions is called to update the currently displayed image to a new one 
    """
    # get the current list of images ( not the current one and the used ones)
    available_images = [img for img in os.listdir(IMAGE_DIR) 
                                if img != "current.jpg" and img not in used_images]
    
    if available_images:
        # get a new
        new_image = available_images.pop()
        
        new_image_path = os.path.join(IMAGE_DIR, new_image)
        
        # update current image
        shutil.copy(new_image_path, CURRENT_IMAGE)  # Replace current.jpg with the new image
        
        # log print
        print(f"[ {datetime.now()} ] Image updated to: {new_image}")


# This updates the current pool of images in static/images from the API

scheduler.start()
    
    
    
@app.route("/") 
def home(): 
    
    
    cat_description = 'cat cat cat'
    return render_template('home.html',  
                           cat_foto=CURRENT_IMAGE) 
  
# run the application 
if __name__ == "__main__": 
    app.run(debug=True)