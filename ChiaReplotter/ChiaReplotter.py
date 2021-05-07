import subprocess

".\chia.exe plots create -k 32 -b 3700 -u 128 -r 4 -t B:\Chia -d E:\Chia -n 10"

subprocess.call(['powershell', 'cd C:/Users/$env:UserName/AppData/Local/chia-blockchain/app-*/resources/app.asar.unpacked/daemon;'
    './chia.exe plots create -k 32 -b 3700 -u 128 -r 4 -t B:/Chia -d E:/Chia -n 10'], shell=True)