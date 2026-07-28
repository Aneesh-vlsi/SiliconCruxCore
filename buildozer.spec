[app]

# (string) Title of your application
title = SiliconCrux Core

# (string) Package name
package.name = siliconcruxcore

# (string) Package domain (needed for android packaging)
package.domain = org.siliconcrux

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include (comma separated)
# Including py files explicitly ensures eda_engine and mobile_canvas are bundled
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# Add any specialized scientific/math libraries here if eda_engine uses them (e.g., numpy)
requirements = python3==3.11.9,kivy,kivymd


# (string) Custom source folders if any
# source.include_folders = 

# (str) Application version
version = 3.0

# (int) Minimum API your APK will support (Android 8.0)
android.minapi = 26

# (int) Target API your APK will target (Android 14)
android.api = 34

# (str) Android NDK version to use
android.ndk = 26b

# (bool) Use private storage for data (recommended)
android.private_storage = True

# (list) Permissions required by the app
# Adjust if your EDA engine requires file picking or external storage saving
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Architecture to build for (targeting standard modern physical devices)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Skip byte compile for .py files (set to False if you want optimization)
android.skip_byte_compile = False

# (str) Logcat filters to use during debugging
android.logcat_filters = *:S python:D

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

