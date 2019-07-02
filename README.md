Please note that the following scripts are written in Python 2.7. 
# Sample Separator

The sample_separator_v5.py can be used for demultiplexing sequencing data with multiple samples in a NGS run. It identifies sample ID and extracts barcodes for each sample from fastq files based on user-supplied sets of sample ID and user-defined parameters.

## Input
Two input files are needed: NGS data file in fastq format and a text file of sample ID. Sample ID should be written in the format of one ID for each line. The program then prompts the user to input user-defined parameters including barcode length, linker length and number of barcodes in one DNA construct. 
![Image](/images/s_1.png)

Sample ID format:
![Image](/images/s_2.png)

## Output
1. Text file
Extracted barcodes for each sample are exported as individual tab-delimited text file named with its sample ID. If the read begins with an expected sample ID, barcodes will be extracted and reads are written in rows. The first column contains barcodes representing the sample ID and the subsequent columns contain barcodes at different (nth) positions. The total number of columns depends on the number (n) of positions being mutated/barcoded in the study.
![Image](/images/s_3.png)

1. CSV file
It is a report showing the total read count for each sample in the sample ID text file.
![Image](/images/s_4.png)

# Barcode Analyzer
The bc_analyzer_v4.py analyser counts every barcode combinations and discards reads that do not match any expected barcodes in the list of position (nth) barcodes at the nth position. 

## Input
Users can directly input all the output text files from sample separator.py for barcode combination count. The position of the barcodes indicates the location of the target residue being mutated along a DNA sequence. The lists of barcodes specifying the type of amino acid substitutions at a particular location should be provided in separate text files for the input of ‘position (nth) barcode list’ in the format of one barcode for each line. 
![Image](/images/b_1.png)
## Output
It generates a CSV file listing each barcode combination in each row with the count number showing on the last column. Additionally, it generates a general count report for the overall read counts for all the samples.
![Image](/images/b_2.png)
General count report:
![Image](/images/b_3.png)

## License
[MIT](https://choosealicense.com/licenses/mit/)
