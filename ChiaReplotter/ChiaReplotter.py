import os
import argparse
import subprocess

".\chia.exe plots create -k 32 -b 3700 -u 128 -r 4 -t B:\Chia -d E:\Chia -n 10"

'./chia.exe plots create -k 32 -b 3700 -u 128 -r 4 -t B:/Chia -d E:/Chia -n 10'


def replot(chiaLocation):
    cproc = subprocess.call(['powershell', 'cd {}; ./chia.exe plots create -k {} -b {} -u {} -r {} -t {} -d {} -n {}'.format(
        args.chia_loc, args.k, args.b, args.u, args.r, args.t, args.d, args.n)], shell=True)


# Remove first 'remove_count' *.plot files from 'remove_dir' directory
def deletePlots(args):
    plots = os.listdir(args.remove_dir)

    i = 0
    for p in plots:
        if p.endswith('.plot'):
            os.remove(p)
            i += 1
        if i >= args.remove_count:
            break

def run(args):
    run = 0
    for i in range(args.runs):
        if args.remove_count:
            deletePlots(args)
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
    parser.add_argument('--chia_loc', 
                        default='C:/Users/$env:UserName/AppData/Local/chia-blockchain/app-*/resources/app.asar.unpacked/daemon')
    parser.add_argument('--remove_count', default=0, help='Plots to remove per iteration')
    parser.add_argument('--remove_dir', type=str)
    parser.add_argument('--runs', default=1, 'Total iterations to run a set of delete and replots')
    args = parser.parse_args()

    run(args)