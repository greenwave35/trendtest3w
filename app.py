import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

st.set_page_config(page_title="Trend Catcher | 3주차", page_icon="📊")
st.title("Trend Catcher")
st.subheader("3주차 · 개인 YouTube API 키 연결 테스트")
st.info("API 키는 브라우저에서 Google API로 직접 전송합니다. Python에는 영상 통계만 전달합니다.")

HTML = """
<div class="api-box">
  <label for="yt-api-key">YouTube Data API 키 (매번 입력)</label>
  <input id="yt-api-key" type="password" autocomplete="off" spellcheck="false" placeholder="Google Cloud API 키 입력" />
  <div class="actions">
    <button id="yt-test" type="button">인기 영상 5개로 연결 테스트</button>
    <button id="yt-clear" type="button">키 지우기</button>
  </div>
  <p id="yt-status" role="status" aria-live="polite">키는 저장되지 않습니다.</p>
</div>
"""
CSS = """
.api-box {padding: 14px; border: 1px solid #d1d5db; border-radius: 10px; font-family: sans-serif;}
.api-box label {display: block; font-weight: 600; margin-bottom: 8px;}
.api-box input {box-sizing: border-box; width: 100%; padding: 12px; border:1px solid #9ca3af; border-radius:6px; font-size: 14px;}
.actions {display:flex; flex-wrap:wrap; gap:8px; margin-top:12px;}
.actions button {border:0; background: #155e75; color:white; padding:10px 12px; border-radius:6px; cursor:pointer;}
.actions button:last-child {background:#64748b;}
#yt-status {font-size: 13px; white-space:pre-wrap; overflow-wrap:anywhere;}
"""
JS = Path(__file__).with_name("browser_api.js").read_text(encoding="utf-8")

api_widget = st.components.v2.component(
    "trend_catcher_browser_api", html=HTML, css=CSS, js=JS
)
result = api_widget(key="browser_api", on_videos_change=lambda: None)

# JavaScript only sends a strict allowlist of publicly available video metadata.
# It NEVER sends the API key or the HTTP request URL to Python.
videos = result.videos if result.videos else None
if videos:
    clean = []
    for row in videos[:5]:
        if not isinstance(row, dict):
            continue
        clean.append({
            "영상 ID": str(row.get("id", ""))[:32],
            "제목": str(row.get("title", ""))[:200],
            "게시일": str(row.get("publishedAt", ""))[:32],
            "조회수": int(row.get("views", 0)),
            "좋아요": int(row.get("likes", 0)),
            "댓글": int(row.get("comments", 0)),
        })
    if clean:
        df = pd.DataFrame(clean)
        st.success(f"Google에서 {len(df)}개 영상의 공개 통계를 받아 Python으로 전달했습니다.")
        st.dataframe(df, use_container_width=True, hide_index=True)
        df["좋아요율(%)"] = (df["좋아요"] / df["조회수"].replace(0, float("nan")) * 100).round(2)
        df["댓글률(%)"] = (df["댓글"] / df["조회수"].replace(0, float("nan")) * 100).round(2)
        st.subheader("Python 분석 결과")
        st.dataframe(df[["제목", "조회수", "좋아요율(%)", "댓글률(%)"]], use_container_width=True, hide_index=True)
        st.caption("좋아요·댓글 통계가 비공개인 영상은 0으로 표시될 수 있어 정식 분석에서는 결측값 처리가 필요합니다.")

st.divider()
st.markdown("**검증:** 브라우저 개발자 도구 → Network에서 Google(`googleapis.com`)으로 요청하는지, Streamlit 연결 메시지에는 키가 없는지 확인하세요.")
st.caption("교육용 프로토타입 · API 키를 localStorage, sessionStorage, 쿠키, Streamlit Secrets에 저장하지 않음")
