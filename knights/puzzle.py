from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

#have to create a general knowledge base


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight,AKnave),
    Not(And(AKnight,AKnave)),
    #IF A is a knight, then A is a knight and a knave
    Implication(AKnight,And(AKnight,AKnave)),
    #IF A is a knave then A is not a knight AND a Knave
    Implication(AKnave,Not(And(AKnight,AKnave))),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    Or(AKnight,AKnave),
    Not(And(AKnight,AKnave)),
    Or(BKnight,BKnave),
    Not(And(BKnight,BKnave)),
    #we only have to judge on what the knights/knaves tell us
    #if a is a knight then they are both knaves
    Implication(AKnight, And(BKnave,AKnave)),
    #if a is a knave then at least one of them isnt a knave
    Implication(AKnave, Not(And(BKnave,BKnight)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight,AKnave),
    Not(And(AKnight,AKnave)),
    Or(BKnight,BKnave),
    Not(And(BKnight,BKnave)),
    #if a is a knight then they are both the same (cos we are being logical we cant rule out knaves)
    Implication(AKnight, Or(And(AKnight,BKnight),And(AKnave,BKnave))),
    #if a is a knave then they are not both knaves or knights
    Implication(AKnave, Not(Or(And(AKnight,BKnight),And(AKnave,BKnave)))),

    #if b is a knight then either a is a knight and b is a knave or b is a knight and a is a knave
    Implication(BKnight, Or(And(AKnight,BKnave),And(BKnight,AKnave))),
    #if b is a knave then either they are both knaves or knights
    Implication(BKnave, Or(And(AKnave,BKnave),And(BKnight,AKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    Or(AKnight,AKnave),
    Not(And(AKnight,AKnave)),
    Or(BKnight,BKnave),
    Not(And(BKnight,BKnave)),
    Or(CKnight,CKnave),
    Not(And(CKnight,CKnave)),
    #if b is a knight and says that c is a knave and a said that a is a knave
    Implication(BKnight, CKnave),
    Implication(BKnight,
            #a is either a knight or a knave
                #if a is a knight, then a is a knave
        And(
            Implication(AKnight,AKnave),
            Implication(AKnave, AKnight)
        )
    ),
    #if b is a knave
    Implication(BKnave,CKnight),
    Implication(BKnave,
                And(
                    Implication(AKnight,AKnight),
                    Implication(AKnave,AKnave)
                )
                ),
    #if c is a knight
    Implication(CKnight, AKnight),
    #if c is a knave
    Implication(CKnave, AKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
