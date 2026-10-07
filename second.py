import streamlit as st
import time

# Streamlit 카운트다운 타이머


def render_ring(remaining, duration):
    """남은 시간을 원형 진행 바(SVG)로 그린다."""
    fraction = remaining / duration if duration > 0 else 0
    radius = 90
    circumference = 2 * 3.141592653589793 * radius
    offset = circumference * (1 - fraction)  # 남은 만큼 채워짐

    mins, secs = divmod(int(remaining) + (1 if remaining > 0 else 0), 60)
    color = "#FF4B4B" if fraction < 0.25 else "#00C4A7"

    return f"""
    <div style="display:flex; justify-content:center; margin-top:20px;">
      <svg width="220" height="220" viewBox="0 0 220 220">
        <circle cx="110" cy="110" r="{radius}" fill="none"
                stroke="#2b2b2b" stroke-width="16"/>
        <circle cx="110" cy="110" r="{radius}" fill="none"
                stroke="{color}" stroke-width="16" stroke-linecap="round"
                stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"
                transform="rotate(-90 110 110)"
                style="transition: stroke-dashoffset 1s linear;"/>
        <text x="110" y="122" text-anchor="middle"
              font-size="42" font-weight="bold" fill="#31333F"
              font-family="sans-serif">{mins:02d}:{secs:02d}</text>
      </svg>
    </div>
    """


def main():
    st.title("⏱️ 카운트다운 타이머")

    # 세션 상태 초기화
    if "running" not in st.session_state:
        st.session_state.running = False
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "duration" not in st.session_state:
        st.session_state.duration = 0

    # 시간 입력 (분 / 초)
    col_min, col_sec = st.columns(2)
    with col_min:
        minutes = st.number_input("분", min_value=0, max_value=180, value=3)
    with col_sec:
        seconds = st.number_input("초", min_value=0, max_value=59, value=0)

    total_seconds = int(minutes) * 60 + int(seconds)

    # 제어 버튼
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ 시작", use_container_width=True):
            if total_seconds > 0:
                st.session_state.duration = total_seconds
                st.session_state.start_time = time.time()
                st.session_state.running = True
    with col2:
        if st.button("⏸️ 정지", use_container_width=True):
            st.session_state.running = False
    with col3:
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state.running = False
            st.session_state.start_time = None
            st.session_state.duration = 0

    # 타이머 표시 (원형 진행 바)
    placeholder = st.empty()

    if st.session_state.running and st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        remaining = st.session_state.duration - elapsed

        if remaining <= 0:
            placeholder.markdown(
                render_ring(0, st.session_state.duration), unsafe_allow_html=True
            )
            st.success("시간 종료! ⏰")
            st.session_state.running = False
            st.balloons()
        else:
            placeholder.markdown(
                render_ring(remaining, st.session_state.duration),
                unsafe_allow_html=True,
            )
            time.sleep(1)
            st.rerun()
    else:
        # 정지/대기 상태: 설정된 시간을 가득 찬 링으로 표시
        display = st.session_state.duration or total_seconds
        placeholder.markdown(
            render_ring(display, display if display > 0 else 1),
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
