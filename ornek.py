class matematik():
    def __init__(self,sayi1,sayi2):
        self.sayi1=sayi1
        self.sayi2=sayi2

    def topla(self):
        return self.sayi1+self.sayi2
        
    def bolme(self):

        try :
            a=self.sayi1
            b=self.sayi2
            return a/b

        except ZeroDivisionError:
            return "Hatalı işlem!"

a=matematik(3,0)
print(a.topla())
print(a.bolme())