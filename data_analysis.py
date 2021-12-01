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
    3. Run each cell in the 'visulaization.ipynb' file to visualize the hypothesis.

Time taken to run the program:
    .
    .
    .

Database References:
    1. [1] - Exoplanets catalog:
    .
    For any questions on the units and meaning of column refer to the planets_metadata.txt file
    2. [2] - Extremophiles range
Code References:
    1. []
Research References:
    1. [3] - ESI Calculation:
    https://phl.upr.edu/projects/earth-similarity-index-esi
"""
import pandas as pd
import constants as c


def create_exoplanets_catalog(file_name):
    required_columns = ['P_NAME', 'P_MASS', 'P_RADIUS', 'P_TEMP_MEASURED', 'P_ESCAPE', 'P_DENSITY', 'P_DISTANCE',
                        'P_FLUX', 'P_TEMP_EQUIL', 'S_HZ_OPT_MIN', 'S_HZ_OPT_MAX', 'S_HZ_CON_MIN', 'S_HZ_CON_MAX',
                        'S_TIDAL_LOCK', 'P_HABITABLE']
    # load data file with columns required for our analysis into data frame
    exoplanets_catalog = pd.read_csv(
        # input file name (change here if need be)
        file_name,
        # read only required columns
        usecols=lambda column_name: column_name in required_columns
    )
    exoplanets_catalog = exoplanets_catalog.fillna(0)
    calculate_ESI(exoplanets_catalog)
    print(exoplanets_catalog)


def calculate_ESI(exoplanets: pd.DataFrame) -> pd.DataFrame:
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
        earth_similarity_index = earth_similarity_index ** (1/n)
        # Calculated Earth similarity index appended to final dataframe
        P_ESI.append(earth_similarity_index)
    exoplanets['P_ESI'] = P_ESI
    return exoplanets


if __name__ == '__main__':
    create_exoplanets_catalog(".\\data\\phl_exoplanet_catalog.csv")
