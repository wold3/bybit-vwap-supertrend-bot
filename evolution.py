class Evolution:

    def select(self, agents):

        agents.sort(key=lambda a: a.fitness(), reverse=True)

        return agents[:max(2, len(agents)//2)]

    def reproduce(self, selected):

        new_agents = []

        for a in selected:
            new_agents.append(a)
            new_agents.append(a.mutate())

        return new_agents

    def step(self, agents):
        return self.reproduce(self.select(agents))
