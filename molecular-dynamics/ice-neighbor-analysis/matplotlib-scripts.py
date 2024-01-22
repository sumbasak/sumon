x = np.arange(0, num_frames, 1)
y_oth = frac_store12[:, 0]
y_ih = frac_store12[:, 1]
y_ic = frac_store12[:, 2]
y_ii = frac_store12[:, 3]
y_hyd = frac_store12[:, 4]
y_ihyd = frac_store12[:, 5]

# figure
fig = plt.figure(figsize = (6, 4), dpi = 1000)
ax = fig.add_axes([0.15, 0.15, 0.75, 0.75])

ms = 0.5
ax.plot(x, y_oth, label = f'other', 
        color = 'blue', lw = 0.1, marker = '.', markersize = ms)
ax.plot(x, y_ih, label = f'Hexagonal ice', 
        color = 'red', lw = 0.1, marker = '.', markersize = ms)
ax.plot(x, y_ic, label = f'Cubic ice', 
        color = 'magenta', lw = 0.1, marker = '.', markersize = ms)
ax.plot(x, y_ii, label = f'Interfacial ice', 
        color = 'indigo', lw = 0.1, marker = '.', markersize = ms)
ax.plot(x, y_hyd, label = f'Hydrate', 
        color = 'cyan', lw = 0.1, marker = '.', markersize = ms)
ax.plot(x, y_ihyd, label = f'Interfacial hydrate', 
        color = 'green', lw = 0.1, marker = '.', markersize = ms)

# label and title insertion
ax.set_xlabel('Time / 0.1 ns', fontsize = '8')
ax.set_ylabel('Water States / %', fontsize = '8')
ax.set_title(f'{residue}SOL 12Neighbors', fontweight = 'bold')

#ax.set_xlim([1800, 1900])
#ax.set_xlim([900, 1000])

# ticks changing
xt = np.arange(0, num_frames, 250)
plt.xticks(xt, fontsize = '8')
yt = np.arange(0, 100, 10)
plt.yticks(yt, fontsize = '8')

# legend and fontsize for legend
ax.legend(fontsize = '6')

# saves the figure
fig.savefig(f'Tracking states_12neighbors_{residue}SOL.png')

# function that checks image within Jupyter lab
png(f'Tracking states_12neighbors_{residue}SOL.png')
