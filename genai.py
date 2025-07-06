import streamlit as st
import requests
import json
from PIL import Image
import io
from dotenv import load_dotenv
# Hidden API key
API_KEY = st.secrets["OPENAI_API_KEY"]
# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Home Page
if st.session_state.page == 'home':
    st.markdown("""
    <div style='text-align: center; padding: 50px;'>
        <h1 style='font-size: 4rem; color: gold; margin-bottom: 20px;'>🎨 Vistora AI</h1>
        <h3 style='color: white; margin-bottom: 30px;'>Your AI-Powered Brand Identity Generator</h3>
        <p style='font-size: 1.2rem; color: white; max-width: 600px; margin: 0 auto 40px;'>
            Create professional brand identities in seconds. Generate brand names, taglines, 
            color palettes, and logos tailored to your industry and tone.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Creating Your Brand", use_container_width=True, key="start_button"):
            st.session_state.page = 'generator'
            st.rerun()

# Generator Page
elif st.session_state.page == 'generator':
    st.title("🎨 Brand Identity Generator")
    
    if st.button("← Back to Home", key="back_button"):
        st.session_state.page = 'home'
        st.rerun()
    
    # Inputs
    genre = st.selectbox("Genre", ["Select Genre...", "Healthcare", "Tech", "Fashion", "Food", "Finance", "Education", "Sports", "Gaming"], index=0)
    tone = st.selectbox("Tone", ["Select Tone...", "Professional", "Friendly", "Bold", "Elegant", "Playful", "Minimalist", "Luxury"], index=0)
    target_audience = st.selectbox("Target Audience", ["Select Audience...", "Young Adults (18-25)", "Millennials (26-40)", "Gen X (41-55)", "Baby Boomers (56+)", "Professionals", "Students", "Parents", "Entrepreneurs", "Health Enthusiasts", "Tech Savvy"], index=0)
    description = st.text_input("Brief Description", placeholder="e.g., Modern sustainable products for eco-conscious consumers")
    
    # Check if all fields are filled
    all_fields_filled = (genre != "Select Genre..." and 
                        tone != "Select Tone..." and 
                        target_audience != "Select Audience..." and 
                        description.strip() != "")
    
    if st.button("Generate Brand Identity", key="generate_button", disabled=not all_fields_filled):
        if all_fields_filled:
            # Generate brand identity
            prompt = f"""You're a top-tier brand strategist and creative director. Based on the info below, generate a cohesive, unique brand identity tailored to the tone, audience, and business niche. Use strong branding principles, emotional appeal, and visual creativity. Generate a comprehensive brand identity for a {genre} business with {tone} tone targeting {target_audience}. Business description: {description}. 

Provide in this exact format:
**Brand Name:** [Name] then a line break
**Tagline:** [Tagline] then a line break
**Mission Statement:** [Mission] then a line break
**Brand Personality:** [3-5 traits] then a line break
**Color Palette:**  then a line break
- Primary: [Color Name] (#HEXCODE) then a line break
- Secondary: [Color Name] (#HEXCODE) then a line break
- Accent: [Color Name] (#HEXCODE) then a line break
Show the colors in a visually appealing way, with color swatches and names.
**Typography:** [Font names and styles] then a line break
**Logo Description:** [Detailed description for logo generation]then a line break"""
            
            headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
            
            # Text generation
            text_data = {
                "model": "gpt-4",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 300
            }
            
            with st.spinner("Generating your brand identity..."):
                try:
                    text_response = requests.post("https://api.openai.com/v1/chat/completions", json=text_data, headers=headers)
                    
                    if text_response.status_code == 200:
                        brand_content = text_response.json()["choices"][0]["message"]["content"]
                        st.success("✅ Brand Identity Generated!")
                        st.markdown(brand_content)
                        
                        # Extract and display color palette
                        import re
                        hex_colors = re.findall(r'#[0-9A-Fa-f]{6}', brand_content)
                        if hex_colors:
                            st.subheader("🎨 Color Palette")
                            cols = st.columns(len(hex_colors))
                            for i, color in enumerate(hex_colors):
                                with cols[i]:
                                    st.markdown(f"""
                                    <div style='background-color: {color}; height: 80px; width: 100%; border-radius: 10px; margin-bottom: 10px;'></div>
                                    <p style='text-align: center; font-weight: bold;'>{color}</p>
                                    """, unsafe_allow_html=True)
                        
                        # Generate logo
                        logo_prompt = f"Create a sleek, modern logo for a {genre} company targeting {target_audience}. The design should embody a {tone} tone with a clean, minimalist layout and refined elegance. Align with the {description}. Match the logo with the color themes from the color_palette that will be provided in the text generation. Prioritize sharp vector-style lines, flat design, and high contrast. Use sophisticated, well-balanced typography (sans-serif preferred), harmonious geometric or abstract iconography, and a subtle, curated color palette. The logo should feel premium and professional — perfect for use across websites, apps, business cards, and packaging. Present the logo on a white background, centered, with no extra text or watermark. Emphasize symmetry, branding versatility, and high visual impact."
                        logo_data = {
                            "model": "dall-e-3",
                            "prompt": logo_prompt,
                            "size": "1024x1024",
                            "n": 1
                        }
                        
                        with st.spinner("Generating logo..."):
                            logo_response = requests.post("https://api.openai.com/v1/images/generations", json=logo_data, headers=headers)
                            
                            if logo_response.status_code == 200:
                                logo_url = logo_response.json()["data"][0]["url"]
                                st.subheader("🖼️ Generated Logo")
                                st.image(logo_url, caption="Your Brand Logo", width=300)
                            else:
                                st.error(f"Logo generation failed: {logo_response.status_code}")
                                st.error(f"Error details: {logo_response.text}")
                    else:
                        st.error(f"Brand identity generation failed: {text_response.status_code}")
                        st.error(f"Error details: {text_response.text}")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please fill in all fields before generating.")
    
    # Show warning if not all fields are filled
    if not all_fields_filled:
        st.info("👆 Please fill in all fields above to enable brand generation.")
