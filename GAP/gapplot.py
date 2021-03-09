# Module containing plotting tools to visualise GAP and QUIP generated data.
# Visualisation for quality checking of the model and presenting the
# elaborated data.
from ase.io import read
import numpy as np


class QualityPlot(object):
    """QualityPlot is used to compare the real values of either energy or force
    of some configuration to the predict values of QUIP of the same
    configuration."""

    # real_values = .xyz file, outcome of DFT
    # predicted values = .xyz file, outcome of QUIP/GAP
    # axis will be an object, that´s the second returned object of
    # plt.subplot()
    # axis = numpy.ndarray
    def energies_on_energies(self, real_values, predicted_values, axis,
                             title="Energy-Plot"):
        # Read data, skip the last one since this is the single atom energy
        # TODO: -1 is hardcoded, should be -n where n is the number
        # of atom_types
        real_atoms = read(real_values, ':-1')
        predicted_atoms = read(predicted_values, ':-1')

        # Plot real energies on the x axis and predicted energies on the y axis
        real_energies = [a.get_potential_energy() / len(a.get_chemical_symbols())
                         for a in real_atoms]
        predicted_energies = [a.get_potential_energy() / len(a.get_chemical_symbols())
                              for a in predicted_atoms]
        # Make scatter plot
        axis.scatter(real_energies[:], predicted_energies[:])

        # Improve look
        axis.set_title(title)
        energy_array = np.array(real_energies + predicted_energies)
        lim = (energy_array.min(), energy_array.max())
        axis.set_xlim(lim)
        axis.set_ylim(lim)
        # add line of exactly with slope = 1
        axis.plot(energy_array, energy_array, c='g')
        # set labels
        axis.set_ylabel('energy by GAP / (eV/Å)')
        axis.set_xlabel('energy DFT / (eV/Å)')

        # real_values = .xyz file, outcome of DFT
        # predicted values = .xyz file, outcome of QUIP/GAP
        # axis will be an object, that´s the second returned object of
        # plt.subplot()
        # axis = numpy.ndarray

    def forces_on_forces(self, real_values, predicted_values, axis, title="Force-Plot"):
        real_atoms = read(real_values, ':')
        predicted_atoms = read(predicted_values, ':')

        # extract data for only one species
        real_forces, predicted_forces = [], []
        for a_real, a_predicted in zip(real_atoms, predicted_atoms):
            # get all atom_types
            atom_types = a_real.get_chemical_symbols()
            # add force for each atom
            for j, sym in enumerate(atom_types):
                real_forces.append(a_real.get_forces()[j])
                predicted_forces.append(a_predicted.arrays['force'][j])
        # Make scatter plot
        axis.scatter(real_forces[:], predicted_forces)
        # Improve look
        axis.set_title(title)
        force_array = np.array(real_forces + predicted_forces)
        lim = (force_array.min(), force_array.max())
        axis.set_xlim(lim)
        axis.set_ylim(lim)
        # add line with slope = 1
        axis.plot(force_array, force_array, c='g')
        # set labels
        axis.set_ylabel('force by GAP / (eV/Å)')
        axis.set_xlabel('force by DFT / (eV/Å)')
