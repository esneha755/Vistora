import streamlit as st
import requests
import json
from PIL import Image
import io
import zipfile


API_KEY = st.secrets["OPEN_API_KEY"]
# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Home Page
if st.session_state.page == 'home':
    
    # Simple, reliable CSS animations that work in Streamlit
    st.markdown("""
    <style>
    /* Reset and base styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Keyframe animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(-45deg, #667eea, #764ba2, #667eea, #764ba2);
        background-size: 400% 400%;
        animation: gradientShift 0.1s ease infinite;
        text-align: center;
        padding: 80px 30px;
        border-radius: 25px;
        margin-bottom: 50px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 1s ease-out;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 20%, rgba(255,255,255,0.1) 0%, transparent 50%),
                    radial-gradient(circle at 70% 80%, rgba(255,255,255,0.1) 0%, transparent 50%);
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
    }
    
    .hero-title {
        font-size: 4.5rem;
        color: white;
        margin-bottom: 20px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        font-weight: 700;
        letter-spacing: -2px;
        animation: fadeInUp 1s ease-out 0.3s both;
    }
    
    .hero-subtitle {
        color: #f8f9fa;
        margin-bottom: 30px;
        font-weight: 300;
        font-size: 1.8rem;
        animation: fadeInUp 1s ease-out 0.6s both;
    }
    
    .hero-description {
        font-size: 1.3rem;
        color: #e9ecef;
        max-width: 700px;
        margin: 0 auto 50px;
        line-height: 1.7;
        animation: fadeInUp 1s ease-out 0.9s both;
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 20px;
        padding: 35px 25px;
        margin: 20px 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(102, 126, 234, 0.1);
        height: 50%;
        cursor: pointer;
        animation: fadeInUp 1s ease-out both;
    }
    
    .feature-card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 20px;
        animation: bounce 5s infinite;
        display: inline-block;
    }
    
    .feature-icon:nth-of-type(2n) {
        animation: float 3s ease-in-out infinite;
        animation-delay: 0.5s;
    }
    
    .feature-title {
        color: #495057;
        margin-bottom: 15px;
        font-size: 1.4rem;
        font-weight: 600;
    }
    
    .feature-text {
        color: #6c757d;
        line-height: 1.6;
        font-size: 1.1rem;
    }
    
    /* Section Titles */
    .section-title {
        text-align: center;
        color: #495057;
        margin: 60px 0 40px 0;
        font-size: 2.5rem;
        font-weight: 700;
        animation: fadeInUp 1s ease-out;
    }
    
    /* CTA Sections */
    .cta-section {
        text-align: center;
        margin: 60px 0;
        animation: fadeInUp 1s ease-out;
    }
    
    /* Button Enhancements */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 18px 40px;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        min-width: 200px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
        .hero-title {
            font-size: 3rem;
        }
        .hero-subtitle {
            font-size: 1.4rem;
        }
        .hero-description {
            font-size: 1.1rem;
        }
        .stat-item {
            margin: 10px 20px;
        }
        .feature-card {
            margin: 15px 5px;
        }
        .stButton > button {
            padding: 15px 30px;
            font-size: 1.1rem;
            min-width: 180px;
        }
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class='hero-container'>
        <div class='hero-content'>
            <div class='hero-title'>🎨 Vistora AI</div>
            <div class='hero-subtitle'>Your AI-Powered Brand Identity Generator</div>
            <div class='hero-description'>
                Transform your business vision into a compelling brand identity. Generate professional 
                brand names, captivating taglines, stunning color palettes, and memorable logos 
                tailored specifically to your industry and brand personality.
            </div>
        </div>
    """, unsafe_allow_html=True)
    # Call-to-Action Button
    st.markdown("<div class='cta-section'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Creating Your Brand", 
                use_container_width=True, 
                key="start_btn",
                help="Begin your brand identity journey in seconds"):
                st.session_state.page = 'generator'
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Features Section
    st.markdown("<h2 class='section-title'>✨ Powerful Features</h2>", unsafe_allow_html=True)
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🎯</div>
            <div class='feature-title'>AI-Powered Targeting</div>
            <div class='feature-text'>
                Our advanced AI analyzes your target audience, industry trends, and 
                competitor landscape to create perfectly matched brand identities that resonate.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🎨</div>
            <div class='feature-title'>Complete Visual Identity</div>
            <div class='feature-text'>
                Get comprehensive brand packages including custom color palettes, 
                typography recommendations, logo concepts, and brand guidelines.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>⚡</div>
            <div class='feature-title'>Lightning Fast Results</div>
            <div class='feature-text'>
                Generate professional-quality brand identities in under 30 seconds. 
                No more weeks of back-and-forth with designers.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional Features Row
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    
    feature_col4, feature_col5, feature_col6 = st.columns(3)
    
    with feature_col4:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>💡</div>
            <div class='feature-title'>Creative Variations</div>
            <div class='feature-text'>
                Generate multiple creative options and variations to choose from, 
                ensuring you find the perfect match for your brand vision.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col5:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🌍</div>
            <div class='feature-title'>Industry Expertise</div>
            <div class='feature-text'>
                Trained on successful brands across 50+ industries ensuring relevant and effective results.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col6:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📱</div>
            <div class='feature-title'>Multi-Platform Ready</div>
            <div class='feature-text'>
                All generated assets are optimized for digital and print use, 
                ensuring your brand looks great across all platforms and media.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Simple JavaScript for additional interactivity (no external dependencies)
    st.markdown("""
    <script>
    // Simple scroll reveal effect
    function revealOnScroll() {
        const elements = document.querySelectorAll('.feature-card, .testimonial-card');
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    }
    
    // Add scroll listener
    window.addEventListener('scroll', revealOnScroll);
    
    // Initial check
    revealOnScroll();
    
    // Add click effects to buttons
    document.addEventListener('DOMContentLoaded', function() {
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                ripple.classList.add('ripple');
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    });
    </script>
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

                    response = requests.get(logo_url)
                    image_bytes = io.BytesIO(response.content)
                    # Prepare ZIP in memory
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zf:
                        zf.writestr("brand_identity.txt", brand_content)
                        zf.writestr("colors.json", json.dumps(hex_colors))  # Optional
                        
                        # Add image
                        zf.writestr("logo.png", image_bytes.getvalue())

                    zip_buffer.seek(0)

                    # Download button
                    st.download_button(
                        label="📥 Download Brand Kit (ZIP)",
                        data=zip_buffer,
                        file_name='brand_kit.zip',
                        mime='application/zip'
                    )



                else:
                    st.error(f"Logo generation failed: {logo_response.status_code}")
            else:
                st.error(f"Error: {text_response.status_code}")
    
               
                
