## Proje Amacı
- Düşük maliyetli sensörlerle **gerçek zamanlı hava kalitesi izleme** sistemi geliştirmek  
- Sensör verilerini zaman damgası ile **CSV formatında** kayıt altına almak  
- Raspberry Pi üzerinde çalışan **makine öğrenmesi modeli** ile hava kalitesini sınıflandırmak  
- Sonuçları kullanıcıya anlaşılır şekilde **web dashboard** üzerinden sunmak  
- IoT + embedded + edge AI kavramlarını tek bir uygulamada bütünleştirmek  

---

## Sistem Mimarisi ve Veri Akışı
1. **Arduino**, MQ-2, MQ-135 ve sıcaklık/nem sensörlerinden verileri okur.  
2. Okunan veriler **seri haberleşme (USB/Serial)** ile Raspberry Pi’ye gönderilir.  
3. **Raspberry Pi (Python)** seri porttan veriyi alır ve **CSV dosyasına** kaydeder.  
4. Raspberry Pi üzerinde bulunan **eğitilmiş ML modeli (joblib)** ile hava kalitesi sınıflandırılır.  
5. **Streamlit dashboard** anlık metrikleri, grafiklerini ve AI tahminini web arayüzünde gösterir.  

---

## Kullanılan Donanımlar
- Raspberry Pi 4  
- Arduino Uno  
- MQ-2 Gaz Sensörü  
- MQ-135 Gaz Sensörü  
- Sıcaklık/Nem Sensörü (DHT serisi)  
- USB bağlantı kabloları ve bağlantı elemanları  

---

## Kullanılan Yazılım ve Teknolojiler
- Python 3  
- Streamlit (web arayüz)  
- Pandas (veri işleme)  
- Scikit-learn / Joblib (model yükleme ve tahmin)  
- PySerial (seri port iletişimi)  
- Requests (API istekleri - opsiyonel)  
- Arduino IDE  
- Raspberry Pi OS (Linux)  

---

## Veri Formatı (CSV)
Raspberry Pi üzerinde sensör verileri `sensor_log.csv` dosyasına kaydedilir.

Örnek kolonlar:
- `iso_time` : kayıt zamanı (ISO)  
- `unix`     : unix timestamp  
- `temp_c`   : sıcaklık (°C)  
- `hum_pct`  : nem (%)  
- `mq2`      : MQ-2 sensör değeri  
- `mq135`    : MQ-135 sensör değeri  

---

## Edge AI (Uçta Yapay Zeka) Açıklaması
Makine öğrenmesi modeli **Raspberry Pi üzerinde yerel olarak** çalıştırılır. Bu yaklaşım edge AI olarak adlandırılır:
- İnternet bağımlılığını azaltır  
- Gecikmeyi düşürür  
- Veriyi yerelde işleyerek gizlilik sağlar  

Model, son sensör değerlerini kullanarak hava kalitesini **Good / Moderate / Bad** sınıflarından biri olarak tahmin eder ve olasılık değerleriyle (predict_proba) karar güvenini raporlayabilir.


## Teşekkür
- Bu proje Mühendislikte Bilgisayar Uygulamaları dersi kapsamında geliştirilmiştir.

- Bu proje sürecinde değerli yönlendirmeleri ve katkıları için Dr.öğretim Üyesi Halil İbrahim Okur'a teşekkür ederim.

# Raspberry Pi Smart Air Quality Monitoring System
**IoT • Embedded Systems • Edge AI**

Bu proje, **IoT ve gömülü sistemler** kullanılarak ortam hava kalitesinin izlenmesi, sensör verilerinin kayıt altına alınması ve **edge AI (uçta yapay zeka)** yaklaşımıyla hava kalitesi sınıflandırması yapılması amacıyla geliştirilmiştir. Sistem; Arduino ile sensör okuma, Raspberry Pi üzerinde veri işleme/kayıt, makine öğrenmesi modeli ile sınıflandırma ve Streamlit tabanlı web arayüzünden oluşur. Düşük maliyetli donanımlar ile gerçek zamanlı çevresel izleme yapılabileceğini uygulamalı olarak göstermektedir.

---


## Kurulum ve Çalıştırma (Raspberry Pi)

### 1) Sistem gereksinimleri
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version
