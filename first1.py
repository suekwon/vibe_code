import streamlit as st
import time

# Timer app 제작 
# 3min timer -> then alert by sound
# display timer

def main():
    st.title("Timer App")
    
    # Initialize session state
    if 'running' not in st.session_state:
        st.session_state.running = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'duration' not in st.session_state:
        st.session_state.duration = 180  # 3 minutes in seconds
    
    # Timer duration input
    duration = st.number_input("Timer duration (seconds)", min_value=1, max_value=3600, value=180)
    st.session_state.duration = duration
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Start"):
            st.session_state.running = True
            st.session_state.start_time = time.time()
    
    with col2:
        if st.button("Stop"):
            st.session_state.running = False
    
    with col3:
        if st.button("Reset"):
            st.session_state.running = False
            st.session_state.start_time = None
    
    # Display timer
    timer_placeholder = st.empty()
    
    if st.session_state.running and st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        remaining = st.session_state.duration - elapsed
        
        if remaining <= 0:
            timer_placeholder.success("Time's up! ⏰")
            st.session_state.running = False
            
            # Play sound alert
            st.audio("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3", autoplay=True)
        else:
            minutes, seconds = divmod(int(remaining), 60)
            timer_placeholder.info(f"Time remaining: {minutes:02d}:{seconds:02d}")
            st.rerun()
    else:
        timer_placeholder.info("Press Start to begin timer")

if __name__ == "__main__":
    main()
