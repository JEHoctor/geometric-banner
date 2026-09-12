import numpy as np
import numpy.typing as npt
from sklearn import gaussian_process as gp

FloatArray = npt.NDArray[np.float64]


def random_pattern(sample_points: FloatArray) -> FloatArray:
    return np.random.default_rng().random(len(sample_points))


def gaussian_process_pattern(
    sample_points: FloatArray, random_state: np.random.RandomState | None = None
) -> FloatArray:
    if random_state is None:
        random_state = np.random.RandomState()
    kernel = 1.0 * gp.kernels.Matern(length_scale=20.0, length_scale_bounds="fixed")
    gpr = gp.GaussianProcessRegressor(kernel=kernel)
    samples = gpr.sample_y(sample_points, random_state=random_state).flatten()
    samples_min, samples_max = samples.min(), samples.max()
    return (samples - samples_min) / (samples_max - samples_min)
