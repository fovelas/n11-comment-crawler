# N11Crawler
n11.com'da yer alan ürünlere yapılan yorumları çekmek için yazılmıştır.

-----------------------------------------

### Dokümantasyon
* [Kurulum](#kurulum)
* [Kullanım](#kullanım)
* [Parametreler](#parametreler)
* [Fonksiyonlar](#fonksiyonlar)
* [Product Id Nasıl Bulunur?](#product-id-nasıl-bulunur)

-----------------------------------------

### Katkıda Bulunanlar
İstediğiniz veya eksik olan fonksiyonlar için `issue` açabilirsiniz. Ya da katkıda bulunmak için fonksiyonları kendiniz yazın ve `pull request` gönderin.

![Katkıda Bulunanlar](https://contrib.rocks/image?repo=hakansrndk60/n11-comment-crawler)

-----------------------------------------

### Kurulum
`n11_crawler.py` ve `requirements.txt` dosyalarını projenizin olduğu yere atın.

Daha sonra terminalde aşağıdaki kodu çalıştırın.
~~~
pip install -r requirements.txt
~~~

-----------------------------------------

### Kullanım
```python
from n11_crawler import N11Crawler

crawler = N11Crawler("561281932", save_as_json=True, max_comments=100, progress_bar=True)
crawler.run()
```

-----------------------------------------

### Parametreler

| Parametre    | Default Değeri | Açıklama                                                           |
| ------------ | -------------- | ------------------------------------------------------------------ |
| product_id   | Yok            | Ürünün id si.                                                      |
| save_as_json | False          | Çekilen yorumları bitişte otomatik olarak JSON dosyasına kaydeder. |
| max_comments | 1000           | Maksimum kaç tane yorum çekileceğini belirler.                     |
| progress_bar | False          | Progress bar göster/gösterme.                                      |

Parametrelerin kullanımına örnek:
```python
crawler = N11Crawler("561281932", save_as_json=True, max_comments=100, progress_bar=True)
```

-----------------------------------------

### Fonksiyonlar

| Fonksiyon             | Açıklama                                                                                      |
| --------------------- | --------------------------------------------------------------------------------------------- |
| run()                 | Tüm yorumları çekmeye başlar. Diğer fonksiyonlar bu fonksiyondan sonra çağırılmak zorundadır. |
| get_comments()        | Çekilmiş yorumları array olarak verir.                                                        |
| get_page_count()      | Toplam yorum sayfası sayısını verir. Her yorum sayfası maksimum 8 yorumdan oluşur.            |
| get_fetch_time()      | run() fonksiyonunun ne kadar sürede tamamlandığını saniye cinsinden verir.                    |
| get_comments_length() | Çekilmiş yorumların sayısını verir.                                                           |
| save_as_json()        | Yorumları JSON dosyasına kaydeder.                                                            |

Fonksiyonların kullanımına örnekler:
```python
crawler.get_comments()[0]["date"]
crawler.get_page_count()
crawler.get_fetch_time()
crawler.get_comments_length()
crawler.save_as_json(filename="yorumlar") # yorumlar.json
```

-----------------------------------------

### Product Id Nasıl Bulunur?

Aşağıdaki gibi **233 Yorum** yazan yere sağ tık yapıp **İncele** diyerekten bulabilirsiniz. Karşınıza `data-product-id="205217777"` çıkacaktır. Bu ürünün id si `205217777` olmuş olur.

Ya da **Ctrl+F** ile `data-product-id` aratabilirsiniz.

<img src="https://img001.prntscr.com/file/img001/ZatP0bUtSD6UJU2X1Z7n1A.png" width="100%" center />
<img src="https://img001.prntscr.com/file/img001/AmYV2AeoSZiEaK-1AuLT4g.png" width="100%" center />

-----------------------------------------

### Uyarı

Bu proje yorumlardan veri seti oluşturmak amacıyla yazılmıştır. Eğer **n11.com** için sorun teşkil ediyorsa yetkililer bana mail üzerinden ulaşabilir. Projeyi kaldırabilirim.