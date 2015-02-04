import numpy as np
from .geometry import unitize

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

def random_sample(mesh, count):
    '''
    Sample the surface of a mesh, returning the specified number of points
    
    (From our email list):
    1. Sample a triangle proportional to surface area. 
       This assumes your mesh is representative of the surface, 
       so no weirdness like long thin triangles.
    2. Sample uniformly from the barycentric coordinates of the triangle. 
       This works for any simplex.
       
    Arguments
    ---------
    mesh: Trimesh object
    count: number of points to samples
    
    Returns
    ---------
    samples: (count,3) points in space, on the surface of mesh
       
       
    '''
    # will return a list of the areas of each face of the mesh
    area     = mesh.area(sum=False)
    # total area (float)
    area_sum = np.sum(area)
    # cumulative area (len(mesh.faces))
    area_cum = np.cumsum(area)
    
    # create a set of sample areas between 0 and the area_sum
    area_sample = np.random.random(count) * area_sum
    # find the face index which is in that area slot
    # this works because area_cum is sorted, and searchsorted
    # returns the index where area_sample that would need to be inserted
    # to maintain the sort on area_cum
    face_index  = np.searchsorted(area_cum, area_sample)

    triangles   = mesh.vertices[mesh.faces[face_index]]
    barycentric = unitize(np.random.random((count, 3))).reshape((-1,3,1))
    
    samples = np.sum(triangles * barycentric, axis=1)
    return samples
