# Proje Neva

<img src="https://i.imgur.com/MH1no3T.png" alt="Neva Logo" width="250">

## ● Takım İsmi
**AI Grup 2**

## ● Takım Rolleri
* **Product Owner:** `[Beyza  Erdem]`
* **Scrum Master:** `[Osman Şener Gürel]`
* **Developer:** `[Sena Demirbaş]`
* **Developer:** `[Muhammed Enes Güryeli]`
* **Developer:** `[Pelinsu İlçin]`

## ● Ürün İsmi
**Neva**

## ● Ürün Açıklaması
Neva, modern yaşamın getirdiği stres, kaygı ve yalnızlık gibi zorluklarla mücadele eden bireylere destek olmak amacıyla geliştirilmiş, yapay zeka tabanlı bir psikolojik destek ve sohbet asistanıdır. Kullanıcılarına sesli etkileşim yoluyla empatik, yargılamayan ve güvenli bir sohbet ortamı sunar. Amacımız, herkesin ihtiyaç duyduğu anda konuşabileceği bir "dijital sırdaş" yaratarak zihinsel farkındalığı artırmak ve yalnızlık hissini azaltmaktır.

## ● Ürün Özellikleri
* **Sesli Etkileşim:** Kullanıcılar, Neva ile doğal bir konuşma deneyimi yaşayabilmek için metin girişi yerine sesli komutları kullanabilir. Gelişmiş STT (Speech-to-Text) ve TTS (Text-to-Speech) teknolojileri ile akıcı bir diyalog sağlanır.
* **Empati Odaklı Diyalog:** Neva'nın temelinde, kullanıcıyı anlamaya ve ona değer verdiğini hissettirmeye programlanmış, gelişmiş bir Büyük Dil Modeli (LLM) bulunur.
* **Kısa Süreli Hafıza:** Neva, konuşmanın bağlamını korumak için diyaloğun son birkaç adımını hatırlayarak daha tutarlı ve anlamlı cevaplar üretir.
* **Kriz Anı Desteği:** Kullanıcının ifadelerinde kendine zarar verme veya derin bir umutsuzluk gibi kritik durumlar tespit edildiğinde, Neva profesyonel yardım kuruluşlarına yönlendirme yaparak etik ve güvenli bir sınır çizer.
* **Erişilebilir Arayüz:** Özellikle yaşlı veya teknolojiye uzak kullanıcılar düşünülerek tasarlanmış, basit, sade ve kullanımı kolay bir arayüze sahiptir.

## ● Hedef Kitle
* **Birincil Hedef Kitle:** Yoğun iş temposu, eğitim hayatı veya kişisel nedenlerden dolayı stres, kaygı ve tükenmişlik hisseden gençler ve yetişkinler.
* **İkincil Hedef Kitle:** Yalnızlık hisseden ve günlük sohbet ihtiyacı duyan, özellikle yaşlı bireyler.
* **Genel Kitle:** Duygu ve düşüncelerini yargılanma korkusu olmadan paylaşmak isteyen herkes.

## ● Product Backlog
Bu liste, projenin mevcut ve gelecekteki potansiyel özelliklerini içermektedir.

---

# SPRINT 1 RAPORU

**Sprint Adı/Numarası:** Sprint 1: Projeye Başlangıç  
**Takım Adı:** Nova Zihinler  
**Sprint Başlangıç Tarihi:** 29.06.2025  
**Sprint Bitiş Tarihi:** 02.07.2025

---

### 1. Sprint Hedefi (Sprint Goal)
Bu sprintin ana hedefi, projenin her dalını bir nebze olsa da ilerletmek ve temelini oluşturmaktı. Ekip arkadaşlarımızla beraber projemizin adını "Neva" olarak seçtikten sonra, kabaca bir şekilde ekipteki herkes ilgili olduğu alanda çalışmalarına başladı.

---

### 2. Tamamlanan İşler (Completed Work)
- **Sohbet API'si (`/chat`) oluşturuldu:** Uygulama, kullanıcıdan gelen mesajı alıp yapay zeka modeline gönderebiliyor ve modelin cevabını geri döndürebiliyor.
- **Google Generative AI API’si ile chat kısmı oluşturuldu:** Uygulama tabanı olarak hem bir dost hem de psikolojik bir yapay zeka asistanı olarak, karşısındaki insan ile yazılı olarak konuşma özelliği eklendi.
- **Kullanıcının chat üzerindeki hafızası `.json` olarak eklendi:** Uygulama kullanıcının önceki konuşma ve fikirlerini hatırlayacak şekilde güncellendi ve konuşma geçmişi kayıt edildi.
- **Ortak bir çalışma alanı (Github Repo’su) oluşturuldu:** Github üzerinden herkesin erişip çalışabileceği ve PR açabileceği bir ortam oluşturuldu.
- **Uygulamanın ilk arayüz tasarımı oluşturuldu:** .html ile ara yüz tasarımının ilk hali yapıldı.
---

### 3. Tamamlanamayan İşler ve Karşılaşılan Zorluklar
İlk sprintimiz olduğu için net hedefler konulmamıştı, bu yüzden teknik olarak tamamlanamayan bir görev bulunmamaktadır.
- **Karşılaşılan Zorluk:** Ekip olarak toplu olarak bir toplantıya katılıp fikir alış-verişinde bulunmakta  zorlandık fakat son zamanlarda bu sorunun üstesinden gelindi gibi.

---

### 4. Sprint İlerleme Grafiği (Burndown Chart)

![Sprint 1 Burndown Chart](https://i.imgur.com/XvUqLdA.png)

---

### 5. Sprint Geri Bildirimi (Retrospective'den Notlar)
- **İyi Gidenler:** Genel olarak uygulamanın geliştirilmesi, herkesin en sonunda senkronize olup yapılacaklara odaklanması ve birbirine kolaylık sağlaması.
- **Geliştirilmesi Gerekenler:** Takım içi iletişimi daha düzenli hale getirmek ve projedeki boş kalan alanları proaktif olarak doldurmak.

---

### 6. Sonraki Sprint İçin Öncelikli Konular
- TTS (Text-to-Speech) teknolojisinin belirlenmesi ve implementasyonu.
- Backend mimarisinin geliştirilmesi.
- Arayüz tasarımı ve temel kaynak kodlarının geliştirilmesi.