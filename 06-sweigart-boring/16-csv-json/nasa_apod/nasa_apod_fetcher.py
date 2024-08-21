import time
import sys, os
import pprint
from PIL import Image
from io import BytesIO
import webbrowser
import logging
import requests
import logging
logging.basicConfig(level=logging.INFO)

class NasaApodFetcher:

    IMAGE = 'image'
    VIDEO = 'video'
    MEDIA_TYPE = 'media_type'
    URL = 'url'
    DIRECTORY = 'apod_images'
    PREFIX = 'apod_'

    """
    Fetches the Astronomy Picture of the Day (APOD) from NASA's API:
    https://www.perplexity.ai/search/i-ve-done-a-simple-project-wit-k4j0uZc7SXGP9Yq8cyrZVQ

    Project Steps

    1. API Setup:
    - Sign up for a NASA Developer account to obtain an API key for accessing NASA's APIs.
    - Familiarize yourself with the APOD API documentation to understand the available endpoints and parameters.
    
    2. Program Structure:
    - The program will take a date as input from the command line to fetch the picture of the day for that specific date.
    - If no date is provided, the program will default to the current date.
    
    3. Data Retrieval:
    - Use the requests module to make an HTTP GET request to the APOD API endpoint with the specified date and API key.
    - Ensure that the response is successful and handle any potential errors.
    
    4. Data Processing:
    - Parse the JSON response to extract relevant information such as the image URL, title, and description.
    - Handle different media types (e.g., image, video) that the API might return.
    
    5. Display Content:
    - Use a library like PIL (Python Imaging Library) to display images if the media type is an image.
    - For videos or other media types, provide a link or use a web browser to open the content.
    
    6. Enhancements:
    - Add functionality to save the image locally with a filename based on the date.
    - Implement a feature to display the APOD for a range of dates and create a gallery.    

    """
    def __init__(self, 
                 api_key='nT42s3YGpdffPM4WpJtApeSpHb4uRVOmwJM2XGGk'):
        self._api_key = api_key
        self._date = sys.argv[1] if len(sys.argv) > 1 else time.strftime('%Y-%m-%d')
        self._url = f'https://api.nasa.gov/planetary/apod?date={self._date}&api_key={api_key}'
        self._media_json = None
        self._media_type = None
        self._media_url = None

    def fetch_media(self):
        """
        Fetch the Astronomy Picture of the Day (APOD) from NASA's API
        for the specified date.
        """
        # Download the JSON data from NASA's APOD API.
        logging.info(f'Fetching media for date: {self._date}...')
        response = requests.get(self._url)
        response.raise_for_status()
        self._media_json = response.json()
        self._media_type = self._media_json[self.MEDIA_TYPE]
        self._media_url = self._media_json[self.URL]
        logging.info(f'Media type: {self._media_type} Media URL: {self._media_url}')  

    def display_media(self, is_save=False):
        """
        Display the media content based on the media type.
        """
        if self._media_type == self.IMAGE:
            logging.info('Displaying image content...')
            self._display_and_save_image(is_save=is_save)
        elif self._media_type == self.VIDEO:
            logging.info('Displaying video content in a web browser...')
            self._display_video()
        else:
            raise ValueError('Unsupported media type.')
        
    def _display_and_save_image(self, is_save=False):
        """
        Display the image content with PIL (Python Imaging Library).
        """
        # Download the image content.
        response = requests.get(self._media_url)
        response.raise_for_status()

        # Create a directory to save the image  and 
        # save the image locally with a filename based on the date.
        # if is_save=True.
        if is_save:
            logging.info(f'Saving image for date: {self._date} \
                         to directory: {self.DIRECTORY} \
                         with filename: {self.PREFIX}{self._date}.jpg')
            os.makedirs(self.DIRECTORY, exist_ok=True)
            image_filename = f'{self.PREFIX}{self._date}.jpg'
            image_filename = os.path.join(self.DIRECTORY, image_filename)
            with open(image_filename, 'wb') as image_file:
                image_file.write(response.content)

        # Display the image content.
        image = Image.open(BytesIO(response.content))

        # Show the image.
        image.show()

    def _display_video(self):
        """
        Display the video content by opening the URL in a web browser.
        """
        webbrowser.open(self._media_url)

    def find_media(self, media_type=VIDEO):
        """
        Find the media content based on the media type.
        Iterate from the current date to the past date
        until the media type is found.
        """
        while self._media_type != media_type:
            self._date = self._get_previous_date()
            self._url = f'https://api.nasa.gov/planetary/apod?date={self._date}&api_key={self._api_key}'
            self.fetch_media()


    def _get_previous_date(self):
        """
        Get the previous date based on the current date.
        """
        current_date = time.strptime(self._date, '%Y-%m-%d')
        previous_date = time.mktime(current_date) - 86400
        previous_date = time.localtime(previous_date)
        previous_date = time.strftime('%Y-%m-%d', previous_date)
        print(f'Fetching media for date: {previous_date}')
        return previous_date
    
if __name__ == '__main__':
    fetcher = NasaApodFetcher()
    fetcher.fetch_media()
    fetcher.display_media()