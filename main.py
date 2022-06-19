from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import json

keys = open('keys.json')
keysData = json.load(keys)

class InstaBot:
    def __init__(self):
        self.username = keysData['USERNAME']
        self.password = keysData['PASSWORD']
        self.driver = webdriver.Chrome()
        self.driver.get("https://instagram.com")
        sleep(5)
        self.driver.find_element(By.XPATH , "//input[@name=\"username\"]").send_keys(self.username)
        self.driver.find_element(By.XPATH, "//input[@name=\"password\"]").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(15)
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()
        sleep(5)

    def get_non_mutuals(self):

        self.driver.find_element(By.XPATH, "//a[contains(@href, '/{}')]".format(self.username)).click()
        sleep(25)


        self.driver.find_element(By.XPATH, "//a[contains(@href, '/following')]").click()   
        sleep(10) 

        following = self._get_names(True);

        print("Following: ", following)

        self.driver.find_element(By.XPATH, "//a[contains(@href, '/followers')]").click()   
        sleep(10) 

        followers = self._get_names(False);

        print("Followers: ", followers)

        not_following_back = [user for user in following if user not in followers]

        print("Not Following Back: ", not_following_back)

    def _get_names(self, following):

        if following:
            scroll_box = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]")
        else:
            scroll_box = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]")
                                                            
        sleep(1)

        last_ht, ht, i = 0,1,0
        while last_ht != ht:
            last_ht = ht
            i = i+1
            print("Iteration ", i)
            sleep(2)
            ht = self.driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scroll_box)

        links = scroll_box.find_elements(By.TAG_NAME, 'a')
        sleep(2)
        names = [name.text for name in links if name.text != '']

        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[3]/div/button").click()
        
        return names

bot = InstaBot()
bot.get_non_mutuals()