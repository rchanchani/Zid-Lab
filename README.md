# Zid Lab (development shifted to private repo)
### Ribosome Occupancy Model
_Author: Raghav Chanchani_

  A tunable ribosome occupancy model that takes in initiation rate, elongation rate, time length of the simulation, number of ribosomes per mRNA, and the number of mRNA. This is in addition to a .txt file of the mRNA sequence of the gene of interest and the probability of moving forward in an initiation or elongation step. Probabilities of moving between any two codons are assumed to be equal. Once a ribosome reaches the end of an mRNA and moves past the gene's length, it is recycled to the -1 index which represents a location in the cell from which ribosomes can readily reattach to the mRNA of interest. The 0 index is assumed to be the AUG codon. The model does not consider the codons specific to the gene of interest, only its length.
  This model can be used to model the effects of various stresses on arbitrary mRNA by modifying the kI and kE inputs and the probability that the ribosomes move forward for a given timestep. Such a tool is a powerful way to develop an informed hypothesis for expected results and provides a simplified view of incredibly complex translation in an arbitrary cell. Input slider values are set to lie within the range of observed values for all tunable parameters aside from the length of the simulation and probability of moving forward.

### Sequence Analysis Pipeline
_Authors: Raghav Chanchani, Jingxiao Zhang_

  This analysis pipeline allows members of our lab to quickly and effectively analyze large amounts of RNASeq data and extract useful features and graphs from the reads. The highly modular shell script allows users to customize the pipeline for specific uses by easily adding in their own analysis modules as well. The script runs the bowtie alignment software, generates map files, counts and sorts the aligned reads, and extracts features into Excel compatible files that allow the user to generate insightful graphs of their experimental data.
 
### Polarity Pipeline
_Author: Jingxiao Zhang_

  A Polarity pipeline allows members of our lab to measure the gene specific polarity. It takes in the xls file which contains ribosome counts per position with start and end position for each gene. We use the definition of polarity described in article "eIF5A Functions Globally in Translation Elongation and Termination" by Schuller et al.. The polarity for a gene with length l is calculated as the sum of polarity at each position in the gene. The first and last 15 nuceotides of each gene are excluded in our analysis.
  The output polarity per gene is loaded to a csv file. Also, for each input sequence, we generate 3 plot to visualize how the polarity changes within the sequence. The first one shows the polarity at each position. The second one shows the cumulative distribution of polarity per gene. The third one is a normalized distribution of the gene specific polarities in the sequence.
 
