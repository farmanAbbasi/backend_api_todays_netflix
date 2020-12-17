from bs4 import BeautifulSoup
import requests
from flask import Flask
from flask import request
app = Flask(__name__)
import json
from flask_cors import CORS, cross_origin
CORS(app)

def getMovieUrl():
    url = "https://flixpatrol.com/top10/netflix"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
   
    special_divs = soup.find_all('div',{'class':'threedots'})
    count=0
    finalArray=[]
    rank=0
    for text in special_divs:
        count+=1
        if(count>20):
            break
        download = text.find_all('a', href = True)
        
        
        for text in download:
            data={}
            text=str(text)
            splited=text.split('"')
            #change image url for better resolution
            #format now: https://filmtoro.cz/img3/tv/zU0htwkhNvBQdVSIKB9s6hgVeFK.jpg
            #https://filmtoro.cz/img2/tv/zU0htwkhNvBQdVSIKB9s6hgVeFK.jpg
            img_url=splited[7]
            img_url=img_url.replace("/img3","/img2")
            
            rank=rank+1
            data={"rank":rank,
                  "title":splited[9],
                  "image_url":img_url}
            finalArray.append(data)

    return finalArray                 
            


@app.route('/netflixToday', methods=['GET'])
def loadData():
    finalData=getMovieUrl()
    return json.dumps({"data": finalData})    

@app.route('/', methods=['GET'])
def getData():
    return json.dumps({"msg": "hello"})

if __name__ == '__main__':
    app.run()
    
        
