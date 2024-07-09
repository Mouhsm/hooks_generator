import streamlit as st
import requests
import os

# Get the API key from the environment variable
API_KEY = os.getenv('GEMINI_API_KEY')

# Set up the Streamlit app
st.title('Hook Generator')
st.write('Generate creative hooks for your content!')

# Custom CSS for background color
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Input fields
user_input = st.text_area('Enter your idea:', height=100)
content_type = st.selectbox(
    'Select Content Type:',
    ['short video', 'email', 'social post', 'blog posts', 'video intro', 'ad', 'essay', 'speech']
)

# Generate hooks button and spinner
if st.button('Generate Hooks'):
    if user_input:
        with st.spinner('Generating hooks...'):
            prompt = f"""as an expert copywriter specialized in hook generation, your task is to analyze these 10 hook examples: [{"You won't believe this!"
            "What happens next will surprise you."
            "Here's the secret no one tells you."
            "Are you making this mistake?"
            "Transform your life in minutes."
            "Discover the truth about..."
            "Ready for a game-changer?"
            "This simple trick changed everything."
            "Stop doing this right now!"
            "Unlock your full potential."}] 
            and use the templates that fit most to generate 3 new Hooks for the following topic: {user_input} and Usage in: {content_type} I need you to write only the three short hooks, nothing else. The output should be a Only The list of Hooks with the type."""

            headers = {
                'Content-Type': 'application/json',
            }

            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }

            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}',
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    candidates = response_data.get('candidates', [])

                    hooks_list = []
                    for candidate in candidates:
                        content = candidate.get('content', {}).get('parts', [{}])[0].get('text', '')
                        hooks_list.append(content)

                    # Display hooks
                    hooks_placeholder = st.empty()
                    hooks_placeholder.markdown('\n\n'.join(hooks_list))

                except Exception as e:
                    st.error('Error parsing response. Please try again.')
            else:
                st.error(f'Error generating hooks: {response.status_code} - {response.text}')
    else:
        st.warning('Please enter your idea.')
