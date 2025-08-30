import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="Image Processing Laboratory",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling with soft background
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        min-height: 100vh;
    }
    
    /* Main content area */
    .main .block-container {
        background: rgba(255, 255, 255, 255);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .main-header {
        background: white; /* Change header background to white */
        color: #333; /* Adjust text color for contrast */
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        font-size: 1.5rem;
    }
    
    .control-panel {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(230, 230, 230, 0.5);
        backdrop-filter: blur(5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .image-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin-bottom: 1rem;
        background: white;
        padding: 0.5rem;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        backdrop-filter: blur(5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border: none;
        border-radius: 2px;
        margin: 2rem 0;
        opacity: 0.7;
    }
    
    .welcome-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        text-align: center;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
        border-top: 4px solid #667eea;
        backdrop-filter: blur(5px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        box-shadow: 2px 0 15px rgba(0,0,0,0.1);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        padding: 0.25rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        margin: 0.25rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'image' not in st.session_state:
    st.session_state.image = None

def calculate_image_stats(image):
    """Calculate various image statistics"""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    stats = {
        'Width': image.shape[1],
        'Height': image.shape[0],
        'Channels': len(image.shape) if len(image.shape) == 2 else image.shape[2],
        'Mean Brightness': np.mean(gray),
        'Std Brightness': np.std(gray),
        'Min Intensity': np.min(gray),
        'Max Intensity': np.max(gray),
        'Total Pixels': image.shape[0] * image.shape[1]
    }
    return stats, gray

def apply_image_processing(image, params):
    """Apply image processing based on parameters"""
    processed = image.copy()
    
    # Convert to grayscale if requested
    if params['grayscale']:
        if len(processed.shape) == 3:
            processed = cv2.cvtColor(processed, cv2.COLOR_RGB2GRAY)
            processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB)
    
    # Apply Gaussian blur
    if params['blur'] > 0:
        ksize = int(params['blur']) * 2 + 1
        processed = cv2.GaussianBlur(processed, (ksize, ksize), 0)
    
    # Adjust brightness
    if params['brightness'] != 0:
        processed = cv2.convertScaleAbs(processed, beta=params['brightness'])
    
    # Adjust contrast
    if params['contrast'] != 1.0:
        processed = cv2.convertScaleAbs(processed, alpha=params['contrast'])
    
    # Apply edge detection
    if params['edge_detection']:
        if len(processed.shape) == 3:
            gray = cv2.cvtColor(processed, cv2.COLOR_RGB2GRAY)
        else:
            gray = processed
        edges = cv2.Canny(gray, params['canny_low'], params['canny_high'])
        processed = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    
    # Apply morphological operations
    if params['morphology'] != 'None':
        if len(processed.shape) == 3:
            gray = cv2.cvtColor(processed, cv2.COLOR_RGB2GRAY)
        else:
            gray = processed
        
        kernel = np.ones((params['kernel_size'], params['kernel_size']), np.uint8)
        
        if params['morphology'] == 'Erosion':
            gray = cv2.erode(gray, kernel, iterations=1)
        elif params['morphology'] == 'Dilation':
            gray = cv2.dilate(gray, kernel, iterations=1)
        elif params['morphology'] == 'Opening':
            gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
        elif params['morphology'] == 'Closing':
            gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        
        processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    
    return processed

# Webcam page
if st.session_state.page == 'webcam':
    st.markdown("""
    <div class="main-header">
        <h1>Webcam Capture</h1>
        <p>Capture images directly from your camera</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("← Back to Main", type="primary", use_container_width=True):
            st.session_state.page = 'main'
            st.rerun()
        
        st.markdown("""
        <div class="control-panel">
            <h4>Instructions</h4>
            <ol>
                <li>Allow camera access when prompted</li>
                <li>Position yourself in frame</li>
                <li>Click capture when ready</li>
                <li>Process your captured image</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        camera_image = st.camera_input("Take a photo")
        
        if camera_image is not None:
            image = np.array(Image.open(camera_image))
            st.session_state.image = image
            
            st.success("Image captured successfully!")
            
            if st.button("Process This Image", type="primary", use_container_width=True):
                st.session_state.page = 'main'
                st.rerun()

# Main processing page
elif st.session_state.page == 'main':
    st.markdown("""
    <div class="main-header">
        <h1>Image Processing Laboratory</h1>
        <p>Professional computer vision and image analysis tools</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Image source selection
    st.subheader("Select Image Source")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Upload File", use_container_width=True):
            st.session_state.image_source = 'upload'
    
    with col2:
        if st.button("Use Camera", use_container_width=True):
            st.session_state.page = 'webcam'
            st.rerun()
    
    with col3:
        if st.button("Sample Images", use_container_width=True):
            st.session_state.image_source = 'sample'
    
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    # Image loading based on selection
    image = st.session_state.image if st.session_state.image is not None else None
    
    # Handle different image sources
    if hasattr(st.session_state, 'image_source'):
        if st.session_state.image_source == 'upload':
            uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
            if uploaded_file is not None:
                image = np.array(Image.open(uploaded_file))
                st.session_state.image = image
        
        elif st.session_state.image_source == 'sample':
            sample_choice = st.selectbox(
                "Choose a sample image:",
                ["Portrait Style", "Checkerboard Pattern", "Random Noise", "Color Gradient", "Geometric Shapes"]
            )
            
            if st.button("Load Selected Sample"):
                if sample_choice == "Portrait Style":
                    image = np.zeros((512, 512, 3), dtype=np.uint8)
                    # Create a simple face-like pattern
                    cv2.circle(image, (256, 256), 200, (255, 220, 177), -1)  # Face
                    cv2.circle(image, (200, 200), 30, (255, 255, 255), -1)   # Left eye
                    cv2.circle(image, (312, 200), 30, (255, 255, 255), -1)   # Right eye
                    cv2.circle(image, (200, 200), 15, (50, 50, 150), -1)     # Left pupil
                    cv2.circle(image, (312, 200), 15, (50, 50, 150), -1)     # Right pupil
                    cv2.ellipse(image, (256, 320), (60, 30), 0, 0, 180, (200, 100, 100), -1)  # Mouth
                
                elif sample_choice == "Checkerboard Pattern":
                    image = np.zeros((400, 400, 3), dtype=np.uint8)
                    for i in range(8):
                        for j in range(8):
                            color = [240, 240, 240] if (i + j) % 2 == 0 else [40, 40, 40]
                            image[i*50:(i+1)*50, j*50:(j+1)*50] = color
                
                elif sample_choice == "Random Noise":
                    image = np.random.randint(0, 255, (400, 400, 3), dtype=np.uint8)
                
                elif sample_choice == "Color Gradient":
                    image = np.zeros((400, 400, 3), dtype=np.uint8)
                    for i in range(400):
                        image[i, :] = [i*255//400, (400-i)*255//400, 128]
                
                elif sample_choice == "Geometric Shapes":
                    image = np.ones((400, 400, 3), dtype=np.uint8) * 245  # Light background
                    cv2.rectangle(image, (50, 50), (150, 150), (220, 50, 50), -1)   # Red square
                    cv2.circle(image, (300, 100), 50, (50, 220, 50), -1)            # Green circle
                    points = np.array([[200, 200], [300, 300], [100, 300]], np.int32)
                    cv2.fillPoly(image, [points], (50, 50, 220))                     # Blue triangle
                
                st.session_state.image = image
    
    # Main processing interface
    if image is not None:
        st.success("Image loaded successfully!")
        
        sidebar_col, main_col = st.columns([0.8, 2.3])
        
        with sidebar_col:
            # st.markdown("""
            # <div class="control-panel">
            #     <h7>Processing Controls</h7>
            # </div>
            # """, unsafe_allow_html=True)
            
            # Processing parameters
            params = {}
            
            # Basic adjustments
            st.markdown("**Basic Adjustments**")
            params['grayscale'] = st.checkbox("Convert to Grayscale")
            params['blur'] = st.slider("Gaussian Blur", 0, 10, 0)
            params['brightness'] = st.slider("Brightness", -100, 100, 0)
            params['contrast'] = st.slider("Contrast", 0.1, 3.0, 1.0, 0.1)
            
            st.markdown("---")
            
            # Edge detection
            st.markdown("**Edge Detection**")
            params['edge_detection'] = st.checkbox("Enable Edge Detection")
            if params['edge_detection']:
                params['canny_low'] = st.slider("Low Threshold", 0, 255, 50)
                params['canny_high'] = st.slider("High Threshold", 0, 255, 150)
            else:
                params['canny_low'] = 50
                params['canny_high'] = 150
            
            st.markdown("---")
            
            # Morphological operations
            st.markdown("**Morphological Operations**")
            params['morphology'] = st.selectbox("Operation Type", 
                                              ["None", "Erosion", "Dilation", "Opening", "Closing"])
            if params['morphology'] != 'None':
                params['kernel_size'] = st.slider("Kernel Size", 3, 15, 5, 2)
            else:
                params['kernel_size'] = 5

            st.markdown("---")
            st.markdown("**Export Options**")

            if st.button("Download Processed Image", use_container_width=True):
                st.session_state.download_processed = True

            if st.button("Download Statistics", use_container_width=True):
                st.session_state.download_stats = True

            if st.button("Load New Image", use_container_width=True):
                st.session_state.image = None
                if hasattr(st.session_state, 'image_source'):
                    del st.session_state.image_source
                st.rerun()

                   # Process the image
            processed_image = apply_image_processing(image, params)
            
            # Calculate statistics
            original_stats, original_gray = calculate_image_stats(image)
            processed_stats, processed_gray = calculate_image_stats(processed_image)
            
            

            # Handle downloads
            if hasattr(st.session_state, 'download_processed') and st.session_state.download_processed:
                processed_pil = Image.fromarray(processed_image.astype('uint8'))
                buf = BytesIO()
                processed_pil.save(buf, format='PNG')
                st.download_button(
                    label="Click to Download Processed Image",
                    data=buf.getvalue(),
                    file_name="processed_image.png",
                    mime="image/png",
                )
                st.session_state.download_processed = False

            if hasattr(st.session_state, 'download_stats') and st.session_state.download_stats:
                all_stats = {**{f"Original_{k}": v for k, v in original_stats.items()},
                           **{f"Processed_{k}": v for k, v in processed_stats.items()}}
                stats_df = pd.DataFrame([all_stats])
                csv = stats_df.to_csv(index=False)
                st.download_button(
                    label="Click to Download Statistics",
                    data=csv,
                    file_name="image_statistics.csv",
                    mime="text/csv",
                )
                st.session_state.download_stats = False
            
        with main_col:
            # Process the image
            processed_image = apply_image_processing(image, params)
            
            # Calculate statistics
            original_stats, original_gray = calculate_image_stats(image)
            processed_stats, processed_gray = calculate_image_stats(processed_image)
            
            
            # Display images
            img_col1, img_col2 = st.columns(2)
            
            with img_col1:
                st.markdown("### Original Image")
                st.image(image, use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                with st.expander("View Statistics"):
                    stats_df = pd.DataFrame(list(original_stats.items()), columns=['Property', 'Value'])
                    st.dataframe(stats_df, use_container_width=True, hide_index=True)
            
            with img_col2:
                st.markdown("### Processed Image")
                st.image(processed_image, use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                with st.expander("View Statistics"):
                    processed_stats_df = pd.DataFrame(list(processed_stats.items()), columns=['Property', 'Value'])
                    st.dataframe(processed_stats_df, use_container_width=True, hide_index=True)
            
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            
            # Analysis section
            st.markdown("### Image Analysis & Visualization")
            
            tab1, tab2, tab3 = st.tabs(["Histogram Analysis", "Statistical Comparison", "Intensity Distribution"])
            
            with tab1:
                original_hist = cv2.calcHist([original_gray], [0], None, [256], [0, 256])
                processed_hist = cv2.calcHist([processed_gray], [0], None, [256], [0, 256])
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=list(range(256)),
                    y=original_hist.flatten(),
                    mode='lines',
                    name='Original',
                    line=dict(color='#667eea', width=3),
                    fill='tonexty'
                ))
                
                fig.add_trace(go.Scatter(
                    x=list(range(256)),
                    y=processed_hist.flatten(),
                    mode='lines',
                    name='Processed',
                    line=dict(color='#764ba2', width=3),
                    fill='tonexty'
                ))
                
                fig.update_layout(
                    title='Pixel Intensity Histogram Comparison',
                    xaxis_title='Pixel Intensity (0-255)',
                    yaxis_title='Frequency',
                    hovermode='x unified',
                    height=500,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    brightness_data = {
                        'Metric': ['Mean', 'Standard Deviation', 'Minimum', 'Maximum'],
                        'Original': [original_stats['Mean Brightness'], original_stats['Std Brightness'], 
                                   original_stats['Min Intensity'], original_stats['Max Intensity']],
                        'Processed': [processed_stats['Mean Brightness'], processed_stats['Std Brightness'],
                                    processed_stats['Min Intensity'], processed_stats['Max Intensity']]
                    }
                    
                    brightness_df = pd.DataFrame(brightness_data)
                    fig_brightness = px.bar(brightness_df, x='Metric', y=['Original', 'Processed'],
                                          title='Intensity Statistics Comparison',
                                          barmode='group',
                                          color_discrete_sequence=['#667eea', '#764ba2'])
                    fig_brightness.update_layout(height=400)
                    st.plotly_chart(fig_brightness, use_container_width=True)
                
                with chart_col2:
                    props_data = {
                        'Property': ['Width', 'Height', 'Total Pixels'],
                        'Value': [original_stats['Width'], original_stats['Height'], original_stats['Total Pixels']]
                    }
                    
                    fig_props = px.pie(values=props_data['Value'], names=props_data['Property'],
                                     title='Image Properties',
                                     color_discrete_sequence=px.colors.sequential.Blues_r)
                    fig_props.update_layout(height=400)
                    st.plotly_chart(fig_props, use_container_width=True)
            
            with tab3:
                dist_col1, dist_col2 = st.columns(2)
                
                with dist_col1:
                    intensity_ranges = ['Very Dark (0-63)', 'Dark (64-127)', 'Bright (128-191)', 'Very Bright (192-255)']
                    original_ranges = [
                        np.sum((original_gray >= 0) & (original_gray < 64)),
                        np.sum((original_gray >= 64) & (original_gray < 128)),
                        np.sum((original_gray >= 128) & (original_gray < 192)),
                        np.sum((original_gray >= 192) & (original_gray <= 255))
                    ]
                    
                    fig_pie_orig = px.pie(values=original_ranges, names=intensity_ranges,
                                        title='Original Image Intensity Distribution',
                                        color_discrete_sequence=['#1f4e79', '#2e6ba8', '#4a90d9', '#87ceeb'])
                    fig_pie_orig.update_layout(height=400)
                    st.plotly_chart(fig_pie_orig, use_container_width=True)
                
                with dist_col2:
                    processed_ranges = [
                        np.sum((processed_gray >= 0) & (processed_gray < 64)),
                        np.sum((processed_gray >= 64) & (processed_gray < 128)),
                        np.sum((processed_gray >= 128) & (processed_gray < 192)),
                        np.sum((processed_gray >= 192) & (processed_gray <= 255))
                    ]
                    
                    fig_pie_proc = px.pie(values=processed_ranges, names=intensity_ranges,
                                        title='Processed Image Intensity Distribution',
                                        color_discrete_sequence=['#7b2d26', '#a73c2a', '#d64933', '#ff6b47'])
                    fig_pie_proc.update_layout(height=400)
                    st.plotly_chart(fig_pie_proc, use_container_width=True)
            
    else:
        # Welcome screen
        st.markdown("""
        <div class="welcome-card">
            <h2>Welcome to Image Processing Laboratory</h2>
            <p style="font-size: 1.2em; color: #666; margin-bottom: 2rem;">
                Professional-grade computer vision and image analysis tools
            </p>
            <p>Choose an image source above to begin processing</p>
        </div>
        """, unsafe_allow_html=True)