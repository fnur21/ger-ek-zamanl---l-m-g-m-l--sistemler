Ağırlık Tespit ve Uyarı Sistemi (MicroPython - Raspberry Pi Pico)
Merhaba! Ben Nur, bu proje benim okul ödevim ve pratik elektronik bilgimi geliştirmek için hazırladığım bir çalışmadır.
Bu sistemle, ağırlık belli bir sınırı geçtiğinde LED’lerle görsel uyarı verilmekte ve ileride röle kullanılarak sistemsel tepki verme altyapısı oluşturulmuştur.

🧠 Projenin Amacı
Bu projede amaç, bir yük sensörü (HX711 + load cell) ile anlık ağırlığı ölçmek, LED bar ile görsel olarak seviyeyi göstermek ve eğer belirli bir sınır aşılırsa kırmızı LED ile uyarı vermektir.
İleride röle modülü bağlanarak harici bir cihazın kontrolü (örneğin motor kesme, alarm sistemi) sağlanabilir.
Ayrıca DS1307 RTC modülü ile ağırlığın aşıldığı an kaydedilir.

🔧 Kullanılan Malzemeler
Parça	                        Açıklama
Raspberry Pi Pico           	Ana denetleyici (MicroPython)
HX711 + Load Cell	            Ağırlık ölçüm sensörü
DS1307 RTC	                  Gerçek zaman saati modülü
LED Bar (10’lu)	              Görsel seviye göstergesi
Kırmızı LED	                  Ağırlık aşıldığında uyarı vermek için


⚙️ Nasıl Çalışır?
Başlangıçta teraziyi sıfırlıyoruz (tare()).

Sensörden gelen ağırlık değeri okunur.

Her 5 kg'de bir LED yanar (50 kg = 10 LED).

Ağırlık 50 kg’yi geçerse, kırmızı uyarı LED’i yanar.

RTC modülü üzerinden saat bilgisi alınır ve terminale yazdırılır.
