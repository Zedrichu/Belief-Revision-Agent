import os
from BeliefBase import BeliefBase
from Agent import Agent

belief_base = BeliefBase()
god = Agent(belief_base)


def main_menu():
    choice = 0
    while True:
        res = input("Select option to continue...").strip()
        if int(res) == 1:
            query = input("§ Enter discovery to expand -> ").strip()
            god.expansion(query)
            print(f"\t<> Belief base expanded with {query}")
        elif int(res) == 2:
            query = input("§ Enter statement to remove -> ").strip()
            god.contraction(query)
            print(f"\t<> Belief base contracted with {query}")
        elif int(res) == 3:
            query = input("§ Enter reliable statement to revise -> ").strip()
            god.revision(query)
            print(f"\t<> Belief base revised with {query}")
        elif int(res) == 4:
            query = input("§ Enter statement to check entailment -> ").strip()
            if god.check(query):
                print(f"\t<> The statement {query} is consistent with the belief base")
            else:
                print(f"\t<> The statement {query} contradicts the belief base")
        elif int(res) == 5:
            god.show_belief_base()
        else:
            print("Exiting... Thank you for using the agent!")
            break


# Project entrypoint
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("~~~ Welcome to our Belief Revision Agent! ~~>\n")
    print("_______________________________________________________")
    print("The following operations are supported by the agent:")
    print("1. Add a new discovery to the belief base - expansion")
    print("2. Remove a statement from the belief base - contraction")
    print("3. Update the belief base with a reliable statement - revision")
    print("4. Check if a statement is consistent with the belief base - entailment")
    print("5. Query the state of the belief base")
    print("6. Exit the agent")
    # Involve query caller
    main_menu()
