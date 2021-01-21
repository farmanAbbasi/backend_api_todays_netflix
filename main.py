from bs4 import BeautifulSoup
import requests
from flask import Flask
from flask import request
app = Flask(__name__)
import json
from flask_cors import CORS, cross_origin
CORS(app)
#deploued api
#https://google-get-trending-netflix.herokuapp.com/netflixToday
def getMovieUrl():
    url = "https://flixpatrol.com/top10/netflix"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
   
    special_divs = soup.find_all('div',{'class':'threedots'})
    count=0
    finalArray=[]
    rank=0
    power=21
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
            img_url=img_url.replace("/img3","/img")
            
            rank=rank+1
            power=power-1
            data={"rank":rank,
                  "power":power,
                  "title":splited[9],
                  "image_url":img_url}
            finalArray.append(data)

    return finalArray      

def getNewsUrl(language):
    url_hindi = "https://timesofindia.indiatimes.com/entertainment/hindi/bollywood/news"
    url_english="https://timesofindia.indiatimes.com/entertainment/english/hollywood/news"
    if language=="en":
        url=url_english
    else:
        url=url_hindi
    
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    special_divs = soup.find("div", {"id": "mainlisting"})
    special_anchors=special_divs.find_all("a", href = True)
    #print(special_anchors)
    finalData=[]
    for text in special_anchors:
       
       link="https://timesofindia.indiatimes.com"+text['href']
       
       msg=text.text
       for img in text('img'):
           image_src=img['src']
           image_src=image_src.replace("width-134,height-99","width-500,height-350")
           
       returnData={
            "link":link,
            "msg":msg,
            "image_src":image_src
           }
       finalData.append(returnData)
    finalData.pop()

    finalData2=[]
    for f in finalData:
        print(f)
        if f["msg"]=="":
            continue
        else:
            finalData2.append(f)
    return finalData2

           

@app.route('/hollyBollyToday', methods=['GET'])
def loadDataHolly():
    language=request.args.get('language')
    finalData=getNewsUrl(language)
    return json.dumps({"data": finalData})  
            


@app.route('/netflixToday', methods=['GET'])
def loadData():
    finalData=getMovieUrl()
    return json.dumps({"data": finalData})    

@app.route('/', methods=['GET'])
def getData():
    return json.dumps({"msg": "hello"})

if __name__ == '__main__':
    app.run()
    
        
