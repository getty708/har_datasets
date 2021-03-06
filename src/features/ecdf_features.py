from os.path import join
from collections import defaultdict

import numpy as np

from src.features.base import FeatureBase

__all__ = [
    'ecdf',
]


class ecdf(FeatureBase):
    def __init__(self, parent, n_components, source_filter):
        super(ecdf, self).__init__(
            name=f'ecdf_{n_components}', parent=parent,
            source_filter=source_filter,
        )

        endpoints = defaultdict(dict)

        self.n_components = n_components

        for key, node in parent.outputs.items():
            self.prepare_outputs(
                endpoints=endpoints,
                key=key + ('ecdf',),
                func=calc_ecdf,
                kwargs=dict(
                    n_components=n_components,
                    index=parent.index['index'],
                    data=node,
                )
            )

        self.assign_outputs(endpoints)


def calc_ecdf(key, index, data, n_components):
    """

    Parameters
    ----------
    key
    index
    data
    n_components

    Returns
    -------

    """

    return np.asarray([ecdf_rep(datum, n_components) for datum in data])


def ecdf_rep(data, components):
    """
    Taken from: https://github.com/nhammerla/ecdfRepresentation/blob/master/python/ecdfRep.py

    Parameters
    ----------
    data
    components

    Returns
    -------

    """

    m = data.mean(0)
    data = np.sort(data, axis=0)
    data = data[np.int32(np.around(np.linspace(0, data.shape[0] - 1, num=components))), :]
    data = data.flatten()
    return np.hstack((data, m))
