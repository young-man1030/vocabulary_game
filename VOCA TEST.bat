@echo off
chcp 65001 > nul
title 영단어 반사 암기 테스터 (Reflex Vocab)
echo ========================================================
echo   ⚡ 영단어 반사 암기 테스터를 실행합니다...
echo   (1~3초 내 즉각적인 한국어 뜻 반사 회상 훈련)
echo ========================================================
start "" pythonw "%~dp0reflex_vocab_app.py"
exit
