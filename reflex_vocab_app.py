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
