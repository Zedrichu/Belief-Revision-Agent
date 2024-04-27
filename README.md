# Belief-Revision-Agent
Implementation of an AI agent performing belief revision (using belief base entrenchment contraction and expansion)

## Installation
1. Create virtual environment using python 3.12: `python -m venv .venv` (for windows: `python -m venv C:\path\to\venv`)
2. Active the environment: `source ./.venv/bin/activate` (for windows: `.\.venv\Scripts\activate.ps1`)
3. Install requirements: `pip install -r requirements.txt`

## Usage
To run the application use: `python main.py`.

The Belief-Revision-Agent supports the following operations:
1. Add a new discovery to the belief base - expansion BB + φ
2. Remove a statement from the belief base - contraction BB ÷ φ
3. Update the belief base with a reliable statement - revision BB * φ
4. Check if a statement is consistent with the belief base - entailment BB ⊨ φ
5. Run the AGM postulates
6. Query the state of the belief base BB

**Example of how to run a simple revision:**
```
Select option to continue...1
§ Enter discovery to expand -> p
	<> Belief base expanded with p
Select option to continue...1
§ Enter discovery to expand -> q
	<> Belief base expanded with q
Select option to continue...1
§ Enter discovery to expand -> r
	<> Belief base expanded with r
Select option to continue...3
§ Enter reliable statement to revise -> ~(q | r)
	<> Belief base revised with ~(q | r)
Select option to continue...6
BeliefBase|
	Belief| p
	Belief| ~(q | r)
```

#### Project Completed in Course 02180 Introduction to Artificial Intelligence - Technical University of Denmark 
<img src="https://user-images.githubusercontent.com/65953954/120001846-7f05f180-bfd4-11eb-8c11-2379a547dc9f.jpg" alt="drawing" width="100"/>
