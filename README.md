**Objective**
The purpose of this task is to evaluate the voice morphing system and perform a Mean Opinion Score (MOS) assessment.



**Step 1: Clone the Git Repository**

Open your terminal and clone the repository:

git clone <repository_url>
cd <repository_folder>

**Step 2: Record Your Voice**

Run the audio recording script:

python audiorecording.py

When prompted, replace the sample name with your own name and clearly say the following sentence:

**"This is a local voice morphing test."**

After recording, save the audio file.

**Step 3: Configure Voice Morphing**

Open:

voicemorphing.py

Update the following information:

Change the speaker name to your own name.
Update the recording file name to match the audio file generated in Step 2.

Example:

speaker_name = "John"
audio_file = "John_recording.wav"

**Step 4: Run Voice Morphing**

Execute:

python voicemorphing.py

Wait for the processing to complete.

**Step 5: Record the Output**

Observe the Command Prompt (CMD) output after the program finishes.

Copy and paste the complete result into your report.

**Step 6: Upload the Audio**

Upload the audio in github/elsewhere for members to proceed with MOS evaluation.

**Step 7: Complete MOS Evaluation**

After listening to the generated voice output, complete the MOS evaluation form:

Open the provided Google Sheet.

link: https://docs.google.com/spreadsheets/d/1VUNrHqNb-kO1Y93Whae5ekTF9w1jrgWQ1qtNJDlBB54/edit?usp=sharing

Listen to the generated audio carefully.
