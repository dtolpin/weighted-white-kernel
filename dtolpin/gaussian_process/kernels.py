import numpy as np
from sklearn.gaussian_process.kernels import (Kernel,
                                              StationaryKernelMixin,
                                              Hyperparameter)


class WeightedWhiteKernel(StationaryKernelMixin, Kernel):
    """Weighted white kernel.

    The main use-case of this kernel is as part of a sum-kernel
    where it explains the noise-component of the signal. Tuning
    its parameter corresponds to estimating the noise-level.

    k(x_1, x_2) = weight(x_1)*noise_level if x_1 == x_2 else 0

    This is a modification of WhiteKernel taking care of the case
    when different observations have different noise levels.

    Parameters
    ----------
    weight : float array, weight vector

    noise_level : float, default: 1.0
        Parameter controlling the noise level

    noise_level_bounds : pair of floats >= 0, default: (1e-5, 1e5)
        The lower and upper bound on noise_level

    """
    def __init__(self, noise_weight,
                 noise_level=1.0, noise_level_bounds=(1e-5, 1e5)):
        self.noise_weight = noise_weight
        self.noise_level = noise_level
        self.noise_level_bounds = noise_level_bounds

    @property
    def hyperparameter_noise_level(self):
        return Hyperparameter(
            "noise_level", "numeric", self.noise_level_bounds)

    def __call__(self, X, Y=None, eval_gradient=False):
        """Return the kernel k(X, Y) and optionally its gradient.

        Parameters
        ----------
        X : array, shape (n_samples_X, n_features)
            Left argument of the returned kernel k(X, Y)

        Y : array, shape (n_samples_Y, n_features), (optional, default=None)
            Right argument of the returned kernel k(X, Y). If None, k(X, X)
            if evaluated instead.

        eval_gradient : bool (optional, default=False)
            Determines whether the gradient with respect to the kernel
            hyperparameter is determined. Only supported when Y is None.

        Returns
        -------
        K : array, shape (n_samples_X, n_samples_Y)
            Kernel k(X, Y)

        K_gradient : array (opt.), shape (n_samples_X, n_samples_X, n_dims)
            The gradient of the kernel k(X, X) with respect to the
            hyperparameter of the kernel. Only returned when eval_gradient
            is True.
        """
        X = np.atleast_2d(X)
        if Y is not None and eval_gradient:
            raise ValueError("Gradient can only be evaluated when Y is None.")

        if Y is None:
            if X.shape[0]!=self.noise_weight.shape[0]:
                raise ValueError("X must have the same length as weight " +
                                 "({:d}!={:d})".format(
                                     X.shape[0], self.noise_weight.shape[0]))
            K = self.noise_level * np.diag(self.noise_weight)
            if eval_gradient:
                if not self.hyperparameter_noise_level.fixed:
                    return (K, self.noise_level
                            * np.diag(self.noise_weight)[:, :, np.newaxis])
                else:
                    return K, np.empty((X.shape[0], X.shape[0], 0))
            else:
                return K
        else:
            return np.zeros((X.shape[0], Y.shape[0]))

    def diag(self, X):
        """Returns the diagonal of the kernel k(X, X).

        This method is called when predicting the variance. The same noise
        variance for all points is returned, equal to the average noise 
        variance over the training set.

        Parameters
        ----------
        X : array, shape (n_samples_X, n_features)
            Left argument of the returned kernel k(X, Y)

        Returns
        -------
        K_diag : array, shape (n_samples_X,)
            Diagonal of kernel k(X, X)
        """
        predicted_weight = 1./(1./self.noise_weight).mean()
        return self.noise_level * np.full(X.shape[0], predicted_weight)

    def __repr__(self):
        return "{0}(noise_level={1:.3g})".format(self.__class__.__name__,
                                                 self.noise_level)
