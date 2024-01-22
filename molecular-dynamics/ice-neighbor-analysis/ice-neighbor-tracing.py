residue = 1535 # SOL Number from npt.gro file
residue_particle = {'11943':8871, '12061':8989, '12101':9029, '1535':1151, '3679':2527}
particle = residue_particle[f'{residue}'] # Particle Identifier OVITO

neighbor4 = 4 
neighbor16 = 16 

file_path4 = f'/home/sumon/path/to/another/folder/{residue}SOL_{particle}_{neighbor4}neighbors.xyz'
file_path16 = f'/home/sumon/path/to/another/folder/{residue}SOL_{particle}_{neighbor16}neighbors.xyz'

'''
This entire piece of code allows parsing through the ovito generated files and storing the data for first as well
as second shell neighbors. 

In both cases, the data are stored with unique variable names. For first shell, 4-has been added to all variables
as suffix. And for the second shell, 16 has replaced 4 in all variables. 

The way the script operates is as follows:

- first it checks where the word 'Lattice' is located.
- after detecting 'Lattice', it goes on to store data with the script.
- then, it tries to find if 'SOL' is present in the line and parses requisite data from the lines.
- once no 'SOL' is detected, the script checks for the next instance of 'Lattice' and restarts the loop.
- as the loop continues, all frame data is parsed with an eye on the 'Lattice'. Occurance of this word
marks for a new frame which should be parsed and the data should be stored for further calculation.

Once first and second shell data have been stored, first shell data is subtracted from the second shell
to make sure that first shell influence can be stripped off the second shell and only the second shell influence
can be calculated later on for a selected water molecule. For that reason, 12 has been input as suffix for
all variables in the very last part of it.

frac_store actually stores all the fractions and have been multiplied with 100 to store data in %. That helps
in better visualization. 

Finally, Pandas dataframes have been used to tabulate the data.
'''

# open the file and read all lines
with open(file_path4, 'r') as file_content4:
    all_lines4 = file_content4.readlines()
    file_content4.seek(0) # brings cursor to the beginning of file
    num_frames4 = file_content4.read().count('Lattice') # calculate frame count by searching the phrase 'Lattice'
    
# open the file and read all lines
with open(file_path16, 'r') as file_content16:
    all_lines16 = file_content16.readlines()
    file_content16.seek(0) # brings cursor to the beginning of file
    num_frames16 = file_content16.read().count('Lattice') # calculate frame count by searching the phrase 'Lattice'
    
if num_frames4 == num_frames16:
    num_frames = num_frames16
else:
    print('The frame counts are different. Modify the code!!!')

# store all neighbor fraction
frac_store4 = np.zeros((num_frames, 6))
frac_store16 = np.zeros((num_frames, 6))
frac = 0

# store selected molecule states
selected_mol = np.zeros((num_frames))
sm = 0 # to navigate the frames inside loop

########################################################################################
# store first shell neighbor fraction
frac_store4 = np.zeros((num_frames, 6))
frac = 0

# store first shell neighbor data
other4 = np.zeros(num_frames)
hex_ice4 = np.zeros(num_frames)
cub_ice4 = np.zeros(num_frames)
intf_ice4 = np.zeros(num_frames)
intf_hyd4 = np.zeros(num_frames)
hyd4 = np.zeros(num_frames)

# loop to iterate through the data
for i, string in enumerate(all_lines4): # i gives index, string gives individual lines
    if 'Lattice' in string: # if 'Lattice' is encountered, a while loop starts
        
        other, hex_ice, cub_ice, intf_ice, intf_hyd, hyd = [0] * 6
        
        while 'SOL' in all_lines4[i+1]: # 'Lattice'-subsequent lines are processed only
            elements = all_lines4[i+1].split() # makes a list of strings
            
            # store the states of selected molecule
            if f'{particle}' in all_lines4[i+1] and f'{particle}' == elements[0]:
                if elements[-1] == 'Other':
                    selected_mol[sm] = 0
                if elements[-1] == 'Hexagonal_ice':
                    selected_mol[sm] = 1
                if elements[-1] == 'Cubic_ice':
                    selected_mol[sm] = 2
                if elements[-1] == 'Interfacial_ice':
                    selected_mol[sm] = 3
                if elements[-1] == 'Hydrate':
                    selected_mol[sm] = 4
                if elements[-1] == 'Interfacial_hydrate':
                    selected_mol[sm] = 5
                sm += 1
            
            # store the states of the neighbor molecules
            else: 
                if elements[-1] == 'Other':
                    other += 1
                if elements[-1] == 'Hexagonal_ice':
                    hex_ice += 1
                if elements[-1] == 'Cubic_ice':
                    cub_ice += 1
                if elements[-1] == 'Interfacial_ice':
                    intf_ice += 1
                if elements[-1] == 'Hydrate':
                    hyd += 1
                if elements[-1] == 'Interfacial_hydrate':
                    intf_hyd += 1
    
            # python index starts from zero and finishes 1 before the end
            if i == len(all_lines4) - 2:
                break
            else:
                i += 1
         
        # calculation of num of neighbors
        tot_neighbor = other + hex_ice + cub_ice + intf_hyd + hyd + intf_ice
        
        if tot_neighbor == 0:
            tot_neighbor = 1
            
        # calculation of fraction of each type of neighbors
        frac_store4[frac, 0] = other / tot_neighbor
        frac_store4[frac, 1] = hex_ice / tot_neighbor
        frac_store4[frac, 2] = cub_ice / tot_neighbor
        frac_store4[frac, 3] = intf_hyd / tot_neighbor
        frac_store4[frac, 4] = hyd / tot_neighbor
        frac_store4[frac, 5] = intf_ice / tot_neighbor
        
        # storing of 4 neighbor data
        other4[frac] = other
        hex_ice4[frac] = hex_ice
        cub_ice4[frac] = cub_ice
        intf_ice4[frac] = intf_ice
        intf_hyd4[frac] = intf_hyd
        hyd4[frac] = hyd
        
        frac += 1 # for each iteration, this value goes up by 1
        
        if 'Lattice' in string: # when another 'Lattice' is encountered, loop restarts
            continue 

########################################################################################
# store second shell neighbor fraction
frac_store16 = np.zeros((num_frames, 6))
frac = 0

# store second shell neighbor data
other16 = np.zeros(num_frames)
hex_ice16 = np.zeros(num_frames)
cub_ice16 = np.zeros(num_frames)
intf_ice16 = np.zeros(num_frames)
intf_hyd16 = np.zeros(num_frames)
hyd16 = np.zeros(num_frames)


for i, string in enumerate(all_lines16): # i gives index, string gives individual lines
    if 'Lattice' in string: # if 'Lattice' is encountered, a while loop starts
        
        other, hex_ice, cub_ice, intf_ice, intf_hyd, hyd = [0] * 6
        
        while 'SOL' in all_lines16[i+1]: # 'Lattice'-subsequent lines are processed only
            elements = all_lines16[i+1].split() # makes a list of strings

            # store the states of selected molecule
            if f'{particle}' in all_lines16[i+1] and f'{particle}' == elements[0]:
                pass # stored from first shell data
            
            # store the states of the neighbor molecules
            else: 
                if elements[-1] == 'Other':
                    other += 1
                if elements[-1] == 'Hexagonal_ice':
                    hex_ice += 1
                if elements[-1] == 'Cubic_ice':
                    cub_ice += 1
                if elements[-1] == 'Interfacial_ice':
                    intf_ice += 1
                if elements[-1] == 'Hydrate':
                    hyd += 1
                if elements[-1] == 'Interfacial_hydrate':
                    intf_hyd += 1
    
            # python index starts from zero and finishes 1 before the end
            if i == len(all_lines16) - 2:
                break
            else:
                i += 1
         
        # calculation of num of neighbors
        tot_neighbor = other + hex_ice + cub_ice + intf_hyd + hyd + intf_ice
        
        if tot_neighbor == 0:
            tot_neighbor = 1
        
        # calculation of fraction of each type of neighbors
        frac_store16[frac, 0] = other / tot_neighbor
        frac_store16[frac, 1] = hex_ice / tot_neighbor
        frac_store16[frac, 2] = cub_ice / tot_neighbor
        frac_store16[frac, 3] = intf_hyd / tot_neighbor
        frac_store16[frac, 4] = hyd / tot_neighbor
        frac_store16[frac, 5] = intf_ice / tot_neighbor
        
        # storing of 16 neighbor data
        other16[frac] = other
        hex_ice16[frac] = hex_ice
        cub_ice16[frac] = cub_ice
        intf_ice16[frac] = intf_ice
        intf_hyd16[frac] = intf_hyd
        hyd16[frac] = hyd
        
        frac += 1 # for each iteration, this value goes up by 1
        
        if 'Lattice' in string: # when another 'Lattice' is encountered, loop restarts
            continue

########################################################################################
# calculation for NEW second layer molecules
other12 = np.zeros(num_frames)
hex_ice12 = np.zeros(num_frames)
cub_ice12 = np.zeros(num_frames)
intf_ice12 = np.zeros(num_frames)
intf_hyd12 = np.zeros(num_frames)
hyd12 = np.zeros(num_frames)

frac_store12 = np.zeros((num_frames, 6))

for i in range(num_frames):
    other12[i] = other16[i] - other4[i]
    hex_ice12[i] = hex_ice16[i] - hex_ice4[i]
    cub_ice12[i] = cub_ice16[i] - cub_ice4[i]
    intf_ice12[i] = intf_ice16[i] - intf_ice4[i]
    intf_hyd12[i] = intf_hyd16[i] - intf_hyd4[i]
    hyd12[i] = hyd16[i] - hyd4[i]
    
    tot_neighbor = other12[i] + hex_ice12[i] + cub_ice12[i] + intf_ice12[i] + intf_hyd12[i] + hyd12[i]
    
    frac_store12[i, 0] = other12[i] / tot_neighbor 
    frac_store12[i, 1] = hex_ice12[i] / tot_neighbor 
    frac_store12[i, 2] = cub_ice12[i] / tot_neighbor 
    frac_store12[i, 3] = intf_ice12[i] / tot_neighbor 
    frac_store12[i, 4] = intf_hyd12[i] / tot_neighbor
    frac_store12[i, 5] = hyd12[i] / tot_neighbor

########################################################################################
# dataframe visualization
frac_store4 = frac_store4.copy() * 100
frac_store16 = frac_store16.copy() * 100
frac_store12 = frac_store12.copy() * 100
dataframe(frac_store12)
