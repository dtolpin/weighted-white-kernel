import pytest
import numpy as np
from sklearn.gaussian_process.kernels import  _approx_fprime
from sklearn.utils.testing import assert_equal, assert_almost_equal
from dtolpin.gaussian_process.kernels import WeightedWhiteKernel


def test_weighted_white_kernel_gradient():
    # Compare analytic and numeric gradient of the kernel:
    N = 3
    X = np.random.RandomState(0).normal(0, 1, (N, 1))
    weight = np.exp(np.random.RandomState(0).normal(0, 1, N))
    kernel = WeightedWhiteKernel(noise_weight=1./weight, noise_level=0.1)
    K, K_gradient = kernel(X, eval_gradient=True)

    assert_equal(K_gradient.shape[0], X.shape[0])
    assert_equal(K_gradient.shape[1], X.shape[0])
    assert_equal(K_gradient.shape[2], kernel.theta.shape[0])

    def eval_kernel_for_theta(theta):
        kernel_clone = kernel.clone_with_theta(theta)
        K = kernel_clone(X, eval_gradient=False)
        return K

    K_gradient_approx = \
        _approx_fprime(kernel.theta, eval_kernel_for_theta, 1e-10)

    assert_almost_equal(K_gradient, K_gradient_approx, 4)
