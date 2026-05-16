# Stage Test Checklist — Pre-Evento

> Tutte le verifiche da fare **prima di salire sul palco**.
> Da stampare e seguire una riga alla volta.

---

## 📋 24 ore prima

### Asset

- [ ] Tutte le 17 clip Veo generate e approvate (`deck/assets/videos/scene_*_FINAL.mp4`)
- [ ] Tutti i 14 audio ElevenLabs generati (`deck/assets/audio/`)
- [ ] Musica generata (`deck/assets/audio/music_main_theme.mp3` + `music_outro.mp3`)
- [ ] 11 illustrazioni slide realistic (`deck/assets/images/realistic_*.svg`)
- [ ] Logo Eleven Digital in `deck/assets/images/logo.svg`

### Deck

- [ ] `python scripts/assemble_deck.py` esegue senza errori
- [ ] Report finale dichiara: 0 video mancanti, 0 illustrazioni mancanti
- [ ] `npx serve deck/ -l 8000` avvia il server
- [ ] Apertura in Chrome: tutte le slide visibili
- [ ] Fullscreen (F) funziona
- [ ] Speaker view (S) mostra le note di speech
- [ ] Audio si sente dalle casse del laptop
- [ ] Tutti i video partono in autoplay quando la slide è attiva
- [ ] Crossfade tra slide funziona
- [ ] Transizione speciale scena 12 → slide 13 funziona (overlay arancione)

### Backup

- [ ] Backup MP4 generato (`outputs/backup_video.mp4`, ~2-3 GB, 4K)
- [ ] MP4 riprodotto da inizio a fine senza glitch
- [ ] Copia su USB 1 (per Rocco)
- [ ] Copia su USB 2 (per il fonico)
- [ ] Backup deck completo (`tar -czf deck-backup.tar.gz deck/`) su un terzo storage

### Speech

- [ ] Rocco ha provato lo speech intero almeno 2 volte
- [ ] Tempo cronometrato: 15 min ± 30s
- [ ] Cue sheet stampata in formato A5 (4 pagine, font 18pt)
- [ ] Cue sheet in tasca + foto sul telefono

---

## 📋 3 ore prima (in sala)

### Test proiettore

- [ ] Connessione laptop → proiettore (HDMI o USB-C verificato)
- [ ] Risoluzione corretta (1920x1080 minimo, 4K se supportato)
- [ ] Test colore: la slide 13 ha sfondo PANNA, non grigio
- [ ] Test colore: la bussola arancione si vede bene, satura, non rossa
- [ ] Se i colori sono storti: chiedere al tecnico di calibrare
- [ ] Fullscreen senza barre nere/bordi

### Test audio

- [ ] Connessione laptop → mixer (jack 3.5mm o XLR)
- [ ] Test volume master: scena 3 (tempesta) — il picco — al volume giusto per la sala
- [ ] Verificare che la voce di Rocco e l'audio del deck non si coprano
- [ ] Test SCENA 8 (silenzio intenzionale 8s): assicurarsi che fonico non "spinga" volume pensando sia un guasto

### Test cliccker / controllo

- [ ] Clicker funzionante (batterie cariche, ricevitore connesso)
- [ ] Forward / Back funzionano
- [ ] (Bonus) Pedaliera testata
- [ ] Tastiera laptop con frecce funziona come backup
- [ ] Tasti `F` (fullscreen), `S` (speaker view), `M` (mute), `B` (blackout) testati

### Test laptop di backup

- [ ] Laptop secondario acceso, carico al 100%
- [ ] VLC aperto, MP4 backup caricato, **in pause sulla scena 1**
- [ ] Cavo HDMI/USB-C già collegato (pronto allo switch)
- [ ] Volume sistema al 80%

---

## 📋 1 ora prima

- [ ] Wi-Fi spento su entrambi i laptop
- [ ] Notifiche disattivate (Do Not Disturb)
- [ ] Slack, Mail, Telegram, Messages — chiusi
- [ ] Time Machine, backup cloud, sync — sospesi
- [ ] Cellulare in modalità aereo
- [ ] Reveal.js già aperto in fullscreen sulla slide 0 (cover)
- [ ] Browser senza altre tab aperte
- [ ] Test rapido audio (scena 3) con il volume reale della sala
- [ ] Acqua sul leggio
- [ ] Pastiglie per la voce in tasca
- [ ] Rocco ha bevuto acqua, fatto warm-up vocale (5 min)

---

## 📋 5 minuti prima

- [ ] Tutto pronto sul palco
- [ ] Backup laptop in pause su Scena 1
- [ ] Microfono testato
- [ ] Respiro profondo
- [ ] *"Anno zero. Adesso."*

---

## 🚨 Emergency contact

In caso di problema:
- Backup MP4 → switch laptop in 10 secondi (vedere `docs/08_BACKUP_PLAN.md`)
- Audio rotto → Rocco recita più drammaticamente (vedere scenario C)
- Wi-Fi assente → non è un problema, tutto offline
- Slide non parte → premere → per saltare, narrare comunque

---

## ✅ Post-evento

- [ ] Salvare un backup completo del deck come era prima dell'evento
- [ ] Esportare il MP4 come "production final"
- [ ] Caricare su Google Drive personale + Eleven Digital drive
- [ ] Annotare cosa è andato bene / male per il prossimo evento
- [ ] Cancellare service account GCP temporaneo (se creato per il progetto)
- [ ] Revocare API key ElevenLabs se solo per questo evento
