# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
I noticed that when I entered a guess, the message was always "Go lower" even though the secret number was higher. I also noticed that whenever I input 1 as my guess, the same "Go lower" message appeared. I also noticed that the "New Game" button doesn't appear to work. Whenever I press on it, nothing happens. Actually, it resets the secret number but doesn't reset the attempts. Another bug or inconsistency I found was an incorrect number of attempts. Though on the right side it says I have 8 attempts, under make a guess it says I have 7 attempts left, but I actually only have 6. I found a few more bugs such as there are no parameter limitations, for example , you can input numbers higher than the top possible secret number (and when you do you get a message saying to go higher), when you switch to a different game mode (from hard to easy for example) the secret number does not change, and there are issues with the score. A bug I noticed after playing a few times was that the history isn't reset when changing difficulty.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude in VS code and Copilot. AI correctly identified why the New Game button wasn't working. It let me know that the st.session_state.score needs to be reset to 0, the .status needs to be reset to playing, and the .history needed to be resest to an empty list in order for the "New Game" button to function correctly. While this is correct, there is one issue I found incorrect or that AI didn't catch. The resetting of  st.session_state.secret = random.randint(1, 100) doesn't take into account the mode the game is in, so if it's on easy mode, though the top limit should be 20, the secret number will always be reset to a number between 1 and 100. I verified it by looking at the code myself and walking through the logic. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I had to manually test the New Game button. For example, I tried to fix the New Game button so the game resets. I came across some streamlit errors when trying to fix it. I just had to keep manually clicking the New game button to see if it worked correctly after each cod revision. AI helped me but also created other errors. I would explain to AI what errors I was getting and it was a back and forth of implementing a revision and manually testing the button until all errors were fixed.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---
I didn't notice that the secret number kept changing in the origianl app. I tried it and that wasn't the case for me. If anything, I noticed it did not change even when changing the difficulty. I imagine that if it did, it might have to do with some code regenerating the number everytime the app runs. The way I understand it is that streamlit has a session state where the number should be stored. Some kind of code to check that the game is still running should ensure that enumber doesn't change. Though I didn't see this issue when running the game, there was an issue with streamlit when it came to fixing the "New Game" button.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

I realized how important it is to fix one issue at a time in very small increments in order to understand and catch all the changes being made. If too many changes are made at once and there are errors, it's sometimes difficult to understand exactly why the errors are happening. I learned a lot from this project, from using vs code, to using the terminal on vs code, to using ai within the vs code. A lot of what I'm doing is new so I don't know how to answer what it is I would do differently as it's all new. I definitely learned the value of creating test scripts for debugging so i'll be implementing that into future projects. I love AI to generate code! But I learned that for it to be effective, there needs to be a collaboration between what I want the result to be and what AI thinks the result should be in order to get the results I want. 