#!/bin/sh

# Author: Raghav Chanchani
# Description: RNA sequencing pipeline to align, generate .map files, and extract, count, and sort features.
# Change filepaths to desired version of python by using the "which pythonX.Y" command to find correct path
read -p 'Destination directory is: ' dest
read -p 'Input file to be trimmed is: ' input
# Trim polyAs from user specified input file
/opt/python/bin/python3.4 /home/rchancha/Bowtie/bowtie/Zid-Lab-Pipeline-master/Inputs/trimPolyA.py $input

# Show pipeline options
echo 'To run the entire pipeline enter 0.'
echo 'To remove contaminants enter 1.'
echo 'To align and generate .map files enter 2.'
echo 'To align and sort reads in a .txt file from .map enter 3.'
echo 'To create a MochiView compatible file enter 4.'
echo 'To create a features .txt file enter 5.'
echo 'To sort gene features enter 6.'
echo 'To count sorted gene features and create an Excel sheet enter 7.'
echo 'To exit enter Quit'

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

PS3='Please enter an option: '
options=("0" "1" "2" "3" "4" "5" "6" "7" "Quit")
select progIndex in "${options[@]}"
do
  case $progIndex in
    "0")
      echo "You chose to run the entire pipeline."
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
      read -p 'What would you like to name the Excel sheet? ' sheetName
      read -p 'Start position: ' start
      read -p 'End position: ' end
      read -p 'Selection length: ' length
      /opt/python/bin/python3.4 /home/rchancha/Bowtie/bowtie/Zid-Lab-Pipeline-master/Inputs/countSorted.py $countInput $sheetName $start $end $length
      ;;
    "1")
      echo "You chose to remove contaminants. This will create an unaligned .fq."
      # Create unaligned .fq by removing contaminants
      bowtie -a --best --strata $arg1 $input $arg2 --un $arg3
      # Show pipeline options
      echo 'To run the entire pipeline enter 0.'
      echo 'To align and generate .map files enter 2.'
      echo 'To align and sort reads in a .txt file from .map enter 3.'
      echo 'To create a MochiView compatible file enter 4.'
      echo 'To create a features .txt file enter 5.'
      echo 'To sort gene features enter 6.'
      echo 'To count sorted gene features and create an Excel sheet enter 7.'
      echo 'To exit enter Quit'
      ;;
    "2")
      echo "You chose to align and write the output to a .map file."
      # Create align against specified DNA file and write to .map
      mkdir -p $dest$maps
      bowtie -m 1 --best --strata $arg4 $arg3 $arg5
      # Show pipeline options
      echo 'To run the entire pipeline enter 0.'
      echo 'To remove contaminants enter 1.'
      echo 'To align and sort reads in a .txt file from .map enter 3.'
      echo 'To create a MochiView compatible file enter 4.'
      echo 'To create a features .txt file enter 5.'
      echo 'To sort gene features enter 6.'
      echo 'To count sorted gene features and create an Excel sheet enter 7.'
      echo 'To exit enter Quit'
      ;;
    "3")
      echo "You chose to align and sort reads in a .txt file from .map."
      mkdir -p $dest$alignSortDir
      echo $dest$alignSortDir
      /opt/python/bin/python3.4 /home/rchancha/Bowtie/bowtie/Zid-Lab-Pipeline-master/Inputs/AlignSortCount.py $arg6 $arg5
      # Show pipeline options
      echo 'To run the entire pipeline enter 0.'
      echo 'To remove contaminants enter 1.'
      echo 'To align and generate .map files enter 2.'
      echo 'To create a MochiView compatible file enter 4.'
      echo 'To create a features .txt file enter 5.'
      echo 'To sort gene features enter 6.'
      echo 'To count sorted gene features and create an Excel sheet enter 7.'
      echo 'To exit enter Quit'
      ;;
    "4")
      echo "You chose to create a MochiView compatible file."
      mkdir -p $dest$mochiDir
      echo $dest$mochiDir
      echo "Which file would you like to generate a MochiView .txt file for?" read mochiInput
      /opt/python/bin/python3.4 /home/rchancha/Bowtie/bowtie/Zid-Lab-Pipeline-master/Inputs/MochiView.py $mochiInput
      # Show pipeline options
      echo 'To run the entire pipeline enter 0.'
      echo 'To remove contaminants enter 1.'
      echo 'To align and generate .map files enter 2.'
      echo 'To align and sort reads in a .txt file from .map enter 3.'
      echo 'To create a features .txt file enter 5.'
      echo 'To sort gene features enter 6.'
      echo 'To count sorted gene features and create an Excel sheet enter 7.'
      echo 'To exit enter Quit'
      ;;
    "5")
      echo "You chose to create a features .txt file."
      mkdir -p $dest$featDir
      echo $dest$featDir
      echo "Which file would you like to generate a Feature .txt file for?" read featInput
      /opt/python/bin/python3.4 /home/rchancha/Bowtie/bowtie/Zid-Lab-Pipeline-master/Inputs/.py $featInput
      # Show pipeline options
      echo 'To run the entire pipeline enter 0.'
      echo 'To remove contaminants enter 1.'
      echo 'To align and generate .map files enter 2.'
      echo 'To align and sort reads in a .txt file from .map enter 3.'
      echo 'To create a MochiView compatible file enter 4.'
      echo 'To sort gene features enter 6.'
      echo 'To count sorted gene features and create an Excel sheet enter 7.'
      echo 'To exit enter Quit'
      ;;
    "6")
      echo "You chose to sort gene features."
      echo $dest$sortedGeneDir
      /opt/python/bin/python3.4 /home/rchancha/Bowtie/bowtie/Zid-Lab-Pipeline-master/Inputs/sortFiles.py $sortInput
      # Show pipeline options
      echo 'To run the entire pipeline enter 0.'
      echo 'To remove contaminants enter 1.'
      echo 'To align and generate .map files enter 2.'
      echo 'To align and sort reads in a .txt file from .map enter 3.'
      echo 'To create a MochiView compatible file enter 4.'
      echo 'To create a features .txt file enter 5.'
      echo 'To count sorted gene features and create an Excel sheet enter 7.'
      echo 'To exit enter Quit'
      ;;
    "7")
      echo "You chose to count sorted gene features and create an Excel sheet."
      echo $dest$countSortDir
      read -p 'What would you like to name the Excel sheet? ' sheetName
      read -p 'Start position: ' start
      read -p 'End position: ' end
      read -p 'Selection length: ' length
      /opt/python/bin/python3.4 /home/rchancha/Bowtie/bowtie/Zid-Lab-Pipeline-master/Inputs/countSorted.py $countInput $sheetName $start $end $length
      # Show pipeline options
      echo 'To run the entire pipeline enter 0.'
      echo 'To remove contaminants enter 1.'
      echo 'To align and generate .map files enter 2.'
      echo 'To align and sort reads in a .txt file from .map enter 3.'
      echo 'To create a MochiView compatible file enter 4.'
      echo 'To create a features .txt file enter 5.'
      echo 'To sort gene features enter 6.'
      echo 'To exit enter Quit'
      ;;
    "Quit")
      break
      ;;
    *) echo invalid option;;
  esac
done
