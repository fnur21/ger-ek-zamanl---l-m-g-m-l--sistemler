from machine import Pin, I2C
from hx711 import HX711
from ds1307 import DS1307
import time

# HX711 ayarı
hx = HX711(dout=Pin(13), pd_sck=Pin(12))
hx.set_scale(420)  # Kalibrasyon katsayısı
hx.tare()
print("HX711 başlatıldı. Ağırlık okunuyor...")

# RTC ayarı (I2C: SCL=GP1, SDA=GP0)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
rtc = DS1307(i2c)

# LED bar (yalnızca 10 pin kullanıyoruz)
anot_pins = [Pin(i, Pin.OUT) for i in range(2, 12)]   # GP2–GP11
katot_pins = [Pin(i, Pin.OUT) for i in range(16, 26)] # GP16–GP25

# Sadece 10 pinlik liste alalım
anot_pins = anot_pins[:10]
katot_pins = katot_pins[:10]

# Uyarı LED (kırmızı)
relay_led = Pin(15, Pin.OUT)

# LED bar güncelleme fonksiyonu
def update_led_bar(led_count):
    for i in range(10):
        if i < led_count:
            anot_pins[i].value(1)
            katot_pins[i].value(0)
        else:
            anot_pins[i].value(0)
            katot_pins[i].value(1)

# Ana döngü
while True:
    try:
        # Ağırlığı oku
        weight = hx.get_weight(1)
        if weight is None:
            print("⚠️ Ağırlık okunamadı.")
            continue

        print("Ağırlık: {:.2f} kg".format(weight))

        # LED bar güncelle
        led_level = min(10, max(0, int(weight / 5)))  # 0–100kg için
        update_led_bar(led_level)

        # Saat bilgisini al
        try:
            saat_tuple = rtc.datetime()
            saat, dakika, saniye = saat_tuple[4], saat_tuple[5], saat_tuple[6]
        except:
            saat, dakika, saniye = 0, 0, 0  # RTC hatalıysa varsayılan saat

        # Ağırlık sınır kontrolü
        if weight >= 50:
            relay_led.value(1)
            print("‼️ AŞIM: Ağırlık sınırı geçildi!")
            print("⏰ Saat: {:02d}:{:02d}:{:02d}".format(saat, dakika, saniye))
        else:
            relay_led.value(0)

        time.sleep(1)

    except Exception as e:
        print("⚠️ Hata:", e)
        time.sleep(1)
