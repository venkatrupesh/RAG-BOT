"""Prompt assembly for the interviewer."""

from typing import List


def build_interview_prompt(context: List[str], question: str) -> str:
    """Build a prompt for the interviewer.
    
    Args:
        context: List of relevant text chunks
        question: The interview question
        
    Returns:
        Formatted prompt string
    """
    context_text = "\n\n".join(context)
    
    prompt = f"""You are an expert technical interviewer. Based on the following context from documents, ask an insightful interview question.

Context:
{context_text}

Previous conversation: {question}

Generate a thoughtful follow-up interview question or provide feedback on the candidate's response."""
    
    return prompt


def build_evaluation_prompt(question: str, answer: str, context: List[str]) -> str:
    """Build a prompt for evaluating an answer.
    
    Args:
        question: The interview question
        answer: Candidate's answer
        context: Relevant context from documents
        
    Returns:
        Formatted evaluation prompt
    """
    context_text = "\n\n".join(context)
    
    prompt = f"""You are an expert technical interviewer. Evaluate the following answer based on the provided context.

Context:
{context_text}

Question: {question}

Answer: {answer}

Provide a score from 1-10 and brief feedback on the answer's accuracy, completeness, and clarity."""
    
    return prompt
