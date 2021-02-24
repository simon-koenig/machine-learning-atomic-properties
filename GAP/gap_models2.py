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
    # shell command.
    # GAP_potentialXML is created and contains the trained potential =.xml file
    # params = dict
    # descriptor_type = string (for example: distance_2b)
    # training_data = .xyz file

    def train(self, *parameter_string, training_data, GAP_potential,):
        cmd = (f" gap_fit energy_parameter_name = energy "
               f" force_parameter_name = forces do_copy_at_file = F "
               f" sparse_separate_file = T gp_file = {GAP_potential}"
               f" at_file = \'{training_data}\' "
               f" default_sigma = {{0.008 0.04 0 0}}"
               f" gap = {{ ")

        if len(parameter_string) == 1:
            cmd += parameter_string[0]+'}'

        if len(parameter_string) > 1:
            cmd += parameter_string[0]
            cmd_list = [cmd]
            for s in range(len(parameter_string)-1):
                cmd_list.append(parameter_string[s+1])
            cmd = (':'.join(cmd_list))+'}'

        print(cmd)
        # Execute shell command
        stream = os.popen(cmd)
        output = stream.read()
        print(output)
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
    # file containing the predicted energies.
    # Test_Data = .xyz file
    # GAP_potential = .xml file
    # QUIP_Prediction = .xyz file

    def predict(self, Test_Data, GAP_potential, QUIP_Prediction):
        cmd = (f" quip E=T F=T "
               f" atoms_filename=\'{Test_Data}\' "
               f" param_filename=\'{GAP_potential}\' | grep AT | sed \'s/AT//\' "
               f" > {QUIP_Prediction} ")
        print(cmd)
        try:
            stream = os.popen(cmd)
            output = stream.read()
            print(output)
        except AttributeError as error:
            print(error)
        # Pass the predicted  energy values to class variable
        self.QUIP_Prediction = f"{os.getcwd()}/{QUIP_Prediction}"

    def get_prediction_file(self):
        try:
            return self.QUIP_Prediction
        except AttributeError:
            return ("Prediction did not work. ")


class distance_2b(object):
    """2b_distance descriptor
    descriptor class takes paramters and converts them to a dictionary, which
    is then used by the GAPModel to initialise its paramters. """

    def __init__(self, cutoff, covariance_type, delta, theta_uniform,
                 sparse_method, add_species, n_sparse):
        self.cutoff = cutoff
        self.covariance_type = covariance_type
        self.delta = delta
        self.theta_uniform = theta_uniform
        self.sparse_method = sparse_method
        self.add_species = add_species
        self.n_sparse = n_sparse

        p = {'cutoff': self.cutoff,
             'covariance_type': self.covariance_type,
             'delta': self.delta,
             'theta_uniform': self.theta_uniform,
             'sparse_method': self.sparse_method,
             'add_species': self.add_species,
             'n_sparse': self.n_sparse}
        self.param_dict = p

        param_string = (f" distance_2b cutoff = {p['cutoff']}"
                        f" covariance_type = {p['covariance_type']}"
                        f" delta = {p['delta']}"
                        f" theta_uniform = {p['theta_uniform']}"
                        f" sparse_method = {p['sparse_method']}"
                        f" add_species = {p['add_species']}"
                        f" n_sparse = {p['n_sparse']}")

        print(param_string)

        self.param_string = param_string

        descriptor_type = 'distance_2b'
        self.descriptor_type = descriptor_type

    def get_descriptor_type(self):
        return self.descriptor_type

    def get_parameter_dict(self):
        return self.param_dict

    def get_parameter_string(self):
        return self.param_string


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
        import ase.io
        data = ase.io.read(self.data, ':')

        # Randomize sampling
        import random
        # Take 80percent of the data as training data
        n_train = round(len(data)*self.train_percentage)
        train_index = random.sample(range(1, len(data)+1), n_train)

        # Take 20percent of the data as test data
        n_test = len(data)-(n_train)
        test_index = random.sample(range(1, len(data)+1), n_test)

        # Small test if splitting indices worked correctly
        complete = train_index+test_index
        if len(complete) == len(data):
            train_data = [data[i-1] for i in train_index]
            test_data = [data[i-1] for i in test_index]

        self.train_data = train_data
        self.test_data = test_data

        # Write train and test data to .xyz file format because this format
        # is needed for gap_fit and quip
        ase.io.write(train_data_file, train_data[:])
        ase.io.write(test_data_file, test_data[:])

    def get_splitted_data_files(self):
        return self.train_data_xyz, self.test_data_xyz

    def get_splitted_data(self):
        return self.train_data, self.test_data
