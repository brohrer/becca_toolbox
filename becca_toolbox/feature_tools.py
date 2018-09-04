"""
Some convenient functions for pulling out informtion about Becca features.
"""

import numpy as np


def get_feature_set(brain):
    """
    Get a representation of all the features learned by a Brain.

    At each level in a Brain, sequences are created and passed to the next
    level up to be used as inputs. These higher level representations of the
    inputs provide valuable insights into a brain's behavior and operation.
    This function returns a representation of each sequence in terms of the
    Brains most primitive sensor inputs.

    Parameters
    ----------
    brain : Brain
        The instance of Brain to extract features from.

    Returns
    -------
    feature_set : list of list of array
        A representation of all features at all levels.
    """
    def expand(brain, features_to_expand, i_level):
        """
        Parameters
        ----------
        brain : Brain
            The brain to use for expanding the features.
        features_to_expand : list of arrays of floats
            Expand each array in the list into the sequence of inputs
            that contribute to its activity.
        i_level : int
            The index of the level to be expanded.

        Returns
        -------
        expanded_features : list of arrays of floats
            The set of inputs to this level that maximally activate the
            features_to_expand. A 1 represents a relevant input,
            0 is irrelevant.
        """
        # When you reach the bottom of the hierarchy of levels, stop.
        if i_level == -1:
            return features_to_expand
        # Expand inputs for this level
        expanded_features = brain.levels[i_level].expand(features_to_expand)
        # and for all lower levels.
        expanded_features = expand(brain, expanded_features, i_level - 1)
        return expanded_features

    # Iterate up through each level
    feature_set = []
    for i_level, level in enumerate(brain.levels):
        # and then through the output features in each level.
        level_features = []
        for i_feature in range(level.num_sequences):
            # Expand the features one at a time. Represent each using
            # a one-hot feature array.
            feature_to_expand = np.zeros(level.max_num_inputs)
            feature_to_expand[i_feature] = 1.
            features_to_expand = [feature_to_expand]
            expanded_feature = expand(brain, features_to_expand, i_level)
            level_features.append(expanded_feature)
        feature_set.append(level_features)
    return feature_set
