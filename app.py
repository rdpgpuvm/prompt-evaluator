from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
import os

app = Flask(__name__)

# Pydantic model for structured output
class PromptEvaluation(BaseModel):
    score: int = Field(description="Quality score from 1-10")
    clarity: int = Field(description="Clarity score from 1-10")
    specificity: int = Field(description="Specificity score from 1-10")
    context: int = Field(description="Context score from 1-10")
    overall_feedback: str = Field(description="Overall feedback on the prompt")
    improvement_suggestions: List[str] = Field(description="List of specific improvement suggestions")

# Initialize output parser
parser = PydanticOutputParser(pydantic_object=PromptEvaluation)

# Evaluation prompt template
EVALUATION_TEMPLATE = """You are an expert prompt engineer. Evaluate the quality of the following prompt and provide structured feedback.

Prompt to evaluate:
{prompt}

Evaluate the prompt on the following criteria:
1. Clarity: Is the prompt clear and unambiguous?
2. Specificity: Does it provide enough specific details?
3. Context: Does it include necessary context?

Provide your evaluation in the following JSON format:
{format_instructions}
"""

eval_prompt = PromptTemplate(
    template=EVALUATION_TEMPLATE,
    input_variables=["prompt"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Create evaluation chain
evaluation_chain = eval_prompt | llm | parser

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/evaluate', methods=['POST'])
def evaluate_prompt():
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' field in request body"}), 400
        
        prompt_text = data['prompt']
        
        if not prompt_text or not isinstance(prompt_text, str):
            return jsonify({"error": "Prompt must be a non-empty string"}), 400
        
        # Run evaluation
        result = evaluation_chain.invoke({"prompt": prompt_text})
        
        return jsonify({
            "input_prompt": prompt_text,
            "evaluation": {
                "overall_score": result.score,
                "breakdown": {
                    "clarity": result.clarity,
                    "specificity": result.specificity,
                    "context": result.context
                },
                "feedback": result.overall_feedback,
                "improvements": result.improvement_suggestions
            }
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "service": "Prompt Quality Evaluator",
        "version": "1.0.0",
        "endpoints": {
            "POST /evaluate": "Evaluate a prompt - send JSON with 'prompt' field",
            "GET /health": "Health check"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)