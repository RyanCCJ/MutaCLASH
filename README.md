# Crosslink Induced Mutation Sites (CIMS)

## Description
The **Crosslink Induced Mutation Sites (CIMS)** project is designed to detect the coordinates of CIMS ( **deletions** or **substitutions** ) in NGS data. It provides a comprehensive analysis pipeline for identifying mutation sites and binding sites in hybrid-reads derived from CLASH or iCLIP experiments.

## Features
- Utilizes [CLASH Analyst](https://cosbi7.ee.ncku.edu.tw/CLASHanalyst/input/) to identify suitable NGS reads for analysis
- Uses [ChiRA](https://github.com/pavanvidem/chira) to identify suitable hybrid-reads
- Detects mutation information using [Bowtie2](https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml)
- Utilizes algorithms such as [pirScan](http://cosbi4.ee.ncku.edu.tw/pirScan/), [miRanda](https://bioweb.pasteur.fr/packages/pack@miRanda@3.3a), and [RNAup](https://github.com/ViennaRNA/ViennaRNA) to identify binding sites
- Generates visualizations of the distribution of mutations

## Usage
To run the CIMS pipeline, execute the following command:
```
sh run.sh <input.fa> <regulator.fa> <transcript.fa> <algorithm> <enrichment analysis type>
```
- **input:** NGS data in fasta or csv format.
- **regulator**: regulator file in fasta or csv format.
- **transcript**: transcript file in fasta or csv format.
- **algorithm**: Algorithm used to predict binding sites, which can be `pirScan/miRnada/RNAup`.
- **enrichment analysis type**: Method used to analyze enrichment, which can be `[region/site/up/abu]` refers to "CLASH identified region", "pirScan binding site", "RNAup binding site", "mRNA abundance" (check this in `pipeline/induce_22g/abu_data/`).

After executing the command, the pipeline will run and complete all the necessary steps.

## Output
The output files are stored in the `data/output/` directory. The directory contains the following files:
- **Figures:** The final generated figures are stored in the `figure/` subdirectory.
- **Intermediate Files:** The intermediate files generated during the analysis are stored in various formats (.csv, etc.) and can be found in their respective tool directories.

### Figures
The output figures generated by the CIMS pipeline include:

- **Mutation Distribution:** Provides information on the distribution of mutations, including deletions and substitutions.
<img src="examples/fig/distribution.png" width=300 />

- **Pairing Ratio:** Calculates and analyzes the pairing ratios at both global and individual coordinates.
<img src="examples/fig/pairing_ratio.png" width=500 />
<img src="examples/fig/pairing_ratio_at_position.png" width=300 />

- **Enrichment Analysis:** Performs enrichment analysis, comparing wild-type samples and fold-change measurements.
<!--img src="examples/fig/22G.png" width=300 /-->
<img src="examples/fig/fold_change.png" width=300 />

- **Cumulative Distribution Function (CDF):** Calculates and visualizes the cumulative distribution function.
<!--img src="examples/fig/22G_CDF.png" width=300 /-->
<img src="examples/fig/fold_change_CDF.png" width=300 />

Please refer to the corresponding tool documentation for more details on the specific output files and their interpretations.

## Requirements
- Python >= 3.5
- numpy >= 1.12.1
- seaborn >= 0.9
- matplotlib >= 2.2.2
- pandas >= 0.23.0
- scipy >= 1.1.0
- statannot = 0.2.3
- Bowtie2 >= 2.1.0
- ChiRA >= 1.4.0
- BWA >= 0.7.5a
- miRanda >= 3.3a
- RNAup >= 2.4.10
