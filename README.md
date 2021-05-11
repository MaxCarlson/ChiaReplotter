# ChiaReplotter

This utility was built to help ease the transition from solo farming to pool farming the Chia cryptocurrency when the pooling protocol is released. 
To ensure maximum profitability, this tool automates the process of creating new plots while simultaneously freeing up storage on a drive to do so. 

## Example
Here's an example scenario and associated PowerShell command:
```
You want to delete 5 old plots, then create five new plots
You want to do this 10 times

D:/soloPlots    contains old plots
D:/newPlots     where you would like your new plots to be
B:/tempPlots    the location where you want to have your temporary plots

python ChiaReplotter.py -t "B:/tempPlots" -d "D:/newPlots" --remove_count 5 --remove_dir "D:/soloPlots" --runs 10 
```

## Command Line Arguments

| Command | Default | Description |
| --- | --- | --- |
| -k | 32 | Plot size |
| -b | 3400 | Ram allocated |
| -u | 128 | Bucket size |
| -r | 2 | Threads |
| -t | n/a | Temporary plotting location |
| -d | n/a | Final plot location | 
| -n | 1 | Number of plots to plot |
| --chia_loc | 'C:/Users/$env:UserName/AppData/Local/chia-blockchain/app-*/resources/app.asar.unpacked/daemon' | Location of Chia directory |
| --remove_dir | n/a | Directory to remove plots from |
| --remove_count | 0 | Number of plots to remove from --remove_dir per iteration |
| --runs | 1 | Total iterations to run |
