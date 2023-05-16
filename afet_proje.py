import sqlite3

# Veritabanı bağlantısı oluşturma
baglanti = sqlite3.connect('ekip_veritabani.db')
cursor = baglanti.cursor()

# Ekip tablosunu oluşturma
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ekip (
        ekip_adi TEXT,
        uye_sayisi INTEGER,
        bolume_atanan INTEGER DEFAULT 0
    )
''')

# Kullanıcı tablosunu oluşturma
cursor.execute('''
    CREATE TABLE IF NOT EXISTS kullanici (
        kullanici_adi TEXT,
        sifre TEXT
    )
''')

# Örnek verileri ekleme
cursor.execute("INSERT INTO kullanici VALUES ('admin', '12345')")
cursor.execute("INSERT INTO kullanici VALUES ('ekip1', 'pass1')")
cursor.execute("INSERT INTO kullanici VALUES ('ekip2', 'pass2')")
cursor.execute("INSERT INTO kullanici VALUES ('ekip3', 'pass3')")

# Ekipleri bölgeye yerleştirmek
def ekip_yerlestirme():
    etkilenen_bolge_sayisi = int(input("Etkilenen bölge sayısını girin: "))
    ekip_sayilari = []
    for i in range(etkilenen_bolge_sayisi):
        ekip_sayisi = int(input("{}. bölgeye atanacak ekip sayısını girin: ".format(i+1)))
        ekip_sayilari.append(ekip_sayisi)

# Ekipleri bölgeye dağıtma
    cursor.execute('SELECT COUNT(*) FROM ekip')
    kayit_sayisi = cursor.fetchone()[0]
    bolume_atanan = 0
    for i in range(etkilenen_bolge_sayisi):
        for j in range(ekip_sayilari[i]):
            cursor.execute('UPDATE ekip SET bolume_atanan = ? WHERE rowid = ?', (i+1, kayit_sayisi-bolume_atanan))
            bolume_atanan += 1

    baglanti.commit()
    print("Ekipler başarıyla yerleştirildi.")

# Ekip takibi
def ekip_takibi():
    cursor.execute('SELECT * FROM ekip')
    ekipler = cursor.fetchall()

    for ekip in ekipler:
        ekip_adi = ekip[0]
        uye_sayisi = ekip[1]
        bolume_atanan = ekip[2]

        print("Ekip Adı: {}, Üye Sayısı: {}, Atanan Bölge: {}".format(ekip_adi, uye_sayisi, bolume_atanan))

# İletişim
def iletisim():
    mesaj_gonderen = input("Mesaj gönderen kullanıcıyı girin (admin/ekip_adi): ")
    mesaj_icerigi = input("Mesaj içeriğini girin: ")

    if mesaj_gonderen == "admin":
        cursor.execute('SELECT ekip_adi FROM ekip')
        ekipler = cursor.fetchall()
        for ekip in ekipler:
            print("Admin -> {}: {}".format(ekip[0], mesaj_icerigi))
    else:
         cursor.execute('SELECT ekip_adi FROM ekip WHERE ekip_adi = ?', (mesaj_gonderen,))
         ekip = cursor.fetchone()
         if ekip:
             print("{} -> Admin: {}".format(ekip[0], mesaj_icerigi))
         else:
             print("Geçersiz ekip adı.")
             
             
# Ana menü
def ana_menu():
    print("Lütfen giriş yapmak istediğiniz işlemi seçin:")
    print("1. Sisteme Giriş Yap")
    print("2. Sisteme Ekip Girişi Yap")
    print("3. Şifremi Unuttum")
    print("4. Ekip Yerleştirme")
    print("5. Ekip Takibi")
    print("6. İletişim")
    print("7. Raporlama")
    print("8. Çıkış")
    
    secim = input("Seçiminiz: ")
    
    if secim == "1":
        # Sisteme giriş yap
        kullanici_girisi()
    elif secim == "2":
        # Sisteme ekip girişi yap
        ekip_girisi()
    elif secim == "3":
        # Şifremi unuttum
        sifremi_unuttum()
    elif secim == "4":
        # Ekip yerleştirme
        ekip_yerlestirme()
    elif secim == "5":
        # Ekip takibi
        ekip_takibi()
    elif secim == "6":
        # İletişim
        iletisim()
    elif secim == "7":
        # Raporlama
        raporlama()
    elif secim == "8":
        # Çıkış yap
        print("Çıkış yapılıyor...")
        baglanti.close()
        return
    else:
        print("Geçersiz bir seçim yaptınız. Tekrar deneyin.")
    
    print()  # Boş bir satır ekleyerek daha iyi görünürlük sağlayalım
    ana_menu()

# Kullanıcı girişi
def kullanici_girisi():
    kullanici_adi = input("Kullanıcı Adı: ")
    sifre = input("Şifre: ")
    
    cursor.execute('SELECT * FROM kullanici WHERE kullanici_adi = ? AND sifre = ?', (kullanici_adi, sifre))
    kullanici = cursor.fetchone()
    
    
    # Admin kullanıcı adı ve şifresini kontrol et
    if kullanici_adi == "admin" and sifre == "12345":
        print("Giriş başarılı!")
        ana_menu()
    else:
        print("Hatalı kullanıcı adı veya şifre.")
        kullanici_girisi()
    
# Sisteme ekip girişi yap
def ekip_girisi():
    ekip_adi = input("Ekip Adı: ")
    uye_sayisi = int(input("Ekip Üye Sayısı: "))

    # Ekip verilerini veritabanına ekleme
    cursor.execute('INSERT INTO ekip (ekip_adi, uye_sayisi) VALUES (?, ?)', (ekip_adi, uye_sayisi))
    baglanti.commit()

    print("Ekip girişi başarılı!")
    ana_menu()

# Şifremi unuttum
def sifremi_unuttum():
    kullanici_adi = input("Kullanıcı Adı: ")

    cursor.execute('SELECT * FROM kullanici WHERE kullanici_adi = ?', (kullanici_adi,))
    kullanici = cursor.fetchone()

    if kullanici:
        yeni_sifre = input("Yeni Şifre: ")
        cursor.execute('UPDATE kullanici SET sifre = ? WHERE kullanici_adi = ?', (yeni_sifre, kullanici_adi))
        baglanti.commit()
        print("Yeni şifre başarıyla kaydedildi.")
    else:
        print("Geçersiz kullanıcı adı!")
        sifremi_unuttum()

# Raporlama
def raporlama():
    # Toplam ekip sayısını al
    cursor.execute('SELECT COUNT(*) FROM ekip')
    ekip_sayisi = cursor.fetchone()[0]

    # Çalışan ekip sayısını al
    cursor.execute('SELECT COUNT(*) FROM ekip WHERE bolume_atanan > 0')
    calisan_ekip_sayisi = cursor.fetchone()[0]

    # Kurtarılan kişi sayısını al
    cursor.execute('SELECT SUM(uye_sayisi) FROM ekip WHERE bolume_atanan > 0')
    kurtarilan_kisi_sayisi = cursor.fetchone()[0]

    # Raporu yazdır
    if calisan_ekip_sayisi == ekip_sayisi:
        print("Afet kurtarma işlemi tamamlandı.")
    else:
        print("Afet kurtarma işlemi devam ediyor.")

    print("Çalışan Ekip Sayısı: {}".format(calisan_ekip_sayisi))
    print("Kurtarılan Kişi Sayısı: {}".format(kurtarilan_kisi_sayisi))

# Ana menüyü başlat
ana_menu()

             
             
             
            