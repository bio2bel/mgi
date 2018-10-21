# -*- coding: utf-8 -*-

from bio2bel.downloading import make_df_getter

from ..constants import MARKERS_PATH, MARKERS_URL

__all__ = [
    'get_marker_df',
]

get_marker_df = make_df_getter(
    MARKERS_URL,
    MARKERS_PATH,
    sep='\t',
    usecols=[
        0,  # MGI ID
        6,  # SYMBOL
        8,  # name
        9,  # marker type
        10,  # feature type
    ],
    names=[
        'mgi_id',
        'symbol',
        'name',
        'marker_type',
        'feature_type',
    ],
    skiprows=[0],
)
