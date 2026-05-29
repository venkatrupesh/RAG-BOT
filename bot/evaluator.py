"""Answer evaluation logic."""

import os
from typing import List, Tuple
import openai
from .prompt_builder import build_evaluation_prompt


class Evaluator:
    """Evaluate candidate answers."""
    
    def __init__(self, api_key: str = None):
        """Initialize the evaluator.
        
        Args:
            api_key: OpenAI API key (defaults to env variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
    
    def evaluate_answer(self, question: str, answer: str, context: List[str]) -> Tuple[int, str]:
        """Evaluate a candidate's answer.
        
        Args:
            question: The interview question
            answer: Candidate's answer
            context: Relevant context from documents
            
        Returns:
            Tuple of (score, feedback)
        """
        prompt = build_evaluation_prompt(question, answer, context)
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert technical interviewer evaluating answers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=400
        )
        
        evaluation = response.choices[0].message.content
        
        # Parse score from response (simple approach)
        try:
            score = int(evaluation.split("Score:")[1].split("/")[0].strip())
        except:
            score = 5  # Default score if parsing fails
        
        return score, evaluation
