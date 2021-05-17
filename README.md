# Machine Learning project on the determination of quantum mechanical energies and forces

The package contains all the required tools to reproduce the results of my bachelor thesis. All the theoretical basics and step by step instructions are in my [Thesis](./Thesis). The code is written mostly in python and some in shell script.

The training data was generated using Vienna *ab initio* simulation package (VASP). This work deals with on system of a hydrogen molecule and another one of a hydrogen crystal. The machine learning model was built upon the libAtoms code architecture in [libAtoms](https://github.com/libAtoms/QUIP).

The repository structure is as follows.
- [GAP](./GAP) contains all modules and and classes for the creation of a ml model.
- [MD_H2](./MD_H2) and [MD_c2c_150GPa](./MD_c2c_150GPa) include the quantum mechanical configurations.
- [Results](./results) has notebooks for parameter optimisation and plotting the machine learning outputs. This directory alone is enough for easy recreation of the machine learning model.
- [Tools](./tools) contains visualisations of the analysed quantum mechanical systems using Visual Molecular Dynamics (VMD), a shell script to transform the VASP data from an XML file to required XYZ files. The transformed XYZ files are also included.
- [Thesis](./Thesis) Paper on the project.
