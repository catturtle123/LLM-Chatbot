from dotenv import load_dotenv
from langsmith.evaluation import evaluate
import openai
from langsmith import traceable
from langsmith.wrappers import wrap_openai
from llm import get_history_retriever, get_llm, get_retriever, get_rag_chain, get_dictionary_chain
from dotenv import load_dotenv
from langsmith import Client
from langchain import hub

load_dotenv()

client = Client()

retriever = get_history_retriever()
llm = get_llm()

# 데이터 불러오기
dataset = client.read_dataset(dataset_name="income_tax_dataset")

# RAG bot
class RagBot:
    def __init__(self, retriever, model: str = "gpt-4o"):
        self._retriever = retriever
        self._client = wrap_openai(openai.Client())
        self._model = model
        self._dictionary_chain = get_dictionary_chain()

    @traceable()
    def retrieve_docs(self, question: str):
        normalized_question = self._dictionary_chain.invoke({"question": question})
        docs = self._retriever.invoke({"input": normalized_question})

        return {
            "normalized_question": normalized_question,
            "docs": docs
        }

    @traceable()
    def invoke_llm(self, question, docs):
        rag_chain = get_rag_chain(self._retriever)

        response = rag_chain.invoke(
            {
                "input": question
            },
            config={"configurable": {"session_id": "internal-session"}}
        )

        return {
            "answer": response,
            "contexts": [str(doc) for doc in docs],
        }

    @traceable()
    def get_answer(self, question: str):
        result = self.retrieve_docs(question)
        normalized_question = result["normalized_question"]
        docs = result["docs"]

        return self.invoke_llm(normalized_question, docs)

rag_bot = RagBot(retriever)

def predict_rag_answer(example: dict):
    """답변만 평가할 때 사용"""
    response = rag_bot.get_answer(example["input_question"])
    return {"answer": response["answer"]}

def predict_rag_answer_with_context(example: dict):
    """Context를 활용해서 hallucination을 평가할 때 사용"""
    response = rag_bot.get_answer(example["input_question"])
    return {"answer": response["answer"], "contexts": response["contexts"]}

# Grade prompt
# 답변의 정확도를 측정하기위해 사용되는 프롬프트
grade_prompt_answer_accuracy = prompt = hub.pull("langchain-ai/rag-answer-vs-reference")

# RAG 답변 성능을 측정하기 위한 evaluator
def answer_evaluator(run, example) -> dict:
    input_question = example.inputs["input_question"]
    reference = example.outputs["output_answer"]
    prediction = run.outputs["answer"]

    answer_grader = grade_prompt_answer_accuracy | llm

    score = answer_grader.invoke({"question": input_question,
                                  "correct_answer": reference,
                                  "student_answer": prediction})
    score = score["Score"]

    return {"key": "answer_v_reference_score", "score": score}

# 답변이 사용자의 질문에 얼마나 도움되는지 판단하는 프롬프트
grade_prompt_answer_helpfulness = prompt = hub.pull("langchain-ai/rag-answer-helpfulness")

def answer_helpfulness_evaluator(run, example) -> dict:

    input_question = example.inputs["input_question"]
    prediction = run.outputs["answer"]

    answer_grader = grade_prompt_answer_helpfulness | llm

    # Evaluator 실행
    score = answer_grader.invoke({"question": input_question,
                                  "student_answer": prediction})
    score = score["Score"]

    return {"key": "answer_helpfulness_score", "score": score}

# hallucination 판단을 위한 Evaluator
grade_prompt_hallucinations = prompt = hub.pull("langchain-ai/rag-answer-hallucination")

def answer_hallucination_evaluator(run, example) -> dict:

    input_question = example.inputs["input_question"]
    contexts = run.outputs["contexts"]

    prediction = run.outputs["answer"]

    answer_grader = grade_prompt_hallucinations | llm

    score = answer_grader.invoke({"documents": contexts,
                                  "student_answer": prediction})
    score = score["Score"]

    return {"key": "answer_hallucination", "score": score}

dataset_name = "income_tax_dataset"
experiment_results = evaluate(
    predict_rag_answer_with_context,
    data=dataset_name,
    evaluators=[answer_evaluator, answer_helpfulness_evaluator, answer_hallucination_evaluator],
    experiment_prefix="evalator-with-dic",
    metadata={"version": "income tax v1, gpt-4o"}, 
)