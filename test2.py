import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd

class scrap():
    
    def __init__(self):
        
        self.url = 'https://www.myfitnesspal.com/food/calories/angel-food-cake-188889940'
        self.df = pd.DataFrame({'title': [0], 'serving_size': [0], 'Carbs': [0],
         'Dietary Fiber': [0], 'Sugar': [0], 'Fat': [0], 'Saturated': [0], 'Polyunsaturated': [0], 
         'Monounsaturated': [0], 'Trans': [0], 'Protein': [0], 'Sodium': [0], 'Potassium': [0],
         'Cholesterol': [0], 'Vitamin A': [0], 'Vitamin C': [0], 'Calcium': [0], 'Iron': [0],'Calories':[0],
         'Minutes of Cycling':[0], 'Minutes of Running':[0], 'Minutes of Cleaning':[0]})

    def get_page(self ,url):
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"}
        response = requests.get(url, headers=headers)
        if not response.ok:
           print('server response ', response.status_code, "Not Good")
        else:
            soup = BeautifulSoup(response.text, 'lxml')
            print('server resplonse', response.status_code, "It's Good !!!")
        return soup 

    def myfunc (self, ls):
        s = ''        
        for strg in ls:
            s+=strg
        return s                        
    
    def get_details(self ,soup):
        try:
            title = soup.find('h1', class_="MuiTypography-root MuiTypography-h1").text.strip()
        except:
            title = ''
        #print(title)
        try:
            serving_size = soup.find('div', class_='MuiSelect-root MuiSelect-select MuiSelect-selectMenu MuiInputBase-input MuiInput-input').text.strip()
        except:
            serving_size = ''
        
        try:
            
            arr = []
            tq = soup.find('p', class_="MuiTypography-root MuiTypography-h1 MuiTypography-colorTextPrimary MuiTypography-paragraph MuiTypography-alignCenter").text.strip()
            arr.append(re.findall('\D*\d+' ,tq)[0])

            xq = soup.find('div', class_='inlineActivitiesContainer-2DZep').find_all('div')
            for i in xq:
                ls = re.findall('\D*\d+' ,i.text.strip())
                arr.append(self.myfunc(ls))
        except:
            arr = ['', '', '', '']
        
        sections = []
        divs = []
        dictionary = {}   


        dictionary['title'] = title
        dictionary['serving_size'] = serving_size
        
        dictionary['Calories'] = arr[0]
        dictionary['Minutes of Cycling'] = arr[1]
        dictionary['Minutes of Running'] = arr[2]
        dictionary['Minutes of Cleaning'] = arr[3]


        nutrs = soup.find('div', class_="NutritionalInfoContainer-3XIjH").find_all('div', class_='row-CFHmE')
        for n in nutrs:
            sections.extend(n.find_all('section'))
        for s in sections:
            divs.extend(s.find_all('div')) 
        #print(len(divs))
        for d in divs:
            q = d.text.strip()
            dd = re.findall('\d*\D+',q)
            try:
                dictionary[dd[0]] = dd[1]
                #print(dd[0], len(dd[0]))
            except:
                qq = q.split('-', 1)
                if len(qq) == 2:
                    dictionary[qq[0]] = None
                else:
                    dictionary[dd[0]] = 'else'  #aq unda gaiweros satitaod shemowmeba                    
                #print(dd[0], len(dd[0]))
        #print(dictionary)              
        self.df = self.df.append(dictionary, ignore_index=True)
        #print(self.df)
    
    def page(self, soup):
        links = self.index(soup)
        for l in links:
            self.get_details(self.get_page(l))


    def index(self, soup):
        #up_links = []
        #up = soup.find('div', class_='main-2ZMcp')
        #down = soup.find('section', class_='nutrition-3m1hR')
        container = soup.find('div' ,class_='container-3Yq-c')
        #test1 = up.find_all('a')
        #test2 = down.find_all('a')
        container = container.find_all('a')
        #l = [t.get('href') for t in test1]
        #b = [t.get('href') for t in test2]
        c_str = []
        c = [t.get('href') for t in container]
        for string in c:
            if string != None:
                c_str.append('https://www.myfitnesspal.com/' + string)
        #print(l)
        #print(b)
        #print('all\n', c_str)
        return c_str
            # print(u)
            # href = str(u.find('a').get('href'))
            # up_links.append(href)
        #print(up_links)

def main(fr, to):
    #print(get_details(get_page(url), df))
    #index(get_page('https://www.myfitnesspal.com/food/search?page=3&search=food')) 
    scr = scrap()
    for i in range(fr, to):
        print(i)
        url = 'https://www.myfitnesspal.com/food/search?page={}&search=brand'.format(i)
        print('Number of pages scrapped', i)
        scr.page(scr.get_page(url))
    datf = scr.df.drop(index=[0])
    datf.to_csv('C://Food_Nutrition_scrapper//output.csv' ,line_terminator='\n') 
    # scr = scrap()
    
    # url = 'https://www.myfitnesspal.com/food/search?page=1&search=food'
    # scr.page(scr.get_page(url))
    # datf = scr.df.drop(index=[0])
    # datf.to_csv('C://Food_Nutrition_scrapper//output.csv' ,line_terminator='\n') 




from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(scrap):
    def __init__(self):
        self.udf = 2
        self.uurl = 'abc'
        self.ufrm = 1
        self.uto = 2
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(711, 635)

        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(130, 240, 81, 41))
        self.lineEdit.setObjectName("lineEdit")
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(130, 180, 81, 41))
        self.label.setObjectName("label")
        
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(490, 240, 81, 41))
        self.lineEdit_2.setObjectName("lineEdit_2")
        
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(500, 185, 55, 31))
        self.label_2.setObjectName("label_2")
        
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(0, 450, 711, 191))
        self.pushButton.setIconSize(QtCore.QSize(42, 20))
        self.pushButton.clicked.connect(self.clicked)
        self.pushButton.setObjectName("pushButton")
        
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(32, 380, 651, 41))
        self.lineEdit_3.setObjectName("lineEdit_3")
        
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 691, 171))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setText('Enter # Of pages You Want To Scrap\nAnd The URL ')


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def clicked(self):
        self.textBrowser.setText('abc')
        self.ufrm = int(self.lineEdit.text())
        self.uto = int(self.lineEdit_2.text())
        self.uurl = self.lineEdit_3.text().replace("page=1", 'page={}')
        n = 0
        scr = scrap()
        for i in range(self.ufrm, self.uto):
            print('Number of pages ready', i)
            url = self.uurl.format(i)
            scr.page(scr.get_page(url))
            n+=1
            #self.textBrowser.setText('Number Of Pages Scraped {}'.format(i))
        datf = scr.df.drop(index=[0])
        datf.to_csv('C://Food_Nutrition_scrapper//output.csv' ,line_terminator='\n')
        self.textBrowser.setText('Number Of Pages Scraped {} \nYou have got your file at \nC:\Food_Nutrition_scrapper\output.csv'.format(n)) 

        print('Scrapped up to page ', self.uto)

        

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        #Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        Dialog.setWindowTitle(_translate("dialog", "Data Is The Possibility !!!"))
        self.label.setText(_translate("Dialog", "    From"))
        self.label_2.setText(_translate("Dialog", "     To"))
        self.pushButton.setText(_translate("Dialog", "Scrap"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
