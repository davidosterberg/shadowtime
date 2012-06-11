import unittest

import shadowtime
from pylab import *

class test_shadowtime(unittest.TestCase):

    """

    A test class for the shadowtime module.

    """


    def test_transform_1(self):
        """Check that certain points transform as they should"""
        phi = 0.
        delta = 0.
        h = 0.
        xyz = shadowtime.Geographical_to_Earth_Cartesian(phi,delta,h)
        self.assertTrue( norm(xyz - matrix([[shadowtime.R],[0],[0]])) < 1e-5 )

    def test_transform_2(self):
        """Check that certain points transform as they should"""
        phi = pi
        delta = 0.
        h = 0.
        xyz = shadowtime.Geographical_to_Earth_Cartesian(phi,delta,h)
        self.assertTrue( norm(xyz - matrix([[-shadowtime.R],[0],[0]])) < 1e-5 )

    def test_transform_3(self):
        """Check that certain points transform as they should"""
        phi = -pi
        delta = 0.
        h = 0.
        xyz = shadowtime.Geographical_to_Earth_Cartesian(phi,delta,h)
        self.assertTrue( norm(xyz - matrix([[-shadowtime.R],[0],[0]])) < 1e-5 )

    def test_transform_4(self):
        """Check that certain points transform as they should"""
        phi = 0
        delta = pi/2
        h = 0.
        xyz = shadowtime.Geographical_to_Earth_Cartesian(phi,delta,h)
        self.assertTrue( norm(xyz - matrix([[0],[0],[shadowtime.R]])) < 1e-5 )

    def test_transform_5(self):
        """Check that certain points transform as they should"""
        phi = pi/2
        delta = pi/2
        h = 0.
        xyz = shadowtime.Geographical_to_Earth_Cartesian(phi,delta,h)
        self.assertTrue( norm(xyz - matrix([[0],[0],[shadowtime.R]])) < 1e-5 )



    def test_transform_6(self):
        """Check that geographic to earth cartesian transform inverse is really the inverse"""
        phi = 15./180*pi
        delta = 60./180*pi
        h = 50
        t = 10.2
        xyz = shadowtime.Geographical_to_Earth_Cartesian(phi,delta,h)
        phi2,delta2,h2 = shadowtime.Earth_Cartesian_to_Geographical(xyz)
        self.assertTrue(norm([phi-phi2,delta-delta2,h-h2]) < 1e-5)

    def test_transform_7(self):
        """Check to see that the norm is conserved"""
        ptest = shadowtime.R*matrix([[0.7],[0.5],[0.6]])
        phi,delta,h = shadowtime.Universal_to_Geographical(ptest,0.1)
        self.assertTrue(norm(shadowtime.R + h - norm(ptest)) < 1e-5)

    def test_transform_8(self):
        """Check that complete transform inverse is really the inverse"""
        phi = 15./180*pi
        delta = 60./180*pi
        h = 50
        t = 10.2
        pXYZ = shadowtime.Geographical_to_Universal(phi,delta,h,t)
        phi2,delta2,h2 = shadowtime.Universal_to_Geographical(pXYZ,t)
        errors = array([phi-phi2,delta-delta2,h-h2])
        self.assertTrue(norm(errors) < 1e-5)

    def test_transform_9(self):
        """Check that complete transform inverse is really the inverse"""
        phi = -180./180*pi
        delta = 0./180*pi
        h = 50
        t = 0
        pXYZ = shadowtime.Geographical_to_Universal(phi,delta,h,t)
        phi2,delta2,h2 = shadowtime.Universal_to_Geographical(pXYZ,t)
        errors = array([phi-phi2,delta-delta2,h-h2])
        self.assertTrue(norm(errors) < 1e-5)


if __name__ == '__main__':
    unittest.main()
