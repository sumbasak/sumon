# prerequisite
# install pycdhit 

import pandas as pd
from pycdhit import CDHIT

# create instance of cdhit
cdhit = CDHIT(prog='cd-hit', path='path/to/cdhit/excutatable/bin/')

# load excel file
# to load fasta file, use fasta_reader from functions.py file
df = pd.read_excel('path/to/enzyme/excel/file.xlsx')

# select columns for new data frame
df_in = df[['identifier', 'sequence']]

# run seq similarity check and filtering with cdhit
df_out, df_clstr = cdhit.set_options(**kwargs).cluster(df_in)

# save final data frame and cluster details
df_out.to_excel('desired_file_name.xlsx', index=False)
df_clstr.to_excel('desired_file_name_2.xlsx', index=False)
