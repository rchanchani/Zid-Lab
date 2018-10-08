# Zid-Lab
### Ribosome Occupancy Model
_Author: Raghav Chanchani_
  A tunable ribosome occupancy model that takes in initiation rate, elongation rate, time length of the simulation, number of ribosomes per mRNA, and the number of mRNA. This is in addition to a .txt file of the mRNA sequence of the gene of interest and the probability of moving forward in an initiation or elongation step. Probabilities of moving between any two codons are assumed to be equal. Once a ribosome reaches the end of an mRNA and moves past the gene's length, it is recycled to the -1 index which represents a location in the cell from which ribosomes can readily reattach to the mRNA of interest. The 0 index is assumed to be the AUG codon. The model does not consider the codons specific to the gene of interest, only its length.
  This model can be used to model the effects of various stresses on arbitrary mRNA by modifying the kI and kE inputs and the probability that the ribosomes move forward for a given timestep. Such a tool is a powerful way to develop an informed hypothesis for expected results and provides a simplified view of incredibly complex translation in an arbitrary cell. Input slider values are set to lie within the range of observed values for all tunable parameters aside from the length of the simulation and probability of moving forward.

### Sequence Analysis Pipeline
_Authors: Raghav Chanchani, Jingxiao Zhang_
  This analysis pipeline allows members of our lab to quickly and effectively analyze large amounts of RNASeq data and extract useful features and graphs from the reads. The highly modular shell script allows users to customize the pipeline for specific uses by easily adding in their own analysis modules as well. The script runs the bowtie alignment software, generates map files, counts and sorts the aligned reads, and extracts features into Excel compatible files that allow the user to generate insightful graphs of their experimental data.
 
### Polarity Pipeline
_Author: Jingxiao Zhang_
