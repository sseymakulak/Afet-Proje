# Menü seçenekleri
menu = ["Sisteme Üye Ol", "Sisteme Giriş Yap", "Şifremi Unuttum"]
kullanicilar = {"admin": "1234", "kullanici": "5678"}

# Kullanıcı girişi veya admin girişi
print("Lütfen giriş yapmak istediğiniz kullanıcı türünü seçin: (1-2)")
print("1. Admin")
print("2. Kullanıcı")
secim = input("Seçiminiz: ")

if secim == "1":
    print("Admin girişi yapmak için lütfen bilgilerinizi girin:")
    username='sseyma'
    password='1234'
    kullanici = input("Kullanıcı adınızı girin: ")
    sifre = input("Şifrenizi girin: ")
    if kullanici == username and sifre == password:
        print("Başarıyla giriş yaptınız.")
        print("Yönlendiriliyorsunuz...")
    
    else:
        print("Kullanıcı adı veya şifre yanlış.")
        exit()

while True:
    if secim== "2":
# Kullanıcı İşlem seçenekleri
        print("Lütfen bir işlem seçin:")
    for i in range(len(menu)):
        print(f"{i+1}. {menu[i]}")
    secim = input("Seçiminiz: ")

    if secim == "1":
        # Sisteme üye olma işlemi
        print("Sisteme üye olma işlemi seçildi.")
        yeni_kullanici = input("Kullanıcı adınızı girin: ")
        yeni_sifre = input("Şifrenizi girin: ")
        kullanicilar[yeni_kullanici] = yeni_sifre
        print("Başarıyla kayıt oldunuz.")
       

    elif secim == "2":
        # Sisteme giriş yapma işlemi
        print("Sisteme giriş yapma işlemi seçildi.")
        kullanici = input("Kullanıcı adınızı girin: ")
        sifre = input("Şifrenizi girin: ")
        if kullanici in kullanicilar and kullanicilar[kullanici] == sifre:
            print("Başarıyla giriş yaptınız.")
        else:
            print("Kullanıcı adı veya şifre yanlış.")
      
    
    elif secim == "3":
  
    # Şifremi unuttum işlemi
     print("Şifremi unuttum işlemi seçildi.")
     kullanici = input("Kullanıcı adınızı girin: ")
     if kullanici in kullanicilar:
         yeni_sifre = input("Yeni şifrenizi girin: ")
         kullanicilar[kullanici] = yeni_sifre
         print("Şifreniz başarıyla değiştirildi.")
     else:
         print("Bu kullanıcı adı kayıtlı değil.")

     
