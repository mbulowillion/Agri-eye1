[app]

# App name
title = Agri-Eye

# Package name (reverse domain)
package.name = agrieye
package.domain = org.agrieye

# Source code
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf,txt,csv

# Version
version = 1.0.0
# version.regex = __version__\s*=\s*['"](.*?)['"]
# version.filename = main.py

# Requirements
requirements = python3,kivy,plyer,Pillow,requests,numpy

# Android specifics
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25.2.9519653
android.gradle_dependencies = 'androidx.core:core:1.9.0'
android.archs = arm64-v8a, armeabi-v7a
android.permissions = CAMERA, INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES
android.add_src =
android.add_libs_armeabi =
android.add_libs_arm64-v8a =
android.add_libs_x86 =
android.add_libs_x86_64 =
android.extra_java_deps =

# App icon (optional - place icon.png in the app dir)
# icon.filename = icon.png
# presplash.filename = splash.png

# Orientation
orientation = portrait
fullscreen = 0

# Windows / iOS / macOS (not used for Android, but kept for reference)
osx.package_name = Agri-Eye
osx.bundle_identifier = org.agrieye.agrieye
osx.icon = icon.png

# iOS
ios.package_name = Agri-Eye
ios.bundle_identifier = org.agrieye.agrieye
ios.icon = icon.png

# Log
log_level = 2
log_dir = ./.buildozer/logs
archive = 0

# Store
store = googleplay
