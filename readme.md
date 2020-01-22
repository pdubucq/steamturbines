# Optimization Models for Steam Turbines lecture at TUHH

The files in this library are used in the lecture "Steam Turbine" at Hamburg University of Technology.

## Prerequisites

Easiest way to start is to install Anaconda and follow the steps below.

### Setting up Anaconda in TUHH RZ

- Activate Python/Anaconda using the RZ-Config tool "MyConfig" located on the desktop
- Relogin

### Installing dependencies

- Download "steamturbines" folder from
https://github.com/pdubucq/steamturbines to "My_Documents" and unzip it
- Search and run the "Anaconda Prompt" using the Windows toolbar
- change to the steamturbines directory using the command `cd ../steamturbines`
- Install all needed packages and tools using the command `conda env create -f environment.yml`
- Activate the new environment using the command: `conda activate steamturbines`

### Starting the Jupyter Notebook

- In the Anaconda console run the command `jupyter notebook`

The default browser will open up and you're ready to go

### Troubleshooting ###

- If the jupyter command is not found run `conda install -c anaconda jupyter` 
- If the browser doesnt start, you can find the URL in the console output (if you dont find it try http://localhost:8888/tree)
- If `import pulp` failes add the following two lines at the top of your script:
```
import sys, os
sys.path.append(os.environ["appdata"] + "\..\Local\Continuum\anaconda3\envs\steamturbines\Lib\site-packages\PuLP-1.6.8-py3.7.egg-info")
```



## Authors

Pascal Dubucq

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* The optimzation models are all using PuLP and pandas. Thanks for the great work to the developers.
