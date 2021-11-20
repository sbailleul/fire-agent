from constants import FIELD
from environment import Environment

# Initialisation de l'environnement, création de l'agent
# Boucle principal, chaque tour vaut une résolution de l'objectif par l'agent
# Boucle inbriquée, chaque tour l'agent se base sur son expérience passée en sélectionnant
# la meilleur action à faire en fonction de son état courant.
# L'environnement calcul ensuite la récompense à donner à l'agent en fonction de l'action faite,
# l'agent est ensuite mis à jour par l'environnement
if __name__ == '__main__':
    env = Environment(FIELD)
    agent = env.create_agent()
    for i in range(100):
        j = 0
        while env.get_burning_trees() != 0:
            j += 1
            action = agent.best_action()
            # world change
            env.apply(agent, action)
        print("Iteration : %d, tours: %d, reward : %d " % (i, j, agent.reward))
        agent.reset(env)