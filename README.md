
# 버전 0.2이 새로 나왔습니다!!
## 자세한 사용방법/ 프로그램 정보는 첨부된 파일중 PPT파일을  읽어주세요
==========>>>> 
# [이전 버전 보기 GO!](https://github.com/itziana/SuperDeal).

# 버전 0.2 변경사항
> 1) -파이썬이 설치되지 않은 컴퓨터에서도 EXE 실행파일로 사용이 가능-
    > 201805018 일부 컴퓨터에서 진행이 되지 않아 삭제
> 2) 형태소 분석을 통한 긍정,부정 코멘트 판별문 삭제 (JAVA로 인한 오류와 정확도 문제로 제거)
> 3) 일반 코멘트의 경우 상위 50개를 추가로 긁어와 매우추천, 추천, 보통, 추천안함 의 숫자 카운트 추가
> 4) 크롬 헤드레스로 크롤링 동작을 보여주는 웹페이지 숨김처리 
> 5) -등록한 상품코드가 잘못되었을 경우 오류메시지(타입익셉션) 출력-
    > 작업상 해당 기능 실행 빈도가 거의 없어 삭제
> 6) 상품코드를 제외한 모든 카운트는 숫자형(int)으로 출력
> 7) 프리미엄상품평 텍스트 크롤링 갯수를 코드당 10개로 명시 (과거 한페이지에 있는 모든 상품평을 크롤링 했으나, 일부 코드 10개 이상 페이지에 들어있는 경우 있음)
> 8) 기존 상품코드당 1회 웹드라이버가 열리고 닫혔으나, 실행시 1회 열리고 모든 코드 크롤링 후 닫히는 구조로 변경





### 8. 코드 (SuperDeal-comment.py)
---------------------------------------
# 패키지 임포트
```  
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

```  

# 슈퍼딜 상품코드가 저장된 엑셀파일 불러오기
```  

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
```  
    
# 파싱을 받는 부분
```  
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
```  

# 상품평 정보 분류

```  

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
```  



# 실제 동작 
```  
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
```  


# 최종 데이터프레임 형태 만들기, 엑셀 출력

```  
ala2 = ['item_code', 'prim_comment', 'nomal_comment', 'very-reco','reco','soso','nope', 'p-come1','p-come2','p-come3', 'p-come4', 'p-come5', 'p-come6', 'p-come7', 'p-come8', 'p-come9', 'p-come10']
df=pd.DataFrame(columns=ala2, data=ala)
dd1 = datetime.today().strftime("%Y%m%d")
dd = str(dd1)
da = './' + dd + '.xlsx'
df.to_excel(da,sheet_name='sheet1',header=True, startrow=1, startcol=1)
print ('finished -> ' + da + ' <- check this file')        
```  

