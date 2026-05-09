# AI Destekli Ağ Güvenlik Tarayıcı Aracı

Bu proje BVA5108 Yapay Zeka Destekli Siber Güvenlik final ödevi için hazırlanmıştır.

## Seçilen Modüller

- M1 Port Tarama Modülü: Nmap SYN tarama, servis versiyonu tespiti ve XML parse
- M6 Banner Grabbing Modülü: Açık portlardan banner bilgisi alma

## Etik Uyarı

Bu araç yalnızca kendi lab ortamınızda kullanılmalıdır. Gerçek sistemlere, kurum ağlarına veya üçüncü taraf cihazlara yönelik tarama yapılmamalıdır.

İzin verilen örnek hedefler:

- Metasploitable
- DVWA
- Kendi VirtualBox/VMware lab makineniz
- 192.168.x.x veya 10.x.x.x aralığındaki kendi lab IP adresiniz

## Kurulum

### 1. Kali üzerinde Nmap kurun

```bash
sudo apt update
sudo apt install nmap
```

### 2. Projeyi klonlayın

```bash
git clone REPO_LINKINIZ
cd REPO_KLASOR_ADI
```

### 3. Python sanal ortam oluşturun

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Gereksinimleri yükleyin

```bash
pip install -r requirements.txt
```

### 5. API anahtarını ayarlayın

```bash
cp .env.example .env
nano .env
```

`.env` dosyasına Gemini API anahtarınızı yazın:

```env
GEMINI_API_KEY=GERCEK_API_KEYINIZ
GEMINI_MODEL=gemini-1.5-flash
```

`.env` dosyası GitHub'a yüklenmemelidir.

## Kullanım

```bash
cd src
sudo ../venv/bin/python main.py
```

Program hedef IP adresini isteyecektir. Yalnızca kendi lab makinenizin özel IP adresini girin.

Örnek:

```text
Hedef IP adresini girin: 192.168.56.101
```

## Araç Akışı

1. Kullanıcı hedef IP adresini girer
2. M1 modülü Nmap ile SYN scan ve servis versiyon tespiti yapar
3. Nmap XML çıktısı Python ile parse edilir
4. M6 modülü açık portlarda banner grabbing yapar
5. Bulgular Gemini API'ye gönderilir
6. Türkçe AI güvenlik analizi alınır
7. HTML rapor oluşturulur

## HTML Rapor

Program çalıştıktan sonra rapor şu konumda oluşur:

```text
reports/security_report.html
```

Rapor içeriği:

- M1 port tarama sonuçları
- M6 banner grabbing sonuçları
- AI API'ye gönderilen prompt
- AI tarafından üretilen Türkçe güvenlik analizi

## Kullanılan AI API

Google Gemini Flash kullanılmıştır.

Model:

```text
gemini-1.5-flash
```

## Dosya Yapısı

```text
src/
  main.py
  scanner.py
  banner_grabber.py
  ai_analysis.py
  report_generator.py
requirements.txt
.gitignore
.env.example
README.md
```

## Ekran Görüntüleri

PDF rapor için aşağıdaki ekran görüntüleri alınmalıdır:

1. Programın terminalde çalışması
2. Nmap port tarama çıktısı
3. Banner grabbing çıktısı
4. AI API analiz çıktısı
5. HTML raporun tarayıcıda açılmış hali

## Not

Kodda hazır veya sahte çıktı kullanılmamıştır. Nmap çıktısı gerçek zamanlı alınır ve XML olarak parse edilir.
