# 6.1 Sol Orch · 3 SET Fast

**세 팀은 시작했는데 결과가 합쳐지지 않는 문제를, 공통 계약과 한 명의 총괄로 다룹니다.**

독립적인 작업 세 묶음을 **동시에** 실행하는 Codex 스킬입니다. 총괄 Sol이 조사 주제·수정 파일·산출물을 먼저 나눕니다. 각 SET은 Sol 리더와 두 Luna·한 Sol 작업자를 병렬로 실행하고, 준비된 결과를 출처가 담긴 공유 JSON으로 전달합니다. 같은 총괄이 최종 결과를 검증·통합합니다. 모든 역할에 Fast를 요구하며, 필요한 경우 Astra 검토자를 추가합니다.

[English](README.en.md) · [스킬 지침](skills/6-1-sol-orch-3set-fast/SKILL.md) · [분배 예시](examples/plan.json) · [검증 기록](examples/validation-record.json) · [Apache-2.0](LICENSE)

![같은 총괄 Sol이 세 SET을 동시에 시작하고 공유 근거를 검증해 최종 결과로 통합하는 구조](skills/6-1-sol-orch-3set-fast/assets/topology.png)

위·아래의 큰 Sol은 **같은 총괄**이고, SET 안의 반복 Sol도 같은 리더의 처리 단계입니다. 점선은 선택적 Astra 검토입니다. 그림과 모델 배지는 직접 만든 설명용 도형이며 공식 로고가 아닙니다. [SVG 원본](skills/6-1-sol-orch-3set-fast/assets/topology.svg) · [출처](skills/6-1-sol-orch-3set-fast/assets/ATTRIBUTION.md)

## 설치하고 호출하기

Codex에 다음과 같이 요청합니다.

```text
아래 GitHub 경로의 Codex 스킬을 설치해줘.
기존 설치본이 있으면 스킬 검색 경로 밖에 원본을 백업한 뒤 교체해줘.
https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch-3set-fast/tree/main/skills/6-1-sol-orch-3set-fast
```

실행 환경을 확인한 뒤 현재 채팅의 총괄에게 요청합니다.

```text
$6-1-sol-orch-3set-fast
계정 기능의 API·화면·사용 안내를 만들어줘.
Sol 6.1/medium 리더를 쓰는 별도 로컬 SET 채팅 3개를 생성해줘.
세 채팅이 같은 절대 작업 경로를 사용하도록 하고,
SET1은 API, SET2는 UI, SET3은 문서를 맡아 동시에 시작해줘.
공통 스키마와 파일 소유권은 총괄이 먼저 확정해줘.
각 SET은 두 Luna/high와 한 Sol/high 작업자를 바로 병렬로 실행하고,
출처와 검증 결과를 공유 JSON으로 전달해줘. 모든 역할은 Fast를 사용해줘.
총괄은 결과를 읽고 해시·출처·전체 동작을 확인해 최종 통합해줘.
```

이 요청은 **SET 채팅 3개 생성**을 명시적으로 포함합니다. 별도 채팅은 대화 기록을 자동으로 공유하지 않습니다. 내부 하위 에이전트만 쓰려면 그 방식을 요청하고, 전체 계층을 실행할 수 있는 단일 채팅의 용량과 중첩 호출 지원을 확인해야 합니다. 설치나 문서 열람만으로 SET 채팅이 생성되지는 않습니다.

## 결과가 합쳐지는 방식

| 단계 | 책임과 산출물 |
| --- | --- |
| 총괄이 계약 확정 | 공통 입력·인터페이스, 중복 없는 작업 키, 파일별 단일 작성자, SET별 검증 기준 |
| 세 SET이 동시 실행 | 각 리더가 탐색·조사·작성을 바로 분담하고 준비된 결과부터 게시 |
| 공유 JSON으로 전달 | SET별 변경 불가 리비전, 원자적 게시, 사실·출처·불확실성, 수신 확인과 SHA-256 |
| 총괄이 통합 | 실행 ID·리비전·해시·출처를 확인하고 충돌하는 사실을 해결한 뒤 전체 결과 검증 |

한 SET이 끝나야 다음 SET을 시작하는 순차 구성은 허용하지 않습니다. 실행 전에 공통 계약을 정해 독립적으로 시작할 수 있게 나눕니다. 실제 산출물이 필요한 후속 작업만 근거를 기다리고, 다른 준비된 작업은 계속합니다. [분배 계약](skills/6-1-sol-orch-3set-fast/references/dispatch-contracts.md) · [정보 교환](skills/6-1-sol-orch-3set-fast/references/information-exchange.md)

## 모델과 실행 용량

| 역할 | 수 | 모델 / 추론 |
| --- | --- | --- |
| 총괄 | 1 | `gpt-6.1-sol` / medium |
| SET 리더 | 3 | `gpt-6.1-sol` / medium |
| 탐색자 | SET별 1 | `gpt-6-luna` / high |
| 조사자 | SET별 1 | `gpt-6-luna` / high |
| 작성·구현 작업자 | SET별 1 | `gpt-6.1-sol` / high |
| 선택적 독립 검토자 | SET별 최대 1 | `gpt-6-astra` / low |

**기본 13명, Astra 3명을 함께 추가하면 총 16명**입니다. 별도 SET 채팅마다 리더 포함 최소 4개 슬롯, 검토자까지 함께 쓰면 5개가 필요합니다. 총합 용량으로 개별 SET의 부족한 용량을 대신할 수 없습니다. 세 리더와 기본 자식 역할은 모두 실행하며, 자식은 다시 위임하지 않습니다.

메인 모델과 추론 수준은 호스트에서 선택합니다. 스킬 호출로 활성 총괄의 설정이 바뀌지 않으므로, 불일치는 [런타임 사전 확인](skills/6-1-sol-orch-3set-fast/references/runtime.md)에 따라 처리합니다.

실험 환경에서 확인한 전역 설정입니다. 기존 설정을 보존하고, 권한과 프로필·프로젝트 설정을 확인한 뒤 해당 키만 반영합니다.

```toml
service_tier = "priority"

[features]
fast_mode = true

[agents]
enabled = true
max_concurrent_threads_per_session = 16
```

공식 [하위 에이전트 설정](https://learn.chatgpt.com/docs/agent-configuration/subagents)에서 `max_concurrent_threads_per_session`은 기본 루트를 **제외한** 수입니다. 설정값 16은 루트 포함 17개를 허용하며, 실제 필요한 13명 또는 16명과 구분합니다. 설정 변경 후 새 실행 환경이 필요할 수 있으므로 각 SET 루트에서 실제 용량과 Fast 상속·덮어쓰기를 확인합니다. 전체 구조를 시작할 수 없으면 제한과 부분 결과를 보고합니다. 축소 구성으로 성공했다고 표시하지 않습니다.

공식 [Codex Fast 문서](https://learn.chatgpt.com/docs/agent-configuration/speed)는 `service_tier = "fast"`와 `features.fast_mode = true`를 안내합니다. [API Fast 문서](https://developers.openai.com/api/docs/guides/fast-mode)는 지원하는 API 모델에서 `fast`와 `priority`를 같은 동작으로 설명하며, 모든 Codex 호스트의 저장 설정에 같은 별칭이 적용된다는 증거는 아닙니다. 로컬 실험에서 확인한 설정은 `priority`와 `fast_mode = true`였고, 실제 서버 제공 등급은 관측되지 않아 `observed_tier: null`로 기록했습니다. 추론 수준·설정·실제 제공 등급을 구분합니다. [런타임 절차](skills/6-1-sol-orch-3set-fast/references/runtime.md) · [별도 SET 채팅](skills/6-1-sol-orch-3set-fast/references/three-session.md)

## 분배표 검사

Python 3.9+ 표준 라이브러리만 사용합니다. 저장소 루트에서 실행합니다.

```sh
python skills/6-1-sol-orch-3set-fast/scripts/check_plan.py examples/plan.json --workspace .
python -m unittest discover -s tests -v
```

계획 검사는 성공 시 `0`, 실패 시 `2`를 반환합니다. 버전 2 계획의 병렬 실행 선언·필요 용량, SET 간 파일 소유권·작업 키 중복, 범위 밖 산출물과 순차 SET 의존성을 확인합니다. 전역 계획 파일은 총괄에 예약됩니다. 공유 읽기는 허용합니다. 선언을 검사하는 도구이며 실제 실행 용량·파일 잠금·의미가 같은 조사 주제까지 자동 검증하지는 않습니다.

## 확인한 범위

2026-10-03, 새 로컬 채팅 3개가 각각 자식 4명(두 Luna·Sol·Astra)을 생성해 **총괄 1명 + SET 루트 리더 3명 + 자식 12명 = 16명이 약 35초 동안 겹쳐 실행**했습니다. 새 채팅마다 루트 포함 17개 슬롯을 표시했지만, 직접 확인한 실행은 SET별 루트와 자식 4명의 총 5명입니다. 이는 대기 상태를 유지한 용량 실험입니다.

별도 정보 교환 실험에서는 세 SET의 **11개 사실**을 공유 JSON으로 전달·통합하고, 생성 nonce·수신 기록·바이트 SHA-256과 출처를 확인했습니다. 총괄도 결과를 다시 검증했습니다. 로컬 공유 파일 전달을 확인한 것이며 자동 대화 공유나 다른 호스트의 파일 접근을 보장하지 않습니다.

**작업 속도 향상이나 토큰 절감률은 측정하지 않았고, 실제 Fast 제공 등급도 관측하지 못했습니다.** 검증 결과와 한계는 [검증 기록](examples/validation-record.json)에 정리합니다.

## 수동 설치

현재 [공식 스킬 문서](https://learn.chatgpt.com/docs/build-skills)의 사용자 경로는 `~/.agents/skills`, 저장소 경로는 `.agents/skills`입니다. 아래 절차는 기존 설치본을 활성 검색 경로 밖에 보존한 뒤 교체합니다. 백업은 이 설치 절차의 동작이며, 설치 도구가 자동으로 보장하는 기능은 아닙니다.

<details>
<summary>Windows PowerShell</summary>

```powershell
$ErrorActionPreference = 'Stop'
git clone https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch-3set-fast.git
if ($LASTEXITCODE -ne 0) { throw 'Git clone failed.' }
$skillTarget = Join-Path $HOME '.agents/skills/6-1-sol-orch-3set-fast'
if (Test-Path -LiteralPath $skillTarget) {
    $backupRoot = Join-Path $HOME '.agents/skill-backups'
    New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
    $skillBackup = Join-Path $backupRoot ('6-1-sol-orch-3set-fast-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
    Move-Item -LiteralPath $skillTarget -Destination $skillBackup
    Write-Output ('Preserved original: ' + $skillBackup)
}
New-Item -ItemType Directory -Path (Split-Path $skillTarget) -Force | Out-Null
Copy-Item -LiteralPath './codex-skill-6-1-sol-orch-3set-fast/skills/6-1-sol-orch-3set-fast' -Destination $skillTarget -Recurse
```

</details>

<details>
<summary>macOS / Linux</summary>

```sh
(
  set -eu
  git clone https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch-3set-fast.git
  skill_target="$HOME/.agents/skills/6-1-sol-orch-3set-fast"
  if [ -e "$skill_target" ]; then
    backup_root="$HOME/.agents/skill-backups"
    mkdir -p "$backup_root"
    skill_backup="$backup_root/6-1-sol-orch-3set-fast-$(date -u +%Y%m%dT%H%M%SZ)"
    test ! -e "$skill_backup"
    mv "$skill_target" "$skill_backup"
    printf 'Preserved original: %s\n' "$skill_backup"
  fi
  mkdir -p "$HOME/.agents/skills"
  cp -R ./codex-skill-6-1-sol-orch-3set-fast/skills/6-1-sol-orch-3set-fast "$skill_target"
)
```

</details>

## 라이선스와 출처

[Apache License 2.0](LICENSE). [6-1-sol-orch](https://github.com/Kimhyuntae9665/codex-skill-6-1-sol-orch)를 바탕으로 3 SET 병렬 구조, Fast 요구, 분배 검사와 공유 근거 통합을 추가했습니다. [NOTICE](NOTICE)에 상위 프로젝트 출처를 기록했습니다. OpenAI와 제휴하거나 공식 지원·보증을 받은 프로젝트가 아닙니다.

공식 자료: [Skills](https://learn.chatgpt.com/docs/build-skills) · [Speed](https://learn.chatgpt.com/docs/agent-configuration/speed) · [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [Configuration](https://learn.chatgpt.com/docs/config-file/config-reference)
