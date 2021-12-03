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


def create_exoplanets_catalog(file_name) -> pd.DataFrame:
    """
    Read from phl_exoplanet_catalog.csv file and create a dataframe with required columns.

    :param file_name: given a file name read required columns and store and return the data in pandas dataframe.
    :return: a dataframe with required columns.
    >>> create_exoplanets_catalog(".\\data\\phl_exoplanet_catalog.csv")
              P_NAME      P_MASS  P_RADIUS  ...  S_TIDAL_LOCK  P_RADIUS_EST   P_MASS_EST
    0       11 Com b  6165.86330      0.00  ...      0.642400     12.082709  6165.863300
    1       11 UMi b  4684.78480      0.00  ...      0.648683     12.229641  4684.784800
    2       14 And b  1525.57440      0.00  ...      0.600010     12.848516  1525.574400
    3       14 Her b  1481.07850      0.00  ...      0.445415     12.865261  1481.078500
    4     16 Cyg B b   565.73385      0.00  ...      0.473325     13.421749   565.733850
    ...          ...         ...       ...  ...           ...           ...          ...
    4043    K2-296 b     0.00000      1.87  ...      0.000000      1.870000     4.155456
    4044    K2-296 c     0.00000      2.76  ...      0.000000      2.760000     8.047485
    4045   GJ 1061 b     1.38000      0.00  ...      0.244044      1.102775     1.380000
    4046   GJ 1061 c     1.75000      0.00  ...      0.244044      1.178333     1.750000
    4047   GJ 1061 d     1.68000      0.00  ...      0.244044      1.164989     1.680000
    <BLANKLINE>
    [4048 rows x 16 columns]

    """
    required_columns = ['P_NAME', 'P_MASS', 'P_RADIUS', 'P_TEMP_MEASURED', 'P_ESCAPE', 'P_DENSITY', 'P_DISTANCE',
                        'P_FLUX', 'P_TEMP_EQUIL', 'S_HZ_OPT_MIN', 'S_HZ_OPT_MAX', 'S_HZ_CON_MIN', 'S_HZ_CON_MAX',
                        'S_TIDAL_LOCK', 'P_RADIUS_EST', 'P_MASS_EST']
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
    [4048 rows x 17 columns]
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


if __name__ == '__main__':
    # [1]
    exoplanets_catalog_esi = calculate_ESI(create_exoplanets_catalog(".\\data\\phl_exoplanet_catalog.csv"))
    potentially_habitable_exoplanets = exoplanets_catalog_esi.loc[(exoplanets_catalog_esi['P_calculated_ESI'] >= 0.6)]
    print(identify_habitability_type(potentially_habitable_exoplanets))
