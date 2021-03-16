# Module containing a GAPModelmodel class that is taking descriptor classes as
# inputs.
# Instances of descriptors are initialised with hyperparameters which can't be
# changed afterwards.
# The objects, hence the models are then to be trainind by input training data
# which has to be in a .xyz file format.
# Trained models are then able to make predictions on any given data, which
# again, has to be in .xyz file format.
# The models are able to take two different sets of data as an input. Usually
# one containing the the coordinates and the other containing the correct
# energy values. The model then makes predictions based on the coordinates and
# compares them with the (given) correct energy values. The outcome is then
# displayed and visualised.
import os


class GAPModel(object):
    """Model to be trained takes no arguments and is simply an untrained model.
    The paramters from the descriptor class need to be transferred
    from the given dictionary to  arguments for the 'train' method.
    This is done by indexing the dictionary by the name of the needed parameter.
    """

    def __init__(self):
        pass

    # train method takes parameters from dictionary and performs a shell
    # command.
    # The shell command then produces an out_file (standard is xml-file). The
    # output file contains the trained GAP Potential.
    # the descriptor_type needs to be passed, in order to perform the right
    # shell command. Print Output to the command window is optional,
    # the default is True.
    # Sigma is the default regularisation corresponding to energy, force,
    # virial, hessian
    # GAP_potentialXML is created and contains the trained potential =.xml file
    # params = dict
    # descriptor_type = string (for example: distance_2b)
    # training_data = .xyz file
    # sigma = string, 4 integers  larger than zero e.g.: 0.1 0.2 0.2 0.0
    # sigma values = 'energy force virial, hessian'

    def train(self, *parameter_string, training_data, GAP_potential, sigma,
              print_output=True):
        cmd = (f" gap_fit energy_parameter_name = energy "
               f" force_parameter_name = forces do_copy_at_file = F "
               f" sparse_separate_file = T gp_file = {GAP_potential}"
               f" at_file = \'{training_data}\' "
               f" default_sigma = {{ {sigma} }}"
               f" gap = {{ ")

        if len(parameter_string) == 1:
            cmd += parameter_string[0]+'}'

        if len(parameter_string) > 1:
            cmd += parameter_string[0]
            cmd_list = [cmd]
            for s in range(len(parameter_string)-1):
                cmd_list.append(parameter_string[s+1])
            cmd = (' :'.join(cmd_list))+'}'

        if print_output is True:
            print(cmd)
        # Execute shell command
        try:
            stream = os.popen(cmd)
            output = stream.read()
            if print_output is True:
                print(output)
        except AttributeError as error:
            print(error)

        # Pass the trained potential to class variable
        self.GAP_potential = f"{os.getcwd()}/{GAP_potential}"

    def get_potential_file(self):
        try:
            return self.GAP_potential
        except AttributeError:
            return ("Model not trained. You need to train the model first to"
                    "get a trained GAP_potential")

    # The predict method takes an atom configuration and predicts the ground
    # state energies. Therefore test data needs to be passed, which contains
    # the atom configuration. A trained potential needs to be passed which
    # usually stems from the model.train-method. QUIP_Prediction is the output
    # file containing the predicted energies. Print Output to the command
    # window is optional, the default is True.

    # Test_Data = .xyz file
    # GAP_potential = .xml file
    # QUIP_Prediction = .xyz file

    def predict(self, Test_Data, GAP_potential, QUIP_Prediction, print_output=True):
        cmd = (f" quip E=T F=T "
               f" atoms_filename=\'{Test_Data}\' "
               f" param_filename=\'{GAP_potential}\' | grep AT | sed \'s/AT//\' "
               f" > {QUIP_Prediction} ")

        if print_output is True:
            print(cmd)
        try:
            stream = os.popen(cmd)
            output = stream.read()
            if print_output is True:
                print(output)
        except AttributeError as error:
            print(error)
        # Pass the predicted  energy values to class variable
        self.QUIP_Prediction = f"{os.getcwd()}/{QUIP_Prediction}"

    def get_prediction_file(self):
        try:
            return self.QUIP_Prediction
        except AttributeError:
            return ("Prediction did not work.")

    # Function to return the Root Mean Squared Error - RMSE
    def RMSE(self, real_values, predicted_values):
        # Get number of unique atom types, n_types
        from ase.io import read
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
        # Calculate Root Mean Squared Error (RMSE)
        import numpy as np
        r = np.array(real_energies)
        p = np.array(predicted_energies)
        RMSE = np.sqrt(np.sum(np.power(r-p, 2))/len(r))

        return RMSE

    # Function to return the coefficient of determination  - R2_score
    def R2_Score(self, real_values, predicted_values):
        # Get number of unique atom types, n_types
        from ase.io import read
        step = read(real_values, "0")
        n_types = len(set(step.get_chemical_symbols()))

        # Read in real values and predicted values
        real_atoms = read(real_values, f":-{n_types}")
        predicted_atoms = read(predicted_values, f":-{n_types}")

        # Plot real energies on the x axis and predicted energies on the y axis
        real_energies = [a.get_potential_energy() /
                         len(a.get_chemical_symbols()) for a in real_atoms]
        predicted_energies = [a.get_potential_energy() /
                              len(a.get_chemical_symbols())
                              for a in predicted_atoms]

        # Calculate coefficient of determination (R2_score)
        import numpy as np
        r = np.array(real_energies)
        p = np.array(predicted_energies)
        mean = np.mean(r)

        SQR = np.sum(np.power((r-p), 2))
        SQT = np.sum(np.power((r-mean), 2))

        R2_score = 1 - (SQR/SQT)

        return R2_score


class Split(object):
    """Splitting up data into train and test data in whichever percentage
    wanted. Recommended is a 80:20 split."""

    # data_file = .xyz file
    # train_percentage float between 0 and 1
    def __init__(self, data_file, train_percentage):
        self.data = data_file
        self.train_percentage = train_percentage
        self.test_percentage = 1 - train_percentage

    def get_percentages(self):
        str = (f" Percentile of training data: {self.train_percentage} | "
               f" Percentile of test data: {self.test_percentage} ")
        return str
    # Performs the split and returns a file containing the training data and
    # a file containing the test data.
    # The wanted output filenames need to be passed, in order to avoid unwanted
    # future overwriting or duplicating.
    # train_data_file = .xyz file
    # test_data_file = .xyz file

    def split(self, train_data_file, test_data_file):
        # Assign to self variables
        self.train_data_xyz = train_data_file
        self.test_data_xyz = test_data_file

        # Read data that´s going to be split to atoms object for easier handle.
        # Read all atoms, except the last one, because this is the isolated atom.
        # The isolated energy is then put at the end of the training data.
        # Get number of unique atom types, n_types
        from ase.io import read
        step = read(self.data, "0")
        n_types = len(set(step.get_chemical_symbols()))

        # Read in Data
        data = read(self.data, f":-{n_types}")

        # Randomize sampling
        import random
        # Take 80percent of the data as training data
        n_train = round(len(data)*self.train_percentage)
        train_index = random.sample(range(1, len(data)+1), n_train)

        # Take 20percent of the data as test data
        n_test = len(data)-(n_train)
        test_index = random.sample(range(1, len(data)+1), n_test)

        # Get isolated_atom to then add to the end of training data.
        # TODO: This is hardcoded, but can be replaced by variable number
        # number of occuring atom types.
        from ase.io import read
        step = read(self.data, "0")
        n_types = len(set(step.get_chemical_symbols()))
        isolated_atom = read(self.data, f"-{n_types}")

        # Small test if splitting indices worked correctly
        complete = train_index+test_index
        if len(complete) == len(data):
            train_data = [data[i-1] for i in train_index] + [isolated_atom]
            test_data = [data[i-1] for i in test_index]

        self.train_data = train_data
        self.test_data = test_data

        # Write train and test data to .xyz file format because this format
        # is needed for gap_fit and quip.
        from ase.io import write
        write(train_data_file, train_data[:])
        write(test_data_file, test_data[:])

    def get_splitted_data_files(self):
        return self.train_data_xyz, self.test_data_xyz

    def get_splitted_data(self):
        return self.train_data, self.test_data
