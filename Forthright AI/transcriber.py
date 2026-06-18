from faster_whisper import WhisperModel

# Load model only once
model = WhisperModel(
    "large-v3",
    device="cpu",
    compute_type="int8"
)

def remove_repeated_sentences(text):

    sentences = text.split(".")

    unique_sentences = []
    seen = set()

    for sentence in sentences:

        sentence = sentence.strip()

        if sentence and sentence not in seen:

            unique_sentences.append(sentence)

            seen.add(sentence)

    if len(unique_sentences) == 0:
        return text

    return ". ".join(unique_sentences) + "."


def transcribe(audio_path):

    segments, info = model.transcribe(
        audio_path,
        beam_size=1,
        best_of=1,
        temperature=0.0,
        condition_on_previous_text=False,
        vad_filter=True,
        repetition_penalty=1.2
    )

    text = ""

    for segment in segments:

        text += segment.text + " "

    text = text.strip()

    text = remove_repeated_sentences(text)

    return text