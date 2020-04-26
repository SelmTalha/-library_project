
class GirmeHatasi(Exception):
    pass
    
sayi=int(input("Değer:"))

try :
    raise GirmeHatasi("0 girilemez:","das")
    print(sayi)

except GirmeHatasi as e:
    print(e)
