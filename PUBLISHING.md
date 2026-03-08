# Guía: publicar ytdl en Homebrew

## Estructura del proyecto

```
ytdl/
├── ytdl/
│   ├── __init__.py
│   ├── __main__.py      # permite: python -m ytdl
│   └── cli.py           # lógica principal + entry point
├── Formula/
│   └── ytdl.rb          # fórmula de Homebrew
├── .github/
│   └── workflows/
│       └── release.yml  # publica en PyPI + crea GitHub Release
├── pyproject.toml
└── README.md
```

---

## Paso 1 — Subir el código a GitHub

```bash
git init
git add .
git commit -m "chore: initial release"
gh repo create tu-usuario/ytdl --public --source=. --push
```

---

## Paso 2 — Crear un tag y hacer push (dispara el workflow)

```bash
git tag v1.0.0
git push origin v1.0.0
```

El workflow de GitHub Actions:
1. Construye el paquete y lo sube a PyPI
2. Genera un tarball y crea el GitHub Release

---

## Paso 3 — Obtener el sha256 del tarball

Después de que el Release esté creado, descarga el tarball:

```bash
curl -sL https://github.com/tu-usuario/ytdl/archive/refs/tags/v1.0.0.tar.gz \
  | sha256sum
```

Copia ese hash — lo necesitas en el siguiente paso.

---

## Paso 4 — Crear el tap de Homebrew

Un *tap* es un repositorio de GitHub con el prefijo `homebrew-`:

```bash
gh repo create tu-usuario/homebrew-ytdl --public
```

---

## Paso 5 — Generar los bloques `resource` de la fórmula

```bash
pip install homebrew-pypi-poet
poet ytdl
```

`poet` imprime los bloques `resource` con las URLs y sha256 exactos
de cada dependencia Python. Pégalos en `Formula/ytdl.rb`.

---

## Paso 6 — Completar y subir la fórmula

Edita `Formula/ytdl.rb`:
- Reemplaza `REEMPLAZA_CON_SHA256_REAL` con el hash del Paso 3
- Pega los bloques `resource` del Paso 5

Luego súbela al tap:

```bash
# Clona el tap vacío
git clone https://github.com/tu-usuario/homebrew-ytdl
cd homebrew-ytdl
mkdir Formula
cp /ruta/al/proyecto/Formula/ytdl.rb Formula/
git add Formula/ytdl.rb
git commit -m "feat: add ytdl formula v1.0.0"
git push
```

---

## Paso 7 — Instalar y probar

```bash
brew tap tu-usuario/ytdl
brew install ytdl
ytdl
```

---

## Actualizaciones futuras

1. Haz tus cambios en el código
2. Sube el número de versión en `pyproject.toml`
3. Crea un nuevo tag: `git tag v1.1.0 && git push origin v1.1.0`
4. El workflow publica automáticamente
5. Actualiza `sha256` y versión en `Formula/ytdl.rb` y haz push al tap

---

## Estructura de URLs de referencia

| Recurso | URL |
|---|---|
| Repositorio principal | `https://github.com/tu-usuario/ytdl` |
| Tap de Homebrew | `https://github.com/tu-usuario/homebrew-ytdl` |
| Paquete en PyPI | `https://pypi.org/project/ytdl` |
| Instalar via pip | `pip install ytdl` |
| Instalar via brew | `brew tap tu-usuario/ytdl && brew install ytdl` |
