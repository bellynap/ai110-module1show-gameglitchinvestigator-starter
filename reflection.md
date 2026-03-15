# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
I noticed that when I entered a guess, the message was always "Go lower" even though the secret number was higher. I also noticed that whenever I input 1 as my guess, the same "Go lower" message appeared. I also noticed that the "New Game" button doesn't appear to work. Whenever I press on it, nothing happens. Actually, it resets the secret number but doesn't reset the attempts. Another bug or inconsistency I found was an incorrect number of attempts. Though on the right side it says I have 8 attempts, under make a guess it says I have 7 attempts left, but I actually only have 6. I found a few more bugs such as there are no parameter limitations, for example , you can input numbers higher than the top possible secret number (and when you do you get a message saying to go higher), when you switch to a different game mode (from hard to easy for example) the secret number does not change, and there are issues with the score. 
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude in VS code. AI correctly identified why the New Game button wasn't working. It let me know that the st.session_state.score needs to be reset to 0, the .status needs to be reset to playing, and the .history needed to be resest to an empty list in order for the "New Game" button to function correctly. While this is correct, there is one issue I found incorrect or that AI didn't catch. The resetting of  st.session_state.secret = random.randint(1, 100) doesn't take into account the mode the game is in, so if it's on easy mode, thought the top limit should be 20, the secret number will always be reset to a number between 1 and 100. I verified it by looking at the code myself and walking through the logic. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
