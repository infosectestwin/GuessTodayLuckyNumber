import random
import streamlit as st
from streamlit_bokeh import streamlit_bokeh
from guess_draw import render_history
import time

# --- Page setup ---
st.markdown("""
    <style>
    h1 {
        white-space: nowrap;           /* prevent line breaks */
        overflow: hidden;              /* hide anything too long */
        text-overflow: ellipsis;       /* optional: add "..." if it overflows */
    }
    .block-container {
        max-width: 1000px;             /* allow more horizontal space */
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="🎯 What is your today's Lucky Number?", page_icon="🎮", layout="centered")

# --- Title ---
st.markdown("<h1 style='text-align: center;'>🎯 What is your today's LUCKY Number</h1>", unsafe_allow_html=True)

# --- Initialize session state ---
# --- Initialize session state ---
if "lucky_number" not in st.session_state:
    st.session_state.lucky_number = None
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "ready" not in st.session_state:
    st.session_state.ready = False
if "restart" not in st.session_state:
    st.session_state.restart = False
if "start_clicked" not in st.session_state:
        st.session_state.start_clicked = False
        st.session_state.message = "Click the glowing circle to start the game!"
if "guesses" not in st.session_state:
    st.session_state.guesses = []

if st.button("🔄 Play Again", key="play_again"):
    st.session_state.restart = True
    st.session_state._force_rerun = True
    st.info(f"inside Play state: {st.session_state.restart}")
    st.rerun()

if st.session_state.get("restart"):
    # reset everything here
    st.session_state.clear()
    st.session_state.restart = False
    st.rerun()

st.markdown("""
     <style>   
            .element-container:nth-of-type(1)  button {
                width: 180px !important;
                height: 180px !important;
                border-radius: 50% !important;
                font-size: 22px !important;
                font-weight: bold !important;
                color: white !important;
                background: radial-gradient(circle at 30% 30%, #6dd5ed, #2193b0) !important;
                border: none !important;
                box-shadow: 0 0 20px rgba(33,147,176,0.6), 0 0 40px rgba(33,147,176,0.4);
                animation: pulse 2s infinite;
                transition: all 0.2s ease-in-out;
            }
        
            .element-container:nth-of-type(1) button:hover {
                transform: scale(1.08);
                box-shadow: 0 0 25px rgba(33,147,176,0.8), 0 0 50px rgba(33,147,176,0.6);
                cursor: pointer;
            }        
            
    </style>    
""", unsafe_allow_html=True)
if not st.session_state.start_clicked:
    st.info(st.session_state.message)
    col1, col2, col3 = st.columns([1, 0.4, 1])
    with col2:
        start_clicked = st.button("START", key="start_button")

    if start_clicked and not st.session_state.ready:
        with st.spinner("✨ Generating a lucky number..."):
            time.sleep(1.5)
            st.session_state.lucky_number = random.randint(1, 100)
            st.session_state.ready = True
            st.session_state.start_clicked = True
            st.session_state.attempts = 0
        st.rerun()

# Ready to guess lucky number
if st.session_state.ready:
    if not st.session_state.restart:
        st.success("✅ The LUCKY number is ready! Start guessing below 👇")
        guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1,key="guess_input")
        submit_clicked = st.button("Submit Guess", key="submit_button")
        render = render_history(10,100)
        if submit_clicked:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 10:
                st.warning(f"❌ Game over! You have reached the maximum number of attempts!")
                st.session_state.restart = True
                time.sleep(1.5)
                st.rerun()
            else:
                st.session_state.guesses.append(guess)
                if guess < st.session_state.lucky_number:
                    st.warning("🔻 Too low!")
                elif guess > st.session_state.lucky_number:
                    st.info("🔺 Too high!")
                else:
                    st.balloons()
                    st.success(f"🎉 You got it! The number was {st.session_state.lucky_number}. Attempts: {st.session_state.attempts}")

                if len(st.session_state.guesses) > 0:
                    f = render.generate_history(st.session_state.attempts,st.session_state.guesses)
                    streamlit_bokeh(f, use_container_width=True, theme="streamlit", key="guess_chart")

