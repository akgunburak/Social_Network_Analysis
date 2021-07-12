import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time


class scrape:
    def __init__(self):
        self.browser = webdriver.Chrome("C:/Users/burak/Desktop/chromedriver.exe")
        self.link = ("https://www.instagram.com")

        self.browser.delete_all_cookies()
        self.browser.maximize_window()

    
    # Methods for waiting the elements to be installed
    def wait_for_object(self, type, string):
        return WebDriverWait(self.browser, 10).until(ec.presence_of_element_located((type, string)))

    def wait_for_objects(self, type, string):
        return WebDriverWait(self.browser, 10).until(ec.presence_of_all_elements_located((type, string)))

    def wait_for_click(self, type, string):
        return WebDriverWait(self.browser, 10).until(ec.element_to_be_clickable((type, string)))


    # A method for login
    def login(self, username, password):
        
        # Going to the instagram page
        self.browser.get(self.link)  
        
        # Selecting the username and password fields
        inputs = self.wait_for_objects(By.CSS_SELECTOR, '._2hvTZ.pexuQ.zyHYP')  
        inputs[0].send_keys(username)  # Entering the username
        inputs[1].send_keys(password)  # Entering the password
        
        # Waiting for 1 second
        time.sleep(1)  
        
        # Clicking the enter after typing the username and password           
        inputs[1].send_keys(Keys.ENTER)
     
    
    # Defining scroll down method since without scrolling down, elements won't be installed
    def scroll_down_followers(self):
        command = """
        page = document.querySelector(".isgrP");
        page.scrollTo(0,page.scrollHeight);
        var end_page = page.scrollHeight;
        return end_page;
        """
        end_page = self.browser.execute_script(command)
        return(end_page)
    
    
    # A method to get names of the followers
    def get_followers(self, page, n_followers=999999999999999):
        
        # Going to page that we want to scrape
        self.browser.get(self.link + "/" + page)
        
        # Wait for the page to upload
        wait = self.wait_for_objects(By.CSS_SELECTOR, '.XjzKX')
        
        # Checking if element that contains 'this account is private' exist
        try:
            private = [self.browser.find_element_by_css_selector('.rkEop')]
        except:
            private = []
            pass
        
        if private != []:
            pass
        else:
            # Waiting until followers box to be installed
            self.wait_for_click(By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
            
            # Wait for openning the box
            self.wait_for_objects(By.CSS_SELECTOR, '.FPmhX.notranslate._0imsa')
            
            # Scrolling down to the end of the page
            end_page = self.scroll_down_followers()
            while True:
                end = end_page 
                time.sleep(1)
                end_page = self.scroll_down_followers()
                if end == end_page or len(self.wait_for_objects(By.CSS_SELECTOR, '.FPmhX.notranslate._0imsa')) >= n_followers:
                    break
            
            # Getting the usernames of the followers
            followers = self.wait_for_objects(By.CSS_SELECTOR, '.FPmhX.notranslate._0imsa')
            followers = [follower.text for follower in followers]
    
            return(followers)


    # A method to get relations between followers
    def get_relations(self, page, n_followers):
        
        # Getting the followers of page
        followers = self.get_followers(page, n_followers)
        
        # Creating a dataframe to hold the relations
        relations = pd.DataFrame(columns=["source", "target"])
        
        # Getting followers of each follower
        for follower in followers:
            try:
                temp_df = pd.DataFrame(columns=["source", "target"])
                temp_df["target"] = self.get_followers(follower)
                temp_df["source"] = follower
                relations = pd.concat([relations, temp_df])
            except:
                pass
            time.sleep(0.5)
        
        return(relations)


    # A method for formatting the numbers
    def format_numbers(self, number):
        if "," in number:
            number = number.replace(',', '')
        if "k" in number:
            if "." in number:
                number = number.replace('.', '')
                number = number.replace('k', '00')
            else:
                number = number.replace('k', '000')
        if "m" in number:
            if "." in number:
                number = number.replace('.', '')
                number = number.replace('m', '00000')
            else:
                number = number.replace('m', '000000')
        return(int(number))


    # A method to get meta-data of posts
    def get_metadata(self, page, top_n="all"):
        
        # Going to page that we want to scrape
        self.browser.get(self.link + "/" + page)  
                
       # Creating the lists to hold the data
        number_of_comments = []
        number_of_likes = []
        urls = []
        captions = []
        
        # Finding the elements those contain needed data
        pictures = self.wait_for_objects(By.CSS_SELECTOR, '.KL4Bh')
        
        try:
            for picture in pictures:
                time.sleep(1)
                
                # Right click on the picture to make visible the comment and like numbers
                action_chains = ActionChains(self.browser)
                action_chains.context_click(picture).perform()
                
                # Getting the urls of pictures
                url = picture.find_element_by_class_name('FFVAD').get_attribute("src")
                urls.append(url)
                
                # Getting the captions of pictures
                caption = picture.find_element_by_class_name('FFVAD').get_attribute("alt")
                captions.append(caption)
                
                # Getting the number of likes and comments 
                likes_comments = self.wait_for_objects(By.CSS_SELECTOR, '.-V_eO')
                if len(likes_comments) == 2:
                    number_of_comments.append(likes_comments[1].text)
                    number_of_likes.append(likes_comments[0].text)
                if len(likes_comments) == 1:
                    number_of_comments.append(likes_comments[0].text)
                    number_of_likes.append("0")
                    
        except:
            pass
        
        # While we keep right clicking on the pictures, new picture elements will become
        # visible when we come closer to the end of the page since the IG pages are dynamic.
        # So we will take picture elements and collect the data, once we do that, page will
        # be scrolled down and new elements will be visible. At each iteration we will compare
        # picture elements before scrolling and after scrolling, and collect the data 
        # from elements lastly loaded.
        while True:
            
            # Finding the elements those contain needed data
            pictures_2 = self.wait_for_objects(By.CSS_SELECTOR, '.KL4Bh')
            
            # Finding the pictures that loaded after scrolling down
            diff = [item for item in pictures_2 if item not in pictures]
            
            try:
                for picture in diff:
                    # Right click to the picture to make visible the comment and like numbers
                    action_chains = ActionChains(self.browser)
                    action_chains.context_click(picture).perform()
                    
                    # Getting the urls of pictures
                    url = picture.find_element_by_class_name('FFVAD').get_attribute("src")
                    urls.append(url)
                    
                    # Getting the captions of pictures
                    caption = picture.find_element_by_class_name('FFVAD').get_attribute("alt")
                    captions.append(caption)
                    
                    # Getting the number of likes and comments 
                    likes_comments = self.wait_for_objects(By.CSS_SELECTOR, '.-V_eO')
                    if len(likes_comments) == 2:
                        number_of_comments.append(likes_comments[1].text)
                        number_of_likes.append(likes_comments[0].text)
                    if len(likes_comments) == 1:
                        number_of_comments.append(likes_comments[0].text)
                        number_of_likes.append("0")
                    
            except:
                pass
            
            # If there is no data loaded after scrolling down, that means we are at the end 
            if diff == []:
                break
                
            # Data before scrolling down will be the data after scrolling down from prior iteration
            pictures = pictures_2
        
        # Changing the type of numerical data
        number_of_comments = list(map(self.format_numbers, number_of_comments))
        number_of_likes = list(map(self.format_numbers, number_of_likes))
        
        # Creating a dataframe
        df = pd.DataFrame(list(zip(number_of_comments, number_of_likes, urls, captions)),
                          columns=["comments", "likes", "url", "caption"])
        
        # Sorting the dataframe for number of comments and getting the top n posts
        if top_n == "all":
            df = df.sort_values(by="comments", ascending=False)
        if top_n > 1:
            df = df.sort_values(by="comments", ascending=False)[:top_n]
        return(df)