# Open-Tube Client

## 클라이언트 폴더 구조

```
📦client
 ┣ 📂.storybook
 ┃ ┗ 📜config.js (storybook.js UI 테스트 config)
 ┣ 📂src
 ┃ ┣ 📂components (View - 재사용 컴포넌트 모음)
 ┃ ┃ ┗ 📜page-main.js
 ┃ ┣ 📂css
 ┃ ┃ ┗ 📜foundation.min.css (foundation 프레임워크 css)
 ┃ ┣ 📂libs
 ┃ ┃ ┣ 📜actions.js (Controller)
 ┃ ┃ ┣ 📜litRender.js (lit-html sub module)
 ┃ ┃ ┣ 📜redux-zero.js (redux-zero module)
 ┃ ┃ ┗ 📜store.js (Store)
 ┃ ┣ 📂stories
 ┃ ┃ ┗ 📜index.stories.js (UI 테스트 코드)
 ┃ ┗ 📜main.js (Init 코드)
 ┣ 📂test
 ┃ ┗ 📜index.html (단위 테스트 코드)
 ┣ 📜.babelrc (바벨 설정)
 ┣ 📜.codebeatignore
 ┣ 📜.eslintignore
 ┣ 📜.eslintrc.js (EsLint 설정)
 ┣ 📜.gitignore
 ┣ 📜.travis.yml (Travis CI 설정)
 ┣ 📜index.css (전체 CSS)
 ┣ 📜index.html (전체 HTML)
 ┣ 📜package-lock.json
 ┣ 📜package.json (패키징 관리)
 ┣ 📜postcss.config.js
 ┣ 📜wct.conf.json
 ┗ 📜webpack.config.js (Webpack 설정)
```

## 테스트하기

* 개발과정 테스트
```bash
# client 폴더로 이동
cd client

# webpack-dev-server 실행
npm run dev

# UI 테스트
npm run storybook
```

* 배포 전 테스트
```bash
# Travis CI 자동 Build 검사
# 단위 테스트
npm test
```

## 배포하기
```bash
# Develop 버전 배포
npm run bundle

# Production 버전 배포
npm run production

## main-bundle.js 생성 후, server에서 구동
## (이후, 파이어베이스에서 사용할 예정)
```

## 기타

다른 세부사항은 `WIKI` 및 `Projects` 패널 참조