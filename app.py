import streamlit as st
import moviepy.editor as mp
import os



st.set_page_config(page_title='VideoResizer')


# Streamlit UI
st.title("MP4 Video Resizer")

# Upload video
uploaded_file = st.file_uploader("Upload a video (MP4 format)", type=["mp4", "mov"])

if uploaded_file is not None:
    st.write("Uploaded video:")
    video_filename = uploaded_file.name
    st.write(uploaded_file.name)
    st.write(uploaded_file.size)
    

    # Check the file extension
    if video_filename.endswith(".mp4") or video_filename.endswith(".mov"):
        # Display the uploaded video
        st.video(uploaded_file)

        # Resize options
        st.write("Choose resize options:")
        new_width = st.number_input("New Width (pixels):", min_value=1, value=640)
        preserve_aspect_ratio = st.checkbox("Preserve Aspect Ratio", value=True)

        # User input for output path
        #output_path = st.text_input("Enter output filename for the resized video", value="resized_video.mp4")
        output_path = "resized_video.mp4"

        if st.button("Resize"):
            if new_width <= 0:
                st.error("Please enter a valid width.")
            else:
                # Save the uploaded video temporarily
                with open(video_filename, "wb") as video_file:
                    video_file.write(uploaded_file.read())

                    

                # Read the video
                video = mp.VideoFileClip(video_filename)

                # Calculate the new height while preserving aspect ratio
                if preserve_aspect_ratio:
                    aspect_ratio = video.size[0] / video.size[1]
                    new_height = int(new_width / aspect_ratio)
                    
                else:
                    new_height = video.size[1]

                # Resize the video
                resized_video = video.resize((new_width, new_height))

                # Save the resized video to the user-specified output path
                output_path = output_path.strip()  # Remove leading/trailing spaces
                resized_video.write_videofile(output_path)


                st.success(f"Video resized:  New width: " + str(new_width) + " - New height: " + str(new_height) )

                # Display the resized video

                st.write("Resized video:")
                st.video(output_path)

                # Allow the user to download the resized video
                #st.download_button(label="Download Resized Video", data=output_path, file_name="Resizedvideo.mp4", key="download_button")

                with open(output_path, "rb") as f:
                    st.download_button("Download Video", data=f, file_name="resized_video_width"+str(new_width)+".mp4")

                # Clean up the resources
                resized_video.close()
                video.close()

                # Remove temporary uploaded video
                os.remove(video_filename)
    else:
        st.error("Please upload a video in MP4 format.")
