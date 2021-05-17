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
        # Read data, skip the last ones since these are the single atom energy
        # Get number of unique atom types, n_types
        step = read(real_values, "0")
        n_types = len(set(step.get_chemical_symbols()))
        # Read in real values and predicted values
        real_atoms = read(real_values, f":-{n_types}")
        predicted_atoms = read(predicted_values, f":-{n_types}")

        # Plot real energies on the x axis and predicted energies on the y axis
        real_energies = [a.get_potential_energy() / len(a.get_chemical_symbols())
                         for a in real_atoms]
        predicted_energies = [a.get_potential_energy() / len(a.get_chemical_symbols())
                              for a in predicted_atoms]
        # Make scatter plot
        axis.scatter(real_energies[:], predicted_energies[:], c='k', s=20)

        # Improve look
        axis.set_title(title, fontsize=13, fontname="Times New Roman")
        energy_array = np.array(real_energies + predicted_energies)
        lim = (energy_array.min(), energy_array.max())
        axis.set_xlim(lim)
        axis.set_ylim(lim)
        # add line of exactly with slope = 1
        axis.plot(energy_array, energy_array, c='g', alpha=0.5)
        # set labels
        axis.set_ylabel(r'Energy by Model / eV')
        axis.set_xlabel(r'Energy by DFT / eV')

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
        axis.scatter(real_forces[:], predicted_forces[:], c='k')
        # Improve look
        axis.set_title(title)
        force_array = np.array(real_forces + predicted_forces)
        lim = (force_array.min(), force_array.max())
        axis.set_xlim(lim)
        axis.set_ylim(lim)
        # add line with slope = 1
        axis.plot(force_array, force_array, c='g', alpha=0.5)
        # set labels
        axis.set_ylabel('force by GAP / (eV/Å)')
        axis.set_xlabel('force by DFT / (eV/Å)')
