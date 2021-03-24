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
lattice=`grep  -A 3 -m 2 \"basis\" $infile | awk '{print $2,$3,$4}' | tail -n+2 | head -n+3 | tr '\n' ' '`
# Get the 9 lattice constants seperately to then expand the fractional coordinates to cartesian coordinates
lattice_ax=`echo $lattice | awk '{print $1}'`
lattice_ay=`echo $lattice | awk '{print $2}'`
lattice_az=`echo $lattice | awk '{print $3}'`
lattice_bx=`echo $lattice | awk '{print $4}'`
lattice_by=`echo $lattice | awk '{print $5}'`
lattice_bz=`echo $lattice | awk '{print $6}'`
lattice_cx=`echo $lattice | awk '{print $7}'`
lattice_cy=`echo $lattice | awk '{print $8}'`
lattice_cz=`echo $lattice | awk '{print $9}'`
echo $lattice_ax
echo $lattice_ay
echo $lattice_az
echo $lattice_bx
echo $lattice_by
echo $lattice_bz
echo $lattice_cx
echo $lattice_cy
echo $lattice_cz


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


energies=`grep  -A  5 'eentropy' $infile | grep "e_0_energy" | awk '{print $3}'`


echo "Read number of MD steps from " $infile " infile. nsteps = " $nsteps
echo "Read number of atoms from " $infile " infile. natoms = " $natom
echo "Read line number at which the simulationstarts from " $infile "infile = " $startline
echo "Read lattice constants from " $infile "infile." "lattice constants = " $lattice

# Transfer positions, forces and atom_types to arrays for better indexing possibilities
energies_array=( $energies )
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
    echo "Lattice=\"$lattice\" Properties=species:S:1:pos:R:3:forces:R:3:energies:R:1 energy=${energies_array[${i}*2+1]} pbc=\"T T T\"" >> $outfile


    for j in `seq 0 1 $natommo`
    do
        # Multiply fractional coordinates with matrix of lattice vectors and
        # write, together with forces and constant 0 (quip syntax demands some
        # constant here), to outfile.
        fracx=`echo ${pos_array[${i}*${natom}*3+${j}*3]} | bc -l`
        fracy=`echo ${pos_array[${i}*${natom}*3+${j}*3+1]} | bc -l`
        fracz=`echo ${pos_array[${i}*${natom}*3+${j}*3+2]} | bc -l`
        x=`echo $fracx"*"$lattice_ax"+"$fracy"*"$lattice_bx"+"$fracz"*"$lattice_cx| bc -l `
        y=`echo $fracx"*"$lattice_ay"+"$fracy"*"$lattice_by"+"$fracz"*"$lattice_cy| bc -l `
        z=`echo $fracx"*"$lattice_az"+"$fracy"*"$lattice_bz"+"$fracz"*"$lattice_cz| bc -l `
        echo ${atom_type_array[$j]} $x $y $z\
        ${for_array[${i}*${natom}*3+${j}*3]} ${for_array[${i}*${natom}*3+${j}*3+1]} \
        ${for_array[${i}*${natom}*3+${j}*3+2]} " 0.00000000" >> $outfile
    done

done

# e.g. Lattice="20.0 0.0 0.0 0.0 20.0 0.0 0.0 0.0 20.0"
# Properties=species:S:1:pos:R:3:forces:R:3:energies:R:1
# Energie=3.21 free_Energie=3.21 pbc="T T T"
echo "1"  >> $outfile
echo "Lattice=\"$lattice\" Properties=species:S:1:pos:R:3:forces:R:3:energies:R:1 energy=3.21 free_Energie=3.21 pbc=\"T T T\"" >> $outfile
echo "H        0.00000000       0.00000000       0.00000000       0.00000000       0.00000000       0.00000000       3.21000000" >> $outfile
