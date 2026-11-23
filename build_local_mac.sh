#!/usr/bin/env bash
# Сборка IPA на локальном Mac (нужен Xcode и Homebrew).
# Полученный IPA без подписи — подпиши через AltStore / Sideloadly.
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v xcodegen >/dev/null 2>&1; then
  brew install xcodegen
fi
xcodegen generate

rm -rf build
xcodebuild -project Keeper.xcodeproj \
  -scheme Keeper -configuration Release \
  -destination 'generic/platform=iOS' \
  -archivePath build/Keeper.xcarchive \
  CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO \
  CODE_SIGN_IDENTITY="" PROVISIONING_PROFILE_SPECIFIER="" \
  archive

mkdir -p build/ipa/Payload
cp -R build/Keeper.xcarchive/Products/Applications/Keeper.app build/ipa/Payload/Keeper.app
(cd build/ipa && zip -qry ../Keeper.ipa Payload)

echo "Готово: build/Keeper.ipa"
