# project-standard-kit

새 프로젝트를 **질문에 고르기만 하면** 바로 개발할 수 있는 상태로 만들어 주는 Claude Code 플러그인입니다.

- `project-setup` 스킬: 프로젝트 기본 → 규모 → 환경(개발만 / 개발·운영 / 개발·검증·운영) → 인프라 → 코드 → API → 클라이언트 → 흐름 → 배포를 권장안과 함께 묻고, 답으로 문서·인프라 구성도·저장소·CI·배포 스크립트를 만듭니다.
- 표준 틀(`skills/project-setup/standard/`): 프로젝트 표준 틀, 개발 규약 15개(언어와 상관없는 공통 규칙은 자세히, 도구·인프라는 셋업 때 정할 자리로), 양식 7개(질문지 정본은 `양식/프로젝트 개발 규약 양식.md`).

## 설치

플러그인(권장):

```bash
claude plugin marketplace add project-standard-kit/project-standard-kit
claude plugin install project-standard-kit@project-standard-kit
```

스킬만 복사:

```bash
scripts/install.sh            # ~/.claude/skills/project-setup
scripts/install.sh --codex    # Codex(~/.agents/skills)에도
scripts/install.sh --vault    # 옵시디안 볼트에 표준 틀도 복사(있는 파일은 건너뜀)
```

## 쓰기

Claude Code에서 "새 프로젝트 셋업해 줘", 또는 직접 부르기: 플러그인 설치면 `/project-standard-kit:project-setup`, `install.sh` 설치면 `/project-setup`. 기획서가 있으면 먼저 위치를 알려 주면 권장안이 그 기획에 맞춰집니다.

## 설정(환경변수, 모두 선택)

| 변수 | 뜻 | 없으면 |
|---|---|---|
| `PROJECT_STANDARD_DIR` | 표준 틀 폴더(팀이 고친 틀) | 볼트 → 함께 배포된 사본 |
| `OBSIDIAN_VAULT_PATH` | 옵시디안 볼트. 문서는 `20 Projects/<프로젝트>/`에 | 문서 위치를 물음 |
| `WORKSPACE` | 코드 저장소 상위 폴더 | 지금 폴더를 권장안으로 물음 |
| `SECRETS_ROOT` | 비밀정보 파일 위치 | `~/.secrets`를 권장안으로 물음 |
| `BACKUP_ROOT` | 백업 위치 | 셋업 질문 B6에서 정함 |

## 기대는 것

- 개발 규약 13절(티켓 진행 방식)은 `ticket-workflow` 같은 티켓 단위 에이전트 절차를 가정한다. 이 패키지에 들어 있지 않으며, 없으면 같은 7단계를 쓰는 절차로 대신한다.
- 문서 링크는 옵시디안 위키링크(`[[30 Areas/Development Standard/...]]`)다. 볼트의 그 경로에 틀을 두면(`install.sh --vault`) 열린다.

## 하지 않는 것

비밀정보 값 입력, 계정 로그인, 유료 자원 생성, 서버 접속, 이슈 트래커 생성, 원격 저장소 공개, 운영 배포는 할 일 목록으로 남기고 사람이 합니다.

## 업데이트

틀이 바뀌면 플러그인 버전이 오릅니다. 받으려면:

```bash
claude plugin marketplace update project-standard-kit
claude plugin update project-standard-kit@project-standard-kit
```

## 틀 갱신(관리자)

`skills/project-setup/standard/`와 `.claude-plugin/*.json`의 `version`은 자동으로 만들어집니다. 직접 고치지 마세요.
원본 틀은 관리자의 비공개 저장소에 있고, 원본이 바뀌면 그 저장소의 CI가 `scripts/build_standard.py`로 사본을 만들어(개인 경로·이름·변경 이력을 걷어내고, 남으면 실패) 이 저장소에 커밋합니다. 버전은 원본 틀 `version`(v0.14 → 0.14.0)을 따릅니다.

로컬 확인:

```bash
python3 scripts/build_standard.py <원본 틀 폴더>
claude plugin validate .
```
