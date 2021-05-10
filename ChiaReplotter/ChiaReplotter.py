import os
import sys
import time
import argparse
import subprocess
from threading import Thread, Lock

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
python ChiaReplotter.py -t "C:/Users/$env:UserName/source/repos/ChiaReplotter/ChiaReplotter/newplots" -d "C:/Users/$env:UserName/source/repos/ChiaReplotter/ChiaReplotter/newplots" --remove_count 3 --remove_dir "C:/Users/$env:UserName/source/repos/ChiaReplotter/ChiaReplotter/oldplots" --concurrent 2 --stagger_time 10
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

class PlotDeleter():
    def __init__(self):
        self.lock = Lock()

    def deletePlots(self, args):
        with self.lock:
            print('Entering!!')
            plots = os.listdir(args.remove_dir)
            plots = [p for p in plots if p.endswith('.plot')]
            for i, p in zip(range(args.remove_count), plots):
                pltstr = os.path.join(args.remove_dir, p)
                print('Removing plot {}'.format(pltstr))
                os.remove(pltstr) 

# Singleton class to delete plots without a race 
deleter = PlotDeleter()

class Replotter(Thread):

    def __init__(self, args, idx):
        Thread.__init__(self)
        self.args = args
        self.count = 0
        self.idx = idx

    def poll(self):
        return self.count

    def run(self):
        
        # Sleep if we have a stagger time set and we're not the first plot
        time.sleep(self.args.stagger_time * self.idx)

        print('Starting run for plotter {} ...'.format(self.idx))
        for i in range(self.args.runs):
            print('Step {} of {}'.format(i+1, self.args.runs))
            if self.args.remove_count:
                deleter.deletePlots(self.args)
            self.replot()
            self.count += 1
            # TODO: Print/stop on error state from proc
            #print('Finished plotting {} plots'.format(self.args.n))

    def replot(self):
        if get_platform() == 'Windows':
            proc = subprocess.Popen(['powershell', 'cd {}; ./chia.exe plots create -k {} -b {} -u {} -r {} -t {} -d {} -n {}'.format(
                self.args.chia_loc, self.args.k, self.args.b, self.args.u, 
                self.args.r, self.args.t, self.args.d, self.args.n)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #else:
        #    return subprocess.call(['cd {}'.format(self.args.chia_loc), './chia.exe plots create -k {} -b {} -u {} -r {} -t {} -d {} -n {}'.format(
        #        self.args.k, self.args.b, self.args.u, self.args.r, self.args.t, self.args.d, self.args.n)], shell=self.args.shell)

        #if i < self.args.remove_count:
        #    print('Was only able to remove {} plots!'.format(i))
        #print()

def runLoop(procs):
    ii = 0
    while any(p.is_alive() for p in procs):
        print('\n'*50)
        time.sleep(10)
        s = ''
        for i, p in enumerate(procs):
            count = p.poll()
            s += 'Plotter {} has completed {} plots \n'.format(i, ii)
        print(s)
        ii += 1



def run(args):
    procs = []
    for i in range(args.concurrent):
        procs.append(Replotter(args, i))
        procs[i].start()

    runLoop(procs)

    for p in procs:
        p.join()


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
    parser.add_argument('--concurrent', type=int, default=1)
    parser.add_argument('--stagger_time', type=int, default=0, help='Time to stagger plotting in seconds')


    args = parser.parse_args()

    run(args)