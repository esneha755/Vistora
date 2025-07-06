import streamlit as st
import requests
import json
from PIL import Image
import io

API_KEY = st.secrets["openai_api_key"]

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Home Page
if st.session_state.page == 'home':
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        text-align: center; 
        padding: 60px 20px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    '>
        <h1 style='
            font-size: 4rem; 
            color: white; 
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        '>🎨 Vistora AI</h1>
        <h3 style='
            color: #f0f0f0; 
            margin-bottom: 30px;
            font-weight: 300;
        '>Your AI-Powered Brand Identity Generator</h3>
        <p style='
            font-size: 1.2rem; 
            color: #e8e8e8; 
            max-width: 600px; 
            margin: 0 auto 40px;
            line-height: 1.6;
        '>
            Create professional brand identities in seconds. Generate brand names, taglines, 
            color palettes, and logos tailored to your industry and tone.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Creating Your Brand", 
                     use_container_width=True, 
                     key="start_btn",
                     help="Click to begin your brand identity journey"):
            st.session_state.page = 'generator'
            st.rerun()
    
    # Add features section
    st.markdown("""
    <div style='margin-top: 40px;'>
        <div style='display: flex; justify-content: space-around; flex-wrap: wrap;'>
            <div style='text-align: center; margin: 20px; padding: 20px; background: #f8f9fa; border-radius: 15px; flex: 1; min-width: 250px;'>
                <h4 style='color: #667eea; margin-bottom: 15px;'>🎯 Smart Targeting</h4>
                <p style='color: #666;'>AI analyzes your target audience to create perfectly matched brand identities</p>
            </div>
            <div style='text-align: center; margin: 20px; padding: 20px; background: #f8f9fa; border-radius: 15px; flex: 1; min-width: 250px;'>
                <h4 style='color: #667eea; margin-bottom: 15px;'>🎨 Visual Identity</h4>
                <p style='color: #666;'>Get complete color palettes, logos, and typography recommendations</p>
            </div>
            <div style='text-align: center; margin: 20px; padding: 20px; background: #f8f9fa; border-radius: 15px; flex: 1; min-width: 250px;'>
                <h4 style='color: #667eea; margin-bottom: 15px;'>⚡ Instant Results</h4>
                <p style='color: #666;'>Generate professional brand identities in under 30 seconds</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Generator Page
elif st.session_state.page == 'generator':
    st.title("🎨 Brand Identity Generator")
    
    if st.button("← Back to Home", key="back_btn"):
        st.session_state.page = 'home'
        st.rerun()
    
    # Inputs
    genre = st.selectbox("Genre", ["Select Genre...", "Healthcare", "Tech", "Fashion", "Food", "Finance", "Education", "Sports", "Gaming"], index=0)
    tone = st.selectbox("Tone", ["Select Tone...", "Professional", "Friendly", "Bold", "Elegant", "Playful", "Minimalist", "Luxury"], index=0)
    target_audience = st.selectbox("Target Audience", ["Select Audience...", "Young Adults (18-25)", "Millennials (26-40)", "Gen X (41-55)", "Baby Boomers (56+)", "Professionals", "Students", "Parents", "Entrepreneurs", "Health Enthusiasts", "Tech Savvy"], index=0)
    description = st.text_input("Brief Description", placeholder="e.g., Modern sustainable products for eco-conscious consumers")
    
    if st.button("Generate Brand Identity", key="generate_btn") and genre != "Select Genre..." and tone != "Select Tone..." and target_audience != "Select Audience..." and description:
        # Generate brand identity
        prompt = f"""Generate a comprehensive brand identity for a {genre} business with {tone} tone targeting {target_audience}. Business description: {description}. 

Provide in this exact format:
**Brand Name:** [Name] then a line break
**Tagline:** [Tagline] then a line break
**Mission Statement:** [Mission] then a line break
**Brand Personality:** [3-5 traits] then a line break
**Color Palette:** 
- Primary: [Color Name] (#HEXCODE) then a line break
- Secondary: [Color Name] (#HEXCODE) then a line break
- Accent: [Color Name] (#HEXCODE) then a line break
Make sure to include the primary, secondary, and accent colors with their names and hex codes.
Add the color palette in a visually appealing format.
Include the primary, secondary, and accent colors in the logo description.
**Typography:** [Font names and styles] then a line break 
**Logo Description:** [Detailed description for logo generation]"""
        
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        
        # Text generation
        text_data = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300
        }
        
        with st.spinner("Generating..."):
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
                logo_prompt = f"Modern {tone} logo for {genre} company targeting {target_audience}, clean design, professional, suitable for branding"
                logo_data = {
                    "model": "dall-e-3",
                    "prompt": logo_prompt,
                    "size": "1024x1024",
                    "n": 1
                }
                
                logo_response = requests.post("https://api.openai.com/v1/images/generations", json=logo_data, headers=headers)
                
                if logo_response.status_code == 200:
                    logo_url = logo_response.json()["data"][0]["url"]
                    st.subheader("🖼️ Generated Logo")
                    st.image(logo_url, caption="Your Brand Logo", width=300)
                else:
                    st.error(f"Logo generation failed: {logo_response.status_code}")
            else:
                st.error(f"Error: {text_response.status_code}")
    
