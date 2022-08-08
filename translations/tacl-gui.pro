SOURCES = ../src/SuppliedIntersectController.py
SOURCES = ../src/TaclRunner.py
TRANSLATIONS += en-us.ts

#   Generate ts files
# pylupdate5 translations/tacl-gui.pro

#   Edit translations
# /usr/lib/x86_64-linux-gnu/qt5/bin/linguist translations/en-us.ts

#   Release translations (creates .qm binaries)
# /usr/lib/x86_64-linux-gnu/qt5/bin/lrelease translations/en-us.ts
