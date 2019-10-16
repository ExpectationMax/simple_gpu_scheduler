simple_gpu_scheduler
--------------------

A simple scheduler to run your commands on individual GPUs.  Following the
[KISS principle](https://en.wikipedia.org/wiki/KISS_principle), this script
simply accepts commands via `stdin` and executes them on a specific GPU by
setting the `CUDA_VISIBLE_DEVICES` variable.

The commands read are executed using the login shell, thus redirections `>`
pipes `|` and all other kinds of shell magic can be used.

Installation
------------

The package can simply be installed from
[pypi](https://pypi.org/project/simple-gpu-scheduler/)
```bash
$ pip3 install simple-gpu-scheduler
```

Simple Example
--------------

Suppose you have a file `gpu_commands.txt` with commands that you would like to
execute on the GPUs 0, 1 and 2 in parallel:

```bash
$ cat gpu_commands.txt
python train_model.py --lr 0.001 --output run_1
python train_model.py --lr 0.0005 --output run_2
python train_model.py --lr 0.0001 --output run_3
```

Then you can do so by simply piping the command into the `simple_gpu_scheduler`
script
```bash
$ simple_gpu_scheduler --gpus 0 1 2 < gpu_commands.txt
Processing command `python train_model.py --lr 0.001 --output run_1` on gpu 2
Processing command `python train_model.py --lr 0.0005 --output run_2` on gpu 1
Processing command `python train_model.py --lr 0.0001 --output run_3` on gpu 0
```

For further details see `simple_gpu_scheduler -h`.

Hyperparameter search
---------------------

In order to allow user friendly utilization of the scheduler in the common
scenario of hyperparameter search, a convenience script `simple_hypersearch` is
included in the package. The output can directly be piped into
`simple_gpu_scheduler` or appended to the "queue file" (see [Simple scheduler
for jobs](#simple-scheduler-for-jobs)).

**Grid of all possible parameter configurations in random order:**
```bash
simple_hypersearch "python3 train_dnn.py --lr {lr} --batch_size {bs}" -p lr 0.001 0.0005 0.0001 -p bs 32 64 128 | simple_gpu_scheduler --gpus 0,1,2
```

**5 uniformly sampled parameter configurations:**
```bash
simple_hypersearch "python3 train_dnn.py --lr {lr} --batch_size {bs}" --n-samples 5 -p lr 0.001 0.0005 0.0001 -p bs 32 64 128 | simple_gpu_scheduler --gpus 0,1,2
```

For further information see the `simple_hypersearch -h`.

Simple scheduler for jobs
-------------------------

Combined with some basic command line tools, one can set up a very basic
scheduler which waits for new jobs to be "submitted" and executes them in order
of submission.

Setup and start scheduler in background or in a separate permanent session
(using for example `tmux`):
```bash
touch gpu.queue
tail -f -n 0 gpu.queue | simple_gpu_scheduler --gpus 0,1,2
```
the command `tail -f -n 0` follows the end of the gpu.queue file. Thus if there
was anything written into `gpu.queue` prior to the execution of the command it
will not be passed to `simple_gpu_scheduler`.

Then submitting commands boils down to appending text to the `gpu.queue` file:

```bash
echo "my_command_with | and stuff > logfile" >> gpu.queue
```



TODO
----

 - Multi line jobs (evtl. we would then need a submission script after all)
 - Stop, but let commands finish when receiving a defined signal
 - Tests would be nice, until now the project is still __very small__ but if it
   grows tests should be added
