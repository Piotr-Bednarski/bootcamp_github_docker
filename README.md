## Bootcamp – Zadanie warsztatowe (po setupie)

Poniżej znajdziesz precyzyjne kroki, które wykonamy wspólnie po zakończeniu instalacji i konfiguracji środowiska. Będziemy pracować na tym repozytorium, wykorzystując Git (gałęzie, PR, konflikty), Dockera (Dockerfile, Compose) oraz mini‑projekt ML na zbiorze Iris.

Repo zawiera już:
- `src/data.py`, `src/model.py`, `src/train.py`, `src/predict.py`
- `requirements.txt`, `Dockerfile`, `docker-compose.yml`
- artefakty uczenia zapisywane są do katalogu `artifacts/` (wykluczony w `.gitignore`)

---

## Cel
- Uruchomić trening lokalnie i w Dockerze.
- Przećwiczyć workflow z gałęzią `dev` i PR-ami.
- Wprowadzić drobne modyfikacje modelu (hyperparametry) i porównać accuracy.
- Zademonstrować stash oraz rozwiązanie konfliktu merge.
- Otagować wydanie.

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

## 2) Workflow Git: `dev` + PR

### 2.1 Utworzenie gałęzi `dev` i wypchnięcie do zdalnego
```bash
git switch -c dev
git push -u origin dev
```

### 2.2 Nowa funkcja/eksperyment na gałęzi feature
```bash
git switch -c feature/tune-logreg dev
```
Zmodyfikuj hiperparametry w `src/model.py` (funkcja `build_pipeline()`), np. zmień konfigurację `LogisticRegression`:
```python
("clf", LogisticRegression(max_iter=500, n_jobs=1, random_state=42, C=0.5))
```
Następnie:
```bash
python -m src.train
git add src/model.py
git commit -m "Tune LogisticRegression: max_iter=500, C=0.5"
git push -u origin feature/tune-logreg
```

### 2.3 Pull Request do `dev`
- Otwórz PR z `feature/tune-logreg` → `dev`.
- W opisie PR:
  - krótko: co zmieniono i po co,
  - jak uruchomić i sprawdzić.
- Zrób review w parach i zmerguj (squash merge).

---

## 3) Stash i hotfix

### 3.1 Symulacja pracy w toku
Na `feature/tune-logreg` wprowadź dowolną zmianę „w toku”, ale jej nie commituj (np. dodaj dodatkowy `print` w `src/train.py`).
```bash
git status  # widzisz zmiany w plikach
git stash push -m "work-in-progress: extra logging"
```

### 3.2 Hotfix na `dev`
```bash
git switch dev
git switch -c hotfix/adjust-train-msg
```
W pliku `src/train.py` dodaj czytelniejszy komunikat startu, np.:
```python
print("[train] Starting training pipeline...")
```
```bash
python -m src.train
git add src/train.py
git commit -m "Hotfix: clearer start message in training"
git push -u origin hotfix/adjust-train-msg
```
Otwórz PR `hotfix/adjust-train-msg` → `dev` i zmerguj.

### 3.3 Powrót do pracy i przywrócenie zmian ze stash
```bash
git switch feature/tune-logreg
git stash list
git stash apply  # lub git stash pop
```
Zakończ pracę, zcommituj jeśli trzeba, dopchnij zmiany, ewentualnie zaktualizuj PR.

---

## 4) Ćwiczenie konfliktu merge (krótka symulacja)

Cel: pokazać manualne rozwiązanie konfliktu.
1. Utwórz dwie gałęzie od `dev`: `feature/change-a` i `feature/change-b`.
2. W obu zmień ten sam fragment w `src/predict.py` (np. pierwszy wektor w tablicy `sample`).
3. Zmerge’uj `feature/change-a` → `dev`.
4. Spróbuj zmerge’ować `feature/change-b` → `dev` (pojawi się konflikt).
5. Rozwiąż konflikt lokalnie:
   ```bash
   git pull
   git merge origin/dev
   # edycja plików, usunięcie znaczników konfliktu
   git add .
   git commit
   git push
   ```
6. Dokończ PR.

---

## 5) Wydanie: tag i push tagów
Po zmergowaniu istotnych zmian z `dev` do `main`:
```bash
git switch main
git merge --no-ff dev
git tag v0.1.0 -m "First workshop release"
git push origin main --tags
```

---

## 6) Dobre praktyki (stosujemy podczas zadań)
- **Małe, opisowe commity** (imperatyw, krótki temat).
- **Gałęzie feature/**, PR z opisem i checklistą „jak testować”.
- **Brak sekretów w repo**, artefakty w `artifacts/` i w `.gitignore`.
- **Powtarzalność**: Docker/Compose zapewnia te same wyniki dla każdego.

---

## 7) Szybkie polecenia (ściąga)
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
  git switch -c dev
  git switch -c feature/nazwa dev
  ```
- Stash:
  ```bash
  git stash push -m "msg"
  git stash list
  git stash apply  # albo pop
  ```
