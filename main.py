from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

class MyGPS(GridLayout):
    def __init__(self, **kwargs):
        super(MyGPS, self).__init__(**kwargs)
        self.set_values()

    def set_values(self, **kwargs):
        latitude, longitude, location_name, accuracy = self.getLocation()
        #latitude = "49.58311130"
        #longitude = "11.00884270"
        #location_name = "91052, Erlangen, Bavaria, Rathenau, ... , und mehr"
        #accuracy = "15m (accurate)"
        #print(f'There are {len(self.ids.items())} id(s)')
        self.ids.Latitude.text = latitude
        self.ids.Longitude.text = longitude
        self.ids.Location.text = location_name
        self.ids.Accuracy.text = accuracy

    def getLocation(self):
        chrome_options = Options()
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        timeout = 20
        driver = webdriver.Chrome()
        driver.get("https://mycurrentlocation.net/")
        wait = WebDriverWait(driver, timeout)
        time.sleep(3)
        # Click the "Detect My Location" button
        driver.find_elements(By.XPATH, '/html/body/div[2]/div[4]/div/div[1]/div/div[1]/div/button')[0].click()
        # Click the "Alert Pop-Up" with the text "Yeeay location found!"
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        driver.switch_to.alert.accept()

        longitude = driver.find_elements(By.ID, 'detail-longitude')
        longitude = [x.text for x in longitude]
        longitude = str(longitude[0])

        latitude = driver.find_elements(By.ID, 'detail-latitude')
        latitude = [x.text for x in latitude]
        latitude = str(latitude[0])

        location_name = driver.find_elements(By.ID, 'detail-location-name')
        location_name = [x.text for x in location_name]
        location_name = str(location_name[0])

        accuracy = driver.find_elements(By.ID, 'detail-accuracy')
        accuracy = [x.text for x in accuracy]
        accuracy = str(accuracy[0])

        driver.quit()

        return (latitude, longitude, location_name, accuracy)


class MyLocation(App):
    def build(self):

        return MyGPS()



if __name__ == '__main__':
    app = MyLocation()
    app.run()

