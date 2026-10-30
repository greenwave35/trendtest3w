# Trend Catcher · 3주차

## 실행

1. `py -m pip install -r requirements.txt`
2. `py -m streamlit run app.py`
3. Google Cloud에서 YouTube Data API v3 활성화 후 API 키를 발급하고 API 제한을 설정합니다.
4. 앱의 입력창에 키를 붙여넣고 '인기 영상 5개로 연결 테스트'를 누릅니다.

## 보안 구조

- 브라우저 JavaScript가 YouTube Data API에 직접 `fetch()` 요청합니다.
- `X-Goog-Api-Key` 헤더는 Google 서버로만 전달하고, Python/Streamlit에는 전달하지 않습니다.
- Streamlit Custom Component v2의 `setStateValue`에는 공개 영상 메타데이터만 전달합니다.
- API 키는 localStorage, sessionStorage, Cookie, Streamlit Secrets에 저장하지 않습니다.
- 앱이 열린 동안 입력창 메모리에 키가 남아 있을 수 있습니다. '키 지우기' 또는 탭 닫기를 사용하세요.
- 앱 코드 및 브라우저 스크립트의 보안이 훼손되면 키가 유출될 수 있습니다. 공개 서비스에 쓰기 전 보안 검토가 필요합니다.
- Google Cloud에서 API 제한을 YouTube Data API v3로 한정하고, 웹사이트 제한을 배포 주소로 설정하세요. localhost 개발 환경은 별도로 설정·검증하세요.
- 브라우저 CORS 정책, Google 키 제한 설정에 따라 요청이 실패할 수 있습니다. 실기기에서 검증해야 합니다.

## 범위

이번 단계는 `videos.list`의 `mostPopular` 인기 영상 5개를 불러와 연결과 통신 경로를 테스트합니다. 키워드 검색은 추후 `search.list` 연동 시 별도 구현합니다.
