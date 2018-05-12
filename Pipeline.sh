#!/bin/sh

# Author: Raghav Chanchani
# Description: RNA sequencing pipeline to align, generate .map files, and extract, count, and sort features.
# Change filepaths to desired version of python by using the "which pythonX.Y" command to find correct path

read -p 'Destination directory is: ' dest
read -p 'Input file to be trimmed is: ' input

# Trim polyAs from user specified input file
/opt/python/bin/python3.4 /home/rchancha/Bowtie/bowtie/Zid-Lab-Pipeline-master/Inputs/trimPolyA.py $input

# Set file names and paths for use in bowtie and data extraction
mapDir='/Maps'
# Set index basenames
rdnaDir='/Indexes/rDNA'
geneDir='/Indexes/genome'
ecoliDir='/Indexes/e_coli'
# Set bowtie output filenames
aligned='/alignerdRNA.fq'
unaligned='/unrna.fq'
map='/aligned.map'
alignSortDir='/AlignedSorted'
mochiDir='/MochiView'
featDir='/Feature'


# Create bowtie argument filepaths
arg1=$dest$rdnaDir
arg2=$dest$aligned
arg3=$dest$unaligned
arg4=$dest$geneDir
arg5=$dest$mapDir$map
arg6=$dest$alignSortDir

# Print filepaths to confirm identity
echo $arg1
echo $arg2
echo $arg3

# Create unaligned .fq by removing contaminants
bowtie -a --best --strata $arg1 $input $arg2 --un $arg3

# Create align against specified DNA file and write to .map
mkdir -p $dest$maps
bowtie -m 1 --best --strata $arg4 $arg3 $arg5

# Create directory to store aligned and sorted .txt file using aligned .map input
mkdir -p $dest$alignSortDir
echo $dest$alignSortDir
/opt/python/bin/python3.4 /home/rchancha/Bowtie/bowtie/Zid-Lab-Pipeline-master/Inputs/AlignSortCount.py $arg6 $arg5

# Create and store MochiView files using ___ input
mkdir -p $dest$mochiDir
echo $dest$mochiDir
echo "Which file would you like to generate a MochiView .txt file for?" read mochiInput
/opt/python/bin/python3.4 /home/rchancha/Bowtie/bowtie/Zid-Lab-Pipeline-master/Inputs/MochiView.py $mochiInput

# Create and store Feat.txt to see gene features
mkdir -p $dest$featDir
echo $dest$featDir
echo "Which file would you like to generate a Feature .txt file for?" read featInput
/opt/python/bin/python3.4 /home/rchancha/Bowtie/bowtie/Zid-Lab-Pipeline-master/Inputs/.py $featInput

# Sort gene features
echo $dest$sortedGeneDir
/opt/python/bin/python3.4 /home/rchancha/Bowtie/bowtie/Zid-Lab-Pipeline-master/Inputs/sortFiles.py $sortInput
# Count gene features, generate Excel file, and perform basic data analysis
echo $dest$countSortDir
/opt/python/bin/python3.4 /home/rchancha/Bowtie/bowtie/Zid-Lab-Pipeline-master/Inputs/countSorted.py $countInput
