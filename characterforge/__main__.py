from characterforge.ai import AI

import inquirer

import json

PROMPT = '''
Generate a profile for an NPC for a table top RPG. Your output has to be valid JSON.
Fill in the following information:
name, gender, profession, alignment, age, appearance, character_trades, civil_status, backstory

Example:

{{
    "name": "Humboldt",
    "gender": "male",
    "profession": "forester",
    "alignment": "good",
    "age": 54,
    "appearance": "Humboldt is a tall and lean figure with weathered hands that bear the marks of hard work in the forests. He is bold, but has a thick brown beard with some grey spots. He wears a short-sleeved leather jacket over a worn-out grey shirt.",
    "character_trades": "Although his demeanor is a bit harsh, he's actually a gentle person with a soft spot for children.",
    "civil_status": "widower",
    "backstory": "Humboldt learned forestry from his father, shared a deep bond with his late wife, and now finds solace in the woods while being a kind figure in the community, especially towards children."
}}

Input:

Setting: {setting}
Gender: {gender}
Profession: {profession}
Alignment: {alignment}
Details: {details}

'''


def main():
    ai = AI()

    questions = [
        inquirer.Text(name="setting", message="World setting", default="medieval fantasy"),
        inquirer.List(name="gender", message="Gender", choices=[
            "male",
            "female",
            "androgyn",
            "any"
        ], default="any"),
        inquirer.Text(name="profession", message="Profession", default="blacksmith"),
        inquirer.List(name="alignment", message="Alignment", choices=[
            "good",
            "neutral",
            "bad",
            "any"
        ], default="any"),
        inquirer.Editor(name="details", message="Further details (optional)"),
    ]

    answers = inquirer.prompt(questions)
    if not answers:
        return

    print()

    okay = False

    while not okay:

        response = None
        while not response:
            print("Loading...")
            response = ai.query(PROMPT.format(**answers))
            print(response)
            try:
                response = json.loads(response)
            except ValueError:
                print("error: Generation failed; retry")
                response = None
                continue

        try:
            print()
            print("Name:", response["name"])
            print("Gender:", response["gender"])
            print("Profession:", response["profession"])
            print("Alignment:", response["alignment"])
            print("Age:", response["age"])
            print("Appearance:", response["appearance"])
            print("Character Trades:", response["character_trades"])
            print("Civil Status:", response["civil_status"])
            print("Backstory:", response["backstory"])
            print()
        except KeyError:
            print("error: Missing key in AI response")
            print(response)
            print("retry")
            continue

        another = inquirer.prompt([
            inquirer.Confirm(name="another", message="Generate another", default=True),
        ])
        if another:
            okay = not another["another"]
        else:
            okay = True


if __name__ == "__main__":
    main()
