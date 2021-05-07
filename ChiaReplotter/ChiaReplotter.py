import os
import sys
import argparse
import subprocess

# Note, in order to kill this process (on Windows) once running, you must close the powershell/terminal window
# Ctrl-c does not seem to work

# Example desired plotting command for chia
'./chia.exe plots create -k 32 -b 3400 -u 128 -r 2 -t C:/NewPlots/Temp/Folder -d C:/NewPlots/Final/Folder -n 3'

# Example command to run (without newlines) from directory containing this file
# Running this command will first delete 3 plots in the remove_dir directory
# Next, it will run the above command. It will repeat this five times
"""
python ChiaReplotter.py -t "C:/NewPlots/Temp/Folder"
-d "C:/NewPlots/Final/Folder" --remove_count 3
--remove_dir "C:/Directory/With/Old/Plots"
--runs 5 -n 3
"""

# Example command for my testing
"""
python ChiaReplotter.py -t "C:/Users/$env:UserName/source/repos/ChiaReplotter/ChiaReplotter/newplots" -d "C:/Users/$env:UserName/source/repos/ChiaReplotter/ChiaReplotter/newplots" --remove_count 3 --remove_dir "C:/Users/$env:UserName/source/repos/ChiaReplotter/ChiaReplotter/oldplots"
"""


def get_platform():
    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]

def replot(chiaLocation):
    if get_platform() == 'Windows':
        return subprocess.call(['powershell', 'cd {}; ./chia.exe plots create -k {} -b {} -u {} -r {} -t {} -d {} -n {}'.format(
            args.chia_loc, args.k, args.b, args.u, args.r, args.t, args.d, args.n)], shell=True)
    else:
        return subprocess.call(['cd {}'.format(args.chia_loc), './chia.exe plots create -k {} -b {} -u {} -r {} -t {} -d {} -n {}'.format(
            args.k, args.b, args.u, args.r, args.t, args.d, args.n)], shell=args.shell)


# Remove first 'remove_count' *.plot files from 'remove_dir' directory
def deletePlots(args):
    print()
    plots = os.listdir(args.remove_dir)
    plots = [p for p in plots if p.endswith('.plot')]
    for i, p in zip(range(args.remove_count), plots):
        pltstr = os.path.join(args.remove_dir, p)
        print('Removing plot {}'.format(pltstr))
        os.remove(pltstr) 

    if i < args.remove_count:
        print('Was only able to remove {} plots!'.format(i))
    print()

def run(args):
    run = 0
    print('Starting...')
    for i in range(args.runs):
        print('Step {} of {}'.format(i+1, args.runs))
        if args.remove_count:
            deletePlots(args)
        proc = replot(args)

        # TODO: Print/stop on error state from proc
        print('Finished plotting {} plots'.format(args.n))

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
    parser.add_argument('--remove_count', type=int, default=0, help='Plots to remove per iteration')
    parser.add_argument('--remove_dir', type=str)
    parser.add_argument('--runs', default=1, help="Total iterations to run a set of delete and replots")
    parser.add_argument('--shell', type=bool, default=True)
    args = parser.parse_args()

    run(args)