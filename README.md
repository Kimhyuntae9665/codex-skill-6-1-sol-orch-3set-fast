# 6.1 Sol Orch · 3 SET Fast

**독립적인 작업 세 묶음을 병렬로 진행하고, 최종 결과는 한 명의 Sol이 통합·검증하는 Codex 스킬입니다.**

상위 Sol이 먼저 목표·검색 주제·담당 파일을 나눕니다. 각 SET은 자기 범위 안에서 탐색·조사·구현을 진행하고, 모든 모델은 **Fast 모드**를 요구합니다.

[English](README.en.md) · [스킬 지침](skills/6-1-sol-orch-3set-fast/SKILL.md) · [설치](#설치) · [분배 예시](examples/plan.json) · [Apache-2.0](LICENSE)

![상위 Sol이 세 SET에 독립적인 작업을 분배하고, 각 SET의 Sol·Luna 작업과 선택적 Astra 검토를 거쳐 같은 상위 Sol이 결과를 통합하는 구조](skills/6-1-sol-orch-3set-fast/assets/topology.png)

**위쪽 큰 Sol은 작업 분배, 아래쪽 큰 Sol은 최종 통합을 맡는 같은 총괄입니다.** SET 안의 반복된 Sol도 같은 리더의 처리 단계입니다. 점선은 필요할 때의 Astra 검토, 아래 곡선은 검토를 생략하는 경로입니다.

[구조도 원본 SVG 보기](skills/6-1-sol-orch-3set-fast/assets/topology.svg). 태양·달·별은 직접 만든 설명용 심볼이며 공식 모델 로고가 아닙니다. 그림은 목표 구조를 보여주며 실제 전체 동시 실행 기록은 아닙니다.

## 강점

### 1. 중복을 줄이는 선행 분배

실행 전에 상위 Sol이 **누가 무엇을 조사하고, 어떤 파일을 수정하고, 무엇을 낼지** 정합니다. 같은 질문을 여러 SET에 보내거나 같은 파일을 동시에 수정하는 배정을 막습니다. 선언된 분배표는 Python 검사 도구로 확인하고, 표현만 다른 같은 업무는 상위 Sol이 별도로 점검합니다.

### 2. 세 묶음의 독립적인 작업 진행

API·UI·사용 안내처럼 나눌 수 있는 일을 서로 다른 SET에 맡길 수 있습니다. 공통 계약을 먼저 확정하고 세트별 입력·출력을 정해, 서로의 결과를 기다릴 필요가 없는 구간을 병렬로 진행합니다. 의존하는 작업은 필요한 결과를 받은 뒤 시작합니다.

### 3. 전체 판단과 세부 실행의 책임 분리

상위 Sol은 전체 목표·세트 간 결정·최종 통합을, 각 SET의 Sol은 자기 작업의 세부 분담과 검증을 맡습니다. 자식에게는 해당 작업에 필요한 문맥과 범위만 전달합니다. 범위 변경과 세트 간 재배정은 상위 Sol을 거쳐야 합니다.

### 4. 모든 역할에 Fast 요구

총괄·세트 리더·Luna·Sol 작업자·Astra 모두 Fast를 요구합니다. 추론 수준과 속도 등급을 따로 관리하고, 실제 지원 여부와 설정·상속을 확인하게 합니다. Fast가 불가능한 역할을 Standard로 몰래 대체하지 않습니다.

### 5. 필요한 검토와 실행 한도 관리

Astra 검토는 보안·데이터 무결성·동시성 등 중요한 위험이 있을 때 추가합니다. 상위 Sol이 슬롯을 배분해 대기 중인 리더가 작업자 슬롯까지 점유하는 상황을 피하고, 환경의 실제 한도에 맞춰 실행 순서를 조절합니다.

이 강점들은 **실행 설계와 지침의 특성**입니다. 3배 속도, 토큰 절감률, 충돌 완전 방지는 측정하거나 보장하지 않았습니다.

## 기존 1 SET 스킬과 무엇이 달라졌나요?

| 항목 | [6-1-sol-orch](https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch) | 3 SET Fast |
| --- | --- | --- |
| 책임 구조 | 한 Sol이 분담·통합 | 상위 Sol + 최대 세 SET의 Sol 리더 |
| 분배 단위 | 개별 탐색·조사·구현 작업 | 세트별 패키지, 그 안의 개별 작업 |
| 중복 방지 | 범위 지정·단일 작성자 지침 | 같은 원칙 + 전역 분배표·작업 키·분배 검사 도구 |
| 실행 속도 등급 | 스킬 자체의 Fast 필수 조건 없음 | 모든 역할 Fast 필수 |
| 적용 대상 | 한 작업을 적절히 분담 | 독립적인 큰 작업 묶음을 함께 처리 |

## 역할과 모델

| 역할 | 모델 | 추론 | 속도 |
| --- | --- | --- | --- |
| 상위 총괄 | `gpt-6.1-sol` | medium | Fast 필수 |
| 각 SET 리더 | `gpt-6.1-sol` | medium | Fast 필수 |
| 각 SET 탐색자 | `gpt-6-luna` | high | Fast 필수 |
| 각 SET 조사자 | `gpt-6-luna` | high | Fast 필수 |
| 각 SET 구현 작업자 | `gpt-6.1-sol` | high | Fast 필수 |
| 필요 시 독립 검토자 | `gpt-6-astra` | low | Fast 필수 |

각 SET은 역할별로 최대 한 명만 동시에 사용합니다. 필요 없는 역할은 생략하고, 세트 리더가 다시 세 SET을 만드는 재귀 확장은 금지합니다. 작은 작업은 총괄이 직접 처리합니다.

## 설치

### Codex에 설치 요청

```text
이 GitHub 경로의 Codex 스킬을 설치해줘.
https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch-3set-fast/tree/main/skills/6-1-sol-orch-3set-fast
```

### 직접 설치

Git이 있는 환경에서 실행합니다. 아래는 공식 사용자 스킬 경로 `~/.agents/skills`를 사용합니다. 클라이언트가 다른 경로를 사용하면 실제 검색 경로를 확인하고 같은 스킬을 중복 설치하지 마세요.

**Windows PowerShell**

```powershell
git clone https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch-3set-fast.git
if ($LASTEXITCODE -ne 0) { throw 'Git clone failed.' }
$skillTarget = Join-Path $HOME '.agents/skills/6-1-sol-orch-3set-fast'
if (Test-Path -LiteralPath $skillTarget) { throw 'Skill already exists. Back it up before updating.' }
New-Item -ItemType Directory -Path (Split-Path $skillTarget) -Force | Out-Null
Copy-Item -LiteralPath './codex-skill-6-1-sol-orch-3set-fast/skills/6-1-sol-orch-3set-fast' -Destination $skillTarget -Recurse
```

**macOS / Linux**

```sh
(
  set -eu
  git clone https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch-3set-fast.git
  skill_target="$HOME/.agents/skills/6-1-sol-orch-3set-fast"
  if [ -e "$skill_target" ]; then
    echo 'Skill already exists. Back it up before updating.' >&2
    exit 1
  fi
  mkdir -p "$HOME/.agents/skills"
  cp -R ./codex-skill-6-1-sol-orch-3set-fast/skills/6-1-sol-orch-3set-fast "$skill_target"
)
```

프로젝트에서만 쓰려면 프로젝트의 `.agents/skills/6-1-sol-orch-3set-fast`에 같은 폴더를 복사합니다.

## 사용 예시

메인 모델은 Sol 6.1 / medium, Fast를 선택하고 하위 모델과 중첩 에이전트 호출을 사용할 수 있는지 확인하세요. 스킬 호출만으로 메인 모델이나 호스트 설정이 바뀌지는 않습니다.

```text
$6-1-sol-orch-3set-fast
계정 기능의 API·화면·사용 안내를 만들어줘.
공통 스키마는 상위 Sol이 먼저 확정하고, SET1은 API, SET2는 UI,
SET3은 문서를 담당해줘. 수정 파일과 작업 키의 중복을 검사한 뒤
진행하고, 마지막에 전체 동작과 문서의 일관성을 확인해줘.
```

```text
$6-1-sol-orch-3set-fast
이 12개 회사를 4개씩 세 SET으로 나눠 조사해줘.
회사와 조사 주제의 담당을 중복시키지 말고, 근거를 공통 형식으로 정리해줘.
상위 Sol이 평가 기준을 정하고 전체 결과를 비교해 최종 보고서를 만들어줘.
```

## 분배표 검사하기

Python 3.9+ 표준 라이브러리만 사용합니다. 저장소 루트에서 실행하세요.

```sh
python skills/6-1-sol-orch-3set-fast/scripts/check_plan.py examples/plan.json --workspace .
```

정상 계획은 종료 코드 `0`, 잘못된 계획은 `2`를 반환합니다. SET 간 파일·디렉터리 중복, 같은 작업 키, 담당 범위 밖 산출물, 의존성 순환 등을 검출합니다. 공유 입력 읽기는 허용합니다. 선언된 범위를 검사하며, OS 수준의 파일 잠금이나 의미상 같은 업무의 자동 판별 기능은 아닙니다.

## 실행 환경과 검증 범위

| 전체 동시 실행 슬롯 — 총괄 포함 | 실행 방식 |
| --- | --- |
| 13개 이상 | 총괄 1 + 리더 3 + SET별 작업자 최대 3 |
| 7~12개 | 세 SET을 띄우고 작업자 슬롯을 제한 |
| 3~6개 | 작업자 슬롯을 확보하며 SET을 단계적으로 실행 |
| 2개 이하 | 리더 직접 실행 또는 총괄 단독의 축소 구성 |

세 Astra를 기본 역할에 동시에 추가하면 총 16개 슬롯이 필요합니다. 보통은 완료된 작업자의 슬롯을 사용해 검토합니다. 스킬 자체가 호스트의 슬롯 한도를 늘리지는 않습니다.

Fast의 공식 설정은 `service_tier = "fast"`이며 요청 값 `priority`에 매핑됩니다. Fast 지원은 환경에 따라 다릅니다. 실제 제공 등급이 관측되지 않으면 Fast 설정·요청과 실제 관측 여부를 구분해 보고합니다. [런타임 절차](skills/6-1-sol-orch-3set-fast/references/runtime.md)

검증한 범위는 **분배 검사 17개, 스킬 형식·UI 메타데이터·링크·이미지 출처 확인, Astra의 세 가지 독립 시뮬레이션**입니다. 실제 13~16개 에이전트 동시 실행과 속도·토큰 절감률은 측정하지 않았습니다. [검증 기록](examples/validation-record.json)

```sh
python -m unittest discover -s tests -v
```

## 라이선스와 출처

[Apache License 2.0](LICENSE). 기존 [6-1-sol-orch](https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch)를 바탕으로 3 SET 계층, Fast 필수 조건, 전역 분배표와 검사 도구를 추가했습니다. 상위 프로젝트 출처는 [NOTICE](NOTICE), 도형 출처와 해시는 [이미지 출처](skills/6-1-sol-orch-3set-fast/assets/ATTRIBUTION.md)에 기록했습니다.

이 커뮤니티 프로젝트는 OpenAI와 제휴하거나 OpenAI의 공식 지원·보증을 받은 프로젝트가 아닙니다.

공식 자료: [Skills](https://learn.chatgpt.com/docs/build-skills) · [Speed](https://learn.chatgpt.com/docs/agent-configuration/speed) · [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [Configuration](https://learn.chatgpt.com/docs/config-file/config-reference)
