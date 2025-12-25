# Raspberry Pi Smart Air Quality Monitoring System

Bu proje, Raspberry Pi ve Arduino tabanlı sensörler kullanılarak
ortam hava kalitesini izlemek, verileri analiz etmek ve
yapay zeka destekli sınıflandırma yapmak amacıyla geliştirilmiştir.

## Proje Amacı
Bu çalışmanın amacı, düşük maliyetli sensörler kullanarak
gerçek zamanlı hava kalitesi izleme sistemi geliştirmek
ve elde edilen verileri kullanıcıya anlaşılır bir arayüz
üzerinden sunmaktır.

## Kullanılan Donanımlar
- Raspberry Pi 4
- Arduino Uno
- MQ-2 Gaz Sensörü
- MQ-135 Gaz Sensörü
- DHT11 / DHT22 Sıcaklık-Nem Sensörü

## Kullanılan Yazılımlar ve Teknolojiler
- Python
- Streamlit
- Pandas
- Scikit-learn / Joblib
- Arduino IDE

## Sistem Nasıl Çalışır?
1. Arduino, sensörlerden sıcaklık, nem ve gaz verilerini okur.
2. Okunan veriler seri haberleşme ile Raspberry Pi'ye gönderilir.
3. Raspberry Pi, verileri CSV dosyasına kaydeder.
4. Makine öğrenmesi modeli ile hava kalitesi sınıflandırılır.
5. Streamlit tabanlı web arayüzü üzerinden veriler görselleştirilir.

## Kurulum ve Çalıştırma

```bash
python -m venv venv-air
source venv-air/bin/activate
pip install -r requirements.txt
python veri.py
streamlit run dashboard.py



