# Define infile and outfile
infile=$1
outfile=$2

# Get Number of atoms in simulation (should be $natom for $infile)
natom=`awk '{if($1 == "<atoms>") print $2;}' $infile `

# Get Number of time steps (should be $nsteps for $infile)
nsteps=`grep forces $infile | wc -l`

# Get starting line in .xyz-file. e.g. where the simulation starts and the nsteps begin
startline=`grep -m1 -n velocities vasprun.xml | awk '{print substr($1,1,length($1)-1)}'`

# Get all lines after line with 'positions' after startline
#positions_1=`tail -n +$startline $infile | grep -A  $natom 'positions' | awk '{print $2,$3,$4}'`

# Get all lines after line with 'forces' after startline
#forces_1=`tail -n +$startline $infile | grep -A  $natom 'forces' | awk '{print $2,$3,$4}'`

# Get the 9 lattice constants
lattice=`grep  -A 3 -m 2 \"basis\" $infile | awk '{print$2,$3,$4}' | tail -n+2 | head -n+3`

# Get the atom - element e.g. H (Hydrogen)
natompo=`echo $natom"+1" | bc -l`
atom_type=`grep -A $natompo '>atomtype' $infile | awk -F':' '{split($1,subfield,"");print subfield[12] }' | tail -n +3`

# Get all lines after line with 'positions', just the coordinates without text
# Don´t know how to implement startline
natompt=`echo $natom"+2" | bc -l`
#positions=`tail -n $startline vasprun.xml | grep  -A  $natom 'positions' $infile | sed -e '/positions/,+d' | awk '{print $2,$3,$4}'`
positions=`tail -n $startline vasprun.xml | grep  -B  $natompt 'forces' $infile | sed -e '/forces/,+d' | awk '{print $2,$3,$4}'`

# Get all lines after line with 'forces', just the coordinates without text
# Don´t know how to implement startline
forces=`tail -n $startline vasprun.xml | grep  -A  $natom 'forces' $infile | sed -e '/forces/,+d' | awk '{print $2,$3,$4}'`


echo "Read number of MD steps from " $infile " infile. nsteps = " $nsteps
echo "Read number of atoms from " $infile " infile. natoms = " $natom
echo "Read line number at which the simulationstarts from " $infile "infile = " $startline
echo "Read lattice constants from " $infile "infile." "lattice constants = " $lattice

# Transfer positions, forces and atom_types to arrays for better indexing possibilities
pos_array=( $positions )
for_array=( $forces )
atom_type_array=( $atom_type )

#echo "writing atom type"
#echo $atom_type



# Write the output to outfile
# Outfile doesn´t resemble the .xml file. Arrays contain correct values(except
# pos_array is too long by one step).

natommo=`echo $natom"-1" | bc -l`
nstepsmo=`echo $nsteps"-1" | bc -l`

for i in `seq 0 1 $nstepsmo`
do

    echo $natom >> $outfile
    echo "Lattice=$lattice Properties=species:S:1:pos:R:3:
    forces:R:3:energies:R:1 Energie=dummy_energy pbc=\"T T T\"" >> $outfile
    for j in `seq 0 1 $natommo`
    do
        echo ${atom_type_array[$j]} ${pos_array[${i}*${natom}*3+${j}*3]} ${pos_array[${i}*${natom}*3+${j}*3+1]} \
        ${pos_array[${i}*${natom}*3+${j}*3+2]} ${for_array[${i}*${natom}*3+${j}*3]} ${for_array[${i}*${natom}*3+${j}*3+1]} \
        ${for_array[${i}*${natom}*3+${j}*3+2]} >> $outfile
    done

done

# Write the output to outfile, just a template and not for further use
# for i in `seq 1 1 $nsteps`
# do
#
#    echo $natom >> $outfile
#    echo "Lattice=$lattice Properties=species:S:1:pos:R:3:
#    forces:R:3:energies:R:1 Energie=dummy_energy pbc=\"T T T\"" >> $outfile
#
#    #echo $positions $ forces>> $outfile
#
#    echo "appended output" >> $outfile
#    #echo $nsteps " " $natoms
#    #echo $positions $forces
#
# done


# While loop to iterate over all positions, can only iterate over one argument
# tail -n +$startline $infile | grep -A  $natom 'positions' | awk '{print $2,$3,$4}' | while read line
# do
# echo $line
# done

# not working, tried to loop over all positions
# for (x,y,z) in $positions
# do
#    echo $x $y $z
# done





# Get the atom - element e.g. H (Hydrogen)
# grep -A $natom '>atomtype' $infile | awk -F':' '{split($1,subfield,"");print subfield[12] }' | tail -n +3




# TODO:
# Get energies for each timestep, uncertain which energies to use

# Get energies of isolated atoms (e.g. e_0_Hydrogen)

# concatenate all the needed values to a infile format identical to .xyz (e.g. train.xyz)
