#   Maximum attenuation pass band/Minimum attenuation stop band
def MAPSB(results, pass_band, stop_band):
    # Normalize the output to the low frequency value and convert to array
    norm_out = numpy.asarray(results['|Vn4|'].T/results['|Vn4|'].max())
    
    # Convert to dB
    norm_out_db = 20 * numpy.log10(norm_out)
    
    # Reshape to be scipy-friendly
    norm_out_db = norm_out_db.reshape((max(norm_out_db.shape),))
    
    # Convert angular frequencies to Hz and convert matrix to array
    frequencies = numpy.asarray(results['w'].T/2/math.pi)
    
    # Reshape to be scipy-friendly
    frequencies = frequencies.reshape((max(frequencies.shape),))
    
    # call scipy to interpolate
    norm_out_db_interpolated = scipy.interpolate.interp1d(frequencies, norm_out_db)

    return (-1.0*norm_out_db_interpolated(pass_band), -1.0*norm_out_db_interpolated(stop_band))