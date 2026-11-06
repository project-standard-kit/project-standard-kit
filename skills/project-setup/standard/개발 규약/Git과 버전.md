---
title: Git과 버전
type: standard
part_of: "[[30 Areas/Development Standard/개발 규약|개발 규약]]"
section: 5
updated: 2026-11-07
language: ko
---

# Git과 버전

> [[30 Areas/Development Standard/개발 규약|개발 규약]] 5절. 버전과 변경 이력은 개발 규약 입구 문서에 둔다.

## 1. 브랜치: gitflow (팀 공통)

| 브랜치 | 출발 → 합치는 곳 | 용도 |
|---|---|---|
| `main` | – | 운영. 버전 태그가 붙은 커밋만 |
| `develop` | – | 개발. 다음 배포를 모은다 |
| `feature/<티켓 키>-<설명>` | develop → develop | 기능 작업. 하나로 묶어(squash) 합친다 |
| `release/<x.y.z>` | develop → main, develop | 배포 준비와 확인 |
| `hotfix/<x.y.z>` | main → main, develop | 운영 긴급 수정 |

- `main`·`develop`에는 직접 커밋하지 않는다. PR로만 합친다.
- 브랜치 이름은 소문자와 하이픈: `feature/BOOK-14-reserve-api`.
- 브랜치는 짧게 산다. 며칠을 넘기면 `develop`을 자주 받아 둔다. 합친 브랜치는 지운다.

## 2. 커밋 메시지

Conventional Commits + 티켓 키: `<종류>(<범위>): <티켓 키> <요약>`

- 예: `feat(rental): BOOK-14 예약 API 추가`
- 종류: `feat` 기능, `fix` 버그, `refactor` 동작 변화 없는 구조 변경, `test`, `docs`, `chore` 빌드·설정, `perf`.
- 범위는 도메인 이름(또는 모듈).
- 요약은 50자 안팎, 명령형, 끝에 마침표 없음. 본문에는 "왜"를 쓴다.
- 호환이 깨지는 변경은 `feat!:`처럼 `!`를 붙이고 본문에 `BREAKING CHANGE:`를 쓴다.
- squash로 합치므로 PR 제목이 이 형식을 따르면 된다.

## 3. 버전 태그: `vMAJOR.MINOR.PATCH`

| 자리 | 언제 올리나 |
|---|---|
| MAJOR | DB·API가 이전과 호환되지 않게 바뀔 때 |
| MINOR | 운영 배포(release)마다 |
| PATCH | hotfix마다 |

- 태그는 `main`의 합친 커밋에만 붙인다. 태그를 지우거나 옮기지 않는다.
- 첫 운영 배포는 `v0.1.0`이 기본이다. 정식 오픈 시점의 `v1.0.0`은 프로젝트가 정한다.

## 4. 프로젝트 셋업 때 정할 것

[[30 Areas/Development Standard/양식/프로젝트 개발 규약 양식|프로젝트 개발 규약]] 5절에 적는다.

| 항목 | 정할 내용 |
|---|---|
| 저장소 위치 | 원격(GitHub 등), 보호 브랜치 설정 |
| 티켓 키 | Jira 프로젝트 키(없으면 `E-<번호>` 규칙) |
| 다른 점 | gitflow와 다르게 가는 것이 있으면 이유와 함께(예: 앱 스토어 배포 주기) |
