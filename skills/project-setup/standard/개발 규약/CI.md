---
title: CI (자동 검사)
type: standard
part_of: "[[30 Areas/Development Standard/개발 규약|개발 규약]]"
section: 6
updated: 2026-11-07
language: ko
---

# CI (자동 검사)

> [[30 Areas/Development Standard/개발 규약|개발 규약]] 6절. 버전과 변경 이력은 개발 규약 입구 문서에 둔다.

## 공통 규칙

- **검사 진입점은 저장소마다 하나다.** 로컬과 CI가 같은 명령을 돌린다. 사람도 AI 작업자도 PR 전에 이것 하나만 통과시키면 된다.
- 진입점은 아래 일곱 가지를 모두 포함한다. 빠른 것부터 돌리고 처음 실패에서 멈춘다.
  1. 포맷 확인
  2. 린트
  3. 타입 검사
  4. 아키텍처 테스트([[30 Areas/Development Standard/개발 규약/아키텍처 레이어|1절]])
  5. 테스트
  6. 의존성 취약점
  7. 비밀정보 노출
- CI는 PR마다 돈다. 커밋 훅에서 일부를 먼저 돌려도 CI는 전체를 다시 돈다.
- 실패한 검사를 끄거나 건너뛰어 PR을 통과시키지 않는다. 불안정한 테스트는 [[30 Areas/Development Standard/개발 규약/테스트|8절]]대로 격리하고 티켓을 만든다.
- **예산 예외 규칙.** CI가 요금·사용 시간 부족으로 돌지 못하면, 같은 진입점을 로컬에서 통과시킨 결과를 PR에 붙이는 것으로 대신한다. 그래서 CI를 "통과해야만 합칠 수 있는 필수 검사"로 걸지 않는다. 검사 자체가 실패한 경우는 예외가 아니다.

## 프로젝트 셋업 때 정할 것

[[30 Areas/Development Standard/양식/프로젝트 개발 규약 양식|프로젝트 개발 규약]] 6절에 적는다.

| 항목 | 정할 내용 |
|---|---|
| 진입점 | 명령 이름 |
| 종류별 도구 | 일곱 가지 각각을 무엇으로 검사하나. 해당 없으면 이유 |
| CI 서비스 | 어디서 도나, 트리거 |

## 예

팀 기본값(Python 서비스): `scripts/check.sh`가 `ruff format --check` → `ruff check` → `pyright` → `lint-imports` → `pytest` → `pip-audit` → `gitleaks`를 차례로 돌린다. GitHub Actions에서 PR마다.
