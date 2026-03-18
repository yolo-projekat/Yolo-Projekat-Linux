<div align="center">

# 🗄️ [ARHIVIRANO] YOLO Projekat Linux 
### *Istorijski Native GTK4 Komandni Panel za Autonomnu Sistemsku Kontrolu*

> [!WARNING]  
> **STATUS REPOZITORIJUMA: ARHIVIRAN (DEPRECATED)**
> 
> Ovaj repozitorijum sadrži izvornu **Linux (GTK4/Python)** verziju klijenta za YOLO Projekat i više se ne održava. Sav dalji razvoj grafičkih interfejsa fokusiran je na Android platformu.
>
> **Inženjersko objašnjenje tranzicije:** Iako je GTK4 sa Libadwaita dizajnom pružio izvanredne performanse i nativno iskustvo na Linuxu, doneta je strateška odluka o preraspodeli resursa (Resource Allocation). S obzirom na to da je YOLO Projekat primarno edukativna platforma, analize su pokazale veoma nizak udeo Linux korisnika među ciljnom grupom učenika i studenata. 
> 
> **Trade-offs (Kompromisi):** Održavanje dve potpuno odvojene, nativne baze koda zahtevalo je preveliko rasipanje resursa. Odbacili smo izuzetno brzi, nativni GDK pipeline i Tux-optimizovanu arhitekturu kako bismo centralizovali napore na platformu koju koristi apsolutna većina korisnika u učionicama. Time osiguravamo viši kvalitet i brži razvoj glavnog klijenta.

[![GTK4](https://img.shields.io/badge/Framework-GTK_4-gray?style=for-the-badge&logo=gnome&logoColor=white)](https://www.gtk.org/)
[![Libadwaita](https://img.shields.io/badge/UI-Libadwaita-gray?style=for-the-badge&logo=gnome&logoColor=white)](https://gnome.pages.gitlab.gnome.org/libadwaita/)
[![Python](https://img.shields.io/badge/Language-Python_3-gray?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tux](https://img.shields.io/badge/OS-Linux_Native-gray?style=for-the-badge&logo=linux&logoColor=white)](https://kernel.org)

---

<p align="center">
  <i>Istorijska arhiva: Originalni kod za nativnu Linux aplikaciju koja je koristila GTK4 za direktan pristup hardverskoj akceleraciji i YOLOv8 inteligentno upravljanje vozilom.</i>
</p>

</div>

## 🧩 Originalna Linux-First Arhitektura (Istorija)

Ovaj klijent je bio projektovan za maksimalne performanse na Linux distribucijama. Iako se više ne razvija, posedovao je napredna tehnička rešenja:

* **Native Video Rendering:** Umesto emulacije, korišćen je direktan GDK pipeline za prikaz slike, što je drastično smanjivalo latenciju.
* **Tux-Optimized AI:** YOLOv8 model je bio specifično optimizovan za rad na Linux kernelu, koristeći napredne drajvere za GPU ubrzanje detekcije.
* **Asinhrona Stabilnost:** `asyncio` loop je bio integrisan u samo srce GTK-a, omogućavajući glatko kretanje robota uz tešku AI analizu u pozadini.
* **Keyboard Driver:** Posebno optimizovan za X11 i Wayland protokole, pružao je trenutni odziv na WASD komande.
* **Unified Packaging:** Potpuno automatizovana CI/CD isporuka potpisanih `.deb` i `.rpm` paketa.

---

## 🛠 Stari Tehnološki Stack

| Segment | Tehnologija | Uloga u ovoj verziji (Sada napušteno) |
| :--- | :--- | :--- |
| **Core OS** | **Linux (Kernel Based)** | Osnovno radno okruženje |
| **UI Framework** | **GTK4 / Libadwaita** | Nativni interfejs i sistemsko temiranje |
| **AI Inference** | **Ultralytics YOLOv8** | Računarski vid i primena logike |
| **Networking** | **WebSockets (Async)** | Kontrolni link veoma niske latencije |
| **Automation** | **GitHub Actions** | CI/CD kompajliranje i distribucija paketa |

---

## 🔧 Istorijska Instalacija i Pokretanje

Sistem se oslanjao na lokalnu instalaciju unapred pripremljenih paketa:

* **Distribucija paketa:** `.deb` (Debian/Ubuntu) ili `.rpm` (Fedora) arhiva preuzimala se direktno sa GitHub **Releases** stranice.
* **Lokalna zavisnost:** Aplikacija je bila hardkodovana da učitava `yolov8n.pt` model isključivo ukoliko se on nalazio u korisničkom `Documents` folderu.

---

<div align="center">

**Autor:** Danilo Stoletović • **Mentor:** Dejan Batanjac
**ETŠ „Nikola Tesla“ Niš • 2026**

</div>
