# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:27:50 2021

@author: Aryan
"""
#for redvid downloader
import glob 
import os
from redvid import Downloader

import time
import random
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from credentials import rusername as rusr, rpassword as rpass
import os
import lackey
import requests
from bs4 import BeautifulSoup
import pandas
import csv

class Bot:
    def __init__(self,rusername,rpassword):
     
        self.rusername = rusername
        self.rpassword = rpassword
        profile = webdriver.FirefoxProfile()
       
        self.bot = webdriver.Firefox(profile, executable_path="geckodriver.exe")
        self.bot.set_window_size(1920, 1080)
        self.bot.maximize_window()
        
        


    def check_exists_by_xpath(driver, xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return True

        return False    

    def exit(self):
        bot = self.bot
        bot.quit()
        
        
        
    def phase1(self):
        
        #login
        bot=self.bot
        bot.get('https://www.reddit.com/login/')
        time.sleep(3)
        bot.find_element_by_name('username').send_keys(self.rusername)
        bot.find_element_by_name('password').send_keys(self.rpassword)
        
        time.sleep(1)
        loginButton = bot.find_element_by_css_selector('button[type="submit"][class="AnimatedForm__submitButton m-full-width"]')
        loginButton.click()
        
        time.sleep(7)
        
        #list
        l=[]
        d={}
        
        
        #subreddit finder
        f = open("subredits.txt", "r")
        count=0
        timee=0
        subreddit=[]
        for guy in f:
            subreddit.append(guy)
      
        
      
        for item in subreddit:
            bot.get('https://www.reddit.com/r/'+ item)
            
            #dictonary refreshes after evey iteraton
            d={}
            d["subreddit"] = item
            #mouse center and scroll
            pyautogui.moveTo(677, 327)
            bot.find_element_by_css_selector("body").send_keys(Keys.CONTROL, Keys.END)
            time.sleep(3)
            bot.find_element_by_css_selector("body").send_keys(Keys.CONTROL, Keys.END)
            
            time.sleep(3)
            
            #web scrapping
            page = bot.execute_script('return document.body.innerHTML')
            soup = BeautifulSoup(''.join(page), 'html.parser')
           
            
            yo=soup.findAll("div",{"class":"_1poyrkZ7g36PawDueRza-J _11R7M_VOgKO1RJyRSRErT3"})
            
            
            print(len(yo))
            count=0
            for i in range(0,len(yo)):
                count=count+1
                #remove the if statement if you want post of all category not only videos
                if (yo[i].find("video",{"class":"_1EQJpXY7ExS04odI1YBBlj"})):
                    d={}
                    d["subreddit"] = item
                    caption=(yo[i].find("h3",{"class":"_eYtD2XCVieq6emjKBH3m"}).text)
                        #print(caption)
                    x=yo[i].find_all('a',href=True)[1]
                    postlink=x['href']
                    poststatus = 0
                    if len(postlink) < 150:
                        d["Caption"]=caption
                        d["postlink"]=postlink
                        d["poststatus"]=poststatus
                        print(postlink)
                        print(caption)
                        l.append(d)
                        print('')
                if count>=10:
                    break
                    print('')
                
                    
        
        df=pandas.DataFrame(l)
        
        df.to_csv("output.csv" , mode='a')
        
        
        df1=pandas.read_csv('output.csv')
        df1.sort_values('postlink', ascending=bool)
        df1.drop_duplicates( subset='postlink')
        df1.to_csv("output.csv" , mode='w')
        
        
    
            
        
        
        
     #duplicate
     
    def phase2d(self):
        bot=self.bot
        df3=pandas.read_csv('output.csv')
        while True:
            dfrandom=df3.sample()
            x=dfrandom['poststatus'].values[0]
            if x==0:
                break
            else:
                continue
        print(dfrandom['postlink'].values[0])
        self.postlink = dfrandom['postlink'].values[0]
        print(dfrandom['subreddit'].values[0])
        self.subreddit = dfrandom['subreddit'].values[0]
        print(dfrandom['Caption'].values[0])
        self.caption = dfrandom['Caption'].values[0]
        
        df3.loc[df3['postlink']==self.postlink , 'poststatus']=1
        
        df3.to_csv("output.csv") 
        
        #real dwonloder part
        reddit = Downloader(max_q=True)
        #change this part
        reddit.path = 'C:/Desktop/'
        reddit.url = self.postlink
        reddit.download()

    
        
        
        
        


        
 
        
        

        
        

run = Bot(rusr,rpass)

run.phase1()
run.phase2d()
        
        
