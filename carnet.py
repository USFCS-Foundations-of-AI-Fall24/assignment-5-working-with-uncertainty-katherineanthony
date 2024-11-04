from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination

car_model = BayesianNetwork(
    [
        ("Battery", "Radio"),
        ("Battery", "Ignition"),
        ("Ignition","Starts"),
        ("Gas","Starts"),
        ("Starts","Moves"),
        # ("KeyPresent", "Ignition"),
        # ("KeyPresent", "Gas")
    ]
)

# Defining the parameters using CPT
from pgmpy.factors.discrete import TabularCPD

cpd_battery = TabularCPD(
    variable="Battery", variable_card=2, values=[[0.70], [0.30]],
    state_names={"Battery":['Works',"Doesn't work"]},
)

cpd_gas = TabularCPD(
    variable="Gas", variable_card=2, values=[[0.40], [0.60]],
    state_names={"Gas":['Full',"Empty"]},
)

cpd_radio = TabularCPD(
    variable=  "Radio", variable_card=2,
    values=[[0.75, 0.01],[0.25, 0.99]],
    evidence=["Battery"],
    evidence_card=[2],
    state_names={"Radio": ["turns on", "Doesn't turn on"],
                 "Battery": ['Works',"Doesn't work"]}
)

cpd_ignition = TabularCPD(
    variable=  "Ignition", variable_card=2,
    values=[[0.75, 0.01],[0.25, 0.99]],
    evidence=["Battery"],
    evidence_card=[2],
    state_names={"Ignition": ["Works", "Doesn't work"],
                 "Battery": ['Works',"Doesn't work"]}
)

cpd_starts = TabularCPD(
    variable="Starts",
    variable_card=2,
    values=[[0.95, 0.05, 0.05, 0.001], [0.05, 0.95, 0.95, 0.9999]],
    evidence=["Ignition", "Gas"],
    evidence_card=[2, 2],
    state_names={"Starts":['yes','no'], "Ignition":["Works", "Doesn't work"], "Gas":['Full',"Empty"]},
)

cpd_moves = TabularCPD(
    variable="Moves", variable_card=2,
    values=[[0.8, 0.01],[0.2, 0.99]],
    evidence=["Starts"],
    evidence_card=[2],
    state_names={"Moves": ["yes", "no"],
                 "Starts": ['yes', 'no'] }
)

## TODO: change the following to the KeyPresent one
# cpd_ignition = TabularCPD(
#     variable=  "Ignition", variable_card=2,
#     values=[[0.75, 0.01],[0.25, 0.99]],
#     evidence=["Battery"],
#     evidence_card=[2],
#     state_names={"Ignition": ["Works", "Doesn't work"],
#                  "Battery": ['Works',"Doesn't work"]}
# )


# Associating the parameters with the model structure
def det_query(variables, evidence):
    car_model.add_cpds( cpd_starts, cpd_ignition, cpd_gas, cpd_radio, cpd_battery, cpd_moves)

    car_infer = VariableElimination(car_model)

    # print(car_infer.query(variables=["Moves"],evidence={"Radio":"turns on", "Starts":"yes"}))
    q = car_infer.query(variables=variables,evidence=evidence)
    print(q)

## TODO: add some more queries here

if __name__ == '__main__':
    print("probability of battery not working given the car will not move")
    det_query(variables=["Battery"], evidence={"Moves":"no"})
    print("probability of car not starting given the radio not working")
    det_query(variables=["Starts"], evidence={"Radio":"Doesn't turn on"})
    print("given the battery working, does the probability of the radio working change if we discover that the car has gas in it?")
    det_query(variables=["Radio"], evidence={"Battery":"Works"})
    det_query(variables=["Radio"], evidence={"Battery": "Works", "Gas":"Full"})
    print("no.")
    print("given the car does not move, how does the probability of the ignition failing change if we observe that the car does not have gas in it")
    det_query(variables=["Ignition"], evidence={"Moves":"no"})
    det_query(variables=["Ignition"], evidence={"Moves": "no", "Gas":"Empty"})
    print("it is more likely that the ignition works")
    print("probability that the car starts if the radio works and it is has gas in it")
    det_query(variables=["Starts"], evidence={"Radio": "turns on", "Gas": "Full"})
    pass