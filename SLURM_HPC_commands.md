Here's a list of general commands for navigating a High-Performance Computing (HPC) environment and using a SLURM scheduler, with explanations for each command:

```bash
ssh username@hpc-server.com #Connect to the HPC server via SSH. Replace username with your HPC username and hpc-server.com with the address of your HPC server.

exit #Log out of the HPC server.


pwd #Print the current working directory path.

scp local_file username@hpc-server.com:path/to/destination #Securely copy a file from your local machine to the HPC server.

scp username@hpc-server.com:path/to/file local_destination #Securely copy a file from the HPC server to your local machine.

module load module_name #Load a software module (e.g., Python, CUDA, etc.) available on the HPC system.

module unload module_name #Unload a previously loaded module.

module list #List all currently loaded modules.

squeue #View the status of jobs in the SLURM queue.

sbatch script.sh #Submit a batch job using the SLURM script script.sh.

srun --pty bash #Start an interactive job session.

scancel job_id #Cancel a queued or running job. Replace job_id with the ID of the job.

sinfo #View information about SLURM nodes and partitions.

sacct #Display accounting data for all jobs you have submitted.

sstat job_id #Display status information about a running job.

salloc #Request a SLURM job allocation (i.e., a block of resources).

exit #Exit an interactive (srun or salloc) SLURM session.

```
