import argparse
import subprocess

".\chia.exe plots create -k 32 -b 3700 -u 128 -r 4 -t B:\Chia -d E:\Chia -n 10"

'./chia.exe plots create -k 32 -b 3700 -u 128 -r 4 -t B:/Chia -d E:/Chia -n 10'


def replot(chiaLocation):
    subprocess.call(['powershell', 'cd {}; ./chia.exe plots create -k {} -b {} -u {} -r {} -t {} -d {} -n {}'.format(
        args.ChiaLocation, args.k, args.b, args.u, args.r, args.t, args.d, args.n)], shell=True)


def run(args):
    replot(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', type=int, default=32)
    parser.add_argument('-b', type=int, default=3400)
    parser.add_argument('-u', type=int, default=128)
    parser.add_argument('-r', type=int, default=2)
    parser.add_argument('-t', type=str, help='Temp location')
    parser.add_argument('-d', type=str, help='Final location')
    parser.add_argument('-n', type=int, default=1)
    parser.add_argument('--ChiaLocation', 
                        default='C:/Users/$env:UserName/AppData/Local/chia-blockchain/app-*/resources/app.asar.unpacked/daemon')
    args = parser.parse_args()

    run(args)