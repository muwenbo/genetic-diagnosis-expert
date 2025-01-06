import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
# Initialize the OpenAI client
root_path = Path(__file__).resolve().parent.parent
load_dotenv(root_path / '.env')

def generate_response(prompt):
    """
    Generate a streaming response from ChatGPT
    """
    try:
        client = OpenAI()
        # Create a streaming chat completion
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        
        # Return the stream
        return stream
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def main():
    st.title("Customized Prompt Test for ChatGPT")
    
    # Text input for user prompt
    user_prompt = st.text_input("Enter your prompt:")
    
    # Response container
    response_container = st.empty()
    
    # Generate button
    if st.button("Generate Response"):
        if user_prompt:
            # Clear previous response
            response_container.empty()
            
            # Generate streaming response
            stream = generate_response(user_prompt)
            
            if stream:
                # Collect the full response text
                full_response = ""
                
                # Display streaming response
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        # Get the chunk of text
                        chunk_text = chunk.choices[0].delta.content
                        
                        # Append to full response
                        full_response += chunk_text
                        
                        # Update the container with current response
                        response_container.markdown(full_response)
        else:
            st.warning("Please enter a prompt")

if __name__ == "__main__":
    main()