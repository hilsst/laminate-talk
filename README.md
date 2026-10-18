# Laminate Talk

İngilizce konuşma pratiği uygulaması: kompozit mühendisliği toplantıları, iş iletişimi ve günlük sohbet. 63 konu × 3 seviye, kayıtlı diyalog sesleri, 4/3/2 anlatım, Claude ile toplantı simülasyonu ve Oxford 3000 kelime tekrarı.

- Uygulama: GitHub Pages adresinden açılır, telefona ve bilgisayara "Ana ekrana ekle / Uygulamayı yükle" ile kurulur, internet olmadan da açılır.
- Toplantı partneri, "daha doğal hali" ve kelime bulma için Ayarlar'dan bir Claude API anahtarı girilir (anahtar sadece cihazda saklanır).
- İlerleme cihazda saklanır; Ayarlar'daki yedekle / yedeği yükle ile cihazlar arasında taşınır.

`source/` klasörü içerik kaynaklarını (diyalog metinleri, anlatım planları) ve derleme betiklerini içerir.

Sesler: Piper TTS (rhasspy/piper, en-us lessac ve ryan sesleri). Tarayıcı içi ses motoru: onnxruntime-web 1.18.0 ve phonemizer 1.2.1.
