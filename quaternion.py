
"""
 * Quaternions and some operations on them.
 * The objects are immutable, i.e. once created, they can not be altered.
 * All methods that return a Quaternion create a new one.
 * 
 * @author ThomasJ 19-08-22 from the Java code by the same author
 *
 """

# Note: The attributes W, X, Y, S DO NOT correspond to any angles or coordinates -
# a quaternion is a compact mathematical object that describes a rotational vector
# in space, and can be used as a coordinate (how to rotate a unit vector).
# You must always use these methods to extract the position and heading from a quaternion
# object - do not use w, x, y, z directly !

def heading(q):
    return rotate(q, {'X': 1.0, 'Y': 0.0, "Z": 0.0})

def rotate(q, v):
    return vector(qmult(qmult(q, quaternion(v)), conjugate(q)))

def quaternion(v):
    q = v.copy()
    q['W'] = 0.0
    return q

def vector(q):
    v={}
    v["X"] = q["X"]
    v["Y"] = q["Y"]
    v["Z"] = q["Z"]
    return v

def conjugate(q):
    qc = q.copy()
    qc["X"] = -q["X"]
    qc["Y"] = -q["Y"]
    qc["Z"] = -q["Z"]
    return qc

def qmult(q1, q2):
    q={}
    q["W"] = q1["W"]*q2["W"]-q1["X"]*q2["X"]-q1["Y"]*q2["Y"]-q1["Z"]*q2["Z"]
    q["X"] = q1["W"]*q2["X"]+q1["X"]*q2["W"]+q1["Y"]*q2["Z"]-q1["Z"]*q2["Y"]
    q["Y"] = q1["W"]*q2["Y"]-q1["X"]*q2["Z"]+q1["Y"]*q2["W"]+q1["Z"]*q2["X"]
    q["Z"] = q1["W"]*q2["Z"]+q1["X"]*q2["Y"]-q1["Y"]*q2["X"]+q1["Z"]*q2["W"]
    return q
