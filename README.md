# 한전 AI 업무활용 실습교재

- 웹 교재: https://jhs512.github.io/chuncheon-ai-workbook/
- 노션 교재: https://jangka44.notion.site/AI-3f6d4cdd4f478194a8dbda7adef5ccbd

Windows의 ChatGPT·Claude 앱과 Gemini 웹을 사용하는 6시간 실습교재입니다.
`content/`의 마크다운이 원본이며 `docs/`는 GitHub Pages 배포본입니다.
교재에 참조된 승인 캡처와 실습 자료만 포함합니다.
실습 예제의 수치와 문서는 학습용 자료이며 실제 기관의 내부자료로 해석하지 않습니다.

## 갱신

`content/`의 원본 Markdown을 수정한 뒤 다음 명령으로 웹 배포본을 다시 생성합니다.

```sh
python -m pip install -r requirements.txt
python scripts/build.py
```

춘천 제작 작업 폴더에서는 `.prep/build_github_pages.py`로 최신 원본과 자료를 이 저장소에 반영합니다.
게시 설정은 main 브랜치의 /docs 폴더입니다. `content/manifest.json`에 원본·게시 파일의 SHA-256을 기록합니다.
