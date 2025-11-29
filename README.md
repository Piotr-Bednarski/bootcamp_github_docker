## Bootcamp – Zadanie warsztatowe 

## Cel
- Uruchomić trening lokalnie i w Dockerze.
- Przećwiczyć workflow z gałęzią `dev_1` i PR → merge do `main`.
- Wprowadzić drobną zmianę w kodzie (np. komunikat lub hiperparametr) i wypchnąć ją.
- Zademonstrować podstawy Dockera: `docker images`, `docker ps`, wejście do kontenera (`docker exec`).
- (Opcjonalnie) Pokazać `git pull --rebase` na gałęzi `dev_1`.
- (Opcjonalnie) Otagować wydanie.

---

## 1) Szybkie uruchomienie projektu

### 1.1 Lokalnie (Python)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.train
python -m src.predict
```
Oczekiwane:
- po treningu powstanie plik `artifacts/model.joblib`,
- w konsoli zobaczysz accuracy i predykcje.

### 1.2 Docker (build + run)
```bash
docker build -t bootcamp-ml:latest .
docker run --rm -v "$PWD/artifacts:/app/artifacts" bootcamp-ml:latest
```

### 1.3 Docker Compose (zalecane na warsztacie)
```bash
docker compose up --build
```

---

## 2) Workflow Git: `dev_1` → PR → merge do `main`

### 2.1 Utworzenie gałęzi `dev_1` od `main` i wypchnięcie do zdalnego
```bash
git switch -c dev_1
git push -u origin dev_1
```

### 2.2 Edycja kodu, commit i push
Przykład 1 (czytelniejszy komunikat w `src/train.py`):
```bash
git add src/train.py
git commit -m "zmiana parametrów"
git push
```

Przykład 2 (lekka zmiana hiperparametru w `src/model.py`, funkcja `build_pipeline()`):
```python
("clf", LogisticRegression(max_iter=500, n_jobs=1, random_state=42))
```

### 2.3 Pull Request
- Otwórz PR z `dev_1` → `main`.
- W opisie PR:
  - krótko: co zmieniono i po co,
  - jak uruchomić i sprawdzić.
- Zrób review w parach i zmerguj (np. squash merge).

---

## 3) Docker – krótkie demo: ps, obrazy, wejście do kontenera

### 3.1 Obrazy i kontenery
```bash
docker images
docker ps
docker ps -a
```

### 3.2 Build obrazu i uruchomienie kontenera na chwilę
Uruchom standardowy trening:
```bash
docker build -t bootcamp-ml:latest .
docker run --rm -v "$PWD/artifacts:/app/artifacts" --name ml-train-once bootcamp-ml:latest
docker ps -a  # zobaczysz zakończony kontener ml-train-once
```

Aby zademonstrować wejście do działającego kontenera, wystartuj go w tle:
```bash
docker run -d --name ml-demo -v "$PWD/artifacts:/app/artifacts" bootcamp-ml:latest tail -f /dev/null
docker ps  # teraz widać ml-demo
docker logs ml-demo
docker exec -it ml-demo /bin/sh   # lub /bin/bash, jeśli dostępny
# wewnątrz kontenera:
python -m src.train
exit
docker stop ml-demo && docker rm ml-demo
```

### 3.3 Compose 
```bash
docker compose up --build         # trening i zakończenie
docker compose up --build -d      # uruchom w tle (zakończy się szybko po treningu)
docker compose ps
docker compose logs -n 100
docker compose down
```

---

## 4) (Opcjonalnie) `git pull --rebase` na `dev_1`

Jeśli `main` poszedł do przodu, możesz zaktualizować `dev_1`:
```bash
git switch dev_1
git fetch origin
git pull --rebase origin main      # lub: git rebase origin/main
```
Rozwiąż ewentualne konflikty, dokończ rebase i wypchnij:
```bash
git push --force-with-lease
```

---

## 5) Wydanie: tag i push tagów
Po zmergowaniu PR z `dev_1` do `main`:
```bash
git switch main
git pull
git tag v0.1.0 -m ""
git push origin main --tags
```

---
---

## 6) Szybkie polecenia (ściąga)
- Uruchom lokalnie:
  ```bash
  python -m src.train && python -m src.predict
  ```
- Uruchom Docker:
  ```bash
  docker build -t bootcamp-ml:latest .
  docker run --rm -v "$PWD/artifacts:/app/artifacts" bootcamp-ml:latest
  ```
- Uruchom Compose:
  ```bash
  docker compose up --build
  ```
- Gałęzie:
  ```bash
  git switch -c dev_1
  git push -u origin dev_1
  ```
- Pull rebase:
  ```bash
  git pull --rebase origin main
  ```
- Docker ps / exec:
  ```bash
  docker images
  docker ps -a
  docker exec -it <container_id_or_name> /bin/sh
  ```
