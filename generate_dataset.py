from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from PIL import Image
from io import BytesIO
import timeit
import base64
import uuid
import sys

# chrome driver configuration for selenium
CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_argument('--headless')
CHROME_OPTIONS.add_argument('--no-sandbox')
CHROME_OPTIONS.add_argument('lang')
CHROME_OPTIONS.add_argument("--disable-gpu")
CHROME_OPTIONS.add_argument("start-maximized")
CHROME_OPTIONS.add_argument('--disable-dev-shm-usage')


def extract_catpcha_image(captcha_page_url: str) -> Image:
    """
    Extract the captcha image from a webpage and generates a PIL Image.
    (you should customize this function for your specific webpage)
    
    :param captcha_page_url: url to the page that contains the captcha 
    :return: A PIL image
    """""
    browser = webdriver.Chrome(options=CHROME_OPTIONS)
    browser.get(captcha_page_url)
    base64_img_data = browser.find_element_by_xpath("//td[@align='right']/img[@height='24']").get_attribute('src')
    parsed_base64_data = base64_img_data.replace('data:image/png;base64,', '')
    browser.close()
    return Image.open(BytesIO(base64.b64decode(parsed_base64_data)))


def save_image(image: Image):
    """
    Saves the given image.
    (you can customize this function to save on another location or upload the image to the cloud)
    :param image: that will be saved
    """
    image.save('./dataset/captcha_{}.png'.format(uuid.uuid1()))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception('It is required to pass the link to extract the captcha as a command line argument. '
                        'Try running: python3 generate_dataset.py [PAGE_URL] [TOTAL_CAPTCHAS_TO_COLLECT]')
    captcha_page_url = sys.argv[1]
    total_captchas = int(sys.argv[2])
    print('#### Captcha dataset generator ####')
    print('scrapping captchas from {}'.format(captcha_page_url))

    for index in range(total_captchas):
        start_time = timeit.default_timer()
        captcha_image = extract_catpcha_image(captcha_page_url)
        save_image(captcha_image)
        print('captcha {} extracted in {:.2f} seconds'.format(index, timeit.default_timer() - start_time))
