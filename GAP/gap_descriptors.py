# Module contains GAP descriptors which can be used to describe an
# atom-configuration. The descriptors generate strings, these strings
# are then passed to the gap_models to execute a fit according to the
# parameters defined in the descriptor class.


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


class angle_3b(object):
    """angle_3b descriptor
    descriptor class takes paramters and converts them to a dictionary, which
    is then used by the GAPModel to initialise its paramters. """

    def __init__(self, cutoff, covariance_type, delta, theta_fac,
                 sparse_method, add_species, n_sparse):
        self.cutoff = cutoff
        self.covariance_type = covariance_type
        self.delta = delta
        self.theta_fac = theta_fac
        self.sparse_method = sparse_method
        self.add_species = add_species
        self.n_sparse = n_sparse

        p = {'cutoff': self.cutoff,
             'covariance_type': self.covariance_type,
             'delta': self.delta,
             'theta_fac': self.theta_fac,
             'sparse_method': self.sparse_method,
             'add_species': self.add_species,
             'n_sparse': self.n_sparse}
        self.param_dict = p

        param_string = (f" angle_3b cutoff = {p['cutoff']}"
                        f" covariance_type = {p['covariance_type']}"
                        f" delta = {p['delta']}"
                        f" theta_fac = {p['theta_fac']}"
                        f" sparse_method = {p['sparse_method']}"
                        f" add_species = {p['add_species']}"
                        f" n_sparse = {p['n_sparse']}")

        print(param_string)

        self.param_string = param_string

        descriptor_type = 'distance_3b'
        self.descriptor_type = descriptor_type

    def get_descriptor_type(self):
        return self.descriptor_type

    def get_parameter_dict(self):
        return self.param_dict

    def get_parameter_string(self):
        return self.param_string


class soap(object):
    """soap descriptor
    descriptor class takes paramters and converts them to a dictionary, which
    is then used by the GAPModel to initialise its paramters. """

    def __init__(self, l_max, n_max, atom_sigma, cutoff,
                 radial_scaling, cutoff_transition_width,
                 central_weight, n_sparse, delta, covariance_type, zeta,
                 sparse_method):
        self.l_max = l_max
        self.n_max = n_max
        self.atom_sigma = atom_sigma
        self.cutoff = cutoff
        self.radial_scaling = radial_scaling
        self.cutoff_transition_width = cutoff_transition_width
        self.central_weight = central_weight
        self.n_sparse = n_sparse
        self.delta = delta
        self.covariance_type = covariance_type
        self.zeta = zeta
        self.sparse_method = sparse_method

        p = {'l_max': self.l_max,
             'n_max': self.n_max,
             'atom_sigma': self.atom_sigma,
             'cutoff': self.cutoff,
             'radial_scaling': self.radial_scaling,
             'cutoff_transition_width': self.cutoff_transition_width,
             'central_weight': self.central_weight,
             'n_sparse': self.n_sparse,
             'delta': self.delta,
             'covariance_type': self.covariance_type,
             'zeta': self.zeta,
             'sparse_method': self.sparse_method}
        self.param_dict = p

        param_string = (f" soap l_max = {p['l_max']}"
                        f" n_max = {p['n_max']}"
                        f" atom_sigma = {p['atom_sigma']}"
                        f" cutoff = {p['cutoff']}"
                        f" radial_scaling = {p['radial_scaling']}"
                        f" cutoff_transition_width = {p['cutoff_transition_width']}"
                        f" central_weight = {p['central_weight']}"
                        f" n_sparse = {p['n_sparse']}"
                        f" delta = {p['delta']}"
                        f" covariance_type = {p['covariance_type']}"
                        f" zeta = {p['zeta']}"
                        f" sparse_method = {p['sparse_method']}")

        print(param_string)

        self.param_string = param_string

        descriptor_type = 'soap'
        self.descriptor_type = descriptor_type

    def get_descriptor_type(self):
        return self.descriptor_type

    def get_parameter_dict(self):
        return self.param_dict

    def get_parameter_string(self):
        return self.param_string
