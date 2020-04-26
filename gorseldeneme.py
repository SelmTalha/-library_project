from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from mysql.connector import MySQLConnection
import datetime
import sys

class Kutuphane(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('arayuz.ui', self)
        self.liste=[]
        self.database_olustur()
        self.tablolari_olustur()
        self.model=self.getmodel()
        self.tv.setModel(self.model)
        self.secili=None
        self.model2=self.getmodel2()
        self.tv2.setModel(self.model2)
        self.tv.clicked.connect(self.secildiginde)
        self.tv2.clicked.connect(self.secildiginde2)
        self.ke_button.clicked.connect(self.kayitEkle)
        self.ks_button.clicked.connect(self.kayitSil)
        self.kg_button.clicked.connect(self.kayitGuncelle)
        self.kikayitButton.clicked.connect(self.kitapkayit)
        print(self.liste)

    def database_olustur(self):
        baglanti = {
            "host":"localhost",
            "user": "root",
            "password":"",
            "autocommit":True,
            "charset":"utf8",
        }
        connection = MySQLConnection(**baglanti)
        lbdb = connection.cursor()
        lbdb.execute("SET NAMES UTF8")
        sql="CREATE DATABASE IF NOT EXISTS kutuphane"
        lbdb.execute(sql)

    def tablolari_olustur(self):
        baglanti = {
            "host":"localhost",
            "user": "root",
            "password":"",
            "autocommit":True,
            "charset":"utf8",
            "database":"kutuphane"
        }
        connection = MySQLConnection(**baglanti)
        lbdb = connection.cursor()
        lbdb.execute("SET NAMES UTF8")
        sql="""CREATE TABLE IF NOT EXISTS kullanici(Mno INT AUTO_INCREMENT PRIMARY KEY,
        K_Adi varchar(155) NOT NULL ,K_Soyadi varchar(155) NOT NULL,Kitap_Adi varchar(55) NOT NULL,
        Alim_Tarihi DATE NOT NULL,Teslim_Tarihi DATE NOT NULL)"""
        lbdb.execute(sql)
        sql="""CREATE TABLE IF NOT EXISTS kitaplar(Kitap_No INT AUTO_INCREMENT PRIMARY 
        KEY,Kitap_Adi varchar(55) NOT NULL,Kitap_Yazari varchar(55) NOT NULL,Sayfa_No INT NOT NULL)"""
        lbdb.execute(sql)
        sql="""ALTER TABLE kullanici Add Foreign key(Kitap_Adi) References kitaplar(Kitap_Adi)"""
        lbdb.execute(sql)

    #TableView üzerinde bir seçim yaptığımızda herhangi bir iteme tıkladığımızdaki Kontroller:
    def secildiginde(self, index: QModelIndex):
        dizin = index.row() #dizin=Sıra da diyebiliriz kaçıncı sırada olduğunu bulmamızı sağlıyor.
        sutun = index.column()
        id = index.sibling(dizin, 0).data() #0.dizindeki değerin datasını al ve id içine koy.
        self.secili = id #None olan secili değeri tıkladığımızda bulunduğu dizinin 0.indexindeki datayı alan id'ye eşitle.
        ad = index.sibling(dizin, 1).data()
        soyad = index.sibling(dizin, 2).data()
        kitap_adi = index.sibling(dizin, 3).data()
        alim_tarihi = index.sibling(dizin, 4).data()
        teslim_tarihi = index.sibling(dizin, 5).data()
        self.secili_degerleri_getir(ad, soyad, kitap_adi)
    
    def secili_degerleri_getir(self, ad, soyad, kitap_adi):
        self.ka_line.setText(ad)
        self.ks_line.setText(soyad)
        self.kka_line.setText(kitap_adi)

    def secildiginde2(self, index: QModelIndex):
        dizin = index.row()
        sutun = index.column()
        kitap_ad = index.sibling(dizin, 1).data()
        kitap_yazar = index.sibling(dizin, 2).data()
        sayfa_no = index.sibling(dizin, 3).data()
        self.kitap_secili_degerler(kitap_ad, kitap_yazar, sayfa_no)

    def kitap_secili_degerler(self, ad, soyad, no):
        self.KitapA.setText(ad)
        self.KitapY.setText(soyad)
        self.SayfaN.setText(no)
        self.kka_line.setText(ad)

    def kayitSil(self):
        id=self.secili
        if self.secili is not None:
            sql = "DELETE FROM kullanici WHERE Mno = {id}".format(id=self.secili)
            baglanti = {
                "host":"localhost",
                "user": "root",
                "password":"",
                "autocommit":True,
                "charset":"utf8",
                "database":"kutuphane"
                }
            connection = MySQLConnection(**baglanti)
            lbdb = connection.cursor()
            lbdb.execute(sql)
            self.tv.setModel(self.getmodel())
            self.secili=None

    def kayitEkle(self):
        try:
            baglanti = {
                "host":"localhost",
                "user": "root",
                "password":"",
                "autocommit":True,
                "charset":"utf8",
                "database":"kutuphane"
            }
            connection = MySQLConnection(**baglanti)
            lbdb = connection.cursor()
            sql="INSERT INTO kullanici(K_Adi,K_Soyadi,Kitap_Adi,Alim_Tarihi,Teslim_Tarihi) Values (%s,%s,%s,%s,%s)"
            ka_line=self.ka_line.text()
            ks_line=self.ks_line.text()
            kka_line=self.kka_line.text()
            a_tarihi=datetime.datetime.now()
            t_tarihi=a_tarihi
            for degerler in self.liste:
                if degerler==kka_line:         
                    tt=int(self.k_gun.text())
                    if tt>50:
                        self.k_gun.setText("50")
                        tt=50
                    gelecek=datetime.timedelta(days=tt)
                    t_tarihi=t_tarihi+gelecek
                    lbdb=connection.cursor(dictionary=True)
                    lbdb.execute(sql,[ka_line,ks_line,kka_line,a_tarihi,t_tarihi])
                    lbdb.execute("select * from kullanici")
                    self.id=None
                    for i in lbdb.fetchall():
                        id=QStandardItem(str(i['Mno']))
                        self.id=id
                    #Item Registration
                    item1=QStandardItem(ka_line)
                    item2=QStandardItem(ks_line)
                    item3=QStandardItem(kka_line)
                    item4=QStandardItem(str(a_tarihi))
                    item5=QStandardItem(str(t_tarihi))
                    self.model.appendRow([self.id,item1,item2,item3,item4,item5])
                    self.tv.setModel(self.getmodel())
                    break
        except :
            pass


    def kayitGuncelle(self):
        try:
            id=self.secili
            if self.secili is not None:
                baglanti = {
                    "host":"localhost",
                    "user": "root",
                    "password":"",
                    "autocommit":True,
                    "charset":"utf8",
                    "database":"kutuphane"
                }
                connection = MySQLConnection(**baglanti)
                lbdb = connection.cursor()
                ka_line=self.ka_line.text()
                ks_line=self.ks_line.text()
                kka_line=self.kka_line.text()
                a_tarihi=datetime.datetime.now()
                t_tarihi=a_tarihi
                tt=int(self.k_gun.text())
                gelecek=datetime.timedelta(days=tt)
                t_tarihi=t_tarihi+gelecek
                sql="UPDATE kullanici SET K_Adi=%s,K_Soyadi=%s,Kitap_Adi=%s,Alim_Tarihi=%s,Teslim_Tarihi=%s WHERE Mno=%s "
                lbdb.execute(sql,[ka_line,ks_line,kka_line,a_tarihi,t_tarihi,self.secili])
                self.tv.setModel(self.getmodel())
                self.secili=None
        except:
            pass

    def kitapkayit(self):
        try:
            baglanti={
                "host":"localhost",
                "user":"root",
                "password":"",
                "database":"kutuphane"
            }
            connection=MySQLConnection(**baglanti)
            lbdb=connection.cursor()
            ad=self.KitapA.text()
            yazar=self.KitapY.text()
            No=self.SayfaN.text()
            sql="INSERT INTO kitaplar (Kitap_Adi,Kitap_Yazari,Sayfa_No) VALUES (%s,%s,%s)" 
            lbdb.execute(sql,[ad,yazar,No])
            #Item Registration
            item=QStandardItem(ad)
            item2=QStandardItem(yazar)
            item3=QStandardItem(str(No))
            self.model2.appendRow([item,item2,item3])
            self.tv2.setModel(self.getmodel2())
        except:
            pass

    def getmodel(self):
        temp=QStandardItemModel()
        temp.setHorizontalHeaderLabels(['Mno','K_Adı','K_Soyadı','Kitap_Adi','Alim_Tarihi','Teslim_Tarihi'])
        baglanti = {
            "host":"localhost",
            "user": "root",
            "password":"",
            "autocommit":True,
            "charset":"utf8",
            "database":"kutuphane"
        }
        connection = MySQLConnection(**baglanti)
        lbdb = connection.cursor(dictionary=True)
        lbdb.execute("Select * From kullanici ORDER BY Mno")
        a=lbdb.fetchall()
        for i in a:
            id=QStandardItem(str(i['Mno']))
            k_adi=QStandardItem(i['K_Adi'])
            k_soyad=QStandardItem(i['K_Soyadi'])
            kitap_adi=QStandardItem(i['Kitap_Adi'])
            alim_t=QStandardItem(str(i['Alim_Tarihi']))
            teslim_t=QStandardItem(str(i['Teslim_Tarihi']))
            temp.appendRow([id,k_adi,k_soyad,kitap_adi,alim_t,teslim_t])
        return temp
    
    def getmodel2(self):
        temp=QStandardItemModel()
        temp.setHorizontalHeaderLabels(['Kitap_No','K_Adı','K_Yazarı','Sayfa_Sayısı'])
        baglanti = {
            "host":"localhost",
            "user": "root",
            "password":"",
            "autocommit":True,
            "charset":"utf8",
            "database":"kutuphane"
        }
        connection = MySQLConnection(**baglanti)
        lbdb = connection.cursor(dictionary=True)
        lbdb.execute("SELECT * FROM kitaplar ORDER BY Kitap_No ")
        a=lbdb.fetchall()
        for i in a:
            id=QStandardItem(str(i['Kitap_No']))
            ad=QStandardItem(i['Kitap_Adi'])
            self.liste.append(i['Kitap_Adi'])
            yazar=QStandardItem(i['Kitap_Yazari'])
            sayfa_sayisi=QStandardItem(str(i['Sayfa_No']))
            temp.appendRow([id,ad,yazar,sayfa_sayisi])
        return temp

if __name__=="__main__":
    app = QApplication(sys.argv)
    pencere = Kutuphane()
    pencere.show()
    sys.exit(app.exec_())