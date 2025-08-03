# 📕 TaxChatbot
세금 관련 질의응답을 도와주는 LLM 기반 Chatbot 리포지토리

<div align="center">
<img alt="GitHub issues" src="https://img.shields.io/github/issues/catturtle123/LLM-Chatbot?label=Issues&labelColor=32439c&color=a0ddff">
<img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/catturtle123/LLM-Chatbot?label=PRs&labelColor=32439c&color=a0ddff">
<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/w/catturtle123/LLM-Chatbot?label=Commits&labelColor=32439c&color=a0ddff">
</div>

## 🧾 프로젝트 소개

**Chatbot**은 GPT 기반의 LLM과 RAG 구조를 활용하여 세금 관련 질문에 정확하고 신뢰할 수 있는 답변을 제공하는 챗봇 서비스입니다.  
문서 기반 질의응답에서 발생하는 표현 불일치, 문맥 단절, 이미지 누락 등의 문제를 해결하며, Streamlit 기반의 UI를 통해 실시간 응답 경험을 제공합니다.

> “복잡한 세금 정보, 이제는 쉽게 묻고 정확하게 답 받으세요.”

## ✅ 주요 기능 및 개선 사항

- 📚 Word 문서 기반 세금 정보 벡터화 및 질의 응답
- 🔍 키워드 사전을 활용한 표현 불일치 해결
- 🧠 LLM Evaluation (LangSmith)
- 🧾 Few-Shot Prompting을 통한 응답 형식 통일
- 💬 대화 히스토리를 반영한 문맥 기반 응답
- ☁️ Streamlit Cloud 배포 환경 대응

## 💻 기술 스택

<div align="center">
<img alt="LangChain" src="https://img.shields.io/badge/LangChain-16c27a?style=flat-square&logo=chainlink&logoColor=white">
<img alt="LangSmith" src="https://img.shields.io/badge/LangSmith-8a44ff?style=flat-square&logo=fastapi&logoColor=white">
<img alt="GPT" src="https://img.shields.io/badge/GPT-000000?style=flat-square&logo=openai&logoColor=white">
<img alt="Pinecone" src="https://img.shields.io/badge/Pinecone-5cb1ff?style=flat-square&logo=pinecone&logoColor=white">
<img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-ff4b4b?style=flat-square&logo=streamlit&logoColor=white">
</div>

- LangChain / LangSmith
- OpenAI GPT (RAG 구조 기반)
- Streamlit (with stream, 세션 저장 기능)
- Pinecone (벡터 DB)

## 🧠 프로젝트 기여 내용

### 1. 데이터 전처리 및 키워드 사전 구축
- Word 내 이미지 → Markdown 변환으로 이미지 정보 활용
- ‘사람’ → ‘거주자’ 등 표현 불일치를 해결하는 키워드 사전 도입
- 정확도 향상: **Answer_helpfulness_score 0.95 → 1.00**, **Answer_v_reference_score 0.75 → 0.95**

### 2. LangSmith 기반 LLM 평가 자동화
- 다양한 질문 시나리오 수집 → 정확성 및 hallucination 자동 분석
- 평가 결과를 기반으로 프롬프트 및 키워드 개선 루프 적용

### 3. Few-Shot Prompting 통한 출처 명시 응답 유도
- 답변 내 문서 출처 포함되도록 유도 → 신뢰성 있는 결과 제공

### 4. Chat History 연동
- 이전 질문 포함하여 문맥을 고려한 자연스러운 대화 흐름 지원

### 5. Vector DB 전환 (Chroma → Pinecone)
- 휘발성 Chroma 제거, 클라우드 기반 Pinecone 도입
- Streamlit Cloud 환경에서도 안정적 동작 확보