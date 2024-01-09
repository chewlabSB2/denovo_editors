****COMPUTATIONAL WORKFLOW FOR DENOVO EDITORS****

For Linux environments with SLURM for HPC clusters.

![Picture1](https://github.com/chewlabSB2/denovo_editors/assets/87451986/d1ae18b8-23a2-45fe-bbe5-89fa0f2fb197)

_________________________________________________________________________________________________________________
*Instructions for updating your repository*

Navigate to your local repository's directory and pull the latest changes:
```bash
cd path/to/denovo_editors
git pull origin main
```
_________________________________________________________________________________________________________________
**Instructions for setup**

*1. Clone the denovo_editors repository* 
```bash
cd scratch
git clone https://github.com/chewlabSB2/denovo_editors
```
** Before we proceed, make sure you have conda working. If you want to install Miniforge in your HPC with the latest architecture, go to https://github.com/conda-forge/miniforge and install Miniforge-pypy3-Linux-x86_64 (Linux OS, x86_64 (amd64) architecture). To run install the package:
```bash
bash Miniforge3-Linux-x86_64.sh
./Miniforge3-Linux-x86_64.sh #to run the installer
#you must set the location for creation of the miniforge3 directory:
/home/users/astar/gis/your_username/scratch/denovo_editors/miniforge3
#if this path above is not yours, make sure to edit the miniforge3 paths in the template bash scripts to make them uniform and match your actual path.
```
After you have installed Miniforge, re-initialize the terminal or open a new session. 

*2. CUDA compiler*

Make sure your Cuda compiler driver is 11.1 or later. If you don't have a GPU or don't plan to use a GPU, you can skip this section. if you are running this on HPC with a pre-loaded toolkit, you have to load the module. It is preferable to use the latest available version, in this case that is CUDA 12.1.1. 
```bash
module load cuda/12.1.1
nvcc --version
#nvcc: NVIDIA (R) Cuda compiler driver
#Copyright (c) 2005-2023 NVIDIA Corporation
#Built on Mon_Apr__3_17:16:06_PDT_2023
#Cuda compilation tools, release 12.1, V12.1.105
#Build cuda_12.1.r12.1/compiler.32688072_0
```
If you want to view the full list of modules available in your HPC, as well as which modules you have currently loaded:
```bash
module avail
module list
```
*3. Installation instructions for RFdiffusion*
```bash
cd denovo_editors
git clone https://github.com/RosettaCommons/RFdiffusion.git
cd RFdiffusion
mkdir models && cd models
#install all required model weights
wget http://files.ipd.uw.edu/pub/RFdiffusion/6f5902ac237024bdd0c176cb93063dc4/Base_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/e29311f6f1bf1af907f9ef9f44b8328b/Complex_base_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/60f09a193fb5e5ccdc4980417708dbab/Complex_Fold_base_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/74f51cfb8b440f50d70878e05361d8f0/InpaintSeq_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/76d00716416567174cdb7ca96e208296/InpaintSeq_Fold_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/5532d2e1f3a4738decd58b19d633b3c3/ActiveSite_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/12fc204edeae5b57713c5ad7dcb97d39/Base_epoch8_ckpt.pt
wget http://files.ipd.uw.edu/pub/RFdiffusion/1befcb9b28e2f778f53d47f18b7597fa/RF_structure_prediction_weights.pt
```
We also need to set up the conda environment for RFdiffusion, which uses NVIDIA SE(3)-Transformers:
```bash
#within the RFdiffusion subdirectory:
cd ..
conda env create -f env/SE3nv.yml

conda activate SE3nv
cd env/SE3Transformer
pip install --no-cache-dir -r requirements.txt
python setup.py install
cd ../.. # change into the root directory of the repository
pip install -e . # install the rfdiffusion module from the root of the repository
```
Anytime you run diffusion you should be sure to activate this conda environment by running the following command:
```bash
conda activate SE3nv
conda deactivate #to deactivate the environment
```
Additional setup for RFdiffusion:
```bash
mkdir outputs
mkdir inputs
cd inputs
```
Navigate back to the denovo editors directory to continue setting up.
```bash
cd ..
```
*4. Installation instructions for MPNN*
```bash
git clone https://github.com/dauparas/ProteinMPNN
cd ProteinMPNN
```
We also need to create a conda environment to run MPNN with Pytorch. The latest PyTorch requires Python 3.8 or later so we also need to load the correct python version in our HPC. Here, we avoid using miniforge because it runs python 3.10 as default env, which is not compatible with Pytorch CUDA platform. Instead, we use mamba to create an environment with python3.9 and Pytorch with CUDA 12.1.1
```bash
module load cuda/12.1.1
mamba create -n my_mlfold python=3.9
mamba activate my_mlfold
pip3 install torch torchvision torchaudio 
```
Navigate back to the denovo editors directory to continue setting up.
```bash
mamba deactivate #to deactivate the environment
cd ..
```
*5.  Installation Instructions for Local AlphaFold*

```bash
module load cuda/12.1.1
module load cudnn/8.9.2_cu12
mv localcolabfold local_alphafold
export PATH="/path/to/your/local_alphafold/colabfold-conda/bin:$PATH" #It is recommended to add this export command to ~/.bashrc and restart bash (~/.bashrc will be executed every time bash is started)
```
Now you have all the necessary repositories and scripts to run this workflow. 
_________________________________________________________________________________________________________________
***Instructions for running the workflow***

Prepare your engineered pdb and your reference pdb files before you begin this workflow. This example workflow will use Icsb(8csz.pdb) and a modified pdb file (IscB_8CSZ_5A.pdb):

**Step 1: Import your engineered pdb and reference pdb files into /denovo_editors/RFdiffusion/inputs**

**Step 2: Extract residues for RFdiffusion input**

You need to extract the residues from the modified pdb file. Navigate to /denovo_editors/helper_scripts. In order to extract the input residues for contigmap.contigs and range for contigmap.length:
```bash
nano extract_input_residues.py
#edit line 67: "pdb_file = '/path/to/your/pdb/file.pdb'  # Replace with the actual path"
#If you don't know what your file path is, navigate to the inputs directory and run "pwd" in the command line to get the file path.
python extract_input_residues.py
#/charonfs/scratch/users/astar/gis/diyasri/miniforge3/lib/python3.10/site-packages/Bio/PDB/PDBParser.py:395: PDBConstructionWarning: #Ignoring unrecognized record 'END' at line 1179
  warnings.warn(
#D1-2/2/D4/1/D6/2-12/D14-28/14-24/D34-37/5/D40/3/D44/1/D46/1/D48-51/4/D53/1-11/D60-65/7-17/D73/7-17/D86/1/D88/1/D90-94/5/D96-102/2-12/D104-110/2-12/D112-117/1-11/D119-120/2/D122-124/1-11/D129/1/D131-157/22-32/D159-165/3-13/D168/2/D171/3/D175/1-11/D182/4-14/D192/1/D194-199/8-18/D208-209/2/D211-219/6-16/D223/13-23/D242-246/1-11/D249-251/3/D253/1/D255-257/3/D259/4-14/D269/3/D273/12-22/D291-301/7-17/D304-305/29-39/D339/2/D342/21-31/D369-385/12-22/D387/4-14/D397-403/6-16/D409/3/D413/4/D418-419/2/D421-426/1-11/D428/3/D432-436/5/D438/1/D440-441/3/D444/1/D446-447/3/D450-452/5/D456-462/5-15/D467-468/3-13/D476/1/D478/4/D483-491
#Sum of mod_gap_min and orig_len: 509.0
#Sum of mod_gap_max and orig_len: 789.0
#Sum of gap and orig_len: 649.0
```
The extracted residues to input in the RFdiffusion bash script should print in your terminal as shown above.

**Step 3: Running RFdiffusion**
Navigate to 'helper_scripts/template_scripts/' to copy the template.
1. RFdiffusion
```bash
cd helper_scripts/template_scripts/
cp RFdiffusion_bash.sh /home/users/astar/gis/"your_username"/scratch/denovo_editors/RFdiffusion_run1.sh #example
nano RFdiffusion_run1.sh
```
To view the example RFdiffusion bash script, refer to the example folder.
Edit and save the bash script according to your requirements in your denovo_editors directory. To submit the job:
```bash
sbatch Rfdiffusion_run1.sh
```
You can monitor your job using the following commands:
```bash
squeue #view the entire queue
squeue -u your_username #replace 'your_username', you will be able to view the status of all jobs you have submitted
```
When your submitted job is running, the status will change from "PD" to "R". Once the job completes, it will no longer show in queue and output files should be in the specified output directory. If the run fails, you will see ".err" and ".out" log files in the same directory in which you submitted the bash script. The output of RFdiffusion consists of pdb files that correspond with the total number of designs specified in the RFdiffusion bash script. Each pdb file has a corresponding trb file, and both file types are outputted into the same output directory specified in the bash script as well. 

**Step 4: Prep for MPNN**

Navigate to 'denovo_editors/helper_scripts/'. You need to open and edit trb2json.py, which is used to prepare the pdb and trb files for MPNN in JSON format. To learn more about how this script works, refer to 'denovo_editors/helper_scripts/trb2json_explained.txt'. You need to edit this script so that when executed, it pulls files from the correct RFdiffusion output subdirectory:
```bash
# change the directory containing PDB and TRB files in lines 6 & 7
directory = '/home/users/astar/gis/your_username/scratch/RFdiffusion/outputs/run_1' #assuming that your RFdiffusion outputs were saved to "=outputs/run_1"
json_directory = os.path.join(directory, 'json_residues')
# save changes to the script. Then run it:
python trb2json.py
```
The script creates files containing JSON objects with residues from each respective design, along with a corresponding file. All of the outputted files should be saved to '/denovo_editors/ProteinMPNN/inputs/run_name/' (here, 'run_name' is replaced with 'run_1/').

**Step 5: running MPNN**

Navigate to 'helper_scripts/template_scripts/' to copy the MPNN template and create your bash script.

```bash
cd helper_scripts/template_scripts/
cp MPNN_bash.sh /home/users/astar/gis/"your_username"/scratch/denovo_editors/MPNN_run1.sh #example
nano MPNN_run1.sh
```

To view the example MPNN bash script, refer to the example folder.
Edit and save the bash script according to your requirements in your denovo_editors directory. the bash script will activate the my_mlfold environment and runs MPNN integrated into a loop script for all of the designs. To submit the job:
```bash
sbatch MPNN_run1.sh
```

MPNN will output fasta files for every design, and the number of sequences per design is a paramater that can be determined by you. The files are saved to '/denovo_editors/ProteinMPNN/outputs/run_name/'.

**Step 6: Alphafold**

Navigate to /home/users/astar/gis/diyasri/scratch/denovo_editors/helper_scripts/template_scripts/' to copy the alphafold template and create your bash script:

```bash
cd helper_scripts/template_scripts/
cp Alphafold_bash.sh /home/users/astar/gis/"your_username"/scratch/denovo_editors/Alphafold_run1.sh #example
nano Alphafold_run1.sh
```
Keep in mind when you edit this script, alphafold typically requires a longer runtime. It is recommended to set '#SBATCH --time' to at least: 04:00:00 to prevent the job reaching a time limit without producing some output pdb files. Certain paramters have been set for optimal design of conditional proteins (batch --num-recycle 3 --amber --max-msa 64:128 --num-seeds 1) but you may change them if you wish to. To submit the job:

```bash
sbatch Alphafold_run1.sh
```

If there are no issues, the output files will be saved to output directly in real-time to denovo_editors/local_alphafold/outputs. The outputted pdb files are the end products of this workflow.

**Step 7: extracting your results and output files**

After the predicted pdb files are created, the next step is to visualize them and validate them. Visualization can be done using softwares such as Pymol and ChimeraX. To extract information on the outputs, including the pLDDT scores for each design generated, navigate to '/denovo_editors/helper_scripts' and edit extract2csv.py. This script compiles information on the model outputs from Alphafold. This is useful if you have generated many designs and you wish to rank them and review the feasability of your predicted designs. 
```bash
nano extract2csv.py
#make sure the script compiles information from the correct subdirectory containing all outputs fromm alphafold. Edit lines 5 & 6:
# Relative path to the run directory
#run_dir = '.'
```
Once you have corrected the input directory file path, execute the script:
```bash
python extract2csv.py
```

Then download and open the csv called 'extracted_alphafold_values_run.csv' to view the compiled information. 





