# Deploy — Dalla Scrivania all'Algoritmo

Pubblicare il deck su Vercel. Tutto **free tier**.

> Obiettivo finale: avere un URL tipo `https://dalla-scrivania-allalgoritmo.vercel.app/` che apra direttamente `deck/index.html` in fullscreen, con auto-deploy a ogni `git push` su `main`.

---

## Setup iniziale (una volta sola)

### 1. Installa Vercel CLI

```bash
npm i -g vercel
vercel --version   # deve restituire 32.x o superiore
```

Se non hai mai usato Vercel:
```bash
vercel login
# scegli "Continue with GitHub" — usa lo stesso account di GitHub
```

### 2. Link del progetto

Dalla root del repo (`Progetti_Claude_Code/dalla-scrivania-allalgoritmo`):

```bash
vercel link
```

Risposte consigliate:
- **Set up?** Y
- **Scope (account)?** scegli il tuo account personale
- **Link to existing project?** N (la prima volta)
- **Project name?** `dalla-scrivania-allalgoritmo` (oppure il nome che preferisci — sarà l'URL)
- **Directory?** `.` (la root — è già configurata da `vercel.json`)
- **Override settings?** N

Il comando crea `.vercel/project.json` (già in `.gitignore`).

### 3. Primo deploy

```bash
# preview (URL di test, non production)
vercel

# production (URL definitivo)
vercel --prod
```

Vercel restituisce un URL tipo:
- preview: `https://dalla-scrivania-allalgoritmo-abc123.vercel.app`
- production: `https://dalla-scrivania-allalgoritmo.vercel.app`

**Test minimo**: aprire l'URL su Chrome, premere `F` per fullscreen, navigare con frecce.

---

## Auto-deploy da GitHub (raccomandato)

Una volta che il link è fatto, collega il repo GitHub a Vercel:

1. Vai su https://vercel.com/dashboard
2. Trova il progetto `dalla-scrivania-allalgoritmo`
3. **Settings** → **Git** → **Connect Git Repository**
4. Scegli il repo GitHub
5. Conferma `main` come branch di production

Da quel momento:
- Ogni `git push origin main` → auto-deploy in production
- Ogni `git push origin <altro-branch>` → preview URL automatico (utile per esperimenti)
- I PR su GitHub mostrano un commento Vercel con preview link

---

## Verifica configurazione

```bash
# vede il config attivo e l'ultimo deploy
vercel project ls
vercel ls

# log dell'ultimo deploy se qualcosa non va
vercel logs
```

---

## Cose da sapere

### Asset pesanti (video MP4)

I 17 MP4 Veo possono pesare 200-500 MB totali. Sul free tier:
- **Bandwidth**: 100 GB/mese — più che sufficiente per una presentazione + pochi test
- **Build output**: 1 GB hard limit — se totali sforano, attenzione (riduci bitrate MP4)

Se la build pesa troppo: ridurre risoluzione/bitrate dei video con `ffmpeg`:
```bash
ffmpeg -i scene_01.mp4 -vcodec libx264 -crf 23 -preset slow -acodec aac -b:a 128k scene_01_web.mp4
```

### Headers di cache (già in `vercel.json`)

- Video/audio/immagini: `max-age=31536000, immutable` (cache aggressiva)
- `index.html`: `must-revalidate` (sempre la versione fresca)
- `Accept-Ranges: bytes` su media (permette seek/scrubbing nel browser)

### Custom domain (opzionale, post-evento)

Se vuoi un URL personalizzato (es. `presentazione.elevendigital.it`):
1. Vercel dashboard → progetto → **Settings** → **Domains**
2. Aggiungi il dominio
3. Configura il DNS come indica Vercel (CNAME o A record)

---

## Rollback se qualcosa va male

Vercel mantiene ogni deploy. Per tornare indietro:

```bash
vercel rollback              # interattivo, scegli il deploy precedente
vercel rollback <URL_PREV>   # rollback diretto a un URL specifico
```

In dashboard: **Deployments** → trova quello buono → **Promote to Production**.

---

## Checklist pre-presentazione (giorno 5)

- [ ] `vercel --prod` eseguito con tutti i 17 MP4 + 14 MP3 + 11 PNG presenti
- [ ] URL apre `deck/index.html` correttamente
- [ ] Fullscreen `F` su Chrome funziona
- [ ] Tutti i video partono in autoplay (con audio)
- [ ] Speaker View `S` mostra le note
- [ ] Backup: l'MP4 di `outputs/backup_video.mp4` è scaricato sul laptop offline
- [ ] Backup-backup: chiavetta USB con la versione offline del deck + MP4
- [ ] Test sul proiettore della sala: colori, suono, font

---

## Comandi rapidi (cheatsheet)

```bash
vercel               # deploy preview
vercel --prod        # deploy production
vercel ls            # lista deploy recenti
vercel logs          # log ultimo deploy
vercel rollback      # rollback interattivo
vercel env ls        # variabili d'ambiente (non servono in questo progetto)
vercel domains ls    # domini configurati
```
