import streamlit as st
import os
from litellm import completion

st.set_page_config(
    page_title="YouTube Intro Generator",
    page_icon="🎬",
    layout="centered"
)

LLM_PROVIDERS = [
    "mistral/mistral-medium",
    "cohere/command-r",
    "together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1"
]

llm_provider_api = {
    "mistral/mistral-medium" : "MISTRAL_API_KEY",
    "cohere/command-r": "COHERE_API_KEY",
    "together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1": "TOGETHER_API_KEY"
}

def gen_catchy_intro(script, model, api_key):
    try:
        messages = [
            {
                "role": "system", 
                "content": """You are an expert YouTube content creator 
                who specializes in writing engaging, attention-grabbing intros. 
                Create a punchy, energetic intro that:
                - Is 15-30 seconds long when spoken
                - Hooks the viewer immediately
                - Hints at the key value or excitement in the full video
                - Uses dynamic, conversational language
                - Matches the tone of the provided script"""
            },
            {
                "role": "user", 
                "content": f"Here's the full video script. Please generate a catchy intro:\n\n{script}"
            }
        ]
        response = completion(
            model=model, 
            messages=messages,
            max_tokens=150,
            temperature=0.7,
            api_key=api_key
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating intro with {model}: {str(e)}")
        return None
    

def main():
    st.title("🎬 YouTube Intro Generator")
    st.write("Paste your full video script below to generate a catchy intro!")

    selected_model = st.selectbox(
        "Choose an AI Model", 
        LLM_PROVIDERS,
        index=None,
        placeholder="Select the AI model you want to use for generating the intro"
    )

    api_key = st.text_input("API Key", key="chatbot_api_key", value=st.secrets.get(llm_provider_api[selected_model]),type="password", placeholder="Enter API key")

    script = st.text_area(
        "Video Script", 
        height=250, 
        placeholder="Paste your complete video script here..."
    )

    if st.button("Generate Catchy Intro 🚀"):
        if not script.strip():
            st.warning("Please enter a video script first!")
        else:
            with st.spinner(f"Crafting the perfect intro using {selected_model}..."):
                intro = gen_catchy_intro(script, selected_model,api_key)
                
                if intro:
                    st.subheader("Your Catchy YouTube Intro:")
                    st.write(intro)
                    
                    # Copy to clipboard button
                    st.code(intro)
                    st.toast("Intro generated successfully!", icon="🎉")

if __name__ == "__main__":
    main()