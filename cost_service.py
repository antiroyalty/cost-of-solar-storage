import step1_identify_suitable_buildings as IdentifySuitableBuildings
import step2_pull_buildings as PullBuildings
import step3_build_electricity_load_profiles as BuildElectricityLoadProfiles
import step4_build_gas_load_profiles as BuildGasLoadProfiles
import step5_convert_gas_appliances_to_electrical_appliances as ConvertGasToElectric
import step6_combine_real_and_simulated_electricity_loads as CombineRealAndSimulatedProfiles
import step7_get_weather_files as WeatherFiles
import step8_run_sam_model_for_solar_storage as RunSamModelForSolarStorage
import step9_get_loads_for_rates as GetLoadsForRates
import step10_evaluate_gas_rates as EvaluateGasRates
import step11_evaluate_electricity_rates as EvaluateElectricityRates
# import step12_evaluate_capital_costs

class CostService:
    SCENARIOS = {
        "baseline": {"gas": {"heating", "hot_water", "cooking"}, "electric": {"appliances", "misc"}}, # Almost everything is gas, except normal electrical appliances
        # "heat_pump_and_water_heater": ["heating", "hot_water", "appliances", "misc"],
        # "heat_pump_water_heater_and_induction_stove": ["heating", "cooling", "hot_water", "appliances", "cooking", "misc"],
        # "heat_pump_heating_cooling_water_heater_and_induction_stove": ["heating", "cooling", "hot_water", "appliances", "cooking", "misc"]
    }

    def __init__(self, initial_csv, scenario, housing_type, counties, input_dir, output_dir):
        self.csv_file = initial_csv
        self.scenario = scenario
        self.housing_type = housing_type
        self.counties = counties
        self.input_dir = input_dir
        self.output_dir = output_dir

    def run(self):
        print("----- Step 1 -----")
        result = IdentifySuitableBuildings.process(self.scenario, self.housing_type, output_base_dir="data", target_counties=self.counties, force_recompute=True)
        print(result, "\n")

        print("----- Step 2 -----")
        result = PullBuildings.process(self.scenario, self.housing_type, self.counties, output_base_dir="data", download_new_files=True) # output directory should just be 'data', not 'loadprofiles'
        print(result, "\n")
    
        print("----- Step 3 -----")
        # Make sure I don't pull load profiles on every run, only if they don't already exist
        # result = BuildElectricityLoadProfiles.process(self.SCENARIOS, [self.housing_type], self.counties, "data", "data/loadprofiles", force_recompute=False)
        # print(result, "\n")

        print("----- Step 4 -----")
        # result = BuildGasLoadProfiles.process(self.SCENARIOS, [self.housing_type], "data", "data/loadprofiles", self.counties)
        # print(result, "\n")

        print("----- Step 5 -----")
        # result = ConvertGasToElectric.process("data/loadprofiles", "data/loadprofiles", self.counties, list(self.SCENARIOS.keys()), [self.housing_type] )
        # print(result, "\n")

        print("----- Step 6 -----")
        # result = CombineRealAndSimulatedProfiles.process(self.input_dir, self.output_dir, list(self.SCENARIOS.keys()), [self.housing_type], self.counties)
    
        print("----- Step 7 -----")
        # result = WeatherFiles.process(self.input_dir, self.output_dir, list(self.SCENARIOS.keys()), [self.housing_type], self.counties)
        # print(result, "\n")

        print("----- Step 8 -----")
        # result = RunSamModelForSolarStorage.process(self.input_dir, self.output_dir, list(self.SCENARIOS.keys()), [self.housing_type], self.counties)
        # print(result, "\n")

        print("----- Step 9 -----")
        # result = GetLoadsForRates.process(self.input_dir, self.output_dir, list(self.SCENARIOS.keys()), [self.housing_type], self.counties)
        # print(result, "\n")

        print("----- Step 10 -----")
        # result = EvaluateGasRates.process(self.input_dir, self.output_dir, list(self.SCENARIOS.keys()), [self.housing_type], self.counties, "default") # last argument is  load_type, which can be 'default' or 'solarstorage'
        # print(result, "\n")

        print("----- Step 11 -----")
        # result = EvaluateElectricityRates.process(self.input_dir, self.output_dir, list(self.SCENARIOS.keys()), [self.housing_type], self.counties, "default") # last argument is  load_type, which can be 'default' or 'solarstorage'
        # print(result, "\n")

        return self.csv_file
    

initial_csv = "initial_data.csv" # TODO: update

scenario = "baseline"
housing_type = "single-family-detached"
# counties = ["Alameda County"]
input_dir = "data"
output_dir = "data/loadprofiles"

sample_counties = ["San Francisco County"]

norcal_counties = [
    "Alameda County", "Contra Costa County", "Marin County", "Napa County", 
    "San Francisco County", "San Mateo County", "Santa Clara County", "Solano County", "Sonoma County",  # Bay Area
    "Del Norte County", "Humboldt County", "Lake County", "Mendocino County", "Trinity County",  # North Coast
    "Butte County", "Colusa County", "Glenn County", "Lassen County", "Modoc County", 
    "Nevada County", "Plumas County", "Shasta County", "Sierra County", "Siskiyou County", "Tehama County",  # North Valley & Sierra
]

central_counties = [
    "Fresno County", "Kern County", "Kings County", "Madera County", "Merced County", 
    "Sacramento County", "San Joaquin County", "Stanislaus County", "Sutter County", 
    "Tulare County", "Yolo County",  # Central Valley
    "Monterey County", "San Benito County", "San Luis Obispo County", "Santa Barbara County", 
    "Santa Cruz County", "Ventura County",  # Central Coast
    "Alpine County", "Amador County", "Mono County",  # Eastern Sierra & Inland
]

socal_counties = [
    "Los Angeles County", "Orange County", "San Bernardino County", 
    "Riverside County", "Ventura County",  # Greater Los Angeles
    "San Diego County", "Imperial County"  # San Diego & Imperial
]

cost_service = CostService(initial_csv, scenario, housing_type, counties=norcal_counties, input_dir=input_dir, output_dir=output_dir)

final_csv = cost_service.run()

print("Final processed CSV file:", final_csv)

# Next steps:
# For Gas and Electricity rates, model more regions
# Run for PG&E counties


# # Todo:
# - adjust load profiles to be housed in a single folder
# - why are electricity loads so far off when the simulated loads are incorporated in baseline values? Debug whether this is a units issue, or a conversion issue
# - Annual total electricity loads seem too low for berkeley. Should be around 6K, but getting 1K. 