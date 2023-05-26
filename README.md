# tempstring
### Plotting tools for the SNO+ Cavity and PSUP Temperature String
  
#### **Usage**

First, you need to get the code. Either download a zip from GitHub, or open the terminal and run
```
git clone https://github.com/ddrobner/tempstring
```

Now, it's time to setup the python environment.
This can be done by running
```
cd tempstring
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

We also need to make the directory for the plots to be stored in, one way to do this is to run the command `mkdir plots`

The script gets the database credentials from the environment variables "SNODBUSER" and "SNODBPASS".
To set these, open up your `.bashrc` in your favourite text editor, and add the lines
```
export SNODBUSER="username"
export SNODBPASS="password"
```

Now, you should have your environment properly setup to run the program.
To see the available command line arguments, run `python main.py --help`. Those will be discussed in more detail here.


#### **CLI Arguments**
- `-d`, or `--date-from`: The starting date for the plot. It accepts whatever date format python's dateparse takes but I've only tested `yyyy-mm-dd` so YMMV
- `-D`, or `--date-to`: The end of the time range for the plot, working exactly the same way as the `--date-from` argument
- `--average`: Produces a plot where the average temperature of the specified sensors is plotted. If two indices are given it plots a range, and if more than two are given it plots the specified indices
- `--index`: The simplest type of plot, simply plotting the temperature data for a single sensor index.
- `--multiple-index`: Plots several indices on the same plot. Similarly to the average plot, two indices will plot a range and more than two will plot the specified indices
- `--heatmap`: Produces a matplotlib pcolormesh plot of every sensor
- `--cavity-string`: Toggles plotting the cavity string, if this is omitted the PSUP string is plotted
- `--fill-old`: Overlays plots from the cavity string over the PSUP string. Useful for filling in missing data. Takes individual sensor indices to plot and does an average over all of them.
- `--index-offset-start`: Start dates to compensate for the index shifting on the cavity string.
- `--index-offset-end`: End dates to compensate for the index shifting on the cavity string. Takes the same number of arguments as are passed to `--index-offset-start`, where the corresponding items for each form a time range to shift the indices.
- `--debug`: Enables some debugging features for the program, which at the moment is only a memory profiler.

For more details on the arguments run `python main.py --help`.

#### **Examples**
Here are some examples to illustrate the command line options:

- To produce a plot of index 0 on the PSUP temperature string over the year 2022 run
```
python main.py --date-from 2022-01-01 --date-to 2022-12-31 --index 0
```

- To produce a plot of indices 0-6 on the PSUP temperature string from January to March 2023 run
```
python main.py --date-from 2023-01-01 --date-to 2023-03-31 --multiple-index 0 6
```

- To plot the average of sensors 1, 3, 5 and 9 on the old string over 2022 run
```
python main.py --date-from 2022-01-01 --date-to 2022-12-31 --average 1 3 5 9 --cavity-string
```

- To produce a heatmap plot of the cavity string from January 2018 to December 2022 run (**WARNING**: High memory usage)
```
python main.py --date-from 2018-01-01 --date-to 2022-12-31 --heatmap --cavity-string
```

#### **Contributing**
If anyone has anything to contribute, feel free to do so. I've tried to make my code readable (although it may not always be), and I've added docstrings. In the `docs` folder there is some automatically-generated documentation (which really just presents whatever's in the docstrings in a nicer form). That's more likely to be outdated than the docstrings however.