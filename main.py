import os

from sympy import SympifyError

from src.AGMPostulates import display_agm_postulates
from src.Agent import Agent
from src.BeliefBase import BeliefBase

belief_base = BeliefBase()
god = Agent(belief_base)


def main_menu():
    choice = 0
    while True:
        res = input("Select option to continue...").strip()
        if not res.isdigit():
            print("Invalid input. Please enter a number.")
            print_help()
            continue
        if int(res) == 1:
            # We need error handling around these
            try:
                query = input("§ Enter discovery to expand -> ").strip()
                god.expansion(query)
                print(f"\t<> Belief base expanded with {query}")
            except SympifyError as e:
                print(f"Invalid input: {e}. Operation failed, returning to main menu...")
        elif int(res) == 2:
            try:
                query = input("§ Enter statement to remove -> ").strip()
                god.contraction(query)
                print(f"\t<> Belief base contracted with {query}")
            except SympifyError as e:
                print(f"Invalid input: {e}. Operation failed, returning to main menu...")
        elif int(res) == 3:
            try:
                query = input("§ Enter reliable statement to revise -> ").strip()
                god.revision(query)
                print(f"\t<> Belief base revised with {query}")
            except SympifyError as e:
                print(f"Invalid input: {e}. Operation failed, returning to main menu...")
        elif int(res) == 4:
            try:
                query = input("§ Enter statement to check entailment -> ").strip()
                print("# Checking entailment by belief base...")
                if god.check_entailment(query):
                    print(f"\t<> The statement {query} is entailed (implied)")
                else:
                    print(f"\t<> The statement {query} is not entailed (free or contradicted)")
                print("# Checking consistency (lack of contradiction) with belief base...")
                if god.check_consistent(query):
                    print(f"\t<> The statement {query} is consistent")
                else:
                    print(f"\t<> The statement {query} is inconsistent (contradicted)")
            except SympifyError as e:
                print(f"Invalid input: {e}. Operation failed, returning to main menu...")
        elif int(res) == 5:
            try:
                phi = input("§ Enter φ -> ").strip()
                if phi == "":
                    print("Empty input for φ. Operation failed, returning to main menu...")
                    continue
                psi = input("§ Enter optional ψ (for extensionality) -> ").strip()
                psi = psi if psi else None
                print("# Testing the AGM Postulates...")
                display_agm_postulates(god.get_belief_base(), phi, psi)
            except SympifyError as e:
                print(f"Invalid input: {e}. Operation failed, returning to main menu...")
        elif int(res) == 6:
            print(god.get_belief_base())
        else:
            print("Exiting... Thank you for using the agent!")
            break


def print_help():
    print("_______________________________________________________")
    print("The following operations are supported by the agent:")
    print("1. Add a new discovery to the belief base - expansion BB + φ")
    print("2. Remove a statement from the belief base - contraction BB ÷ φ")
    print("3. Update the belief base with a reliable statement - revision BB * φ")
    print("4. Check if a statement is consistent with the belief base - entailment BB ⊨ φ")
    print("5. Run the AGM postulates")
    print("6. Query the state of the belief base BB")
    print("7. Exit the agent")
    print("_______________________________________________________")
    print("Propositional logic supports the following operators: &, |, ~, >>, <<")


# Project entrypoint
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("~~~ Welcome to our Belief Revision Agent! ~~>\n")
    print_help()
    # Involve query caller
    main_menu()
