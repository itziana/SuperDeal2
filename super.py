from selenium import webdriver
import time 
import selenium.webdriver
from bs4 import BeautifulSoup
import openpyxl
import pandas as pd
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


wd = openpyxl.load_workbook('test1.xlsx')
ws = wd.active
alldfcontents = []
for r in ws.rows:
    row_index = r[0].row    
    kor = r[1].value    
    alldfcontents.append(kor)    
    #40개 까지만 읽어들이기
    if row_index == 40:
         break
tt = list(filter(None.__ne__, alldfcontents))
 
    

def Superdeal(a): 

    driver.get('http://mitem.gmarket.co.kr/Item?goodsCode='+a)
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//*[@id="mainTab1"]/button').click()
    time.sleep(3)
    html = driver.page_source        
    soup1 = BeautifulSoup(html, 'html.parser') 
    driver.find_element_by_xpath('//*[@id="textReviewTab"]').click()
    time.sleep(3)
    html2 = driver.page_source
    soup2 = BeautifulSoup(html2, 'html.parser')  
    #driver.quit()
    soup = (soup1, soup2)        
    return (soup)
        

def Countt(soup):

    #print('working. 4/5')
    contents5 = soup.find('a', { 'id': 'photoReviewTab' })
    contents6 = soup.find('a', { 'id': 'textReviewTab' })

    #print(contents5.span.text, contents6.span.text)
    countz2 = [contents5.span.text, contents6.span.text]
    #print(countz)
    #countz= countz2.replace(",","")
    countz = [countz2[0].replace(",",""), countz2[1].replace(",","")]
    countz = [int (i) for i in countz]
    
    return countz

def countt3(soup):

    
    contents8 = soup.find_all('span', { 'class': 'recommend' })
    
    recovery = 0
    reco = 0
    nomal = 0
    noreco = 0

    for num in range(len(contents8)):
        i4 = contents8[num].get_text().strip()
        if i4 == '적극추천':
            recovery = recovery + 1
        if i4 == '추천' :
            reco = reco + 1
        if i4 == '보통':
            nomal = nomal + 1
        if i4 == '추천안함':
            noreco = noreco + 1
    recofin = [recovery, reco,nomal,noreco]
    
    return(recofin)



def Countt2(soup):    

    
    contents0 = soup.find('div', { 'id': 'photoReviewArea' })
    contents02 = contents0.select('ul > li > a')
   

    dfcontent0 = []
    #print(dfcontent0)
    alldfcontents0 = []
    tdst = []
    i2 = 0
    for content00 in contents02:
        tds=content00.find_all("p")
        tds.pop(0)
        tds.pop(0)
        
        for td in tds:
            i2 = i2 + 1
            if i2 < 11:
                
                dfcontent0.append(td.text)
                #print (dfcontent0)
            else:
                break
        
    return dfcontent0
    
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options) 

#driver = webdriver.Chrome('chromedriver.exe')

ala = []
iq = 1
for i in tt:
    cc0 = str(i)
    print('superdeal item_code '+ cc0 + ' searching' )
    print('working...'+ str(iq) + '/' + str(len(tt)))
    #print(i)
    #print(cc0)
    a = Superdeal(cc0)    
    q2 =  Countt2(a[0])
    #print(q2)
    cc = countt3(a[1]) 
    cc2 =  Countt(a[0])
    yy = cc2 + cc
    #print(yy)
    yy.extend(q2)
    #i2 = str(i)
    yy.insert(0, cc0)
    #print(cc2)
    
    iq = iq + 1  
    ala.append(yy)
    #print(yy)
    
driver.quit()    

ala2 = ['item_code', 'prim_comment', 'nomal_comment', 'very-reco','reco','soso','nope', 'p-come1','p-come2','p-come3', 'p-come4', 'p-come5', 'p-come6', 'p-come7', 'p-come8', 'p-come9', 'p-come10']
df=pd.DataFrame(columns=ala2, data=ala)
dd1 = datetime.today().strftime("%Y%m%d")
dd = str(dd1)
da = './' + dd + '.xlsx'
df.to_excel(da,sheet_name='sheet1',header=True, startrow=1, startcol=1)
print ('finished -> ' + da + ' <- check this file')        
