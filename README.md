PDF to Audiobook Converter is a Python application that transforms PDF documents into spoken audio files. By extracting text from PDFs and generating speech, this tool enables users to listen to their documents, improving accessibility and productivity for various audiences.
Features:
Extracts text from any PDF document
Converts extracted text to speech using pyttsx3
User-friendly graphical interface (Tkinter)
Adjustable volume and reading speed
Playback and export audio as WAV files
Responsive and error-handling design
Tools and Libraries Used:
Python 3.x
PyMuPDF (fitz) for PDF text extraction
pyttsx3 for text-to-speech conversion
Tkinter for GUI
os, threading for file and process handling
GUI Class:
The PDFtoAudioApp class sets up the user interface and orchestrates key operations:
Upload Button: Lets the user select a PDF file. Displays file name and extracts text.
Volume & Speed Sliders: Allow adjustment of audio playback parameters.
Convert Button: Starts conversion in a background thread, keeping the GUI responsive.
Play Button: Plays the generated audio using the operating system’s default player (os.startfile on Windows).
Export Button: Copies the output audio file to a user-specified location.
Error Handling:
If no text is found after uploading, an error message appears and conversion/playback are disabled.
File operations use exception handling to report errors to the user via status messages.
The application is structured to guide users through uploading a PDF, converting it to speech, listening to the output, and exporting the result, all through an intuitive interface with robust error handling.
