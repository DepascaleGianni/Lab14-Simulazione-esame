import model.model as mod

m = mod.Model()
m.buildGraph()
m.searchPath(3)

print(m.solBest)

