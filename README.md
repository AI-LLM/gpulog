# Example of logging NVIDIA GPU utilization
This repo contains small code examples of how to use `nvidia-smi` and `pynvml` to log GPU utilization. This supports 
both offline logging to CSV and online plotting.

## Logging to CSV
To log utilization, run the python script `gpulog.py` Exit logging by pressing `CTRL+C`.

To display logged GPU utilization, run the script `plot_nvidia_dump.py`:
```
$ python plot_nvidia_dump.py gpu_log_[timestamp].csv
```

You can filter out GPUs by giving their integer ids. To filter by these ids, use the `--filter-ids` command line argument to `plot_nvidia_dump.py`:
```
$ python plot_nvidia_dump.py gpu_log_[timestamp].csv --filter-ids 6
```
Would display only utilization for GPU with id 6 (the seventh GPU according to BUS ID, since it's zero-indexed).
 
These ids are enumerated (starting from 0) according to PCI BUS ID, while CUDA by default 
enumerates GPUs based on speed (the fastest GPU first). You can make CUDA use the same number as this script 
(and `nvidia-smi`), set the CUDA_DEVICE_ORDER environment variable to PCI_BUS_ID:

```
export CUDA_DEVICE_ORDER=PCI_BUS_ID
```
Note: this has to be done before you assign GPUs to your running program to make it use the correct ID.

## Online logging
The online logging script depends on pynvml and matplotlib, install these before running this script 
(`pip install pynvml`). Afterwords, start the logging by running:

```
$ python live_gpu_utlization_plot.py
```
You can filter out GPU ids by giving their integer indices (ordered by BUS id like in nvidia-smi).
```
$ python live_gpu_utlization_plot.py 1 2
```
Will only display information for the second and third GPU.

If want to limit the utilization curve to only the last x couple of seconds, use the command line argument 
`--limit-window`, this will continuously move the window so at approximately the given number of seconds are shown. 
To show the utilization for the last minute use:

```
$ python live_gpu_utlization_plot.py --limit-window 60
```
