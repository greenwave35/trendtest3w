export default function(component) {
  const { parentElement, setStateValue } = component;
  const keyInput = parentElement.querySelector('#yt-api-key');
  const testBtn = parentElement.querySelector('#yt-test');
  const clearBtn = parentElement.querySelector('#yt-clear');
  const status = parentElement.querySelector('#yt-status');
  let controller = null;

  function message(text) { status.textContent = text; }

  clearBtn.addEventListener('click', () => {
    if (controller) controller.abort();
    keyInput.value = '';
    setStateValue('videos', []); // video data only, never the API key
    message('키를 지웠습니다. (브라우저에 영구 저장하지 않습니다.)');
  });

  testBtn.addEventListener('click', async () => {
    const apiKey = keyInput.value.trim();
    if (!apiKey) { message('먼저 API 키를 입력하세요.'); return; }
    testBtn.disabled = true;
    message('스마트폰/PC 브라우저에서 Google API에 직접 요청 중…');
    controller = new AbortController();
    try {
      // Using a request header avoids placing the API key in the URL.
      const url = new URL('https://www.googleapis.com/youtube/v3/videos');
      url.searchParams.set('part', 'snippet,statistics');
      url.searchParams.set('chart', 'mostPopular');
      url.searchParams.set('regionCode', 'KR');
      url.searchParams.set('maxResults', '5');
      const response = await fetch(url.toString(), {
        method: 'GET',
        headers: {'X-Goog-Api-Key': apiKey},
        signal: controller.signal,
        cache: 'no-store',
        referrerPolicy: 'strict-origin-when-cross-origin'
      });
      const payload = await response.json();
      if (!response.ok) {
        const reason = payload?.error?.message || `HTTP ${response.status}`;
        throw new Error(reason);
      }
      const safeRows = (payload.items || []).slice(0, 5).map(item => ({
        id: String(item.id || ''),
        title: String(item.snippet?.title || ''),
        publishedAt: String(item.snippet?.publishedAt || ''),
        views: Number(item.statistics?.viewCount || 0),
        likes: Number(item.statistics?.likeCount || 0),
        comments: Number(item.statistics?.commentCount || 0)
      }));
      // IMPORTANT: Only the sanitized data below crosses to Streamlit/Python.
      setStateValue('videos', safeRows);
      message(`연결 성공! ${safeRows.length}개의 영상 정보를 받았습니다. API 키는 Python으로 보내지 않았습니다.`);
    } catch (err) {
      if (err.name !== 'AbortError') {
        // Don't log or transmit credentials, request headers, or URL.
        message('연결 실패: ' + (err instanceof TypeError
          ? '브라우저 네트워크/CORS 차단 가능성. 개발자 도구 Network를 확인하세요.'
          : String(err.message).slice(0, 240)));
      }
    } finally {
      testBtn.disabled = false;
    }
  });

  return () => {
    if (controller) controller.abort();
    // Clear input when the component unmounts.
    keyInput.value = '';
  };
}
