<div align="center">

# 🐧 YOLO Projekat Linux 
### *Native GTK4 Komandni Panel za Autonomnu Sistemsku Kontrolu*

[![GTK4](https://img.shields.io/badge/Framework-GTK_4-62a0ea?style=for-the-badge&logo=gnome&logoColor=white)](https://www.gtk.org/)
[![Libadwaita](https://img.shields.io/badge/UI-Libadwaita-3584e4?style=for-the-badge&logo=gnome&logoColor=white)](https://gnome.pages.gitlab.gnome.org/libadwaita/)
[![Python](https://img.shields.io/badge/Language-Python_3-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tux](https://img.shields.io/badge/OS-Linux_Native-fcd116?style=for-the-badge&logo=linux&logoColor=black)](https://kernel.org)

---

<p align="center">
  <b>YOLO Robot Linux</b> je klijent projektovan za maksimalne performanse na Linux distribucijama. 
  <br>Uz snagu <b>Tux-a</b> pod haubom, aplikacija koristi GTK4 za direktan pristup hardverskoj akceleraciji i YOLOv8 za inteligentno upravljanje.
</p>

</div>

## 🚀 Ključne Komponente

### 🐧 Linux-First Arhitektura
* **Native Video Rendering:** Umesto emulacije, koristimo direktan GDK pipeline za prikaz slike, što drastično smanjuje latenciju u odnosu na Windows verziju.
* **Tux-Optimized AI:** YOLOv8 model je optimizovan za rad na Linux kernelu, koristeći napredne drajvere za GPU ubrzanje detekcije.
* **Unified Packaging:** Zahvaljujući GitHub Akcijama, aplikacija je dostupna kao potpisani `.deb` i `.rpm` paketi, spremni za instalaciju na bilo kojoj distribuciji.

### 🎮 Kontrola i Telemetrija
* **Asinhrona Stabilnost:** `asyncio` loop je integrisan u srce GTK-a, omogućavajući glatko kretanje robota dok se vrši teška AI analiza.
* **Keyboard Driver:** Optimizovan za X11 i Wayland protokole, pružajući trenutni odziv na WASD komande.

---

## 🛠 Tehnološki Stack

| Segment | Tehnologija | Uloga |
| :--- | :--- | :--- |
| **Core OS** | Linux (Kernel Based) | Base Environment |
| **UI Framework** | GTK4 / Libadwaita | Native UI & Theming |
| **AI Inference** | Ultralytics YOLOv8 | Vision & Logic |
| **Networking** | Websockets (Async) | Low-Latency Link |
| **Automation** | GitHub Actions | CI/CD & Caching |

---

## 🔧 Instalacija i Pokretanje

### 📥 Preko paketa (Preporučeno)
Preuzmite `.deb` (Debian/Ubuntu) ili `.rpm` (Fedora) sa **Releases** taba i instalirajte ga. yolov8n.pt treba da se nalazi u Documents folderu.

<div align="center">

Autor: Danilo Stoletović • Mentor: Dejan Batanjac

ETŠ „Nikola Tesla“ Niš • 2026

</div>
