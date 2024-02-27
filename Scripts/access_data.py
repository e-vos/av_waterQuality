''' 
Filename: access_data.py
Author: Elliot Vosburgh
Date: 15 February 2024
Description:
    Search and bulk download remote sensing data.
'''

# Imports 

import ee
import numpy as np
import pandas as pd
import geopandas as gpd
import os, shutil
from scipy.stats import norm, gamma, f, chi2


# Define AOI (rough rectangle of RI state boundaries

geoJSON = {
    "type": "FeatureCollection",
    "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            [
              -71.88835080624801,
              41.296253682653344
            ],
            [
              -71.11161288170406,
              41.296253682653344
            ],
            [
              -71.11161288170406,
              42.027062715688885
            ],
            [
              -71.88835080624801,
              42.027062715688885
            ],
            [
              -71.88835080624801,
              41.296253682653344
            ]
          ]
        ],
        "type": "Polygon"
      }
    }
  ]
}

coords = geoJSON['features'][0]['geometry']['coordinates']
aoi = ee.Geometry.Polygon(coords)