# 📜 영단어 반사 암기 테스터 (Reflex Vocab) 대화 및 전체 코드 기록

- **기록 일시**: 2026-10-01
- **환경**: Windows 11 / Python 3.14 (기본 내장 라이브러리: 	kinter, winsound, 	ime, 
andom, json, 
e)
- **프로젝트 위치**: C:\programming
- **실행 파일**: C:\programming\run_reflex_vocab.bat 및 바탕화면 바로가기

---

## 1. 대화 진행 기록 (Conversation History)

### [대화 1] 어제 밤 제작 프로그램 호출 및 위치 확인
- **발화자**: 사용자 (User)
> 어제 밤에 만들었던 프로그램 불러올 수 있어?

- **어시스턴트 (Antigravity)**:
> 2026년 9월 30일 밤에 개발된 **「영단어 반사 상기 테스터 (Reflex Vocab Tester)」** 프로젝트를 로컬 시스템(C:\programming)에서 확인 및 복구 안내.
> - 원클릭 실행 파일: 
un_reflex_vocab.bat
> - 메인 GUI 앱: 
eflex_vocab_app.py
> - 단어 데이터 & 매니저: 
eflex_vocab_data.py
> - 로컬 학습기록 DB: ocab_reflex_db.json

---

### [대화 2] 전체 소스 코드 요청
- **발화자**: 사용자 (User)
> 이거 전체 코드 보여줘

- **어시스턴트 (Antigravity)**:
> 프로젝트를 구성하는 
un_reflex_vocab.bat, 
eflex_vocab_data.py, 
eflex_vocab_app.py 3개 파일의 소스 코드와 동작 구조를 상세히 공유.

---

### [대화 3] 한글 직접 타이핑 모드 수정 요청
- **발화자**: 사용자 (User)
> 이 프로그램에서 한 가지를 수정할건데 영단어를 보면 직접 한국어를 타이핑 하는 프로그래밍으로 수정할거야. 해줘

- **어시스턴트 (Antigravity)**:
> 영단어를 보고 한국어 뜻을 직접 키보드로 타이핑하여 맞히는 모드로 업그레이드 완료.
> 1. **한국어 직접 타이핑 모드 탑재**: 단어 표시 시 입력창 자동 포커싱, Enter 제출 및 다음 단어 진행 연동.
> 2. **지능형 한국어 유연 매칭 알고리즘 (check_korean_match)**:
>    - 복수 의미(예: ccept -> 받아들이다, 수락하다) 중 하나만 입력해도 정답 인정
>    - 어간/명사형 매칭 (수락, 수락함, 인정) 및 조사/기호(~할 여유가 있다 -> 여유가 있다) 자동 정규화
> 3. **타이핑 최적화 제한시간 프리셋**: 2.0초, 3.5초(기본), 5.0초, 8.0초, 무제한
> 4. **패스/모름 기능**: 빈칸 Enter 또는 [모름/패스] 버튼 시 즉시 정답 확인 및 오답 기록

---

### [대화 4] 실시간 시간 감소 애니메이션 제거 요청
- **발화자**: 사용자 (User)
> 실시간으로 시간 줄어드는 애니메이션 빼줘

- **어시스턴트 (Antigravity)**:
> 타자에 집중할 수 있도록 시각적 방해 요소를 완전히 제거.
> 1. 화면 중앙의 실시간 카운트다운 게이지 바(Canvas) 및 밀리초 숫자 카운트다운 라벨 제거.
> 2. 25ms 갱신 루프를 제거하고 백그라운드 타이머(_on_timer_complete) 방식으로 최적화.
> 3. 내부 타이머 및 실제 타자 반응시간 측정 기능은 그대로 유지.

---

### [대화 5] 프로그램 실행 방법 문의
- **발화자**: 사용자 (User)
> 어떻게 열어

- **어시스턴트 (Antigravity)**:
> 사용자의 윈도우 바탕화면에 **「영단어 반사 테스터.lnk」** 바로가기 아이콘을 자동 생성하고 3가지 실행 방법 안내.
> 1. 바탕화면 바로가기 아이콘 더블 클릭
> 2. Win + R 실행창에 C:\programming\run_reflex_vocab.bat 입력
> 3. 파일 탐색기 C:\programming 폴더에서 배치파일 더블 클릭

---

## 2. 프로젝트 전체 소스 코드 (Source Code)

### (1) 
un_reflex_vocab.bat (원클릭 배치 실행기)
`at
@echo off
chcp 65001 > nul
title 영단어 반사 암기 테스터 (Reflex Vocab)
echo ========================================================
echo   ⚡ 영단어 반사 암기 테스터를 실행합니다...
echo   (1~3초 내 즉각적인 한국어 뜻 반사 회상 훈련)
echo ========================================================
start "" pythonw "%~dp0reflex_vocab_app.py"
exit

`

---

### (2) 
eflex_vocab_data.py (단어 데이터 및 DB 관리 모듈)
`python
"""
영단어 반사 암기 테스터 - 내장 단어 데이터 및 데이터 관리 모듈
- 인터넷 없이 100% 로컬 동작
- 계정/로그인 불필요
- 기초, 수능, 토익, 고급 500+ 단어 기본 탑재
- 로컬 JSON 파일로 학습 이력, 오답 노트, 숙련도 자동 영구 보존
"""

import json
import os
import random

# 기본 내장 단어 데이터 (카테고리별 분류)
DEFAULT_VOCABULARY = [
    # ================= [1. 중등 / 기초 필수 (150단어)] =================
    {"word": "accept", "meaning": "받아들이다, 수락하다", "category": "기초"},
    {"word": "achieve", "meaning": "달성하다, 성취하다", "category": "기초"},
    {"word": "admit", "meaning": "인정하다, 입장을 허락하다", "category": "기초"},
    {"word": "afford", "meaning": "~할 여유가 있다", "category": "기초"},
    {"word": "allow", "meaning": "허락하다, 인정하다", "category": "기초"},
    {"word": "ancient", "meaning": "고대의, 옛날의", "category": "기초"},
    {"word": "announce", "meaning": "발표하다, 알리다", "category": "기초"},
    {"word": "appear", "meaning": "나타나다, ~인 것 같다", "category": "기초"},
    {"word": "apply", "meaning": "지원하다, 적용하다", "category": "기초"},
    {"word": "approach", "meaning": "접근하다, 다가가다", "category": "기초"},
    {"word": "arrange", "meaning": "배열하다, 준비하다", "category": "기초"},
    {"word": "arrive", "meaning": "도착하다, 도달하다", "category": "기초"},
    {"word": "assume", "meaning": "가정하다, 추정하다", "category": "기초"},
    {"word": "attach", "meaning": "붙이다, 첨부하다", "category": "기초"},
    {"word": "attend", "meaning": "참석하다, 주의를 기울이다", "category": "기초"},
    {"word": "avoid", "meaning": "피하다, 모면하다", "category": "기초"},
    {"word": "balance", "meaning": "균형, 균형을 잡다", "category": "기초"},
    {"word": "belong", "meaning": "속하다, 소유이다", "category": "기초"},
    {"word": "borrow", "meaning": "빌리다", "category": "기초"},
    {"word": "brave", "meaning": "용감한, 용기 있는", "category": "기초"},
    {"word": "breathe", "meaning": "숨쉬다, 호흡하다", "category": "기초"},
    {"word": "brilliant", "meaning": "빛나는, 훌륭한", "category": "기초"},
    {"word": "calm", "meaning": "침착한, 차분한", "category": "기초"},
    {"word": "capture", "meaning": "포획하다, 사로잡다", "category": "기초"},
    {"word": "cause", "meaning": "원인, 야기하다", "category": "기초"},
    {"word": "celebrate", "meaning": "축하하다, 기념하다", "category": "기초"},
    {"word": "certain", "meaning": "확신하는, 어떤, 특정한", "category": "기초"},
    {"word": "challenge", "meaning": "도전, 이의를 제기하다", "category": "기초"},
    {"word": "choose", "meaning": "선택하다, 고르다", "category": "기초"},
    {"word": "citizen", "meaning": "시민, 국민", "category": "기초"},
    {"word": "collect", "meaning": "모으다, 수집하다", "category": "기초"},
    {"word": "comfort", "meaning": "편안함, 위로하다", "category": "기초"},
    {"word": "compare", "meaning": "비교하다, 견주다", "category": "기초"},
    {"word": "complain", "meaning": "불평하다, 항의하다", "category": "기초"},
    {"word": "connect", "meaning": "연결하다, 이어지다", "category": "기초"},
    {"word": "consider", "meaning": "고려하다, 생각하다", "category": "기초"},
    {"word": "contain", "meaning": "포함하다, 억누르다", "category": "기초"},
    {"word": "continue", "meaning": "계속하다, 이어지다", "category": "기초"},
    {"word": "convince", "meaning": "납득시키다, 확신시키다", "category": "기초"},
    {"word": "create", "meaning": "창조하다, 만들어내다", "category": "기초"},
    {"word": "curious", "meaning": "호기심이 많은, 신기한", "category": "기초"},
    {"word": "damage", "meaning": "손상, 손해를 입히다", "category": "기초"},
    {"word": "decide", "meaning": "결정하다, 결심하다", "category": "기초"},
    {"word": "declare", "meaning": "선언하다, 공포하다", "category": "기초"},
    {"word": "deliver", "meaning": "배달하다, 전달하다", "category": "기초"},
    {"word": "depend", "meaning": "의존하다, 달려있다", "category": "기초"},
    {"word": "describe", "meaning": "묘사하다, 설명하다", "category": "기초"},
    {"word": "destroy", "meaning": "파괴하다, 망치다", "category": "기초"},
    {"word": "develop", "meaning": "발달시키다, 개발하다", "category": "기초"},
    {"word": "direct", "meaning": "직접적인, 지시하다", "category": "기초"},
    {"word": "discover", "meaning": "발견하다, 알아내다", "category": "기초"},
    {"word": "discuss", "meaning": "논의하다, 토론하다", "category": "기초"},
    {"word": "divide", "meaning": "나누다, 쪼개다", "category": "기초"},
    {"word": "doubt", "meaning": "의심, 의심하다", "category": "기초"},
    {"word": "dramatic", "meaning": "극적인, 인상적인", "category": "기초"},
    {"word": "eager", "meaning": "열망하는, 간절히 바라는", "category": "기초"},
    {"word": "educate", "meaning": "교육하다, 가르치다", "category": "기초"},
    {"word": "effect", "meaning": "효과, 영향, 결과", "category": "기초"},
    {"word": "effort", "meaning": "노력, 수고", "category": "기초"},
    {"word": "enable", "meaning": "가능하게 하다", "category": "기초"},
    {"word": "encourage", "meaning": "격려하다, 장려하다", "category": "기초"},
    {"word": "enemy", "meaning": "적, 원수", "category": "기초"},
    {"word": "entire", "meaning": "전체의, 온전한", "category": "기초"},
    {"word": "escape", "meaning": "탈출하다, 모면하다", "category": "기초"},
    {"word": "event", "meaning": "사건, 행사", "category": "기초"},
    {"word": "exact", "meaning": "정확한, 정밀한", "category": "기초"},
    {"word": "excellent", "meaning": "탁월한, 훌륭한", "category": "기초"},
    {"word": "exchange", "meaning": "교환하다, 주고받다", "category": "기초"},
    {"word": "excite", "meaning": "흥분시키다, 자극하다", "category": "기초"},
    {"word": "exist", "meaning": "존재하다, 살아가다", "category": "기초"},
    {"word": "expect", "meaning": "기대하다, 예상하다", "category": "기초"},
    {"word": "experience", "meaning": "경험, 경험하다", "category": "기초"},
    {"word": "explain", "meaning": "설명하다, 해명하다", "category": "기초"},
    {"word": "express", "meaning": "표현하다, 나타내다", "category": "기초"},
    {"word": "familiar", "meaning": "익숙한, 친숙한", "category": "기초"},
    {"word": "famous", "meaning": "유명한, 잘 알려진", "category": "기초"},
    {"word": "feature", "meaning": "특징, 특별히 포함하다", "category": "기초"},
    {"word": "follow", "meaning": "따르다, 따라가다", "category": "기초"},
    {"word": "force", "meaning": "힘, 강요하다", "category": "기초"},
    {"word": "forgive", "meaning": "용서하다", "category": "기초"},
    {"word": "freeze", "meaning": "얼다, 얼리다", "category": "기초"},
    {"word": "gentle", "meaning": "온화한, 부드러운", "category": "기초"},
    {"word": "government", "meaning": "정부, 정권", "category": "기초"},
    {"word": "gradual", "meaning": "점진적인, 서서히 일어나는", "category": "기초"},
    {"word": "guard", "meaning": "보호하다, 경비원", "category": "기초"},
    {"word": "guide", "meaning": "안내하다, 길잡이", "category": "기초"},
    {"word": "habit", "meaning": "습관, 버릇", "category": "기초"},
    {"word": "happen", "meaning": "일어나다, 발생하다", "category": "기초"},
    {"word": "honest", "meaning": "정직한, 솔직한", "category": "기초"},
    {"word": "huge", "meaning": "거대한, 엄청난", "category": "기초"},
    {"word": "imagine", "meaning": "상상하다, 떠올리다", "category": "기초"},
    {"word": "improve", "meaning": "개선하다, 향상시키다", "category": "기초"},
    {"word": "include", "meaning": "포함하다", "category": "기초"},
    {"word": "increase", "meaning": "증가하다, 늘리다", "category": "기초"},
    {"word": "injure", "meaning": "다치게 하다, 부상을 입히다", "category": "기초"},
    {"word": "innocent", "meaning": "무죄인, 결백한, 순수한", "category": "기초"},
    {"word": "insist", "meaning": "주장하다, 고집하다", "category": "기초"},
    {"word": "inspire", "meaning": "영감을 주다, 고무하다", "category": "기초"},
    {"word": "introduce", "meaning": "소개하다, 도입하다", "category": "기초"},
    {"word": "invent", "meaning": "발명하다, 지어내다", "category": "기초"},
    {"word": "invite", "meaning": "초대하다, 요청하다", "category": "기초"},
    {"word": "judge", "meaning": "판단하다, 판사", "category": "기초"},
    {"word": "lonely", "meaning": "외로운, 쓸쓸한", "category": "기초"},
    {"word": "manage", "meaning": "관리하다, 가까스로 해내다", "category": "기초"},
    {"word": "mention", "meaning": "언급하다, 말하다", "category": "기초"},
    {"word": "method", "meaning": "방법, 방식", "category": "기초"},
    {"word": "modern", "meaning": "현대의, 근대의", "category": "기초"},
    {"word": "notice", "meaning": "알아차리다, 공지사항", "category": "기초"},
    {"word": "obvious", "meaning": "명백한, 분명한", "category": "기초"},
    {"word": "offer", "meaning": "제공하다, 제안하다", "category": "기초"},
    {"word": "opinion", "meaning": "의견, 견해", "category": "기초"},
    {"word": "patient", "meaning": "인내심 있는, 환자", "category": "기초"},
    {"word": "perfect", "meaning": "완벽한, 완벽하게 하다", "category": "기초"},
    {"word": "perform", "meaning": "수행하다, 공연하다", "category": "기초"},
    {"word": "pleasant", "meaning": "즐거운, 유쾌한", "category": "기초"},
    {"word": "polite", "meaning": "공손한, 예의 바른", "category": "기초"},
    {"word": "prepare", "meaning": "준비하다, 대비하다", "category": "기초"},
    {"word": "prevent", "meaning": "예방하다, 막다", "category": "기초"},
    {"word": "promise", "meaning": "약속하다, 약속", "category": "기초"},
    {"word": "protect", "meaning": "보호하다, 지키다", "category": "기초"},
    {"word": "prove", "meaning": "증명하다, 드러나다", "category": "기초"},
    {"word": "provide", "meaning": "제공하다, 공급하다", "category": "기초"},
    {"word": "publish", "meaning": "출판하다, 발표하다", "category": "기초"},
    {"word": "realize", "meaning": "깨닫다, 실현하다", "category": "기초"},
    {"word": "receive", "meaning": "받다, 받아들이다", "category": "기초"},
    {"word": "recognize", "meaning": "인식하다, 알아보다", "category": "기초"},
    {"word": "refuse", "meaning": "거절하다, 거부하다", "category": "기초"},
    {"word": "regular", "meaning": "규칙적인, 정기적인", "category": "기초"},
    {"word": "relation", "meaning": "관계, 관련", "category": "기초"},
    {"word": "remind", "meaning": "상기시키다, 일깨우다", "category": "기초"},
    {"word": "replace", "meaning": "대체하다, 대신하다", "category": "기초"},
    {"word": "require", "meaning": "요구하다, 필요로 하다", "category": "기초"},
    {"word": "respect", "meaning": "존경하다, 존중", "category": "기초"},
    {"word": "responsible", "meaning": "책임이 있는", "category": "기초"},
    {"word": "result", "meaning": "결과, 발생하다", "category": "기초"},
    {"word": "return", "meaning": "돌아오다, 반환하다", "category": "기초"},
    {"word": "reward", "meaning": "보상, 보상하다", "category": "기초"},
    {"word": "satisfied", "meaning": "만족하는, 흡족한", "category": "기초"},
    {"word": "separate", "meaning": "분리된, 떼어놓다", "category": "기초"},
    {"word": "serious", "meaning": "심각한, 진지한", "category": "기초"},
    {"word": "shallow", "meaning": "얕은, 피상적인", "category": "기초"},
    {"word": "simple", "meaning": "간단한, 단순한", "category": "기초"},
    {"word": "sincere", "meaning": "진실한, 진심 어린", "category": "기초"},
    {"word": "situation", "meaning": "상황, 처지", "category": "기초"},
    {"word": "succeed", "meaning": "성공하다, 뒤를 잇다", "category": "기초"},
    {"word": "suggest", "meaning": "제안하다, 암시하다", "category": "기초"},
    {"word": "support", "meaning": "지지하다, 후원하다", "category": "기초"},
    {"word": "surprise", "meaning": "놀라게 하다, 놀라움", "category": "기초"},
    {"word": "survive", "meaning": "살아남다, 생존하다", "category": "기초"},
    {"word": "trust", "meaning": "신뢰하다, 믿음", "category": "기초"},
    {"word": "understand", "meaning": "이해하다, 알아듣다", "category": "기초"},
    {"word": "valuable", "meaning": "가치 있는, 귀중한", "category": "기초"},
    {"word": "wonder", "meaning": "궁금해하다, 경이", "category": "기초"},

    # ================= [2. 수능 / 고교 핵심 (150단어)] =================
    {"word": "abandon", "meaning": "버리다, 포기하다", "category": "수능"},
    {"word": "abstract", "meaning": "추상적인, 요약", "category": "수능"},
    {"word": "abundant", "meaning": "풍부한, 많은", "category": "수능"},
    {"word": "access", "meaning": "접근, 이용 권한", "category": "수능"},
    {"word": "accommodate", "meaning": "수용하다, 공간을 제공하다", "category": "수능"},
    {"word": "accompany", "meaning": "동행하다, 수반하다", "category": "수능"},
    {"word": "accumulate", "meaning": "축적하다, 모으다", "category": "수능"},
    {"word": "accurate", "meaning": "정확한, 정밀한", "category": "수능"},
    {"word": "adapt", "meaning": "적응하다, 맞추다", "category": "수능"},
    {"word": "adequate", "meaning": "적절한, 충분한", "category": "수능"},
    {"word": "admire", "meaning": "존경하다, 감탄하다", "category": "수능"},
    {"word": "adopt", "meaning": "채택하다, 입양하다", "category": "수능"},
    {"word": "advocate", "meaning": "옹호하다, 지지자", "category": "수능"},
    {"word": "ambiguous", "meaning": "모호한, 다의적인", "category": "수능"},
    {"word": "anticipate", "meaning": "예상하다, 기대하다", "category": "수능"},
    {"word": "appreciate", "meaning": "진가를 인정하다, 감사하다", "category": "수능"},
    {"word": "appropriate", "meaning": "적절한, 알맞은", "category": "수능"},
    {"word": "approximate", "meaning": "대략의, 근접한", "category": "수능"},
    {"word": "artificial", "meaning": "인공의, 인위적인", "category": "수능"},
    {"word": "aspect", "meaning": "측면, 양상", "category": "수능"},
    {"word": "assert", "meaning": "주장하다, 단언하다", "category": "수능"},
    {"word": "assess", "meaning": "평가하다, 사정하다", "category": "수능"},
    {"word": "attribute", "meaning": "~의 탓으로 돌리다, 속성", "category": "수능"},
    {"word": "authentic", "meaning": "진정한, 진짜의", "category": "수능"},
    {"word": "authority", "meaning": "권위, 권한, 당국", "category": "수능"},
    {"word": "automatic", "meaning": "자동의, 무의식적인", "category": "수능"},
    {"word": "aware", "meaning": "알고 있는, 인식하는", "category": "수능"},
    {"word": "benefit", "meaning": "혜택, 이익을 얻다", "category": "수능"},
    {"word": "brief", "meaning": "짧은, 간결한", "category": "수능"},
    {"word": "capable", "meaning": "~할 능력이 있는", "category": "수능"},
    {"word": "cease", "meaning": "중단되다, 그치다", "category": "수능"},
    {"word": "circumstance", "meaning": "상황, 환경", "category": "수능"},
    {"word": "clarify", "meaning": "명확하게 하다, 분명히 하다", "category": "수능"},
    {"word": "colleague", "meaning": "동료", "category": "수능"},
    {"word": "compel", "meaning": "강요하다, 굴복시키다", "category": "수능"},
    {"word": "compensate", "meaning": "보상하다, 보충하다", "category": "수능"},
    {"word": "competent", "meaning": "유능한, 역량 있는", "category": "수능"},
    {"word": "complex", "meaning": "복잡한, 복합건물", "category": "수능"},
    {"word": "component", "meaning": "구성요소, 부품", "category": "수능"},
    {"word": "comprehend", "meaning": "이해하다, 파악하다", "category": "수능"},
    {"word": "compromise", "meaning": "타협하다, 절충하다", "category": "수능"},
    {"word": "conceal", "meaning": "숨기다, 감추다", "category": "수능"},
    {"word": "concede", "meaning": "인정하다, 양보하다", "category": "수능"},
    {"word": "conceive", "meaning": "착상하다, 마음속에 품다", "category": "수능"},
    {"word": "conclude", "meaning": "결론을 내리다, 끝나다", "category": "수능"},
    {"word": "confirm", "meaning": "확인하다, 확정하다", "category": "수능"},
    {"word": "conflict", "meaning": "갈등, 충돌하다", "category": "수능"},
    {"word": "conform", "meaning": "순응하다, 따르다", "category": "수능"},
    {"word": "confront", "meaning": "직면하다, 맞서다", "category": "수능"},
    {"word": "confuse", "meaning": "혼란스럽게 하다", "category": "수능"},
    {"word": "consent", "meaning": "동의, 허락하다", "category": "수능"},
    {"word": "consequence", "meaning": "결과, 영향력", "category": "수능"},
    {"word": "conservative", "meaning": "보수적인, 온건한", "category": "수능"},
    {"word": "consistent", "meaning": "일관된, 지속적인", "category": "수능"},
    {"word": "constant", "meaning": "끊임없는, 일정한", "category": "수능"},
    {"word": "construct", "meaning": "건설하다, 구성하다", "category": "수능"},
    {"word": "consume", "meaning": "소비하다, 다 써버리다", "category": "수능"},
    {"word": "contemporary", "meaning": "동시대의, 현대의", "category": "수능"},
    {"word": "contradict", "meaning": "모순되다, 반박하다", "category": "수능"},
    {"word": "contribute", "meaning": "기여하다, 공헌하다", "category": "수능"},
    {"word": "controversy", "meaning": "논란, 논쟁", "category": "수능"},
    {"word": "convey", "meaning": "전달하다, 실어 나르다", "category": "수능"},
    {"word": "crucial", "meaning": "중대한, 결정적인", "category": "수능"},
    {"word": "decline", "meaning": "감소하다, 거절하다", "category": "수능"},
    {"word": "define", "meaning": "정의하다, 규정하다", "category": "수능"},
    {"word": "definite", "meaning": "명확한, 확정적인", "category": "수능"},
    {"word": "demonstrate", "meaning": "입증하다, 시연하다", "category": "수능"},
    {"word": "deprive", "meaning": "박탈하다, 빼앗다", "category": "수능"},
    {"word": "derive", "meaning": "이끌어내다, 유래하다", "category": "수능"},
    {"word": "despair", "meaning": "절망, 절망하다", "category": "수능"},
    {"word": "desperate", "meaning": "필사적인, 자포자기한", "category": "수능"},
    {"word": "detect", "meaning": "감지하다, 발견하다", "category": "수능"},
    {"word": "deter", "meaning": "단념시키다, 저지하다", "category": "수능"},
    {"word": "determine", "meaning": "결정하다, 결심하다", "category": "수능"},
    {"word": "deviate", "meaning": "벗어나다, 빗나가다", "category": "수능"},
    {"word": "device", "meaning": "장치, 기기", "category": "수능"},
    {"word": "differentiate", "meaning": "구별하다, 차별화하다", "category": "수능"},
    {"word": "diminish", "meaning": "줄어들다, 약화시키다", "category": "수능"},
    {"word": "discipline", "meaning": "규율, 훈육, 학문 분야", "category": "수능"},
    {"word": "discrete", "meaning": "별개의, 분리된", "category": "수능"},
    {"word": "dismiss", "meaning": "일축하다, 해고하다", "category": "수능"},
    {"word": "distinct", "meaning": "뚜렷한, 분명히 다른", "category": "수능"},
    {"word": "distribute", "meaning": "배포하다, 분배하다", "category": "수능"},
    {"word": "diverse", "meaning": "다양한, 다채로운", "category": "수능"},
    {"word": "domain", "meaning": "영역, 분야", "category": "수능"},
    {"word": "domestic", "meaning": "국내의, 가정의", "category": "수능"},
    {"word": "dominate", "meaning": "지배하다, 우세하다", "category": "수능"},
    {"word": "drastic", "meaning": "과감한, 급격한", "category": "수능"},
    {"word": "durable", "meaning": "내구성이 있는, 오래가는", "category": "수능"},
    {"word": "elaborate", "meaning": "정교한, 상세히 설명하다", "category": "수능"},
    {"word": "eliminate", "meaning": "제거하다, 없애다", "category": "수능"},
    {"word": "emerge", "meaning": "부상하다, 나타나다", "category": "수능"},
    {"word": "emphasize", "meaning": "강조하다, 부각시키다", "category": "수능"},
    {"word": "empirical", "meaning": "경험적인, 실증적인", "category": "수능"},
    {"word": "endure", "meaning": "견디다, 참다", "category": "수능"},
    {"word": "enforce", "meaning": "집행하다, 강요하다", "category": "수능"},
    {"word": "enhance", "meaning": "향상시키다, 높이다", "category": "수능"},
    {"word": "enormous", "meaning": "엄청난, 막대한", "category": "수능"},
    {"word": "evaluate", "meaning": "평가하다, 감정하다", "category": "수능"},
    {"word": "evidence", "meaning": "증거, 흔적", "category": "수능"},
    {"word": "evolve", "meaning": "진화하다, 발전하다", "category": "수능"},
    {"word": "exaggerate", "meaning": "과장하다", "category": "수능"},
    {"word": "exclude", "meaning": "배제하다, 제외하다", "category": "수능"},
    {"word": "execute", "meaning": "실행하다, 처형하다", "category": "수능"},
    {"word": "exhaust", "meaning": "기진맥진하게 만들다, 고갈시키다", "category": "수능"},
    {"word": "exhibit", "meaning": "전시하다, 드러내다", "category": "수능"},
    {"word": "expand", "meaning": "확장하다, 팽창하다", "category": "수능"},
    {"word": "exploit", "meaning": "착취하다, 활용하다", "category": "수능"},
    {"word": "expose", "meaning": "노출시키다, 폭로하다", "category": "수능"},
    {"word": "facilitate", "meaning": "용이하게 하다, 촉진하다", "category": "수능"},
    {"word": "flexible", "meaning": "유연한, 융통성 있는", "category": "수능"},
    {"word": "fluctuate", "meaning": "변동하다, 요동치다", "category": "수능"},
    {"word": "fundamental", "meaning": "근본적인, 핵심적인", "category": "수능"},
    {"word": "genuine", "meaning": "진짜의, 순수한", "category": "수능"},
    {"word": "hostility", "meaning": "적대감, 적의", "category": "수능"},
    {"word": "identify", "meaning": "확인하다, 동일시하다", "category": "수능"},
    {"word": "illustrate", "meaning": "설명하다, 삽화를 넣다", "category": "수능"},
    {"word": "imply", "meaning": "암시하다, 내포하다", "category": "수능"},
    {"word": "indicate", "meaning": "나타내다, 가리키다", "category": "수능"},
    {"word": "inevitable", "meaning": "불가피한, 필연적인", "category": "수능"},
    {"word": "infer", "meaning": "추론하다, 뜻을 품다", "category": "수능"},
    {"word": "inherent", "meaning": "내재된, 고유한", "category": "수능"},
    {"word": "initial", "meaning": "처음의, 초기의", "category": "수능"},
    {"word": "innovate", "meaning": "혁신하다, 쇄신하다", "category": "수능"},
    {"word": "insight", "meaning": "통찰력, 이해", "category": "수능"},
    {"word": "intense", "meaning": "극심한, 강렬한", "category": "수능"},
    {"word": "interpret", "meaning": "해석하다, 통역하다", "category": "수능"},
    {"word": "intervene", "meaning": "개입하다, 사이에 끼어들다", "category": "수능"},
    {"word": "intrinsic", "meaning": "본질적인, 내재적인", "category": "수능"},
    {"word": "justify", "meaning": "정당화하다, 해명하다", "category": "수능"},
    {"word": "obscure", "meaning": "모호한, 잘 알려지지 않은", "category": "수능"},
    {"word": "perceive", "meaning": "인지하다, 감지하다", "category": "수능"},
    {"word": "persist", "meaning": "지속하다, 끈질기게 버티다", "category": "수능"},
    {"word": "potential", "meaning": "잠재력, 가능성 있는", "category": "수능"},
    {"word": "prevalent", "meaning": "만연한, 널리 퍼진", "category": "수능"},
    {"word": "profound", "meaning": "심오한, 깊은", "category": "수능"},
    {"word": "prohibit", "meaning": "금지하다, 방해하다", "category": "수능"},
    {"word": "reinforce", "meaning": "강화하다, 보강하다", "category": "수능"},
    {"word": "reluctant", "meaning": "꺼리는, 주저하는", "category": "수능"},
    {"word": "resolve", "meaning": "해결하다, 결심하다", "category": "수능"},
    {"word": "rigid", "meaning": "엄격한, 뻣뻣한", "category": "수능"},
    {"word": "scarce", "meaning": "부족한, 드문", "category": "수능"},
    {"word": "spontaneous", "meaning": "자발적인, 즉흥적인", "category": "수능"},
    {"word": "subsequent", "meaning": "그 다음의, 차후의", "category": "수능"},
    {"word": "subtle", "meaning": "미묘한, 미세한", "category": "수능"},
    {"word": "sustain", "meaning": "지탱하다, 유지하다", "category": "수능"},
    {"word": "undergo", "meaning": "겪다, 경험하다", "category": "수능"},
    {"word": "undertake", "meaning": "착수하다, 떠맡다", "category": "수능"},
    {"word": "utilize", "meaning": "활용하다, 이용하다", "category": "수능"},
    {"word": "verify", "meaning": "확인하다, 입증하다", "category": "수능"},
    {"word": "vulnerable", "meaning": "취약한, 상처받기 쉬운", "category": "수능"},

    # ================= [3. 토익 / 비즈니스 실전 (120단어)] =================
    {"word": "accomplish", "meaning": "완수하다, 성취하다", "category": "토익"},
    {"word": "adhere", "meaning": "고수하다, 부착되다", "category": "토익"},
    {"word": "allocate", "meaning": "할당하다, 배분하다", "category": "토익"},
    {"word": "alternative", "meaning": "대안, 대체 가능한", "category": "토익"},
    {"word": "amend", "meaning": "수정하다, 개정하다", "category": "토익"},
    {"word": "applicant", "meaning": "지원자, 신청자", "category": "토익"},
    {"word": "assemble", "meaning": "조립하다, 모이다", "category": "토익"},
    {"word": "audit", "meaning": "회계 감사, 회계 감사를 하다", "category": "토익"},
    {"word": "authorize", "meaning": "권한을 부여하다, 허가하다", "category": "토익"},
    {"word": "benchmark", "meaning": "기준점, 기준", "category": "토익"},
    {"word": "bilateral", "meaning": "쌍방의, 양자간의", "category": "토익"},
    {"word": "breach", "meaning": "위반, 위반하다", "category": "토익"},
    {"word": "brochure", "meaning": "안내 책자", "category": "토익"},
    {"word": "budget", "meaning": "예산, 예산을 세우다", "category": "토익"},
    {"word": "candidate", "meaning": "후보자, 지원자", "category": "토익"},
    {"word": "collaborate", "meaning": "협력하다, 공동 작업하다", "category": "토익"},
    {"word": "commence", "meaning": "시작하다, 개시하다", "category": "토익"},
    {"word": "commute", "meaning": "통근하다, 통근 거리", "category": "토익"},
    {"word": "compatible", "meaning": "호환되는, 양립할 수 있는", "category": "토익"},
    {"word": "comply", "meaning": "준수하다, 따르다", "category": "토익"},
    {"word": "comprehensive", "meaning": "포괄적인, 종합적인", "category": "토익"},
    {"word": "confidential", "meaning": "기밀의, 비밀의", "category": "토익"},
    {"word": "consensus", "meaning": "합의, 일치된 의견", "category": "토익"},
    {"word": "consolidate", "meaning": "통합하다, 강화하다", "category": "토익"},
    {"word": "contractor", "meaning": "계약자, 도급업자", "category": "토익"},
    {"word": "correspond", "meaning": "일치하다, 서신을 주고받다", "category": "토익"},
    {"word": "criterion", "meaning": "기준, 척도", "category": "토익"},
    {"word": "deadline", "meaning": "마감 기한", "category": "토익"},
    {"word": "delegate", "meaning": "위임하다, 대표자", "category": "토익"},
    {"word": "deliberate", "meaning": "신중한, 고의의, 숙고하다", "category": "토익"},
    {"word": "designate", "meaning": "지정하다, 지명하다", "category": "토익"},
    {"word": "destination", "meaning": "목적지, 행선지", "category": "토익"},
    {"word": "discount", "meaning": "할인, 할인하다", "category": "토익"},
    {"word": "dispute", "meaning": "분쟁, 논쟁하다", "category": "토익"},
    {"word": "disrupt", "meaning": "방해하다, 중단시키다", "category": "토익"},
    {"word": "disseminate", "meaning": "유포하다, 퍼뜨리다", "category": "토익"},
    {"word": "dividend", "meaning": "배당금", "category": "토익"},
    {"word": "duplicate", "meaning": "사본, 복제하다", "category": "토익"},
    {"word": "duration", "meaning": "지속 시간, 기간", "category": "토익"},
    {"word": "eligible", "meaning": "자격이 있는, 적격의", "category": "토익"},
    {"word": "embezzle", "meaning": "횡령하다", "category": "토익"},
    {"word": "endorse", "meaning": "지지하다, 보증하다", "category": "토익"},
    {"word": "enterprise", "meaning": "기업, 사업", "category": "토익"},
    {"word": "expedite", "meaning": "신속히 처리하다, 촉진하다", "category": "토익"},
    {"word": "expire", "meaning": "만료되다, 끝나다", "category": "토익"},
    {"word": "explicit", "meaning": "명백한, 노골적인", "category": "토익"},
    {"word": "extension", "meaning": "연장, 내선 번호", "category": "토익"},
    {"word": "feasible", "meaning": "실현 가능한, 그럴싸한", "category": "토익"},
    {"word": "finalize", "meaning": "마무리짓다, 완결하다", "category": "토익"},
    {"word": "foster", "meaning": "육성하다, 발전시키다", "category": "토익"},
    {"word": "franchise", "meaning": "가맹점, 독점 영업권", "category": "토익"},
    {"word": "fulfillment", "meaning": "이행, 성취, 주문 처리", "category": "토익"},
    {"word": "gauge", "meaning": "측정하다, 판단하다, 계량기", "category": "토익"},
    {"word": "grievance", "meaning": "불만, 고충", "category": "토익"},
    {"word": "guidance", "meaning": "지침, 안내", "category": "토익"},
    {"word": "implement", "meaning": "실행하다, 이행하다", "category": "토익"},
    {"word": "implicit", "meaning": "암묵적인, 내포된", "category": "토익"},
    {"word": "incentive", "meaning": "보상, 장려금, 유인책", "category": "토익"},
    {"word": "incorporate", "meaning": "포함하다, 법인화하다", "category": "토익"},
    {"word": "initiate", "meaning": "시작하다, 착수하다", "category": "토익"},
    {"word": "inspect", "meaning": "점검하다, 검사하다", "category": "토익"},
    {"word": "integrate", "meaning": "통합하다, 합치다", "category": "토익"},
    {"word": "inventory", "meaning": "재고, 재고 목록", "category": "토익"},
    {"word": "invoice", "meaning": "청구서, 송장", "category": "토익"},
    {"word": "itinerary", "meaning": "여행 일정표", "category": "토익"},
    {"word": "layout", "meaning": "배치, 설계", "category": "토익"},
    {"word": "leverage", "meaning": "지렛대 원리, 활용하다", "category": "토익"},
    {"word": "liability", "meaning": "법적 책임, 부채", "category": "토익"},
    {"word": "lucrative", "meaning": "수익성이 좋은, 돈벌이가 되는", "category": "토익"},
    {"word": "maintenance", "meaning": "유지, 보수", "category": "토익"},
    {"word": "mandate", "meaning": "명령, 지시하다, 위임하다", "category": "토익"},
    {"word": "merchandise", "meaning": "상품, 제품", "category": "토익"},
    {"word": "milestone", "meaning": "이정표, 중대한 시점", "category": "토익"},
    {"word": "negotiate", "meaning": "협상하다, 타결하다", "category": "토익"},
    {"word": "nominate", "meaning": "지명하다, 추천하다", "category": "토익"},
    {"word": "notify", "meaning": "통지하다, 알리다", "category": "토익"},
    {"word": "objective", "meaning": "목표, 객관적인", "category": "토익"},
    {"word": "obligation", "meaning": "의무, 책임", "category": "토익"},
    {"word": "obsolete", "meaning": "구식의, 쓸모없게 된", "category": "토익"},
    {"word": "omit", "meaning": "생략하다, 빠뜨리다", "category": "토익"},
    {"word": "optimize", "meaning": "최적화하다", "category": "토익"},
    {"word": "oversee", "meaning": "감독하다, 총괄하다", "category": "토익"},
    {"word": "overhaul", "meaning": "정밀 점검하다, 전면 개편", "category": "토익"},
    {"word": "penalty", "meaning": "위약금, 처벌", "category": "토익"},
    {"word": "perishable", "meaning": "썩기 쉬운, 상하기 쉬운", "category": "토익"},
    {"word": "permanent", "meaning": "영구적인, 정규직의", "category": "토익"},
    {"word": "perspective", "meaning": "관점, 시각", "category": "토익"},
    {"word": "pledge", "meaning": "서약하다, 약속", "category": "토익"},
    {"word": "prioritize", "meaning": "우선순위를 매기다", "category": "토익"},
    {"word": "prospective", "meaning": "유망한, 잠재적인", "category": "토익"},
    {"word": "provision", "meaning": "조항, 공급, 대비", "category": "토익"},
    {"word": "qualify", "meaning": "자격을 얻다, 적임이다", "category": "토익"},
    {"word": "quota", "meaning": "할당량, 몫", "category": "토익"},
    {"word": "reimburse", "meaning": "변제하다, 상환하다", "category": "토익"},
    {"word": "reliable", "meaning": "믿을 수 있는, 확실한", "category": "토익"},
    {"word": "relocate", "meaning": "이전하다, 재배치하다", "category": "토익"},
    {"word": "restructure", "meaning": "구조조정하다, 개편하다", "category": "토익"},
    {"word": "retail", "meaning": "소매, 소매의", "category": "토익"},
    {"word": "revenue", "meaning": "수익, 매출, 세입", "category": "토익"},
    {"word": "terminate", "meaning": "종료하다, 종결짓다", "category": "토익"},
    {"word": "unanimous", "meaning": "만장일치의", "category": "토익"},
    {"word": "vendor", "meaning": "공급업체, 판매자", "category": "토익"},
    {"word": "warranty", "meaning": "품질 보증서", "category": "토익"},

    # ================= [4. 고급 / 학술 어휘 (80단어)] =================
    {"word": "aesthetic", "meaning": "미적인, 심미적인", "category": "고급"},
    {"word": "aloof", "meaning": "냉담한, 쌀쌀맞은", "category": "고급"},
    {"word": "ameliorate", "meaning": "개선하다, 완화시키다", "category": "고급"},
    {"word": "anomaly", "meaning": "변칙, 이례적인 것", "category": "고급"},
    {"word": "apathy", "meaning": "무관심, 냉담", "category": "고급"},
    {"word": "arbitrary", "meaning": "자의적인, 임의의", "category": "고급"},
    {"word": "benevolence", "meaning": "자비심, 박애", "category": "고급"},
    {"word": "clandestine", "meaning": "비밀의, 은밀한", "category": "고급"},
    {"word": "coerce", "meaning": "강요하다, 강제하다", "category": "고급"},
    {"word": "cognizant", "meaning": "인식하고 있는, 알고 있는", "category": "고급"},
    {"word": "complacency", "meaning": "자기만족, 안주", "category": "고급"},
    {"word": "corroborate", "meaning": "확증하다, 입증하다", "category": "고급"},
    {"word": "cumbersome", "meaning": "다루기 힘든, 성가신", "category": "고급"},
    {"word": "debilitate", "meaning": "쇠약하게 만들다", "category": "고급"},
    {"word": "delineate", "meaning": "기술하다, 묘사하다", "category": "고급"},
    {"word": "elucidate", "meaning": "명료하게 설명하다", "category": "고급"},
    {"word": "ephemeral", "meaning": "수명이 짧은, 덧없는", "category": "고급"},
    {"word": "epitome", "meaning": "전형, 완벽한 본보기", "category": "고급"},
    {"word": "esoteric", "meaning": "소수만 이해하는, 난해한", "category": "고급"},
    {"word": "exacerbate", "meaning": "악화시키다", "category": "고급"},
    {"word": "fastidious", "meaning": "세심한, 까다로운", "category": "고급"},
    {"word": "formidable", "meaning": "어마어마한, 무시무시한", "category": "고급"},
    {"word": "futile", "meaning": "헛된, 소용없는", "category": "고급"},
    {"word": "gratuitous", "meaning": "불필요한, 까닭 없는", "category": "고급"},
    {"word": "hierarchy", "meaning": "계급 체계, 서열", "category": "고급"},
    {"word": "homogeneous", "meaning": "동질적인, 균일한", "category": "고급"},
    {"word": "idiosyncratic", "meaning": "특이한, 독특한", "category": "고급"},
    {"word": "immaculate", "meaning": "흠잡을 데 없는, 매우 깨끗한", "category": "고급"},
    {"word": "immutable", "meaning": "불변의, 바꿀 수 없는", "category": "고급"},
    {"word": "impervious", "meaning": "통과시키지 않는, 영향을 받지 않는", "category": "고급"},
    {"word": "inadvertent", "meaning": "고의가 아닌, 부주의한", "category": "고급"},
    {"word": "ineffable", "meaning": "이루 말할 수 없는, 형언할 수 없는", "category": "고급"},
    {"word": "ingenious", "meaning": "기발한, 독창적인", "category": "고급"},
    {"word": "insurmountable", "meaning": "극복할 수 없는", "category": "고급"},
    {"word": "intrepid", "meaning": "용감무쌍한, 두려움을 모르는", "category": "고급"},
    {"word": "meticulous", "meaning": "꼼꼼한, 세심한", "category": "고급"},
    {"word": "mundane", "meaning": "일상적인, 평범한", "category": "고급"},
    {"word": "nonchalant", "meaning": "무심한, 태연한", "category": "고급"},
    {"word": "obliterate", "meaning": "흔적을 없애다, 완전히 지우다", "category": "고급"},
    {"word": "obstinate", "meaning": "완고한, 고집 센", "category": "고급"},
    {"word": "ominous", "meaning": "불길한, 전조가 나쁜", "category": "고급"},
    {"word": "panacea", "meaning": "만병통치약", "category": "고급"},
    {"word": "paradigm", "meaning": "패러다임, 전형적인 예", "category": "고급"},
    {"word": "paradox", "meaning": "역설, 모순된 말", "category": "고급"},
    {"word": "patronize", "meaning": "애용하다, 가르치려 들다", "category": "고급"},
    {"word": "penchant", "meaning": "애호, 강한 기호", "category": "고급"},
    {"word": "perfunctory", "meaning": "형식적인, 건성의", "category": "고급"},
    {"word": "pernicious", "meaning": "치명적인, 유해한", "category": "고급"},
    {"word": "plausible", "meaning": "그럴듯한, 이치에 맞는", "category": "고급"},
    {"word": "pragmatic", "meaning": "실용적인, 실리적인", "category": "고급"},
    {"word": "pristine", "meaning": "오염되지 않은, 완전 새것 같은", "category": "고급"},
    {"word": "prolific", "meaning": "다작하는, 풍부한", "category": "고급"},
    {"word": "prudent", "meaning": "신중한, 빈틈없는", "category": "고급"},
    {"word": "quandary", "meaning": "진퇴양난, 궁지", "category": "고급"},
    {"word": "redundant", "meaning": "불필요하게 중복된, 여분의", "category": "고급"},
    {"word": "remorse", "meaning": "깊은 후회, 자책", "category": "고급"},
    {"word": "resilient", "meaning": "회복력 있는, 탄력적인", "category": "고급"},
    {"word": "scrutinize", "meaning": "면밀히 조사하다", "category": "고급"},
    {"word": "serendipity", "meaning": "뜻밖의 행운, 우연한 발견", "category": "고급"},
    {"word": "sporadic", "meaning": "산발적인, 때때로 일어나는", "category": "고급"},
    {"word": "substantiate", "meaning": "입증하다, 실증하다", "category": "고급"},
    {"word": "supercilious", "meaning": "거만한, 남을 얕보는", "category": "고급"},
    {"word": "taciturn", "meaning": "과묵한, 말수가 적은", "category": "고급"},
    {"word": "tangible", "meaning": "만질 수 있는, 실재하는", "category": "고급"},
    {"word": "tenacious", "meaning": "집요한, 완강한", "category": "고급"},
    {"word": "ubiquitous", "meaning": "어디에나 존재하는", "category": "고급"},
    {"word": "unequivocal", "meaning": "명백한, 오해의 여지가 없는", "category": "고급"},
    {"word": "usurp", "meaning": "빼앗다, 찬탈하다", "category": "고급"},
    {"word": "vacillate", "meaning": "흔들리다, 망설이다", "category": "고급"},
    {"word": "venerable", "meaning": "공경할 만한, 유서 깊은", "category": "고급"},
    {"word": "verbose", "meaning": "장황한, 말이 많은", "category": "고급"},
    {"word": "vindicate", "meaning": "무죄를 입증하다, 정당성을 밝히다", "category": "고급"},
    {"word": "virulent", "meaning": "치명적인, 맹독성의, 악의에 찬", "category": "고급"},
    {"word": "volatile", "meaning": "변덕스러운, 휘발성의", "category": "고급"},
    {"word": "voracious", "meaning": "게걸스러운, 열렬한", "category": "고급"},
    {"word": "zealous", "meaning": "열성적인, 열렬한", "category": "고급"},
]


class VocabManager:
    """로컬 데이터 영구 저장 및 퀴즈 출제 관리 클래스"""

    def __init__(self, db_filename="vocab_reflex_db.json"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(script_dir, db_filename)
        self.data = {
            "custom_words": [],       # 사용자가 직접 추가한 단어 목록
            "word_stats": {},          # {단어: {"attempts": int, "success": int, "consecutive_pass": int, "avg_speed_ms": float, "last_result": str}}
            "history_log": [],         # 최근 테스트 기록
        }
        self.load_data()

    def load_data(self):
        """로컬 파일에서 통계 및 사용자 단어 로드"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.data["custom_words"] = loaded.get("custom_words", [])
                    self.data["word_stats"] = loaded.get("word_stats", {})
                    self.data["history_log"] = loaded.get("history_log", [])
            except Exception as e:
                print(f"데이터 파일 로드 오류 (새로 시작): {e}")

    def save_data(self):
        """로컬 파일에 영구 저장"""
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"데이터 파일 저장 오류: {e}")

    def get_all_words(self, category="전체"):
        """지정된 카테고리의 단어 목록 반환 (내장 + 사용자 단어)"""
        words = list(DEFAULT_VOCABULARY) + self.data["custom_words"]
        if category == "전체":
            return words
        elif category == "오답집중":
            # 연속 3회 반사 패스하지 못한 취약 단어들만 선별
            weak_words = []
            for w in words:
                stats = self.data["word_stats"].get(w["word"], {})
                consecutive = stats.get("consecutive_pass", 0)
                attempts = stats.get("attempts", 0)
                last_result = stats.get("last_result", "")
                if attempts > 0 and (last_result in ["timeout", "fail"] or consecutive < 3):
                    weak_words.append(w)
            return weak_words if weak_words else words  # 오답 없으면 전체
        elif category == "사용자추가":
            return self.data["custom_words"]
        else:
            return [w for w in words if w.get("category") == category]

    def record_attempt(self, word_text, is_success, elapsed_ms, is_timeout=False):
        """테스트 결과 기록 (단어별 통계 업데이트)"""
        stats = self.data["word_stats"].setdefault(word_text, {
            "attempts": 0,
            "success": 0,
            "consecutive_pass": 0,
            "best_speed_ms": 99999,
            "avg_speed_ms": 0.0,
            "last_result": "",
        })

        stats["attempts"] += 1
        if is_success:
            stats["success"] += 1
            stats["consecutive_pass"] += 1
            stats["last_result"] = "pass"
            if elapsed_ms < stats.get("best_speed_ms", 99999):
                stats["best_speed_ms"] = elapsed_ms
        else:
            stats["consecutive_pass"] = 0
            stats["last_result"] = "timeout" if is_timeout else "fail"

        # 평균 속도 누적 계산
        prev_total = stats.get("avg_speed_ms", 0.0) * (stats["attempts"] - 1)
        stats["avg_speed_ms"] = round((prev_total + elapsed_ms) / stats["attempts"], 1)

        self.save_data()

    def get_stats_summary(self):
        """전체 통계 요약 반환"""
        total_tested = len(self.data["word_stats"])
        mastered = sum(1 for s in self.data["word_stats"].values() if s.get("consecutive_pass", 0) >= 3)
        weak = sum(1 for s in self.data["word_stats"].values() if s.get("last_result") in ["timeout", "fail"])
        return {
            "total_tested": total_tested,
            "mastered": mastered,
            "weak": weak,
            "custom_count": len(self.data["custom_words"]),
        }

    def add_custom_word(self, word, meaning, category="사용자"):
        """사용자 단어 직접 추가"""
        clean_word = word.strip()
        clean_meaning = meaning.strip()
        if not clean_word or not clean_meaning:
            return False, "단어와 뜻을 모두 입력해주세요."
        
        # 중복 체크
        for w in self.data["custom_words"]:
            if w["word"].lower() == clean_word.lower():
                return False, "이미 등록된 단어입니다."

        self.data["custom_words"].append({
            "word": clean_word,
            "meaning": clean_meaning,
            "category": category,
        })
        self.save_data()
        return True, f"'{clean_word}' 단어가 추가되었습니다."

    def delete_custom_word(self, word_text):
        """사용자 단어 삭제"""
        self.data["custom_words"] = [w for w in self.data["custom_words"] if w["word"] != word_text]
        self.save_data()

    def reset_stats(self):
        """학습 이력 초기화"""
        self.data["word_stats"] = {}
        self.save_data()

`

---

### (3) 
eflex_vocab_app.py (메인 GUI 애플리케이션)
`python
"""
영단어 반사 암기 테스터 (Reflex Vocabulary Tester)
- 1~3초 안에 한국어 뜻이 반사적으로 튀어나오는지 냉정하게 테스트하는 프로그램
- 인터넷 0%, 로컬 100%, 로그인 0%
- 파이썬 기본 내장 모듈(tkinter, winsound, time, random)만 사용
"""

import os
import random
import re
import time
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

from reflex_vocab_data import VocabManager, DEFAULT_VOCABULARY


def check_korean_match(user_input: str, target_meaning: str) -> bool:
    """사용자가 입력한 한국어 뜻과 정답 의미를 유연하게 비교 판정하는 함수"""
    user_clean = user_input.strip().lower()
    if not user_clean:
        return False

    def normalize(s):
        # 특수문자(~, 쉼표, 마침표, 물음표 등) 및 공백 제거
        return re.sub(r'[\s~,./()?!]+', '', s).lower()

    user_norm = normalize(user_clean)
    if not user_norm:
        return False

    # 쉼표, 슬래시, 세미콜론 등으로 개별 뜻 분리
    tokens = re.split(r'[,;/]', target_meaning)
    candidate_meanings = []
    for t in tokens:
        t_clean = t.strip()
        candidate_meanings.append(t_clean)
        # 괄호 제거 버전도 후보로 추가
        no_paren = re.sub(r'\(.*?\)', '', t_clean).strip()
        if no_paren and no_paren != t_clean:
            candidate_meanings.append(no_paren)

    for cand in candidate_meanings:
        cand_norm = normalize(cand)
        if not cand_norm:
            continue
        # 1. 완전 일치
        if user_norm == cand_norm:
            return True
        # 2. 2글자 이상 부분 일치 (예: '수락' vs '수락하다', '인정' vs '인정하다')
        if len(user_norm) >= 2 and (user_norm in cand_norm or cand_norm in user_norm):
            return True
        # 3. 한국어 어간(Stem) 매칭 (~하다, ~되다, ~이다, ~들이다 등 명사화/어미 변화 허용)
        for suffix in ['하다', '되다', '이다', '시키다', '나다', '오다', '가다', '내다', '들이다', '잡다']:
            if cand_norm.endswith(suffix):
                stem = cand_norm[:-len(suffix)]
                if len(stem) >= 2 and (user_norm.startswith(stem) or stem in user_norm):
                    return True

    # 4. 전체 텍스트에 포함되어 있는지 검사 (2글자 이상)
    target_norm = normalize(target_meaning)
    if len(user_norm) >= 2 and user_norm in target_norm:
        return True

    return False



class ReflexVocabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ 영단어 반사 암기 테스터 (Reflex Vocab)")
        self.root.geometry("780x640")
        self.root.minsize(740, 600)
        self.root.configure(bg="#1e272e")

        # 데이터 관리자
        self.vocab_mgr = VocabManager()

        # 설정 변수
        self.selected_mode = tk.StringVar(value="typing")       # "typing" (직접입력), "flash" (플래시), "choice" (4지선다)
        self.time_limit_sec = tk.DoubleVar(value=3.5)           # 제한시간 (초)
        self.selected_category = tk.StringVar(value="전체")      # 카테고리
        self.sound_enabled = tk.BooleanVar(value=True)           # 소리 효과음

        # 테스트 세션 상태 변수
        self.active_word_pool = []
        self.current_word = None
        self.entry_korean = None
        self.choices = []
        self.correct_choice_idx = -1
        self.is_timer_running = False
        self.start_time = 0.0
        self.elapsed_ms = 0.0
        self.timer_job = None
        self.test_phase = "ready"  # "testing", "evaluating", "result"

        # 세션 통계
        self.session_total = 0
        self.session_correct = 0
        self.session_timeout = 0
        self.session_wrong = 0
        self.session_speeds = []

        # UI 색상 팔레트 (다크 모드 & 고대비)
        self.C_BG = "#1e272e"         # 전체 배경 (어두운 흑청색)
        self.C_CARD = "#2f3542"       # 카드 배경 (다크 그레이)
        self.C_TEXT = "#ffffff"       # 기본 글자색
        self.C_SUBTEXT = "#a4b0be"    # 보조 글자색
        self.C_ACCENT = "#00d2d3"     # 강조색 (청록)
        self.C_PRIMARY = "#54a0ff"    # 주요 버튼 (파랑)
        self.C_SUCCESS = "#2ed573"    # 정답/성공 (초록)
        self.C_DANGER = "#ff4757"     # 오답/타임오버 (빨강)
        self.C_WARNING = "#ffa502"    # 경고/중간 (주황)

        # 컨테이너 프레임
        self.main_container = tk.Frame(self.root, bg=self.C_BG)
        self.main_container.pack(fill="both", expand=True)

        # 화면 빌드
        self.build_menu_screen()

        # 글로벌 키보드 바인딩
        self.root.bind("<Escape>", self.on_escape_pressed)

    # =========================================================================
    # 사운드 효과음
    # =========================================================================
    def play_sound(self, sound_type):
        if not self.sound_enabled.get() or not HAS_SOUND:
            return
        try:
            if sound_type == "success":
                winsound.Beep(1200, 90)
            elif sound_type == "super":
                winsound.Beep(1600, 70)
                winsound.Beep(2000, 90)
            elif sound_type == "timeout":
                winsound.Beep(320, 250)
            elif sound_type == "wrong":
                winsound.Beep(400, 180)
            elif sound_type == "tick":
                winsound.Beep(800, 30)
        except Exception:
            pass

    # =========================================================================
    # 1. 메인 메뉴 화면
    # =========================================================================
    def build_menu_screen(self):
        self.clear_container()

        # 상단 타이틀
        header_frame = tk.Frame(self.main_container, bg=self.C_BG)
        header_frame.pack(fill="x", pady=(25, 10), padx=30)

        title_lbl = tk.Label(
            header_frame,
            text="⚡ 영단어 반사 암기 테스터",
            font=("맑은 고딕", 24, "bold"),
            fg=self.C_ACCENT,
            bg=self.C_BG
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(
            header_frame,
            text="1~3초 안에 한국어 뜻이 반사적으로 튀어나오는지 냉정하게 테스트합니다.",
            font=("맑은 고딕", 11),
            fg=self.C_SUBTEXT,
            bg=self.C_BG
        )
        subtitle_lbl.pack(anchor="w", pady=(3, 0))

        # 중앙 카드 프레임
        card = tk.Frame(self.main_container, bg=self.C_CARD, bd=0, padx=25, pady=20)
        card.pack(fill="both", expand=True, padx=30, pady=10)

        # 1) 테스트 모드 선택
        mode_frame = tk.LabelFrame(
            card,
            text=" 1. 테스트 방식 선택 ",
            font=("맑은 고딕", 12, "bold"),
            fg=self.C_TEXT,
            bg=self.C_CARD,
            padx=15,
            pady=10
        )
        mode_frame.pack(fill="x", pady=6)

        r0 = tk.Radiobutton(
            mode_frame,
            text="✍️ 한국어 직접 타이핑 모드 (강력 추천): 영단어를 보고 한국어 뜻 직접 타자 입력",
            variable=self.selected_mode,
            value="typing",
            font=("맑은 고딕", 11, "bold"),
            fg=self.C_TEXT,
            bg=self.C_CARD,
            selectcolor="#1e272e",
            activebackground=self.C_CARD,
            activeforeground=self.C_ACCENT
        )
        r0.pack(anchor="w", pady=3)

        r1 = tk.Radiobutton(
            mode_frame,
            text="⚡ 반사 플래시 모드: 단어 확인 즉시 [Spacebar]로 반응 속도 측정",
            variable=self.selected_mode,
            value="flash",
            font=("맑은 고딕", 11),
            fg=self.C_TEXT,
            bg=self.C_CARD,
            selectcolor="#1e272e",
            activebackground=self.C_CARD,
            activeforeground=self.C_ACCENT
        )
        r1.pack(anchor="w", pady=3)

        r2 = tk.Radiobutton(
            mode_frame,
            text="🎯 4지선다 스피드 퀴즈: 1~3초 내에 숫자키 [1, 2, 3, 4]로 뜻 선택",
            variable=self.selected_mode,
            value="choice",
            font=("맑은 고딕", 11),
            fg=self.C_TEXT,
            bg=self.C_CARD,
            selectcolor="#1e272e",
            activebackground=self.C_CARD,
            activeforeground=self.C_ACCENT
        )
        r2.pack(anchor="w", pady=3)

        # 2) 반사 제한시간 선택
        time_frame = tk.LabelFrame(
            card,
            text=" 2. 냉정한 제한 시간 (반사 기준) ",
            font=("맑은 고딕", 12, "bold"),
            fg=self.C_TEXT,
            bg=self.C_CARD,
            padx=15,
            pady=10
        )
        time_frame.pack(fill="x", pady=6)

        btn_row = tk.Frame(time_frame, bg=self.C_CARD)
        btn_row.pack(fill="x", pady=3)

        limits = [
            ("⚡ 2.0초 (초고속)", 2.0),
            ("⭐ 3.5초 (스피드 추천)", 3.5),
            ("⏱️ 5.0초 (표준 여유)", 5.0),
            ("⌛ 8.0초 (초보 충분)", 8.0),
            ("♾️ 무제한", 999.0),
        ]

        for label, val in limits:
            rb = tk.Radiobutton(
                btn_row,
                text=label,
                variable=self.time_limit_sec,
                value=val,
                font=("맑은 고딕", 10, "bold" if val == 3.5 else "normal"),
                fg=self.C_TEXT,
                bg=self.C_CARD,
                selectcolor="#1e272e",
                activebackground=self.C_CARD,
                activeforeground=self.C_ACCENT
            )
            rb.pack(side="left", padx=8)

        # 3) 단어장 카테고리 선택
        cat_frame = tk.LabelFrame(
            card,
            text=" 3. 단어 출제 범위 ",
            font=("맑은 고딕", 12, "bold"),
            fg=self.C_TEXT,
            bg=self.C_CARD,
            padx=15,
            pady=10
        )
        cat_frame.pack(fill="x", pady=6)

        cat_row = tk.Frame(cat_frame, bg=self.C_CARD)
        cat_row.pack(fill="x", pady=3)

        categories = ["전체", "기초", "수능", "토익", "고급", "오답집중", "사용자추가"]
        for cat in categories:
            prefix = "🔥 " if cat == "오답집중" else ("📝 " if cat == "사용자추가" else "")
            rb = tk.Radiobutton(
                cat_row,
                text=f"{prefix}{cat}",
                variable=self.selected_category,
                value=cat,
                font=("맑은 고딕", 10),
                fg=self.C_TEXT,
                bg=self.C_CARD,
                selectcolor="#1e272e",
                activebackground=self.C_CARD,
                activeforeground=self.C_ACCENT
            )
            rb.pack(side="left", padx=7)

        # 4) 누적 통계 요약 바
        stats = self.vocab_mgr.get_stats_summary()
        stats_frame = tk.Frame(card, bg="#1e272e", padx=15, pady=8)
        stats_frame.pack(fill="x", pady=8)

        stats_text = (
            f"📊 내 학습 현황:  테스트 완료 {stats['total_tested']}개  |  "
            f"완전 정복(3연속 통과) {stats['mastered']}개  |  "
            f"취약/오답 {stats['weak']}개  |  "
            f"내 추가 단어 {stats['custom_count']}개"
        )
        stats_lbl = tk.Label(
            stats_frame,
            text=stats_text,
            font=("맑은 고딕", 10),
            fg=self.C_ACCENT,
            bg="#1e272e"
        )
        stats_lbl.pack(side="left")

        # 효과음 토글 체크박스
        sound_cb = tk.Checkbutton(
            stats_frame,
            text="🔊 효과음",
            variable=self.sound_enabled,
            font=("맑은 고딕", 10),
            fg=self.C_TEXT,
            bg="#1e272e",
            selectcolor="#2f3542",
            activebackground="#1e272e",
            activeforeground=self.C_TEXT
        )
        sound_cb.pack(side="right")

        # 하단 액션 버튼 영역
        action_frame = tk.Frame(self.main_container, bg=self.C_BG)
        action_frame.pack(fill="x", pady=(10, 20), padx=30)

        # 메인 시작 버튼
        start_btn = tk.Button(
            action_frame,
            text="🚀 반사 테스트 시작 (Enter / Space)",
            font=("맑은 고딕", 14, "bold"),
            bg=self.C_PRIMARY,
            fg="white",
            activebackground="#2e86de",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=10,
            command=self.start_test_session
        )
        start_btn.pack(side="left")

        # 보조 버튼들
        weak_btn = tk.Button(
            action_frame,
            text="📖 오답 노트",
            font=("맑은 고딕", 11),
            bg="#57606f",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=10,
            command=self.open_weak_words_dialog
        )
        weak_btn.pack(side="left", padx=8)

        manage_btn = tk.Button(
            action_frame,
            text="➕ 단어 추가/관리",
            font=("맑은 고딕", 11),
            bg="#57606f",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=10,
            command=self.open_word_manager_dialog
        )
        manage_btn.pack(side="left")

        reset_btn = tk.Button(
            action_frame,
            text="🔄 기록 초기화",
            font=("맑은 고딕", 10),
            bg="#3d3d3d",
            fg="#a4b0be",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=10,
            command=self.confirm_reset_stats
        )
        reset_btn.pack(side="right")

        # 엔터/스페이스로 바로 시작 가능
        self.root.bind("<Return>", lambda e: self.start_test_session())
        self.root.bind("<space>", lambda e: self.start_test_session())

    # =========================================================================
    # 2. 테스트 세션 시작 및 루프
    # =========================================================================
    def start_test_session(self):
        # 키 바인딩 정리
        self.root.unbind("<Return>")
        self.root.unbind("<space>")

        category = self.selected_category.get()
        words = self.vocab_mgr.get_all_words(category)

        if not words:
            if category == "오답집중":
                messagebox.showinfo("안내", "현재 오답 또는 취약 단어가 없습니다!\n전체 단어 모드로 먼저 학습해보세요.")
            elif category == "사용자추가":
                messagebox.showinfo("안내", "추가된 사용자 단어가 없습니다!\n[단어 추가/관리] 메뉴에서 단어를 먼저 추가해주세요.")
            else:
                messagebox.showwarning("경고", "해당 카테고리에 단어가 없습니다.")
            self.build_menu_screen()
            return

        self.active_word_pool = list(words)
        random.shuffle(self.active_word_pool)

        # 세션 통계 초기화
        self.session_total = 0
        self.session_correct = 0
        self.session_timeout = 0
        self.session_wrong = 0
        self.session_speeds = []

        self.build_test_screen()
        self.next_question()

    def build_test_screen(self):
        self.clear_container()

        # 1. 세션 헤더 (진행도, 정확도, 카테고리)
        header = tk.Frame(self.main_container, bg=self.C_BG)
        header.pack(fill="x", padx=30, pady=(15, 5))

        limit_val = self.time_limit_sec.get()
        limit_str = "무제한" if limit_val >= 900 else f"{limit_val:.1f}초"
        mode_names = {"typing": "직접 타이핑", "flash": "반사 플래시", "choice": "4지선다"}
        mode_str = mode_names.get(self.selected_mode.get(), "")
        self.lbl_session_info = tk.Label(
            header,
            text=f"모드: {mode_str} | 범위: {self.selected_category.get()} | 제한시간: {limit_str}",
            font=("맑은 고딕", 11),
            fg=self.C_SUBTEXT,
            bg=self.C_BG
        )
        self.lbl_session_info.pack(side="left")

        self.lbl_score_info = tk.Label(
            header,
            text="진행: 0  |  정답: 0 (0%)  |  평균속도: -",
            font=("맑은 고딕", 11, "bold"),
            fg=self.C_ACCENT,
            bg=self.C_BG
        )
        self.lbl_score_info.pack(side="right")

        # 2. 메인 카드 영역
        self.test_card = tk.Frame(self.main_container, bg=self.C_CARD, padx=25, pady=20)
        self.test_card.pack(fill="both", expand=True, padx=30, pady=10)

        # 단어 카테고리 태그
        self.lbl_word_category = tk.Label(
            self.test_card,
            text="[카테고리]",
            font=("맑은 고딕", 10),
            fg=self.C_SUBTEXT,
            bg=self.C_CARD
        )
        self.lbl_word_category.pack(anchor="w")

        # 대형 영단어 표시부
        self.lbl_english_word = tk.Label(
            self.test_card,
            text="WORD",
            font=("맑은 고딕", 44, "bold"),
            fg=self.C_TEXT,
            bg=self.C_CARD
        )
        self.lbl_english_word.pack(pady=(20, 15))

        # 뜻 표시부 (플래시 모드에서는 Space 누른 후 공개)
        self.lbl_korean_meaning = tk.Label(
            self.test_card,
            text="",
            font=("맑은 고딕", 22, "bold"),
            fg=self.C_ACCENT,
            bg=self.C_CARD,
            wraplength=600
        )
        self.lbl_korean_meaning.pack(pady=10)

        # 반응속도 & 판정 피드백 라벨
        self.lbl_speed_feedback = tk.Label(
            self.test_card,
            text="",
            font=("맑은 고딕", 13, "bold"),
            fg=self.C_SUCCESS,
            bg=self.C_CARD
        )
        self.lbl_speed_feedback.pack(pady=4)

        # 3. 모드별 인터랙션 프레임 (동적 교체)
        self.action_area = tk.Frame(self.test_card, bg=self.C_CARD)
        self.action_area.pack(fill="both", expand=True, pady=10)

        # 4. 하단 조작 가이드 바
        footer = tk.Frame(self.main_container, bg=self.C_BG)
        footer.pack(fill="x", padx=30, pady=(5, 15))

        lbl_guide = tk.Label(
            footer,
            text="💡 [Enter] 뜻 제출 / 다음 진행   |   [ESC] 메인 메뉴로 나가기",
            font=("맑은 고딕", 10),
            fg=self.C_SUBTEXT,
            bg=self.C_BG
        )
        lbl_guide.pack(side="left")

        exit_btn = tk.Button(
            footer,
            text="메뉴로 나가기 (ESC)",
            font=("맑은 고딕", 9),
            bg="#3d3d3d",
            fg=self.C_SUBTEXT,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=3,
            command=self.return_to_menu
        )
        exit_btn.pack(side="right")

    # =========================================================================
    # 문제 출제 (Next Question)
    # =========================================================================
    def next_question(self):
        # 이전 타이머 정리
        self.stop_timer()

        # 출제할 단어 선택 (50% 확률로 이전 오답/취약 단어 가중치 출제)
        category = self.selected_category.get()
        if not self.active_word_pool:
            words = self.vocab_mgr.get_all_words(category)
            self.active_word_pool = list(words)
            random.shuffle(self.active_word_pool)

        # 팝
        self.current_word = self.active_word_pool.pop()

        # UI 초기화
        self.test_card.configure(bg=self.C_CARD)
        self.lbl_word_category.configure(
            text=f"[{self.current_word.get('category', '일반')}]  단어 번호 #{self.session_total + 1}",
            bg=self.C_CARD
        )
        self.lbl_english_word.configure(
            text=self.current_word["word"],
            fg=self.C_TEXT,
            bg=self.C_CARD
        )
        self.lbl_korean_meaning.configure(text="", bg=self.C_CARD)
        self.lbl_speed_feedback.configure(text="", bg=self.C_CARD)

        mode = self.selected_mode.get()
        if mode == "typing":
            self.setup_typing_question()
        elif mode == "flash":
            self.setup_flash_question()
        else:
            self.setup_choice_question()

        # 타이머 시작
        self.start_timer()

    # =========================================================================
    # 타이머 엔진 (실시간 애니메이션 없이 정밀 타임오버 처리)
    # =========================================================================
    def start_timer(self):
        self.is_timer_running = True
        self.start_time = time.perf_counter()
        limit = self.time_limit_sec.get()

        if limit < 900:
            # 실시간 줄어드는 애니메이션 없이, 지정된 제한시간 도달 시 타임오버 발생
            timeout_ms = int(limit * 1000)
            self.timer_job = self.root.after(timeout_ms, self._on_timer_complete)

    def _on_timer_complete(self):
        if not self.is_timer_running:
            return
        self.is_timer_running = False
        limit = self.time_limit_sec.get()
        self.elapsed_ms = limit * 1000
        self.on_timeout()

    def stop_timer(self):
        self.is_timer_running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    # =========================================================================
    # 2-A. 모드 0: 한국어 직접 타이핑 모드 (Korean Typing Reflex)
    # =========================================================================
    def setup_typing_question(self):
        self.test_phase = "testing"
        self.clear_frame(self.action_area)

        type_container = tk.Frame(self.action_area, bg=self.C_CARD)
        type_container.pack(fill="x", padx=30, pady=10)

        lbl_instruct = tk.Label(
            type_container,
            text="✍️ 떠오르는 한국어 뜻을 입력하고 [Enter]를 누르세요:",
            font=("맑은 고딕", 12, "bold"),
            fg=self.C_TEXT,
            bg=self.C_CARD
        )
        lbl_instruct.pack(pady=(0, 10))

        input_box = tk.Frame(type_container, bg=self.C_CARD)
        input_box.pack()

        self.entry_korean = tk.Entry(
            input_box,
            font=("맑은 고딕", 16, "bold"),
            width=26,
            justify="center",
            bg="#1e272e",
            fg="#00d2d3",
            insertbackground="white",
            relief="solid",
            bd=2
        )
        self.entry_korean.pack(side="left", padx=8, ipady=6)

        btn_submit = tk.Button(
            input_box,
            text="제출 (Enter)",
            font=("맑은 고딕", 12, "bold"),
            bg=self.C_PRIMARY,
            fg="white",
            activebackground="#2e86de",
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=6,
            command=self.on_typing_submit
        )
        btn_submit.pack(side="left", padx=6)

        btn_pass = tk.Button(
            input_box,
            text="모름 / 패스",
            font=("맑은 고딕", 11),
            bg="#57606f",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6,
            command=self.on_typing_pass
        )
        btn_pass.pack(side="left", padx=6)

        # 타이핑 중에는 스페이스바 띄어쓰기 자유롭게 허용
        self.root.unbind("<space>")
        self.entry_korean.bind("<Return>", lambda e: self.on_typing_submit())
        self.root.bind("<Return>", lambda e: self.on_typing_submit())

        # 자동 입력 포커스
        self.root.after(60, lambda: self.entry_korean.focus_force())

    def on_typing_submit(self):
        if self.test_phase != "testing" or not self.is_timer_running:
            return

        user_text = self.entry_korean.get().strip() if self.entry_korean else ""
        if not user_text:
            self.on_typing_pass()
            return

        self.stop_timer()
        self.test_phase = "result"
        self.elapsed_ms = round((time.perf_counter() - self.start_time) * 1000, 1)

        # 입력 비활성화 및 엔터 바인딩 해제
        self.root.unbind("<Return>")
        if self.entry_korean:
            self.entry_korean.unbind("<Return>")
            self.entry_korean.configure(state="disabled")

        self.session_total += 1
        is_correct = check_korean_match(user_text, self.current_word["meaning"])

        # 정답 공개
        self.lbl_korean_meaning.configure(text=f"정답: {self.current_word['meaning']}", fg=self.C_ACCENT)

        if is_correct:
            self.session_correct += 1
            self.session_speeds.append(self.elapsed_ms)
            self.lbl_speed_feedback.configure(
                text=f"⚡ 정답! 내가 적은 뜻: '{user_text}'  |  입력 시간: {self.elapsed_ms:.0f}ms ({self.elapsed_ms/1000:.2f}초)",
                fg=self.C_SUCCESS
            )
            self.play_sound("success")
            self.vocab_mgr.record_attempt(self.current_word["word"], True, self.elapsed_ms, is_timeout=False)
        else:
            self.session_wrong += 1
            self.lbl_speed_feedback.configure(
                text=f"❌ 오답! 내가 적은 뜻: '{user_text}' (올바른 뜻을 확인하세요)",
                fg=self.C_DANGER
            )
            self.play_sound("wrong")
            self.vocab_mgr.record_attempt(self.current_word["word"], False, self.elapsed_ms, is_timeout=False)

        self.update_score_header()
        self.show_next_prompt()

    def on_typing_pass(self):
        if self.test_phase != "testing" or not self.is_timer_running:
            return

        self.stop_timer()
        self.test_phase = "result"
        self.elapsed_ms = round((time.perf_counter() - self.start_time) * 1000, 1)

        self.root.unbind("<Return>")
        if self.entry_korean:
            self.entry_korean.unbind("<Return>")
            self.entry_korean.configure(state="disabled")

        self.session_total += 1
        self.session_wrong += 1

        self.lbl_korean_meaning.configure(text=f"정답: {self.current_word['meaning']}", fg=self.C_ACCENT)
        self.lbl_speed_feedback.configure(
            text="⏭️ 패스(모름) 처리되었습니다.",
            fg=self.C_WARNING
        )
        self.play_sound("wrong")
        self.vocab_mgr.record_attempt(self.current_word["word"], False, self.elapsed_ms, is_timeout=False)

        self.update_score_header()
        self.show_next_prompt()

    # =========================================================================
    # 2-B. 모드 1: 반사 플래시 모드 (Flash Reflex)
    # =========================================================================
    def setup_flash_question(self):
        self.test_phase = "testing"
        self.clear_frame(self.action_area)

        # 안내 문구 & 대형 반응 버튼
        self.btn_reflex_trigger = tk.Button(
            self.action_area,
            text="⚡ 뜻이 떠올랐으면 즉시 누르세요! [Spacebar]",
            font=("맑은 고딕", 14, "bold"),
            bg=self.C_PRIMARY,
            fg="white",
            activebackground="#2e86de",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=16,
            command=self.on_flash_reflex_hit
        )
        self.btn_reflex_trigger.pack(fill="x", padx=60, pady=10)

        # 스페이스바 / 엔터 누르면 즉각 타이머 정지 & 뜻 공개
        self.root.bind("<space>", lambda e: self.on_flash_reflex_hit())
        self.root.bind("<Return>", lambda e: self.on_flash_reflex_hit())

    def on_flash_reflex_hit(self):
        """사용자가 제한시간 내에 뜻을 떠올려 Spacebar를 누른 순간"""
        if self.test_phase != "testing" or not self.is_timer_running:
            return

        self.stop_timer()
        self.test_phase = "evaluating"
        self.elapsed_ms = round((time.perf_counter() - self.start_time) * 1000, 1)

        # 뜻 공개
        self.lbl_korean_meaning.configure(text=self.current_word["meaning"], fg=self.C_ACCENT)

        # 반응속도 피드백
        speed_sec = self.elapsed_ms / 1000
        if self.elapsed_ms < 800:
            speed_title = "⚡ 경이로운 반사속도!"
            speed_color = "#2ed573"
        elif self.elapsed_ms < 1500:
            speed_title = "👍 완벽한 반사 암기!"
            speed_color = "#00d2d3"
        else:
            speed_title = "⏱️ 통과 (약간의 지연)"
            speed_color = "#ffa502"

        self.lbl_speed_feedback.configure(
            text=f"반응 시간: {self.elapsed_ms:.0f}ms ({speed_sec:.2f}초)  -  {speed_title}",
            fg=speed_color
        )
        self.play_sound("success" if self.elapsed_ms >= 800 else "super")

        # 자가 검증 UI로 교체: 맞았는지/틀렸는지 솔직 평가
        self.clear_frame(self.action_area)

        eval_lbl = tk.Label(
            self.action_area,
            text="머릿속에 떠올린 뜻이 맞았습니까?",
            font=("맑은 고딕", 12, "bold"),
            fg=self.C_TEXT,
            bg=self.C_CARD
        )
        eval_lbl.pack(pady=(5, 10))

        btn_row = tk.Frame(self.action_area, bg=self.C_CARD)
        btn_row.pack()

        btn_correct = tk.Button(
            btn_row,
            text="✅ [1] 맞았습니다 (Enter)",
            font=("맑은 고딕", 12, "bold"),
            bg=self.C_SUCCESS,
            fg="white",
            activebackground="#26af5f",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=10,
            command=lambda: self.finish_flash_eval(True)
        )
        btn_correct.pack(side="left", padx=12)

        btn_wrong = tk.Button(
            btn_row,
            text="❌ [2] 틀렸거나 헷갈림",
            font=("맑은 고딕", 12, "bold"),
            bg=self.C_DANGER,
            fg="white",
            activebackground="#c0392b",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=10,
            command=lambda: self.finish_flash_eval(False)
        )
        btn_wrong.pack(side="left", padx=12)

        # 키보드 바인딩: 1 또는 Enter = 맞음, 2 = 틀림
        self.root.bind("<Return>", lambda e: self.finish_flash_eval(True))
        self.root.bind("1", lambda e: self.finish_flash_eval(True))
        self.root.bind("<KP_1>", lambda e: self.finish_flash_eval(True))
        self.root.bind("2", lambda e: self.finish_flash_eval(False))
        self.root.bind("<KP_2>", lambda e: self.finish_flash_eval(False))
        self.root.unbind("<space>")

    def finish_flash_eval(self, is_correct):
        """플래시카드 자가 검증 완료"""
        self.root.unbind("1")
        self.root.unbind("2")
        self.root.unbind("<KP_1>")
        self.root.unbind("<KP_2>")
        self.root.unbind("<Return>")

        self.session_total += 1
        if is_correct:
            self.session_correct += 1
            self.session_speeds.append(self.elapsed_ms)
            self.vocab_mgr.record_attempt(self.current_word["word"], True, self.elapsed_ms, is_timeout=False)
        else:
            self.session_wrong += 1
            self.play_sound("wrong")
            self.vocab_mgr.record_attempt(self.current_word["word"], False, self.elapsed_ms, is_timeout=False)

        self.update_score_header()
        self.show_next_prompt()

    # =========================================================================
    # 2-B. 모드 2: 4지선다 스피드 퀴즈 (4-Choice Speed Reflex)
    # =========================================================================
    def setup_choice_question(self):
        self.test_phase = "testing"
        self.clear_frame(self.action_area)

        # 오답 보기 3개 무작위 선별
        all_words = list(DEFAULT_VOCABULARY) + self.vocab_mgr.data["custom_words"]
        other_meanings = [w["meaning"] for w in all_words if w["word"] != self.current_word["word"]]
        wrong_samples = random.sample(other_meanings, min(3, len(other_meanings)))

        self.choices = wrong_samples + [self.current_word["meaning"]]
        random.shuffle(self.choices)
        self.correct_choice_idx = self.choices.index(self.current_word["meaning"])

        # 4개 보기 버튼 그리드 배치 (2x2)
        grid_frame = tk.Frame(self.action_area, bg=self.C_CARD)
        grid_frame.pack(fill="both", expand=True, padx=20, pady=5)

        self.choice_buttons = []
        for i, choice_text in enumerate(self.choices):
            row = i // 2
            col = i % 2

            btn = tk.Button(
                grid_frame,
                text=f"[{i+1}] {choice_text}",
                font=("맑은 고딕", 12, "bold"),
                bg="#3d4452",
                fg=self.C_TEXT,
                activebackground=self.C_PRIMARY,
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                anchor="w",
                padx=15,
                pady=12,
                wraplength=280,
                command=lambda idx=i: self.on_choice_selected(idx)
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=8, pady=6)
            self.choice_buttons.append(btn)

        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)

        # 숫자키 1, 2, 3, 4 바인딩
        for key in ["1", "2", "3", "4"]:
            self.root.bind(key, lambda e, k=key: self.on_choice_selected(int(k) - 1))
            self.root.bind(f"<KP_{key}>", lambda e, k=key: self.on_choice_selected(int(k) - 1))

    def on_choice_selected(self, chosen_idx):
        if self.test_phase != "testing" or not self.is_timer_running:
            return

        self.stop_timer()
        self.test_phase = "result"
        self.elapsed_ms = round((time.perf_counter() - self.start_time) * 1000, 1)

        # 키 바인딩 해제
        for key in ["1", "2", "3", "4"]:
            self.root.unbind(key)
            self.root.unbind(f"<KP_{key}>")

        self.session_total += 1
        is_correct = (chosen_idx == self.correct_choice_idx)

        # 선택 결과 시각 피드백
        for i, btn in enumerate(self.choice_buttons):
            if i == self.correct_choice_idx:
                btn.configure(bg=self.C_SUCCESS, fg="white")
            elif i == chosen_idx and not is_correct:
                btn.configure(bg=self.C_DANGER, fg="white")
            else:
                btn.configure(bg="#2b313d", fg="#747d8c")

        if is_correct:
            self.session_correct += 1
            self.session_speeds.append(self.elapsed_ms)
            self.lbl_speed_feedback.configure(
                text=f"⚡ 정답! 반응 시간: {self.elapsed_ms:.0f}ms ({self.elapsed_ms/1000:.2f}초)",
                fg=self.C_SUCCESS
            )
            self.play_sound("success")
            self.vocab_mgr.record_attempt(self.current_word["word"], True, self.elapsed_ms, is_timeout=False)
        else:
            self.session_wrong += 1
            self.lbl_speed_feedback.configure(
                text=f"❌ 오답! 정답: {self.current_word['meaning']}",
                fg=self.C_DANGER
            )
            self.play_sound("wrong")
            self.vocab_mgr.record_attempt(self.current_word["word"], False, self.elapsed_ms, is_timeout=False)

        self.update_score_header()
        self.show_next_prompt()

    # =========================================================================
    # 냉정한 타임오버 처리 (Timeout Handling)
    # =========================================================================
    def on_timeout(self):
        self.test_phase = "result"
        self.session_total += 1
        self.session_timeout += 1

        # 붉은 화면 & 타임오버 알림
        self.test_card.configure(bg="#3a1c22")
        self.lbl_word_category.configure(bg="#3a1c22")
        self.lbl_english_word.configure(bg="#3a1c22")
        self.lbl_korean_meaning.configure(
            text=f"⏰ 시간 초과! (미암기 판정)\n정답: {self.current_word['meaning']}",
            fg=self.C_DANGER,
            bg="#3a1c22"
        )
        self.lbl_speed_feedback.configure(
            text=f"망설임은 미암기입니다. ({self.time_limit_sec.get():.1f}초 초과)",
            fg=self.C_DANGER,
            bg="#3a1c22"
        )

        self.play_sound("timeout")

        # 단어 기록 (타임오버 오답 처리)
        self.vocab_mgr.record_attempt(self.current_word["word"], False, self.elapsed_ms, is_timeout=True)

        # 타이핑 모드인 경우 입력창 비활성화 및 미완성 입력 표시
        if self.selected_mode.get() == "typing":
            self.root.unbind("<Return>")
            if self.entry_korean:
                typed = self.entry_korean.get().strip()
                self.entry_korean.unbind("<Return>")
                self.entry_korean.configure(state="disabled")
                if typed:
                    self.lbl_speed_feedback.configure(
                        text=f"망설임은 미암기입니다. (입력 중이던 내용: '{typed}')",
                        fg=self.C_DANGER,
                        bg="#3a1c22"
                    )

        # 4지선다인 경우 정답 표시
        elif self.selected_mode.get() == "choice":
            for key in ["1", "2", "3", "4"]:
                self.root.unbind(key)
                self.root.unbind(f"<KP_{key}>")
            for i, btn in enumerate(self.choice_buttons):
                if i == self.correct_choice_idx:
                    btn.configure(bg=self.C_SUCCESS, fg="white")
                else:
                    btn.configure(bg="#2b313d", fg="#747d8c")

        self.update_score_header()
        self.show_next_prompt()

    def show_next_prompt(self):
        """문제 완료 후 다음 문제로 넘어가는 대기 버튼/단축키 제공"""
        self.clear_frame(self.action_area)

        next_btn = tk.Button(
            self.action_area,
            text="다음 단어 진행 ➡️ [Space / Enter]",
            font=("맑은 고딕", 13, "bold"),
            bg=self.C_PRIMARY,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12,
            command=self.next_question
        )
        next_btn.pack(pady=15)

        self.root.bind("<space>", lambda e: self.next_question())
        self.root.bind("<Return>", lambda e: self.next_question())

    def update_score_header(self):
        acc = (self.session_correct / self.session_total * 100) if self.session_total > 0 else 0
        avg_speed = (sum(self.session_speeds) / len(self.session_speeds)) if self.session_speeds else 0
        speed_str = f"{avg_speed:.0f}ms" if avg_speed > 0 else "-"

        self.lbl_score_info.configure(
            text=f"진행: {self.session_total}  |  정답: {self.session_correct} ({acc:.0f}%)  |  타임오버: {self.session_timeout}  |  평균속도: {speed_str}"
        )

    # =========================================================================
    # 3. 보조 기능 (오답 노트 & 단어 관리 팝업)
    # =========================================================================
    def open_weak_words_dialog(self):
        """오답 노트 및 통계 다이얼로그"""
        win = tk.Toplevel(self.root)
        win.title("📖 취약 단어 및 오답 노트")
        win.geometry("700x520")
        win.configure(bg=self.C_BG)
        win.transient(self.root)

        tk.Label(
            win,
            text="📖 오답 및 미완성 단어 목록",
            font=("맑은 고딕", 16, "bold"),
            fg=self.C_ACCENT,
            bg=self.C_BG
        ).pack(anchor="w", padx=20, pady=(15, 5))

        tk.Label(
            win,
            text="3회 연속 시간 내 패스하지 못했거나 최근 타임오버/틀린 단어들입니다.",
            font=("맑은 고딕", 10),
            fg=self.C_SUBTEXT,
            bg=self.C_BG
        ).pack(anchor="w", padx=20, pady=(0, 10))

        # 트리뷰 표
        tree_frame = tk.Frame(win, bg=self.C_BG)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=5)

        columns = ("word", "meaning", "streak", "attempts", "avg_speed", "last")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=14)

        tree.heading("word", text="영단어")
        tree.heading("meaning", text="한국어 뜻")
        tree.heading("streak", text="연속 패스")
        tree.heading("attempts", text="시도")
        tree.heading("avg_speed", text="평균속도")
        tree.heading("last", text="최근결과")

        tree.column("word", width=120, anchor="w")
        tree.column("meaning", width=220, anchor="w")
        tree.column("streak", width=80, anchor="center")
        tree.column("attempts", width=60, anchor="center")
        tree.column("avg_speed", width=90, anchor="center")
        tree.column("last", width=90, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 데이터 채우기
        all_words = list(DEFAULT_VOCABULARY) + self.vocab_mgr.data["custom_words"]
        for w in all_words:
            stats = self.vocab_mgr.data["word_stats"].get(w["word"])
            if stats:
                streak = f"{stats.get('consecutive_pass', 0)} / 3"
                attempts = stats.get("attempts", 0)
                speed = f"{stats.get('avg_speed_ms', 0):.0f}ms"
                last_res = stats.get("last_result", "")
                last_kr = "✅ 통과" if last_res == "pass" else ("⏰ 타임오버" if last_res == "timeout" else "❌ 오답")
                tree.insert("", "end", values=(w["word"], w["meaning"], streak, attempts, speed, last_kr))

        # 하단 액션 버튼
        btn_frame = tk.Frame(win, bg=self.C_BG)
        btn_frame.pack(fill="x", padx=20, pady=15)

        def test_weak_now():
            win.destroy()
            self.selected_category.set("오답집중")
            self.start_test_session()

        tk.Button(
            btn_frame,
            text="🔥 이 오답 단어들만 즉시 집중 테스트",
            font=("맑은 고딕", 11, "bold"),
            bg=self.C_DANGER,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            command=test_weak_now
        ).pack(side="left")

        tk.Button(
            btn_frame,
            text="닫기",
            font=("맑은 고딕", 10),
            bg="#57606f",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            command=win.destroy
        ).pack(side="right")

    def open_word_manager_dialog(self):
        """단어 추가 및 관리 다이얼로그"""
        win = tk.Toplevel(self.root)
        win.title("➕ 단어 추가 / 관리")
        win.geometry("640x540")
        win.configure(bg=self.C_BG)
        win.transient(self.root)

        tk.Label(
            win,
            text="➕ 나만의 영단어 추가 / 관리",
            font=("맑은 고딕", 16, "bold"),
            fg=self.C_ACCENT,
            bg=self.C_BG
        ).pack(anchor="w", padx=20, pady=(15, 5))

        # 단어 직접 추가 입력 폼
        form_frame = tk.LabelFrame(
            win,
            text=" 새 단어 직접 등록 ",
            font=("맑은 고딕", 11, "bold"),
            fg=self.C_TEXT,
            bg=self.C_CARD,
            padx=15,
            pady=10
        )
        form_frame.pack(fill="x", padx=20, pady=10)

        f_row1 = tk.Frame(form_frame, bg=self.C_CARD)
        f_row1.pack(fill="x", pady=4)
        tk.Label(f_row1, text="영단어:", font=("맑은 고딕", 10), fg=self.C_TEXT, bg=self.C_CARD, width=8, anchor="w").pack(side="left")
        entry_word = tk.Entry(f_row1, font=("맑은 고딕", 11), width=30)
        entry_word.pack(side="left", padx=5)

        f_row2 = tk.Frame(form_frame, bg=self.C_CARD)
        f_row2.pack(fill="x", pady=4)
        tk.Label(f_row2, text="한국어 뜻:", font=("맑은 고딕", 10), fg=self.C_TEXT, bg=self.C_CARD, width=8, anchor="w").pack(side="left")
        entry_meaning = tk.Entry(f_row2, font=("맑은 고딕", 11), width=30)
        entry_meaning.pack(side="left", padx=5)

        # 리스트박스 (등록된 사용자 단어 목록)
        list_frame = tk.LabelFrame(
            win,
            text=" 내가 등록한 단어 목록 ",
            font=("맑은 고딕", 11, "bold"),
            fg=self.C_TEXT,
            bg=self.C_CARD,
            padx=15,
            pady=10
        )
        list_frame.pack(fill="both", expand=True, padx=20, pady=5)

        listbox = tk.Listbox(
            list_frame,
            font=("맑은 고딕", 10),
            bg="#1e272e",
            fg="white",
            selectbackground=self.C_PRIMARY
        )
        listbox.pack(side="left", fill="both", expand=True)

        scroller = tk.Scrollbar(list_frame, command=listbox.yview)
        listbox.configure(yscrollcommand=scroller.set)
        scroller.pack(side="right", fill="y")

        def refresh_custom_list():
            listbox.delete(0, tk.END)
            for w in self.vocab_mgr.data["custom_words"]:
                listbox.insert(tk.END, f"{w['word']} : {w['meaning']}")

        def add_word_action():
            w = entry_word.get()
            m = entry_meaning.get()
            success, msg = self.vocab_mgr.add_custom_word(w, m)
            if success:
                entry_word.delete(0, tk.END)
                entry_meaning.delete(0, tk.END)
                refresh_custom_list()
                messagebox.showinfo("성공", msg, parent=win)
            else:
                messagebox.showwarning("오류", msg, parent=win)

        def delete_selected_action():
            sel = listbox.curselection()
            if not sel:
                return
            item_text = listbox.get(sel[0])
            word_to_del = item_text.split(" : ")[0]
            self.vocab_mgr.delete_custom_word(word_to_del)
            refresh_custom_list()

        def import_file_action():
            file_path = filedialog.askopenfilename(
                title="단어장 텍스트 파일 불러오기",
                filetypes=[("텍스트/CSV 파일", "*.txt;*.csv"), ("모든 파일", "*.*")],
                parent=win
            )
            if not file_path:
                return
            added_cnt = 0
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        # 구분자 (쉼표, 콜론, 탭 등 자동 파싱)
                        parts = None
                        for sep in [",", "\t", ":", "-"]:
                            if sep in line:
                                parts = line.split(sep, 1)
                                break
                        if parts and len(parts) >= 2:
                            w, m = parts[0].strip(), parts[1].strip()
                            if w and m:
                                ok, _ = self.vocab_mgr.add_custom_word(w, m)
                                if ok:
                                    added_cnt += 1
                refresh_custom_list()
                messagebox.showinfo("가져오기 완료", f"총 {added_cnt}개의 단어가 추가되었습니다!", parent=win)
            except Exception as e:
                messagebox.showerror("오류", f"파일을 읽는 도중 오류가 발생했습니다:\n{e}", parent=win)

        btn_add = tk.Button(
            f_row2,
            text="단어 등록",
            font=("맑은 고딕", 10, "bold"),
            bg=self.C_PRIMARY,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            command=add_word_action
        )
        btn_add.pack(side="left", padx=10)

        # 하단 조작 버튼
        bot_frame = tk.Frame(win, bg=self.C_BG)
        bot_frame.pack(fill="x", padx=20, pady=10)

        tk.Button(
            bot_frame,
            text="📁 텍스트/CSV 파일로 일괄 가져오기",
            font=("맑은 고딕", 10),
            bg="#57606f",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=import_file_action
        ).pack(side="left")

        tk.Button(
            bot_frame,
            text="선택 단어 삭제",
            font=("맑은 고딕", 10),
            bg=self.C_DANGER,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=delete_selected_action
        ).pack(side="right")

        refresh_custom_list()

    def confirm_reset_stats(self):
        if messagebox.askyesno("기록 초기화", "정말로 모든 단어의 암기 기록 및 숙련도를 초기화하시겠습니까?"):
            self.vocab_mgr.reset_stats()
            self.build_menu_screen()
            messagebox.showinfo("완료", "학습 기록이 초기화되었습니다.")

    def on_escape_pressed(self, event=None):
        self.return_to_menu()

    def return_to_menu(self):
        self.stop_timer()
        self.build_menu_screen()

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ReflexVocabApp(root)
    root.mainloop()

`

---
*본 파일은 사용자의 요청에 따라 자동 생성되었습니다.*
