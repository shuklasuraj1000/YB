from __future__ import unicode_literals
from flask import Flask, render_template, request
from flask_cors import CORS,cross_origin
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pytube import YouTube
import youtube_dl
import json
import requests
import os

app = Flask(__name__)

@app.route('/',methods=['GET']) # route to display the home page
@cross_origin()
def Homepage():
    return render_template("index.html")

@app.route('/page1',methods=['GET','POST']) # route to display the home page
@cross_origin()
def page1():
    return render_template("page1.html")

@app.route('/page2',methods=['GET','POST']) # route to display the home page
@cross_origin()
def page2():
    return render_template("page2.html")


@app.route('/review',methods=['POST','GET']) # route to show channel name, videos title (max 329), and URL of videos in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            youtube_url = "https://www.youtube.com/" + searchString + "/videos?view=0&sort=dd&flow=grid"
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
            col5 = []
            col6 = []
            col8 = []
            #with Chrome(r"C:\Users\Admin\PycharmProjects\ImageScrapper\chromedriver.exe") as driver:
            wait = WebDriverWait(driver, 2)
            driver.get(youtube_url)

                # Scrolling web page 10 time after wait of 2 seconds. If you need to scroll more change value (ex. 10, 50, 100)
            for item in range(10):
                wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                time.sleep(2)

            for a in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#video-title"))):
                col5.append(a.text)

            for a in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#video-title"))):
                col6.append(a.get_attribute('href'))

            for span in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#metadata-line"))):
                a = span.text.split('\n')
                col8.append(a[0])


            # Creating new file and feeding data
            fw = open("table.csv", "w")
            fw.close()
            time.sleep(10)
            fw = open("table.csv", "w")
            headers = "Channel, title, url, Views \n"
            fw.write(headers)
            reviews = []
            for i in range(len(col5)):
                try:
                    mydict = {"Channel": searchString, "title": col5[i], "url": col6[i], "Views": col8[i]}
                    reviews.append(mydict)

                except:
                    name = 'No Name'

            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('page1.html')

    else:
        return render_template('page1.html')



@app.route('/review2',methods=['POST','GET']) # route to show channel name, videos title (max 329), and URL of videos in a web UI
@cross_origin()
def index2():
    if request.method == 'POST':
        try:
            searchString = request.form['content2'].replace(" ","")
            youtube_url = searchString
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
            col1 = []
            col2 = []
            #with Chrome(r"C:\Users\Admin\PycharmProjects\ImageScrapper\chromedriver.exe") as driver:
            wait = WebDriverWait(driver, 2)
            driver.get(youtube_url)

            # Scrolling web page 10 time after wait of 2 seconds. If you need to scroll more change value (ex. 10, 50, 100)
            for item in range(10):
                wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                time.sleep(2)

            for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content-text"))):
                col1.append(comment.text)

            for a in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#author-text"))):
                col2.append(a.text)


            # Creating new file and feeding data
            fw = open("table1.csv", "w")
            fw.close()
            time.sleep(10)
            fw = open("table1.csv", "w")
            headers = "user, comment \n"
            fw.write(headers)
            reviews1 = []
            for i in range(len(col1)):
                try:
                    mydict1 = {"user": col2[i], "comment": col1[i]}
                    reviews1.append(mydict1)

                except:
                    name = 'No Name'

            return render_template('results1.html', reviews=reviews1[0:(len(reviews1)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('page2.html')

    else:
        return render_template('page2.html')


@app.route('/review3',methods=['POST','GET'])  # route to show channel name, videos title (max 329), and URL of videos in a web UI
@cross_origin()
def index3():
    if request.method == 'POST':
        try:


            searchString = request.form['content3'].replace(" ","")
            link = searchString
            thumbnail = YouTube(link).thumbnail_url
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
                ydl.download([thumbnail])
                time.sleep(10)

            headers = {
                "Authorization": "Bearer ya29.a0AVA9y1s-WL2PiNMiZoJpnsOsCUoOymJs-EeWEvzOOClnSz3IotZpIIKeX6aUXuzo9DQqHCD4SJAFEehvaKYwaLAGSqSB24bPsl_6BfShssqqM5-U3tbNVRbSO-wKRYn6F-gZG47RPWigYqIY-T3pF4ih0JGtaCgYKATASARMSFQE65dr8Vf0KCwXeORBdGirgbSC_Bw0163"}
            para = {
                "name": "samplefile.png",
                "parents": ["1v334xDf2-ZKLAofn0gwmSctr3YuwwCor"]
            }

            f = open("./sddefault-sddefault.jpg", "rb")

            files = {
                'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
                'file': f

            }
            r = requests.post(
                "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                headers=headers,
                files=files
            )
            f.close()

            time.sleep(10)
            os.remove(r"./sddefault-sddefault.jpg")

            return render_template('index.html')

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('index.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)
