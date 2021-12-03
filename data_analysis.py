"""
Project Name: Life Beyond Earth
Designed By:
    1. Saahil Hiranandani
    2. Manasi Karale
Description:
    Life beyond the Earth has always been a fascinating quest for scientists. Roughly 12% out of an approximate 5000
    exoplanets have been found to be in the “habitable zone [1]” in our observed universe, yet there exists a question
    on whether these planets could actually host life. At the same time, there are organisms on earth –
    the extremophiles, that can survive under extreme conditions these exoplanets [2] have to offer.
    Our study analyzes these planets and examines the survival rate of extremophiles [3] on these planets.

Pre-requisite Installations:
    1. Install these libraries in your cloned project via PyCharm:
        1. pandas

Acceptable Input:
    1. phl_exoplanet_catalog.csv - data store of 4048 observable exoplanets

Acceptable Output:
    1. Hypothesis 1 - TRUE or FALSE
    2. Hypothesis 2 - TRUE or FALSE
    3. Various visualizations

Direction to run the program:
    1. Ensure 'phl_exoplanet_catalog.csv' in the 'data' folder.
    2. Run the main method in 'data_analysis.py' file to perform the analysis and derive the result for hypothesis.
    3. Run each cell in the 'visualizations.ipynb' file to visualize the hypothesis.

Time taken to run the program:
    .
    .
    .

Database References:
    1. [1] - Exoplanets catalog:
    https://phl.upr.edu/projects/habitable-exoplanets-catalog/data/database
    For any questions on the units and meaning of column refer to the planets_metadata.txt file
    2. [2] - Extremophiles range
Code References:
    1. []
Research References:
    1. [3] - ESI Calculation:
    https://www.liebertpub.com/doi/pdfplus/10.1089/ast.2010.0592?casa_token=ThEocKPBuRgAAAAA:BI1329Vwl7j0_zO7qtkLeHVp5-WPIBMlqypxHfVM1y7byLyj1RL2NuelTFga4t7VtTl_DvzNaFtwliqR
    2. [4] - ESI Reference Values and Weight Exponent constants:
    https://phl.upr.edu/projects/earth-similarity-index-esi
"""
# TODO: Code polishing required


import pandas as pd
import constants as c
import pandasql as ps


def create_exoplanets_catalog(file_name) -> pd.DataFrame:
    """
    Read from phl_exoplanet_catalog.csv file and create a dataframe with required columns.

    :param file_name: given a file name read required columns and store and return the data in pandas dataframe.
    :return: a dataframe with required columns.
    >>> create_exoplanets_catalog(".\\data\\phl_exoplanet_catalog.csv")
    ... # doctest: +NORMALIZE_WHITESPACE
              P_NAME      P_MASS  P_RADIUS  ...  P_HABITABLE P_RADIUS_EST   P_MASS_EST
    0       11 Com b  6165.86330      0.00  ...            0    12.082709  6165.863300
    1       11 UMi b  4684.78480      0.00  ...            0    12.229641  4684.784800
    2       14 And b  1525.57440      0.00  ...            0    12.848516  1525.574400
    3       14 Her b  1481.07850      0.00  ...            0    12.865261  1481.078500
    4     16 Cyg B b   565.73385      0.00  ...            0    13.421749   565.733850
    ...          ...         ...       ...  ...          ...          ...          ...
    4043    K2-296 b     0.00000      1.87  ...            2     1.870000     4.155456
    4044    K2-296 c     0.00000      2.76  ...            0     2.760000     8.047485
    4045   GJ 1061 b     1.38000      0.00  ...            0     1.102775     1.380000
    4046   GJ 1061 c     1.75000      0.00  ...            1     1.178333     1.750000
    4047   GJ 1061 d     1.68000      0.00  ...            1     1.164989     1.680000
    <BLANKLINE>
    [4048 rows x 19 columns]
    """
    required_columns = ['P_NAME', 'P_MASS', 'P_RADIUS', 'P_TEMP_MEASURED', 'P_ESCAPE', 'P_DENSITY', 'P_DISTANCE',
                        'P_FLUX', 'P_TEMP_EQUIL', 'P_TEMP_EQUIL_MIN', 'P_TEMP_EQUIL_MAX',
                        'S_NAME', 'S_HZ_OPT_MIN', 'S_HZ_OPT_MAX', 'S_HZ_CON_MIN', 'S_HZ_CON_MAX',
                        'P_HABITABLE', 'P_RADIUS_EST', 'P_MASS_EST']
    # load data file with columns required for our analysis into data frame
    exoplanets_catalog = pd.read_csv(
        # input file name (change here if need be)
        file_name,
        # read only required columns
        usecols=lambda column_name: column_name in required_columns
    )
    exoplanets_catalog = exoplanets_catalog.fillna(0)
    return exoplanets_catalog


def calculate_ESI(exoplanets: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the ESI on basis of 4 planetary properties.
    :param exoplanets: required dataframe from which we use values to calculate our own ESI.
    :return: same input dataframe with an additional column of calculated_ESI.
    >>> calculate_ESI(create_exoplanets_catalog(".\\data\\phl_exoplanet_catalog.csv"))
              P_NAME      P_MASS  ...   P_MASS_EST  P_calculated_ESI
    0       11 Com b  6165.86330  ...  6165.863300               0.0
    1       11 UMi b  4684.78480  ...  4684.784800               0.0
    2       14 And b  1525.57440  ...  1525.574400               0.0
    3       14 Her b  1481.07850  ...  1481.078500               0.0
    4     16 Cyg B b   565.73385  ...   565.733850               0.0
    ...          ...         ...  ...          ...               ...
    4043    K2-296 b     0.00000  ...     4.155456               0.0
    4044    K2-296 c     0.00000  ...     8.047485               0.0
    4045   GJ 1061 b     1.38000  ...     1.380000               0.0
    4046   GJ 1061 c     1.75000  ...     1.750000               0.0
    4047   GJ 1061 d     1.68000  ...     1.680000               0.0
    <BLANKLINE>
    [4048 rows x 20 columns]
    """
    # Subset the dataframe to required columns
    ESI_fields_exoplanet_details = exoplanets[['P_RADIUS', 'P_DENSITY', 'P_ESCAPE', 'P_TEMP_EQUIL']]
    # Reference data of earth used as terrestrial reference values
    terrestrial_reference_value = [c.REFERENCE_VALUE_RADIUS, c.REFERENCE_VALUE_DENSITY,
                                   c.REFERENCE_VALUE_VELOCITY, c.REFERENCE_VALUE_TEMPERATURE]
    # Weight exponents for the respective planetary properties
    weight_exponent = [c.WEIGHT_EXPONENT_RADIUS, c.WEIGHT_EXPONENT_DENSITY,
                       c.WEIGHT_EXPONENT_VELOCITY, c.WEIGHT_EXPONENT_TEMPERATURE]
    n = c.NUMBER_OF_PARAMETERS_TO_CALCULATE_ESI
    P_ESI = []
    # Calculate ESI for each planet
    for each_row in range(0, ESI_fields_exoplanet_details.shape[0]):
        earth_similarity_index = 1
        for each_parameter in range(1, ESI_fields_exoplanet_details.shape[1]):
            xi = float(ESI_fields_exoplanet_details.iloc[each_row][each_parameter])
            xio = terrestrial_reference_value[each_parameter]
            wi = weight_exponent[each_parameter]
            # [3]
            earth_similarity_index *= (1 - abs((xi - xio) / (xi + xio))) ** wi
        earth_similarity_index = earth_similarity_index ** (1 / n)
        # Calculated Earth similarity index appended to final dataframe
        P_ESI.append(earth_similarity_index)
    exoplanets['P_calculated_ESI'] = P_ESI
    return exoplanets


def get_habitable_zone_planets(exoplanets: pd.DataFrame) -> pd.DataFrame:
    """
    Returns list of exoplanets that fall in the habitable zone.
    :param exoplanets: same input dataframe with filtered exoplanets.
    :return:
    >>> get_potentially_habitable_exoplanets(calculate_ESI(create_exoplanets_catalog(".\\data\\phl_exoplanet_catalog.csv")))
                P_NAME       P_MASS  ...   P_MASS_EST  P_calculated_ESI
    135       GJ 143 b    22.699276  ...    22.699276          0.687067
    157       GJ 357 b     1.840224  ...     1.840224          0.654383
    830     HD 80606 b  1392.086700  ...  1392.086700          0.636489
    981       K2-146 c     7.494384  ...     7.494384          0.617501
    1029       K2-18 b     8.921432  ...     8.921432          0.813958
    1146      K2-263 b    14.801250  ...    14.801250          0.663082
    1153      K2-266 e    14.299082  ...    14.299082          0.619196
    1179      K2-285 e    10.701269  ...    10.701269          0.603094
    1337    KOI-3680 b   613.408050  ...   613.408050          0.607695
    1489   Kepler-11 g    25.108412  ...    25.108412          0.694571
    1850  Kepler-138 b     0.066744  ...     0.066744          0.601465
    1851  Kepler-138 c     1.970534  ...     1.970534          0.791120
    1852  Kepler-138 d     0.638834  ...     0.638834          0.768840
    2310   Kepler-20 d    10.068791  ...    10.068791          0.651218
    2488   Kepler-26 c     6.200824  ...     6.200824          0.641576
    2890  Kepler-413 b    67.061709  ...    67.061709          0.793707
    2986   Kepler-48 d     7.945700  ...     7.945700          0.653588
    3066  Kepler-539 b   308.293160  ...   308.293160          0.628438
    3663    LHS 1140 b     6.979503  ...     6.979503          0.708638
    3664    LHS 1140 c     1.808441  ...     1.808441          0.761213
    3667  LTT 1445 A b     2.199370  ...     2.199370          0.748333
    3806  TRAPPIST-1 b     0.848601  ...     0.848601          0.771585
    3807  TRAPPIST-1 c     1.379374  ...     1.379374          0.902225
    3808  TRAPPIST-1 d     0.409998  ...     0.409998          0.903853
    3809  TRAPPIST-1 e     0.619765  ...     0.619765          0.813324
    3810  TRAPPIST-1 f     0.680152  ...     0.680152          0.695922
    3811  TRAPPIST-1 g     1.341234  ...     1.341234          0.693644
    <BLANKLINE>
    [27 rows x 20 columns]
    """
    return exoplanets.loc[(exoplanets['P_HABITABLE'] == 1) | (exoplanets['P_HABITABLE'] == 2)]


def get_potentially_habitable_exoplanets(exoplanets: pd.DataFrame) -> pd.DataFrame:
    """
    Filter exoplanets with ESI >= 0.6
    :param exoplanets: required dataframe with calculated ESI.
    :return: same input dataframe with filtered exoplanets.
    >>> get_potentially_habitable_exoplanets(calculate_ESI(create_exoplanets_catalog(".\\data\\phl_exoplanet_catalog.csv")))
                P_NAME       P_MASS  ...   P_MASS_EST  P_calculated_ESI
    135       GJ 143 b    22.699276  ...    22.699276          0.687067
    157       GJ 357 b     1.840224  ...     1.840224          0.654383
    830     HD 80606 b  1392.086700  ...  1392.086700          0.636489
    981       K2-146 c     7.494384  ...     7.494384          0.617501
    1029       K2-18 b     8.921432  ...     8.921432          0.813958
    1146      K2-263 b    14.801250  ...    14.801250          0.663082
    1153      K2-266 e    14.299082  ...    14.299082          0.619196
    1179      K2-285 e    10.701269  ...    10.701269          0.603094
    1337    KOI-3680 b   613.408050  ...   613.408050          0.607695
    1489   Kepler-11 g    25.108412  ...    25.108412          0.694571
    1850  Kepler-138 b     0.066744  ...     0.066744          0.601465
    1851  Kepler-138 c     1.970534  ...     1.970534          0.791120
    1852  Kepler-138 d     0.638834  ...     0.638834          0.768840
    2310   Kepler-20 d    10.068791  ...    10.068791          0.651218
    2488   Kepler-26 c     6.200824  ...     6.200824          0.641576
    2890  Kepler-413 b    67.061709  ...    67.061709          0.793707
    2986   Kepler-48 d     7.945700  ...     7.945700          0.653588
    3066  Kepler-539 b   308.293160  ...   308.293160          0.628438
    3663    LHS 1140 b     6.979503  ...     6.979503          0.708638
    3664    LHS 1140 c     1.808441  ...     1.808441          0.761213
    3667  LTT 1445 A b     2.199370  ...     2.199370          0.748333
    3806  TRAPPIST-1 b     0.848601  ...     0.848601          0.771585
    3807  TRAPPIST-1 c     1.379374  ...     1.379374          0.902225
    3808  TRAPPIST-1 d     0.409998  ...     0.409998          0.903853
    3809  TRAPPIST-1 e     0.619765  ...     0.619765          0.813324
    3810  TRAPPIST-1 f     0.680152  ...     0.680152          0.695922
    3811  TRAPPIST-1 g     1.341234  ...     1.341234          0.693644
    <BLANKLINE>
    [27 rows x 20 columns]
    """
    return exoplanets.loc[(exoplanets['P_calculated_ESI'] >= 0.6)]


def identify_habitability_type(exoplanets: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    """
    Distinguish between the two types
    :param exoplanets:
    :return:
    >>> df = calculate_ESI(create_exoplanets_catalog(".\\data\\phl_exoplanet_catalog.csv"))
    >>> p_df = df.loc[(df['P_calculated_ESI'] >= 0.6)]
    >>> identify_habitability_type(p_df)
    (            P_NAME  P_RADIUS_EST  P_MASS_EST  P_calculated_ESI
    157       GJ 357 b       1.22189    1.840224          0.654383
    1850  Kepler-138 b       0.52687    0.066744          0.601465
    1851  Kepler-138 c       1.19947    1.970534          0.791120
    1852  Kepler-138 d       1.21068    0.638834          0.768840
    3664    LHS 1140 c       1.27794    1.808441          0.761213
    3667  LTT 1445 A b       1.37883    2.199370          0.748333
    3806  TRAPPIST-1 b       1.08737    0.848601          0.771585
    3807  TRAPPIST-1 c       1.05374    1.379374          0.902225
    3808  TRAPPIST-1 d       0.77349    0.409998          0.903853
    3809  TRAPPIST-1 e       0.91922    0.619765          0.813324
    3810  TRAPPIST-1 f       1.04253    0.680152          0.695922
    3811  TRAPPIST-1 g       1.13221    1.341234          0.693644,            P_NAME  P_RADIUS_EST  P_MASS_EST  P_calculated_ESI
    981      K2-146 c       2.18595    7.494384          0.617501
    1029      K2-18 b       2.36531    8.921432          0.813958
    1146     K2-263 b       2.41015   14.801250          0.663082
    1179     K2-285 e       1.95054   10.701269          0.603094
    2488  Kepler-26 c       2.72403    6.200824          0.641576
    2986  Kepler-48 d       2.04022    7.945700          0.653588
    3663   LHS 1140 b       1.72634    6.979503          0.708638)
    """
    habitability_details = exoplanets[['P_NAME', 'P_RADIUS_EST', 'P_MASS_EST', 'P_calculated_ESI']]
    conservative_habitable_planets = habitability_details.loc[
        ((0.5 < (round(habitability_details['P_RADIUS_EST'], 2)))
         & (round(habitability_details['P_RADIUS_EST'], 2) <= 1.5))
        |
        ((0.1 < (round(habitability_details['P_MASS_EST'], 2)))
         & (round(habitability_details['P_MASS_EST'], 2) <= 5.0))
        ]
    optimistic_habitable_planets = habitability_details.loc[
        ((1.5 < (round(habitability_details['P_RADIUS_EST'], 2)))
         & (round(habitability_details['P_RADIUS_EST'], 2) <= 2.5))
        |
        ((5.1 < (round(habitability_details['P_MASS_EST'], 2)))
         & (round(habitability_details['P_MASS_EST'], 2) <= 10.0))
        ]
    return conservative_habitable_planets, optimistic_habitable_planets


def identifying_surviving_extremophiles(extremophiles_csv, potentially_habitable_exoplanets_local):
    """
    Identifies Extremophiles that can survive on Potentially Habitable Exoplanets.
    :param potentially_habitable_exoplanets_local: A dataframe containing all potentially habitable planets.
    :param extremophiles_csv: A CSV
    file containing information such as temperature, pressure, and radiation in which an Extremophile can survive.
    :return temperature_surviving_extremophiles: All extremophiles that can survive based on the temperature of the
    planet
    :return temperature_surviving_extremophiles: All extremophiles that can survive based on the surface pressure
    of the planet
    :return temperature_surviving_extremophiles: All extremophiles that can survive based on
    the UV radiation of the planet
    >>> exoplanets = calculate_ESI(create_exoplanets_catalog(".\\data\\phl_exoplanet_catalog.csv"))
    >>> habitable_exoplanets = exoplanets.loc[(exoplanets['P_calculated_ESI'] >= 0.6)]
    >>> identifying_surviving_extremophiles(".\\data\\Extremophiles Range.csv", habitable_exoplanets)
    ... # doctest: +NORMALIZE_WHITESPACE
    (                                                                                     P_NAME
    Strain
    "Geothermobacterium terrireducens" FW-1a               HD 80606 b, KOI-3680 b, Kepler-539 b
    AcUnopolysporarighensis H23                            HD 80606 b, KOI-3680 b, Kepler-413 b
    Acid/anus in/emus So4a                                 HD 80606 b, KOI-3680 b, Kepler-539 b
    Anoxybacillus pushchinensis K1                         HD 80606 b, KOI-3680 b, Kepler-539 b
    C,yomyces antarcticus MA5682                                       LHS 1140 b, TRAPPIST-1 f
    Colwell/a piezophila ATCC BAA-637                                       HD 80606 b, K2-18 b
    Colwell/a sp.MT-41                                        HD 80606 b, K2-18 b, TRAPPIST-1 d
    Deinococcus geothermalis DSM 11300                     HD 80606 b, KOI-3680 b, Kepler-539 b
    Deinococcus radiodurans Rl                                         LHS 1140 b, TRAPPIST-1 f
    Halarsenatrbacter silvermanii SLAS-1                   HD 80606 b, KOI-3680 b, Kepler-539 b
    Halobacterium salinarum NRC-1             HD 80606 b, KOI-3680 b, Kepler-413 b, Kepler-5...
    Halomonas campisalis MCM B-365                                                   HD 80606 b
    Methanopyrus kandleri 116                 GJ 143 b, HD 80606 b, KOI-3680 b, Kepler-11 g,...
    Oceanobacillus iheyensis HTE831                                      HD 80606 b, KOI-3680 b
    Pedobacter arcticus A12                                                          HD 80606 b
    Picrophrius oshimae KAW 2/2                            HD 80606 b, KOI-3680 b, Kepler-539 b
    Serpentinomonas sp. 81                                 HD 80606 b, KOI-3680 b, Kepler-413 b
    Shewane/18 piezotOlerans\\r\\nWP3                                                  HD 80606 b
    Thermococcus gammatolerans EJ3                         HD 80606 b, KOI-3680 b, Kepler-539 b
    Thermoooccus piazophilus COGS                          HD 80606 b, KOI-3680 b, Kepler-539 b,                                                                               P_NAME
    Strain
    Colwell/a piezophila ATCC BAA-637  GJ 143 b, GJ 357 b, HD 80606 b, K2-146 c, K2-1...
    Colwell/a sp.MT-41                 GJ 143 b, GJ 357 b, HD 80606 b, K2-146 c, K2-1...
    Methanopyrus kandleri 116          GJ 357 b, K2-146 c, K2-18 b, K2-263 b, K2-266 ...
    Oceanobacillus iheyensis HTE831    Kepler-138 b, Kepler-138 d, Kepler-20 d, Keple...
    Shewane/18 piezotOlerans\\r\\nWP3    Kepler-138 b, Kepler-138 d, Kepler-20 d, Keple...
    Thermoooccus piazophilus COGS      Kepler-138 b, Kepler-138 d, Kepler-20 d, Keple...,                                                                            P_NAME
    Strain
    Deinococcus radiodurans Rl      K2-18 b, Kepler-138 d, Kepler-413 b, LHS 1140 ...
    Halobacterium salinarum NRC-1   K2-18 b, Kepler-138 d, Kepler-413 b, LHS 1140 ...
    Thermococcus gammatolerans EJ3  K2-18 b, Kepler-138 d, Kepler-413 b, LHS 1140 ...)
    """

    converted_units_df = pd.DataFrame()

    converted_units_df['P_NAME'] = potentially_habitable_exoplanets_local['P_NAME']
    converted_units_df['S_NAME'] = potentially_habitable_exoplanets_local['S_NAME']
    converted_units_df.loc[:, 'P_MASS'] = potentially_habitable_exoplanets_local['P_MASS'] * c.MASS
    converted_units_df.loc[:, 'P_RADIUS'] = potentially_habitable_exoplanets_local['P_RADIUS'] * (c.DIAMETER / 2)
    converted_units_df.loc[:, 'P_DENSITY'] = potentially_habitable_exoplanets_local['P_DENSITY'] * c.DENSITY
    converted_units_df.loc[:, 'P_FLUX'] = potentially_habitable_exoplanets_local['P_FLUX'] * c.SOLAR_FLUX
    converted_units_df.loc[:, 'P_TEMP_EQUIL_MIN'] = potentially_habitable_exoplanets_local['P_TEMP_EQUIL_MIN']
    converted_units_df.loc[:, 'P_TEMP_EQUIL_MAX'] = potentially_habitable_exoplanets_local['P_TEMP_EQUIL_MAX']

    converted_units_df['P_PRESSURE'] = calculate_pressure(converted_units_df['P_DENSITY'],
                                                          converted_units_df['P_MASS'],
                                                          converted_units_df['P_RADIUS'])
    converted_units_df = converted_units_df.set_index('P_NAME')

    extremophiles_df = pd.DataFrame(pd.read_csv(extremophiles_csv,
                                                usecols=['Strain', 'Extremophile_Type', 'Temperature_Min_K',
                                                         'Temperature_Max_K', 'Pressure_Min_Bars', 'Pressure_Max_Bars',
                                                         'Radiation']))
    extremophiles_df = extremophiles_df.fillna(0)
    temperature_surviving_extremophiles = ps.sqldf(
        "Select converted_units_df.P_NAME , extremophiles_df.Strain "
        "from extremophiles_df left outer join converted_units_df "
        "where extremophiles_df.Temperature_Min_K >= converted_units_df.P_TEMP_EQUIL_MIN "
        "and extremophiles_df.Temperature_Max_K <= converted_units_df.P_TEMP_EQUIL_MAX")

    temperature_surviving_extremophiles = temperature_surviving_extremophiles.groupby('Strain').agg(
        {'P_NAME': lambda x: ', '.join(x)})

    pressure_surviving_extremophiles = ps.sqldf(
        "Select converted_units_df.P_NAME , extremophiles_df.Strain "
        "from extremophiles_df left outer join converted_units_df "
        "where extremophiles_df.Pressure_Min_Bars >= converted_units_df.P_PRESSURE")
    pressure_surviving_extremophiles = pressure_surviving_extremophiles.groupby('Strain').agg(
        {'P_NAME': lambda x: ', '.join(x)})

    radiation_surviving_extremophiles = ps.sqldf(
        "Select converted_units_df.P_NAME , extremophiles_df.Strain "
        "from extremophiles_df left outer join converted_units_df "
        "where extremophiles_df.Radiation >= converted_units_df.P_FLUX")
    radiation_surviving_extremophiles = radiation_surviving_extremophiles.groupby('Strain').agg(
        {'P_NAME': lambda x: ', '.join(x)})

    return temperature_surviving_extremophiles, pressure_surviving_extremophiles, radiation_surviving_extremophiles


def calculate_pressure(density, mass, radius):
    """
    Calulates Pressure based on Pascal's Pressure Principle
    # Source https://www.physicsforums.com/threads/pressure-at-center-of-planet.66257/
    :param density: Density of the planet in kg/m^3
    :param mass: Mass of the planet in kg
    :param radius: Radius of the planet in Meters
    :return: Pressure in Bars
    >>> calculate_pressure(c.DENSITY, c.MASS, (c.DIAMETER / 2))
    1.0812762002812073
    """

    depth = 2  # Since we want surface pressure
    g = (c.G * mass) / (radius ** 2)
    pressure = density * g * depth  # According to Pascal's Pressure Principle
    return pressure * (10 ** -5)


if __name__ == '__main__':
    # [1]
    all_exoplanets_with_esi = calculate_ESI(create_exoplanets_catalog(".\\data\\phl_exoplanet_catalog.csv"))
    planets_in_habitable_zone = get_habitable_zone_planets(all_exoplanets_with_esi)
    print(planets_in_habitable_zone)
    potentially_habitable_exoplanets = get_potentially_habitable_exoplanets(all_exoplanets_with_esi)
    print(potentially_habitable_exoplanets)
    print(identify_habitability_type(planets_in_habitable_zone))
    print(identifying_surviving_extremophiles(".\\data\\Extremophiles Range.csv", potentially_habitable_exoplanets))
