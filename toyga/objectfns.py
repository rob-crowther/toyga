# objectfns.py
# Module meant to contain objective functions for sample evaluation and
# comparison
from warnings import warn
import numpy
import scipy

def MAPSB(results, label, pass_band, stop_band):
    """Maximum attenuation pass band/Minimum attenuation stop band"""
    if label[0] != label[-1] != '|':
        label = "|" + label + "|"
    if not label in results.keys():
        warn("The simulated circuit does not contain the output node.")

    # Normalize the output to the low frequency value
    norm_out = results[label] / results[label].max()

    # Convert to dB
    norm_out_db = 20 * numpy.log10(norm_out)

    # Reshape to be scipy-friendly
    norm_out_db = norm_out_db.reshape((max(norm_out_db.shape),))

    # Convert angular frequencies to Hz and convert matrix to array
    frequencies = results['w'] / 2 / numpy.pi

    # Reshape to be scipy-friendly
    frequencies = frequencies.reshape((max(frequencies.shape),))

    # call scipy to interpolate
    norm_out_db_interpolated = scipy.interpolate.interp1d(
        frequencies, norm_out_db)

    return (-1.0 * norm_out_db_interpolated(pass_band), -1.0 * norm_out_db_interpolated(stop_band))
