class Evolution:

    def select(self, agents):

        agents.sort(key=lambda a: a.fitness(), reverse=True)

        return agents[:len(agents)//2]

    def reproduce(self, selected):

        new_pop = []

        for a in selected:
            new_pop.append(a)
            new_pop.append(a.mutate())

        return new_pop

    def step(self, agents):

        return self.reproduce(self.select(agents))
