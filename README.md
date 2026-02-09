# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo

![Game Screenshot] <img width="1470" height="920" alt="Screenshot 2026-02-04 at 9 55 18 PM" src="https://github.com/user-attachments/assets/c7519306-015b-4976-9482-8e9a6b90e404" />


## 🚀 Stretch Features

<img width="1470" height="920" alt="Screenshot 2026-02-04 at 10 39 01 PM" src="https://github.com/user-attachments/assets/0850ecae-19cd-46fb-b949-4b394c631e5d" />

<img width="1470" height="920" alt="Screenshot 2026-02-04 at 10 38 47 PM" src="https://github.com/user-attachments/assets/3a597c78-5466-495d-9ac8-572d214ebb71" />


