"""Command line tool to distribute jobs read from stdin onto GPUs."""
import argparse
import threading
import subprocess
import sys
import os


class GPUManager():
    """GPU manager, keeps track which GPUs used and which are avaiable."""

    def __init__(self, available_gpus):
        """Initialize GPU manager.

        Args:
            available_gpus: GPU ids of gpus that can be used.

        """
        self.semaphore = threading.BoundedSemaphore(len(available_gpus))
        self.gpu_list_lock = threading.Lock()
        self.available_gpus = list(available_gpus)

    def get_gpu(self):
        """Get a GPU, if none is available, wait until there is."""
        self.semaphore.acquire()
        with self.gpu_list_lock:
            gpu = self.available_gpus.pop()
        return GPU(gpu, self)

    def release_gpu(self, gpu):
        """Relesae a GPU after use.

        Args:
            gpu: GPU object returned from get_gpu.

        """
        gpu = gpu.nr
        with self.gpu_list_lock:
            self.available_gpus.append(gpu)
            self.semaphore.release()


class GPU():
    """Representation of a GPU."""

    def __init__(self, nr, manager):
        """Set up GPU Object.

        Args:
            nr: Which GPU id the GPU has
            manager: The manager of the GPU

        """
        self.nr = nr
        self.manager = manager

    def release(self):
        """Release the GPU."""
        self.manager.release_gpu(self)

    def __str__(self):
        """Return string representation of GPU."""
        return str(self.nr)


def run_command_with_gpu(command, gpu):
    """Run command using Popen, set CUDA_VISIBLE_DEVICE and free GPU when done.

    Args:
        command: string with command
        gpu: GPU object

    Returns: Thread object of the started thread.

    """
    myenv = os.environ.copy()
    myenv['CUDA_VISIBLE_DEVICES'] = str(gpu)
    print(f'Processing /bin/bash command `{command}` on gpu {gpu}')

    def run_then_release_GPU(command, gpu):
        myenv = os.environ.copy()
        myenv['CUDA_VISIBLE_DEVICES'] = str(gpu)
        print("Trying bash command')
        proc = subprocess.Popen(
            args=["/bin/bash", "-i", "-c", command],
            shell=True,
            env=myenv,
            executable='/bin/bash',
        )
        proc.wait()
        gpu.release()
        return

    thread = threading.Thread(
        target=run_then_release_GPU,
        args=(command, gpu)
    )
    thread.start()
    # returns immediately after the thread starts
    return thread


def read_commands_and_run(gpu_manager):
    """Read commands from stdin and run them on gpus from the gpu manager.

    Args:
        gpu_manager: A GPUManager instance

    """
    for line in sys.stdin:
        line = line.rstrip()
        gpu = gpu_manager.get_gpu()
        run_command_with_gpu(line, gpu)


def main():
    """Read command line arguments and start reading from stdin."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpus', nargs='+', type=str, required=True)
    args = parser.parse_args()

    # Support both comma separated and individually passed GPU ids
    gpus = args.gpus if len(args.gpus) > 1 else args.gpus[0].split(',')
    gpu_manager = GPUManager(gpus)
    read_commands_and_run(gpu_manager)


if __name__ == '__main__':
    main()
