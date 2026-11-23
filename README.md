# Keeper — IPA / PWA из твоего HTML

Проект упаковывает HTML-прототип (`gemini-code-1795445316832.html`) в iOS-приложение
с иконкой `киппер.jpg`. Название — **Keeper**.

## Что внутри

| Путь | Что это |
|---|---|
| `www/index.html` | твой HTML + метатеги iOS/PWA + service worker |
| `www/manifest.json`, `www/sw.js`, `www/icons/` | PWA-часть (иконки 64–1024) |
| `Sources/AppDelegate.swift` | минимальный WKWebView-контейнер |
| `Resources/Info.plist` | имя Keeper, ориентация, статус-бар |
| `Resources/Assets.xcassets/AppIcon.appiconset/` | все размеры иконки iOS |
| `project.yml` | спецификация XcodeGen (генерирует `Keeper.xcodeproj`) |
| `.github/workflows/build-ipa.yml` | сборка `.ipa` в облаке на macOS |
| `Keeper-PWA.zip` | готовая PWA-папка для загрузки на хостинг |
| `scripts/make_icons.py`, `scripts/make_pwa.py` | пересборка иконок и HTML |

## Почему не просто файл IPA

IPA — это ZIP с `Payload/Keeper.app`, внутри которого скомпилированный код.
Собрать его на Linux нельзя: нужен macOS + Xcode. Здесь лежит готовый проект,
который соберёт IPA **бесплатно** на macOS-раннере GitHub (без Мака и без
платного аккаунта разработчика).

## Вариант A — настоящий IPA через GitHub (рекомендую)

1. Зарегистрируйся на [github.com](https://github.com) и создай **публичный**
   репозиторий, например `keeper`.
2. Загрузи в него **всю папку `Keeper/`**, включая скрытую `.github`.
   Проще через терминал:
   ```bash
   cd Keeper
   git init
   git add .
   git commit -m "Keeper"
   git remote add origin https://github.com/<твой-логин>/keeper.git
   git branch -M main
   git push -u origin main
   ```
   Можно и через веб: `Add file → Upload files` → перетащи папку целиком.
3. Открой вкладку **Actions** → слева **Build Keeper IPA** → **Run workflow** →
   зелёная кнопка **Run workflow**.
4. Через 3–7 минут открой задачу → внизу **Artifacts** → скачай `Keeper-ipa`.
   Это `.zip`, внутри него `Keeper.ipa`.
5. Установи на iPhone через **AltStore** или **Sideloadly** (бесплатный Apple ID;
   платный разработчик не нужен). При первом запуске:
   `Настройки → Конфиденциальность и безопасность → Доверять разработчику`.

## Вариант B — PWA без IPA (быстрее всего)

Папка `Keeper/www` (или готовый `Keeper-PWA.zip`) — самодостаточное приложение.
Распакуй и залей на любой хостинг: GitHub Pages, Netlify, Vercel — бесплатно.
Открой ссылку в **Safari** на iPhone → «Поделиться» → **«На домашний экран»**.
Появится иконка Keeper, приложение откроется полноэкранно без адресной строки.
Работает офлайн.

GitHub Pages: залей содержимое `www/` в ветку `gh-pages`, затем
`Settings → Pages → Deploy from a branch → gh-pages`.

## Вариант C — свой Mac

```bash
cd Keeper
chmod +x build_local_mac.sh
./build_local_mac.sh
# результат: build/Keeper.ipa → дальше AltStore / Sideloadly
```

Нужны Xcode и Homebrew (`brew install xcodegen` скрипт сделает сам).

## Обновление HTML

Положи новый файл по пути из `scripts/make_pwa.py` (сейчас
`/home/nigga/Загрузки/gemini-code-1795445316832.html`) и выполни:

```bash
python3 scripts/make_pwa.py
python3 scripts/make_icons.py
cd www && zip -qr ../Keeper-PWA.zip . && cd ..
git add . && git commit -m "update" && git push
```

Потом снова запусти workflow в Actions.

## Примечание

Это **демо-прототип интерфейса**: он не подключается к блокчейну, не хранит
секретную фразу и не работает с реальными активами. Функция «Выдача токенов»
(двойной тап по FAQ) создаёт искусственные балансы только для показа UI.
