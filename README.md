# GDG BMSIT&M - Simple Chatbot with Gemini

Quick chatbot using streamlit, gemini api and ngrok for sharing

## Setup

1) Install packages:
```
pip install streamlit google-generativeai python-dotenv ngrok
```
*Mac users: Use `pip3` instead of `pip` if needed*

2) Get your gemini api key from https://makersuite.google.com/app/apikey

3) Put your api key in the `.env` file

4) Run it:
```
streamlit run app.py
```
*Mac users: Use `python3 -m streamlit run app.py` if the above doesn't work*

## Make it interesting

The basic version just talks normally. But you can make it act like different characters!

In `app.py`, comment out line 27 and uncomment lines 30-32 to make it a pirate bot.

Try changing the system_prompt to make it:
- A cooking chef
- A fitness trainer  
- Shakespeare
- Whatever you want

## Share with friends

Want others to try your bot? Use ngrok:

1) Download ngrok from ngrok.com
2) Run `ngrok http 8501` in a new terminal
3) Share the https link with anyone

Now your friends can chat with your custom AI from any of their devices enjoyyy : )

---

Built by [@DevAdy](https://github.com/DevAdy)  
Connect with me [linktr.ee/aditya.b.career](https://linktr.ee/aditya.b.career)