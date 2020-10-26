from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

model = BayesianModel([('Burglary', 'Alarm'), ('Earthquake', 'Alarm'),('Alarm', 'JohnCalls'),('Alarm', 'MaryCalls')])
cpd_Burglary = TabularCPD(variable='Burglary', variable_card=2, values=[[0.001],[0.999]])
cpd_Earthquake = TabularCPD(variable='Earthquake', variable_card=2, values=[[0.002],[0.998]])
cpd_Alarm = TabularCPD('Alarm', 2,
                            [[0.95, 0.94, 0.29, 0.001],
                            [0.05, 0.06, 0.71, 0.999]],
                  evidence=['Burglary', 'Earthquake'], evidence_card=[2, 2])

cpd_JohnCalls = TabularCPD('JohnCalls', 2,
                            [[0.90, 0.05],
                            [0.1,0.95]],
                  evidence=['Alarm'], evidence_card=[2])

cpd_MaryCalls = TabularCPD('MaryCalls', 2,
                            [[0.70, 0.01],
                            [0.3,0.99]],
                  evidence=['Alarm'], evidence_card=[2])

# Associating the CPDs with the network structure.
model.add_cpds(cpd_Burglary, cpd_Earthquake, cpd_Alarm,cpd_JohnCalls,cpd_MaryCalls )

# Some other methods
print(model.get_cpds())


# check_model check for the model structure and the associated CPD and returns True if everything is correct otherwise throws an exception
print(model.check_model())


print(model.get_independencies())

infer = VariableElimination(model)

print("\n\nfirst query\n")

prob = infer.query(variables = ['Burglary'],joint=False)
print("\n0 => True\n1 => False\n")
print(prob['Burglary'])

print("\n\nsecond query\n")

prob = infer.query(variables = ['Burglary'],evidence={'MaryCalls':0},joint=False)
print("\n0 => True\n1 => False\n")
print(prob['Burglary'])

print("\n\nThird query\n")

prob = infer.query(variables = ['Burglary'],evidence={'MaryCalls':0,'JohnCalls':0},joint=False)
print("\n0 => True\n1 => False\n")
print(prob['Burglary'])

print("\n\nfourth query\n")

prob = infer.query(variables = ['Burglary'],evidence={'MaryCalls':0,'JohnCalls':0,'Earthquake':1},joint=False)
print("\n0 => True\n1 => False\n")
print(prob['Burglary'])

print("\n\nFifrth query\n")

prob = infer.query(variables = ['Burglary'],evidence={'MaryCalls':0,'JohnCalls':0},joint=False)
print("\n0 => True\n1 => False\n")
print(prob['Burglary'])

print("\n\nSixth query\n")

prob = infer.query(variables = ['MaryCalls'],evidence={'Alarm':1,},joint=False)
print("\n0 => True\n1 => False\n")
print(prob['MaryCalls'])


print("\n\nSeventh query\n")

prob = infer.query(variables = ['Burglary'],evidence={'MaryCalls':1,'JohnCalls':1},joint=False)
print("\n0 => True\n1 => False\n")
print(prob['Burglary'])

print("\n\nEigth query\n")

prob = infer.query(variables = ['Burglary'],evidence={'MaryCalls':0,'JohnCalls':0},joint=False)
print("\n0 => True\n1 => False\n")
print(prob['Burglary'])

print("\n\nNinth query\n")

prob = infer.query(variables = ['Alarm'],evidence={'MaryCalls':0,'JohnCalls':0,'Burglary':1,'Earthquake':1},joint=False)
print("\n0 => True\n1 => False\n")
print(prob['Alarm'])


print("\n\nTenth query\n")

prob = infer.query(variables = ['MaryCalls'],evidence={'Alarm':0,'JohnCalls':1},joint=False)
print("\n0 => True\n1 => False\n")
print(prob['MaryCalls'])

print("\n\nEleventh query\n")

prob = infer.query(variables = ['MaryCalls'],evidence={'Alarm':0},joint=False)
print("\n0 => True\n1 => False\n")
print(prob['MaryCalls'])

