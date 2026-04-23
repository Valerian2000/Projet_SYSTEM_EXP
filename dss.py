from experta import KnowledgeEngine

class SystemeExpert(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.regles_dynamiques = []

    def ajouter_regle(self, conditions, conclusion):
        """
        conditions: dict -> {"fievre": True, "toux": True}
        conclusion: dict -> {"grippe": True}
        """
        self.regles_dynamiques.append((conditions, conclusion))

    def verifier_regles_dynamiques(self):
        """
        Vérifie les règles dynamiques à chaque cycle
        """
        faits = {k: v for fact in self.facts.values() if isinstance(fact, Fact) for k, v in fact.items()}
        for conditions, conclusion in self.regles_dynamiques:
            if all(faits.get(k) == v for k, v in conditions.items()):
                # éviter duplication
                deja_present = any( 
                    all(f.get(k) == v for k, v in conclusion.items()) for f in self.facts.values() if isinstance(f, Fact)
                    )

                if not deja_present:
                    print(f"Règle dynamique appliquée : {conditions} => {conclusion}")
                    self.declare(Fact(**conclusion))

    @Rule()
    def moteur_dynamique(self):
        self.verifier_regles_dynamiques()

    
engine = SystemeExpert()
engine.reset()

# Ajout de faits
engine.declare(Fact(fievre=True))
engine.declare(Fact(toux=True))
engine.declare(Fact(faim=True))
# Ajout de règles dynamiques
engine.ajouter_regle(
    {"fievre": True, "toux": True},
    {"grippe": True}
)

engine.ajouter_regle(
    {"faim": True},
    {"manger": True}
)

engine.ajouter_regle(
    {"grippe": True},
    {"repos": True}
)

engine.run()

print("\nFaits finaux :")
for f in engine.facts.values():
    if isinstance(f, Fact):
        print(dict(f))