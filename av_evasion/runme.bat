rem Batch Script for compiling python code into an executable
rem on windows with py2exe
rem Usage: Drop into your Python folder and click, or anywhere if Python is in your system path

python setup.py py2exe
cd dist
move payload.exe ../
cd ..
rmdir /S /Q build
rmdir /S /Q dist
