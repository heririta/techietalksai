import os

import streamlit as st
from agno.media import Image as AgnoImage
from medical_agent import agent
from PIL import Image as PILImage

# from agno.models.anthropic import Claude
from agno.models.deepseek import DeepSeek
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.models.google import Gemini


st.set_page_config(
    page_title="Medical Imaging Analysis",
    page_icon="🏥",
    layout="wide",
)
st.markdown("##### 🏥 built using [Agno](https://github.com/agno-agi/agno)")


def main():
    with st.sidebar:
        st.info(
            "This tool provides AI-powered analysis of medical imaging data using "
            "advanced computer vision and radiological expertise."
        )
        st.warning(
            "⚠️DISCLAIMER: This tool is for educational and informational purposes only. "
            "All analyses should be reviewed by qualified healthcare professionals. "
            "Do not make medical decisions based solely on this analysis.",
            # icon="⚠️"
        )

    st.title("🏥 Medical Imaging Diagnosis Agent")
    st.write("Upload a medical image for professional analysis")

    # Create containers for better organization
    upload_container = st.container()
    image_container = st.container()
    analysis_container = st.container()

    with upload_container:
        uploaded_file = st.file_uploader(
            "Upload Medical Image",
            type=["jpg", "jpeg", "png", "dicom"],
            help="Supported formats: JPG, JPEG, PNG, DICOM",
        )

    if uploaded_file is not None:
        with image_container:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # Use PILImage for display
                pil_image = PILImage.open(uploaded_file)
                width, height = pil_image.size
                aspect_ratio = width / height
                new_width = 500
                new_height = int(new_width / aspect_ratio)
                resized_image = pil_image.resize((new_width, new_height))

                st.image(
                    resized_image,
                    caption="Uploaded Medical Image",
                    use_container_width=True,
                )

                analyze_button = st.button(
                    "🔍 Analyze Image", type="primary", use_container_width=True
                )

                additional_info = st.text_area(
                    "Provide additional context about the image (e.g., patient history, symptoms)",
                    placeholder="Enter any relevant information here...",
                )

        with analysis_container:
            if analyze_button:
                image_path = "temp_medical_image.png"
                # Save the resized image
                resized_image.save(image_path, format="PNG")

                with st.spinner("🔄 Analyzing image... Please wait."):
                    try:
                        # Use AgnoImage for the agent
                        agno_image = AgnoImage(filepath=image_path)
                        prompt = (
                            f"Analyze this medical image considering the following context: {additional_info}"
                            if additional_info
                            else "Analyze this medical image and provide detailed findings."
                        )
                        response = agent.run(
                            prompt,
                            images=[agno_image],
                        )


                        response_stream: Iterator[RunResponse] = agent.run(
                            prompt,
                            images=[agno_image],
                            stream=True
                        )
                        
                        response_text = ""
                        placeholder = st.empty()
                        
                        for chunk in response_stream:
                            response_text += chunk.content
                            
                            placeholder.markdown(response_text + "▌")
                        
                        placeholder.markdown("### 📋 Analysis Results")
                        placeholder.markdown("---")
                        placeholder.markdown(response_text)

                        # st.markdown("### 📋 Analysis Results")
                        # st.markdown("---")
                        # if hasattr(response, "content"):
                        #     st.markdown(response.content)
                        # elif isinstance(response, str):
                        #     st.markdown(response)
                        # elif isinstance(response, dict) and "content" in response:
                        #     st.markdown(response["content"])
                        # else:
                        #     st.markdown(str(response))
                        # st.markdown("---")
                        st.warning(
                            "Note: This analysis is generated by AI and should be reviewed by "
                            "a qualified healthcare professional.",
                            icon="⚠️"
                        )

                    except Exception as e:
                        st.error(f"Analysis error: {str(e)}")
                        st.info(
                            "Please try again or contact support if the issue persists."
                        )
                        print(f"Detailed error: {e}")
                    finally:
                        if os.path.exists(image_path):
                            os.remove(image_path)
    else:
        st.info("👆 Please upload a medical image to begin analysis")


if __name__ == "__main__":
    main()
