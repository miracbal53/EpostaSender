## Toplu E-posta Gönderim Uygulaması

Bu uygulama, toplu e-posta gönderim işlemleri için kullanılır. Excel'den .txt'ye e-posta dönüştürücü ile e-posta adreslerini bir .txt dosyasına dönüştürebilir ve bu adreslere toplu e-posta gönderebilirsiniz.

## Özellikler

Belirli bir .txt dosyasından e-posta adreslerini okur ve toplu e-posta gönderimi yapar.
Dakikalık, saatlik ve günlük e-posta gönderim limitlerini kontrol eder.
Gönderim sırasında işlem durdurulabilir.
Gönderim durumu ve son gönderim zamanını gösterir.
Gereksinimler
Bu uygulama, Windows işletim sistemi için oluşturulmuş bir .exe dosyası içerir. Herhangi bir ek yazılım veya bağımlılık kurulumu gerektirmez.

## Kurulum

EmailSender.zip dosyasını indirin ve bilgisayarınızdaki bir klasöre çıkartın.
Kullanım
Çıkarttığınız klasördeki email_sender.exe dosyasını çalıştırmak için üzerine çift tıklayın.

Uygulama arayüzü açıldığında, aşağıdaki adımları izleyin:

Gönderici E-posta Adresi ve Gönderici Şifre alanlarını doldurun.
Konu ve Mesaj alanlarını doldurun.
Dosya Seç butonuna tıklayarak e-posta adreslerini içeren .txt dosyasını seçin.
Gönderilecek Kişi Sayısı ve Bekleme Süresi (saniye) alanlarını doldurun.
Gönder butonuna tıklayarak e-posta gönderim işlemini başlatın.
Gönderim işlemi sırasında Durdur butonuna tıklayarak işlemi durdurabilirsiniz.
E-posta gönderim durumu ve son gönderim zamanı arayüzde görüntülenecektir.

## Notlar

E-posta gönderim limitleri (dakikalık, saatlik, günlük) aşıldığında, uygulama otomatik olarak bekler ve limitlerin sıfırlanmasını sağlar.
Daha önce gönderilmiş e-posta adresleri sent_emails.txt dosyasına kaydedilir ve tekrar gönderim yapılmaz.
Gönderim durumu ve son gönderim zamanı bilgileri periyodik olarak güncellenir ve email_count.json dosyasında saklanır.
Hata Ayıklama
Eğer herhangi bir hata alırsanız veya işlem sırasında bir sorun yaşarsanız, uygulama log penceresinde hata mesajını görüntüleyecektir. Bu hata mesajını not alarak destek için bizimle iletişime geçebilirsiniz.

# Excel'den .txt'ye E-posta Dönüştürücü

Bu uygulama, Excel dosyasındaki (sadece A sütunundaki) e-posta adreslerini bir .txt dosyasına dönüştürmenize olanak tanır.

## Gereksinimler

Bu uygulama, Windows işletim sistemi için oluşturulmuş bir .exe dosyası içerir. Herhangi bir ek yazılım veya bağımlılık kurulumu gerektirmez.

## Kurulum

1. **ExceldenTXTyeDonusturucu.zip** dosyasını indirin ve bilgisayarınızdaki bir klasöre çıkartın.

## Kullanım

1. Çıkarttığınız klasördeki **email_converter.exe** dosyasını çalıştırmak için üzerine çift tıklayın.

2. Uygulama arayüzü açıldığında, **"Excel Dosyası Seç ve Dönüştür"** butonuna tıklayın.
   - Açılan dosya seçim penceresinden, e-posta adreslerini içeren Excel dosyasını seçin (sadece A sütununda e-posta adresleri olmalıdır).

3. Ardından, e-posta adreslerinin kaydedileceği .txt dosyasını kaydetmek için bir konum ve dosya adı seçin.

4. Dönüştürme işlemi tamamlandığında, uygulama log penceresinde işlem sonucunu görüntüleyecektir. E-posta adresleri başarıyla seçtiğiniz .txt dosyasına kaydedilecektir.

## Önemli Notlar

- Excel dosyasındaki e-posta adresleri sadece A sütununda yer almalıdır. Diğer sütunlar dikkate alınmayacaktır.
- .txt dosyasına kaydedilen e-posta adresleri her satırda bir adet olacak şekilde yazılacaktır.

## Hata Ayıklama

Eğer herhangi bir hata alırsanız veya işlem sırasında bir sorun yaşarsanız, uygulama log penceresinde hata mesajını görüntüleyecektir. Bu hata mesajını not alarak destek için bizimle iletişime geçebilirsiniz.

