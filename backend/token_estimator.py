import re
from typing import Union, List, Dict

class TokenEstimator:
    def __init__(self):
        # Approximate ratios for different languages and content types
        self.ratios = {
            'english': 0.75,  # ~4 characters per token for English
            'chinese': 1.5,   # ~2 characters per token for Chinese
            'code': 0.8,      # Slightly higher than English text
            'json': 0.85,     # JSON typically uses more tokens due to special characters
        }
        
        # Common special tokens
        self.special_tokens = {
            '<|endoftext|>': 1,
            '<|im_start|>': 1,
            '<|im_end|>': 1,
            '\n': 1,
        }

    def estimate_tokens(self, 
                       text: Union[str, List, Dict], 
                       language: str = 'english',
                       include_special_tokens: bool = True) -> int:
        """
        Estimate the number of tokens in a given text.
        
        Args:
            text: Input text, list, or dictionary
            language: Language of the text ('english', 'chinese', 'code', 'json')
            include_special_tokens: Whether to count special tokens
            
        Returns:
            Estimated token count
        """
        if isinstance(text, (list, dict)):
            text = str(text)
            language = 'json'
            
        # Convert text to string if it isn't already
        text = str(text)
        
        # Base character count
        char_count = len(text)
        
        # Count whitespace
        whitespace_count = len(re.findall(r'\s+', text))
        
        # Adjust character count for whitespace
        adjusted_char_count = char_count - (whitespace_count * 0.5)
        
        # Calculate base token estimate using language ratio
        ratio = self.ratios.get(language.lower(), self.ratios['english'])
        estimated_tokens = int(adjusted_char_count * ratio)
        
        # Add special tokens if requested
        if include_special_tokens:
            for token, count in self.special_tokens.items():
                estimated_tokens += text.count(token) * count
        
        # Add tokens for structural elements
        estimated_tokens += text.count('.') * 0.5  # Periods often get their own token
        estimated_tokens += len(re.findall(r'[A-Z][a-z]*', text)) * 0.2  # Capitalized words
        
        return max(1, int(estimated_tokens))

    def estimate_completion_tokens(self, 
                                 prompt: str, 
                                 expected_completion_length: str = 'medium') -> tuple:
        """
        Estimate tokens for both prompt and expected completion.
        
        Args:
            prompt: Input prompt
            expected_completion_length: 'short', 'medium', or 'long'
            
        Returns:
            Tuple of (prompt_tokens, estimated_completion_tokens)
        """
        prompt_tokens = self.estimate_tokens(prompt)
        
        # Rough completion length multipliers
        completion_multipliers = {
            'short': 0.5,
            'medium': 1.5,
            'long': 3.0
        }
        
        multiplier = completion_multipliers.get(expected_completion_length, 1.5)
        completion_tokens = int(prompt_tokens * multiplier)
        
        return prompt_tokens, completion_tokens

def token_estimation_from_text(full_text):
    estimator = TokenEstimator()

    # Estimate tokens for a prompt
    text = full_text

    # Estimate both prompt and completion tokens
    prompt_tokens, completion_tokens = estimator.estimate_completion_tokens(text)
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Estimated completion tokens: {completion_tokens}")
    print(f"Total estimated tokens: {prompt_tokens + completion_tokens}")

# Example usage
if __name__ == "__main__":
    estimator = TokenEstimator()
    
    # Example text
    prompt = "Explain the theory of relativity in simple terms."
    prompt_tokens, completion_tokens = estimator.estimate_completion_tokens(prompt)
    
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Estimated completion tokens: {completion_tokens}")
    print(f"Total estimated tokens: {prompt_tokens + completion_tokens}")