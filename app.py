import streamlit as st
import unidecode
import time

# --- Paragraphs ---
spanish_paragraphs = [
    "Ir de vacaciones es relajante y descanso del trabajo y del instituto. Pero muy rico para mí.",
    "No, no he visitado España. Pero me gustaría ir un día, escuché es lujoso y grande, a mi madre le gusta España y viaja todos los años.",
    "Mis vacaciones ideales serían en la playa. Me gustaría tomar sol y nadar, también visitar los monumentos. Además, mis vacaciones deben ser preciosas.",
    "El fin de semana pasado fui a mi club donde jugue al futbol con mi hermano porque es demasiado divertido!",
    "Vivo en Crewe, es un pueblo en el noroeste. Me chifla mi pueblo porque hay mucho que hacer y esta en el campo.",
    "Me gustaria cambiar mi vida, es muy frenetica, puede ser un poco aburrido. Me decepsiona mi pueblo, no hay un hospital. Que desastre!",
]

german_paragraphs = [
    "Mein perfektes Wochenend ware unmoglich fur mich. Ich wurde Mount Everest besteigen. Wenn ich die Wahl hatte, wurde ich gern zeit mit meine Grosseltern verbringen.",
    "Nein, ich bin beschafigt. Wenn ich die wahl hatte, wurde ich mit meinen Freund Komodien sehen. Meistens, alles Fernsehen ist schrecklich.",
    "Nein nicht wirklich. Ich finde fern sehr langweilig. Ich sehe jeden Monat fern, obwohl meine Familie geniesst es, ich hasse es. Als ich junger war, gluckte ich gern Realityshows.",
    "Mein perfektes Wochenende mit meinen Familien wird auf dem Strand sein, ich wurde gern mich sonnen, auch gebaude besuchen. Ich kann kaum warten!",
    "Letztes Jahr, fotografierte ich meine amusante Familie. Auf dem Foto gab es meinen kleinen Bruder und meine zwei Eltern, sie sagte das Foto ist doof und ich denke sie sind pessimistich.",
    "Naturlich ist mein Lieblingsfestival meinen Geburtstag. Zur Abwechslung wache ich auf um funf Uhr, repaire ich mein Geburtstag Gedenknis. Normalerweise das Gedenknis wird jedes Jahr von vielen Touristen besucht.",
]

# --- Streamlit App ---
st.title("🧠 Language Flashcard Game")

if "language" not in st.session_state:
    st.session_state.language = "Spanish"
    st.session_state.index = 0
    st.session_state.errors = []
    st.session_state.step = 3
    st.session_state.start = 0
    st.session_state.end = 8
    st.session_state.skip = False
    st.session_state.completed = False

# --- Language Selection ---
language = st.selectbox("Choose Language", ["Spanish", "German"])
if language != st.session_state.language:
    st.session_state.language = language
    st.session_state.index = 0
    st.session_state.errors = []
    st.session_state.start = 0
    st.session_state.end = 8
    st.session_state.completed = False

# --- Paragraphs ---
paragraphs = spanish_paragraphs if st.session_state.language == "Spanish" else german_paragraphs
selected_para = st.selectbox("Pick Paragraph", range(1, len(paragraphs) + 1), index=st.session_state.index)
st.session_state.index = selected_para - 1
words = paragraphs[st.session_state.index].split()

# --- Skip Mode ---
st.session_state.skip = st.checkbox("Skip Mode (Full Paragraph)", value=st.session_state.skip)

# --- Display Flashcard ---
if st.session_state.skip:
    current_part = ' '.join(words)
    st.session_state.completed = True
else:
    current_part = ' '.join(words[st.session_state.start:st.session_state.end])

# Show and auto-clear the flashcard
memorize_box = st.empty()
memorize_box.info("Memorize this part:")
memorize_box.markdown(f"**{current_part}**")
time.sleep(5)
memorize_box.empty()


# --- Input Area ---
st.write("Now type what you remember:")
user_input = st.text_area("Your Answer", height=150)

def get_hint(text):
    parts = text.split()
    if not parts: return "", ""
    return parts[0], parts[-1]

first_word, last_word = get_hint(current_part)
st.caption(f"Hint: `{first_word} ... {last_word}`")

# --- Check Button ---
if st.button("Check"):
    normalized_input = unidecode.unidecode(user_input.strip())
    normalized_part = unidecode.unidecode(current_part.strip())

    if normalized_input == normalized_part:
        st.success("✅ Correct! Well done!")
        if not st.session_state.skip:
            st.session_state.start += st.session_state.step
            st.session_state.end = st.session_state.start + st.session_state.step

        if st.session_state.start >= len(words):
            st.session_state.completed = True
            st.balloons()
            st.info("You've completed the paragraph!")
    else:
        # Error feedback
        original_words = normalized_part.split()
        user_words = normalized_input.split()
        errors = []
        for i, (a, b) in enumerate(zip(original_words, user_words)):
            if a != b:
                errors.append((i, a, b))
        if len(user_words) < len(original_words):
            for i in range(len(user_words), len(original_words)):
                errors.append((i, original_words[i], ""))
        elif len(user_words) > len(original_words):
            for i in range(len(original_words), len(user_words)):
                errors.append((i, "", user_words[i]))

        st.session_state.errors.extend(errors)
        for index, expected, got in errors:
            st.error(f"❌ Word {index + 1}: Expected `{expected}` but got `{got}`")

# --- Show Errors ---
if st.button("Review Errors"):
    if not st.session_state.errors:
        st.success("No errors to review. 🎉")
    else:
        st.subheader("Mistake Review")
        for index, expected, got in st.session_state.errors:
            st.write(f"- Word {index + 1}: Expected **{expected}**, got **{got}**")

