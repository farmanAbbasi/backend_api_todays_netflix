from bs4 import BeautifulSoup
import requests
import pandas as pd
import ssl
from flask import Flask
from flask import request
app = Flask(__name__)
import json
from flask_cors import CORS, cross_origin
CORS(app)

def getMovieFromNetflixXLSX():
    url = "https://www.netflix.com/tudum/top10/data/all-weeks-global.xlsx"
    try:
        finalArray = []
        # Ignore SSL certificate verification
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Read the Excel file
        df = pd.read_excel(url,nrows=10,usecols=['week', 'category', 'weekly_rank', 'show_title', 'season_title'])
        print(df)
        for index, row in df.iterrows():
            # Create a dictionary for the current row
            row_dict = {
                'rank': row['weekly_rank'],
                'power': 11-row['weekly_rank'],
                'title': row['show_title'],
                'img_url':None
            }
            # Append the dictionary to the list
            finalArray.append(row_dict)
        return finalArray

        # data={"rank":d,
        #           "power":power,
        #           "title":splited[9],
        #           "image_url":img_url}
        # finalArray.append(data)

        # return finalArray  
    except Exception as e:
        print("Error reading the Excel file:", e)


                

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
           image_src=image_src.replace("width-134,height-99","width-800,height-600")
           
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
    finalData=getMovieFromNetflixXLSX()
   
    return json.dumps({"data": finalData})    

@app.route('/', methods=['GET'])
def getData():
    return json.dumps({"msg": "hello"})

if __name__ == '__main__':
    app.run()
    
        
