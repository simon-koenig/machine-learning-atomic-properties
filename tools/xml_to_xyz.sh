file=$1
outfile=$2

# Get Number of atoms in simulation (shoulb be $natom for $file)
natom=`awk '{if($1 == "<atoms>") print $2;}' $file `
nsteps=`grep forces $file | wc -l`

echo "Read number of MD steps from " $file " file. nsteps=" $nsteps
echo "Read number of atoms from " $file " file. natoms=" $natom

for i in `seq 1 1 $nsteps`
do

echo $i > $outfile

echo "appended output" >> $outfile
echo $nsteps " " $natoms

done

# Get all lines after line with 'positions'
#grep -A $natom 'positions' $file | awk '{print $2,$3,$4}'


# Get all lines after line with with 'forces'
# grep -A $natom 'forces' $file | awk '{print $2,$3,$4}'


# Get the atom - element e.g. H (Hydrogen)
# grep -A $natom '>atomtype' $file | awk -F':' '{split($1,subfield,"");print subfield[12] }' | tail -n +3


#TODO:
# Get energies for each timestep

# Get lattice constants

# Get energies of isolated atoms (e.g. e_0_Hydrogen)

# concatenate all the needed values to a file format identical to .xyz (e.g. train.xyz)
