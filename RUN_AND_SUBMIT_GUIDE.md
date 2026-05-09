# From Zero to Submission Guide

## 1. Lab hazırlığı

1. Kali Linux VM açın.
2. Metasploitable veya DVWA lab makinesini açın.
3. İki makinenin aynı host-only/internal network üzerinde olduğundan emin olun.
4. Lab makinesinin IP adresini bulun.

Örnek komut:

```bash
ip a
```

veya Kali tarafından keşif için:

```bash
netdiscover -r 192.168.56.0/24
```

## 2. Projeyi çalıştırma

```bash
sudo apt update
sudo apt install nmap python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
cd src
sudo ../venv/bin/python main.py
```

## 3. Ekran görüntüleri

Şunları screenshot alın:

1. Program başlangıcı ve hedef IP girişi
2. Nmap sonuçlarının terminalde görünmesi
3. Banner grabbing sonuçları
4. AI analiz çıktısı
5. `reports/security_report.html` dosyasının tarayıcıda açılmış hali

## 4. GitHub yükleme

Repo adı hocanın istediği formatta olmalı:

```text
OgrenciNo_AdSoyad
```

Komutlar:

```bash
git init
git add .
git commit -m "Initial final project submission"
git branch -M main
git remote add origin GITHUB_REPO_URL

git push -u origin main
```

Kontrol edin:

- `.env` GitHub'a gitmedi
- README görünüyor
- requirements.txt var
- Kod dosyaları var

## 5. PDF rapor hazırlama

`Final_Report_Template.docx` dosyasını açın.

Şunları doldurun:

- Ad soyad
- Öğrenci no
- Tarih
- GitHub linki
- YouTube linki
- Ekran görüntüleri
- Gerçek port sonuçları
- AI prompt ve AI cevabı

Sonra PDF olarak export edin.

## 6. Teslim

Ders sistemine şu üç şeyi yükleyin:

1. GitHub repo linki
2. YouTube video linki
3. PDF rapor
