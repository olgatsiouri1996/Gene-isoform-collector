import os
from pyfaidx import Fasta
import argparse
# Create the parser object
ap = argparse.ArgumentParser(description='Searches and exports the isoforms of each input gene loci')

# Add arguments for the input files
ap.add_argument('-loci','--loci file', required=True, help='1-column text file containing gene loci')
ap.add_argument('-input','--input fasta file', required=True, help='input multi-FASTA file')
ap.add_argument('-dir','--output directory', required=False, type=str, default='.', help='Directory to save fasta files. Default is the current directory')

# Add optional arguments
ap.add_argument('-name','--multifasta filename', type=str,required=False, help='output single file name')
ap.add_argument('-type','--type', required=False, type=int, default=1, help="output type to choose. 1: single file, 2: 1 file per gene loci, 3: 1 file per gene isoform. Default is 1")

# Parse the arguments
args = vars(ap.parse_args())

# Helper function to wrap fasta sequence to 60 characters per line
def wrap_fasta_seq(seq):
    return '\n'.join([seq[i:i+60] for i in range(0, len(seq), 60)])


# Read in the FASTA file with long names
fasta = Fasta(args['input fasta file'], read_long_names=True)

# Read in the gene loci file
with open(args['loci file'], 'r') as f:
    loci_list = [line.rstrip() for line in f]

# Initialize a dictionary to store the sequences
seq_dict = {}

# Loop through the loci and search for matches in the FASTA file
for key in fasta.keys():
    for locus in loci_list:
        if locus in key:
            # If the locus is found, add it to the dictionary
            seq_dict[key.rstrip()] = wrap_fasta_seq(fasta[key][:].seq)

# Choose directory to save output files
os.chdir(args['output directory'])

# Write the output
if args['type'] == 1:
    # Output all sequences in a single file
    with open(args['multifasta filename']+'.fasta', 'w') as f:
        for locus, seq in seq_dict.items():
            f.write(f'>{locus}\n{seq}\n')
elif args['type'] == 2:
    # Create separate files 1 for each input loci
    for loci in loci_list:
        with open(loci+'.fasta', 'w') as f:
            for locus, seq in seq_dict.items():
                    if loci in locus:
                        f.write(f'>{locus}\n{seq}\n')
else:
    for locus, seq in seq_dict.items(): # Create separate files 1 for each gene isoform
        with open(locus.split(' ')[0]+'.fasta', 'w') as f:
            f.write(f'>{locus}\n{seq}\n')
