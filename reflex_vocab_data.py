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
