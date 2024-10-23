# How to run fusioncatcher
## How to create synthetic data
Define the file `genes_panels.txt` where there are the genes to be used to create the data.

### Fusim
Fusim allows you to generate merges from `genes_panels.txt`.

To install fusim:
```shell
wget https://github.com/aebruno/fusim/raw/master/releases/fusim-0.2.2-bin.zip
unzip fusim-0.2.2-bin.zip
rm fusim-0.2.2-bin.zip

wget -O refFlat.txt.gz http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/refFlat.txt
gunzip refFlat.txt.gz
mv refFlat.txt fusim-0.2.2/refFlat.txt

wget http://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/chromFa.tar.gz
tar -xzf chromFa.tar.gz
cat chr*.fa > fusim-0.2.2/hg19.fa
rm chromFa.tar.gz
rm chr*.fa

apt install samtools
samtools faidx fusim-0.2.2/hg19.fa
```

To run fusim on two genes `gene1` and `gene2`, use the following command specifying `dir_path`:
```shell
java -jar ./fusim-0.2.2/fusim.jar \
        --gene-model=./fusim-0.2.2/refFlat.txt \
        --fusions=10 \
        --reference=./fusim-0.2.2/hg19.fa \
        --fasta-output=dir_path/fusion_gene1_gene2.fasta \
        --text-output=dir_path/fusion_gene1_gene2.txt \
        -1 gene1 \
        -2 gene2 \
        --cds-only \
        --auto-correct-orientation
```
Run the following python script `fusim_data.py` to form all possible merges between genes contained in `genes_panel.txt`.

### ART ILLUMINA
ART ILLUMINA is the tool that allows you to obtain synthetics read from fasta files.

To install ART ILLUMINA install the following package:
```shell
apt install art-nextgen-simulation-tools
```

ART ILLUMINA takes a folder of fasta files and returns the synthetic reads.
Run the following python script `art_data.py` to get the reads of all fasta files obtained from fusim.

---

## Fusion Catcher
### Run Fusion Catcher using human_v102
Download human_v102 inside the data folder by running the following command:
```shell
mkdir -p data
wget --no-check-certificate http://sourceforge.net/projects/fusioncatcher/files/data/human_v102.tar.gz.aa -P data
wget --no-check-certificate http://sourceforge.net/projects/fusioncatcher/files/data/human_v102.tar.gz.ab -P data
wget --no-check-certificate http://sourceforge.net/projects/fusioncatcher/files/data/human_v102.tar.gz.ac -P data
wget --no-check-certificate http://sourceforge.net/projects/fusioncatcher/files/data/human_v102.tar.gz.ad -P data

cat human_v102.tar.gz.* > human_v102.tar.gz
rm -f human_v102.tar.gz.*

tar -xzf human_v102.tar.gz
```

Start a container using the fusioncatcher image `fusioncatcher_data:v1`:
```shell
sudo docker run -v "$(pwd)/data":/opt/fusioncatcher/v1.30/data -it fusioncatcher_data:v1
```

Once the container is started enter the fusioncatcher installation folder, to run the tool call the python file `fusioncatcher.py` contained in the bin folder.

Usage ([Docs](https://github.com/ndaniel/fusioncatcher/blob/master/doc/manual.md#6---usage)):
```shell
python2 fusioncatcher.py \
-d /some/human/data/directory/ \
-i /some/input/directory/containing/fastq/files/ \
-o /some/output/directory/
```

Usage with human_v102:
```shell
cd /opt/fusioncatcher/v1.30/
python2 bin/fusioncatcher.py -d data/human_v102 -i some/input/directory/containing/fastq/files/ -o /some/output/directory/
```

In case you want to use fusioncatcher on 'single-end' reads they have to be longer than 130 and you have to specify the `--single-end` parameter.


### Run Fusion Catcher on the ART ILLUMINA sequences.

Run the docker container by mounting the `data` folder making sure that the `fasta.fq` outputs of ART ILLUMINA are present.

```shell
sudo docker run -v "$(pwd)/data":/opt/fusioncatcher/v1.30/data -it fusioncatcher_data:v1
```

Run Fusion Catcher:
```shell
cd opt/fusioncatcher/v1.30/
mkdir -p data/some_output
python2 bin/fusioncatcher.py -d data/human_v102 -i data/art_output -o data/some_output
```

### Notes on the input of Fusion Catcher

Fusion catcher assumes that the folder containing fastq files are paired-read, specifically they will be paired two by two in alphabetical order. The following are some examples:

Consider a folder with the following files:
```
L002_R1.fastq.gz
L002_R2.fastq.gz
L003_R1.fastq.gz
L003_R2.fastq.gz
```
*FusionCatcher* will assume that the first two files are a pair and the second two are another pair.


For example, this **NOT** is a valid input:
```
10_L002_R2_05.fastq.gz
11_L002_R1_06.fastq.gz
12_L002_R2_06.fastq.gz
1_L002_R1_01.fastq.gz
2_L002_R2_01.fastq.gz
3_L002_R1_02.fastq.gz
4_L002_R2_02.fastq.gz
5_L002_R1_03.fastq.gz
6_L002_R2_03.fastq.gz
7_L002_R1_04.fastq.gz
8_L002_R2_04.fastq.gz
9_L002_R1_05.fastq.gz
```
It is important that the input folder contains only fastq files related to the reads to be analyzed.

### Notes on the output of Fusion Catcher

Within the folder specified with the parameter `-o data/output/` fusioncatcher will produce several output files, the two most relevant ones below:

`final-list_candidate_fusion_genes.txt` - Contains the final table with the new candidate fusion genes (fusion point with * is also present);
`summary_candidate_fusions.txt` - Contains a summary of candidate fusion genes found;

Table 1 - Description of columns contained in `final-list_candidate-fusion-genes.txt`:

| **Column** | **Description** |
|:-----------|:----------------|
| **Gene\_1\_symbol(5end\_fusion\_partner)** | Gene symbol of the 5' end fusion partner |
| **Gene\_2\_symbol\_2(3end\_fusion\_partner)** | Gene symbol of the 3' end fusion partner |
| **Gene\_1\_id(5end\_fusion\_partner)** | Ensembl gene id of the 5' end fusion partner |
| **Gene\_2\_id(3end\_fusion\_partner)** | Ensembl gene id of the 3' end fusion partner |
| **Exon\_1\_id(5end\_fusion\_partner)** | Ensembl exon id of the 5' end fusion exon-exon junction |
| **Exon\_2\_id(3end\_fusion\_partner)** | Ensembl exon id of the 3' end fusion exon-exon junction |
| **Fusion\_point\_for\_gene\_1(5end\_fusion\_partner)** | Chromosomal position of the 5' end of fusion junction (chromosome:position:strand); 1-based coordinate |
| **Fusion\_point\_for\_gene\_2(3end\_fusion\_partner)** | Chromosomal position of the 3' end of fusion junction (chromosome:position:strand); 1-based coordinate |
| **Spanning\_pairs** | Count of pairs of reads supporting the fusion (**including** also the multimapping reads) |
| **Spanning\_unique\_reads** | Count of unique reads (i.e. unique mapping positions) mapping on the fusion junction. Shortly, here are counted all the reads which map on fusion junction minus the PCR duplicated reads. |
| **Longest\_anchor\_found** | Longest anchor (hangover) found among the unique reads mapping on the fusion junction |
| **Fusion\_finding\_method** | Aligning method used for mapping the reads and finding the fusion genes. Here are two methods used which are: (i) **BOWTIE** = only Bowtie aligner is used for mapping the reads on the genome and exon-exon fusion junctions, (ii) **BOWTIE+BLAT** = Bowtie aligner is used for mapping reads on the genome and BLAT is used for mapping reads for finding the fusion junction,  (iii) **BOWTIE+STAR** = Bowtie aligner is used for mapping reads on the genome and STAR is used for mapping reads for finding the fusion junction, (iv) **BOWTIE+BOWTIE2** = Bowtie aligner is used for mapping reads on the genome and Bowtie2 is used for mapping reads for finding the fusion junction. |
| **Fusion\_sequence** | The inferred fusion junction (the asterisk sign marks the junction point) |
| **Fusion\_description** | Type of the fusion gene (see the Table 2) |
| **Counts\_of\_common\_mapping\_reads** | Count of reads mapping simultaneously on both genes which form the fusion gene. This is an indication how similar are the DNA/RNA sequences of the genes forming the fusion gene (i.e. what is their homology because highly homologous genes tend to appear show as candidate fusion genes). In case of completely different sequences of the genes involved in forming a fusion gene then here it is expected to have the value zero. |
| **Predicted\_effect** | Predicted effect of the candidate fusion gene using the annotation from Ensembl database. This is shown in format **effect\_gene\_1**/**effect\_gene\_2**, where the possible values for effect\_gene\_1 or effect\_gene\_2 are: **intergenic**, **intronic**, **exonic(no-known-CDS)**, **UTR**, **CDS(not-reliable-start-or-end)**, **CDS(truncated)**, or **CDS(complete)**. In case that the fusion junction for both genes is within their CDS (coding sequence) then only the values **in-frame** or **out-of-frame** will be shown. |
| **Predicted\_fused\_transcripts** | All possible known fused transcripts in format ENSEMBL-TRANSCRIPT-1:POSITION-1/ENSEMBLE-TRANSCRIPT-B:POSITION-2, where are fused the sequence 1:POSITION-1 of transcript ENSEMBL-TRANSCRIPT-1 with sequence POSITION-2:END of transcript ENSEMBL-TRANSCRIPT-2 |
| **Predicted\_fused\_proteins** | Predicted amino acid sequences of all possible fused proteins (separated by ";").  |

For more information on the abbreviations used by Fusion Catcher visit [this github](https://github.com/ndaniel/fusioncatcher/blob/master/doc/manual.md#6---usage).
