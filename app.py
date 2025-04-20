import tkinter as tk
from tkinter import messagebox
import unidecode

# Define the Spanish paragraphs
spanish_paragraphs = [
    "Ir de vacaciones es relajante y descanso del trabajo y del instituto. Pero muy rico para mí.",
    "No, no he visitado España. Pero me gustaría ir un día, escuché es lujoso y grande, a mi madre le gusta España y viaja todos los años.",
    "Mis vacaciones ideales serían en la playa. Me gustaría tomar sol y nadar, también visitar los monumentos. Además, mis vacaciones deben ser preciosas.",
    "El fin de semana pasado fui a mi club donde jugue al futbol con mi hermano porque es demasiado divertido!",
    "Vivo en Crewe, es un pueblo en el noroeste. Me chifla mi pueblo porque hay mucho que hacer y esta en el campo.",
    "Me gustaria cambiar mi vida, es muy frenetica, puede ser un poco aburrido. Me decepsiona mi pueblo, no hay un hospital. Que desastre!",
]

# Define the German paragraphs
german_paragraphs = [
    "Mein perfektes Wochenend ware unmoglich fur mich. Ich wurde Mount Everest besteigen. Wenn ich die Wahl hatte, wurde ich gern zeit mit meine Grosseltern verbringen.",
    "Nein, ich bin beschafigt. Wenn ich die wahl hatte, wurde ich mit meinen Freund Komodien sehen. Meistens, alles Fernsehen ist schrecklich.",
    "Nein nicht wirklich. Ich finde fern sehr langweilig. Ich sehe jeden Monat fern, obwohl meine Familie geniesst es, ich hasse es. Als ich junger war, gluckte ich gern Realityshows.",
    "Mein perfektes Wochenende mit meinen Familien wird auf dem Strand sein, ich wurde gern mich sonnen, auch gebaude besuchen. Ich kann kaum warten!",
    "Letztes Jahr, fotografierte ich meine amusante Familie. Auf dem Foto gab es meinen kleinen Bruder und meine zwei Eltern, sie sagte das Foto ist doof und ich denke sie sind pessimistich.",
    "Naturlich ist mein Lieblingsfestival meinen Geburtstag. Zur Abwechslung wache ich auf um funf Uhr, repaire ich mein Geburtstag Gedenknis. Normalerweise das Gedenknis wird jedes Jahr von vielen Touristen besucht.",
    "In meiner Stadt, gibt es viel Verschmutzung und verfallen Gebaude. Leider, wohne ich in einer Hundehutte mit meinen Hundert Hunden. Und du?",
    "Mein Traumurlaub ware auf der Welt. Meinen Freuden und ich waren Jeden Tag Pizza essen, es ware so toll! Ich were dieses Erlebnis nie vergessen.",
    "Gestern, habe ich ein Nickerschen gemacht, ich habe uber ein besser Leben getraumt. Meine Hund ehaben mich auf gewacht. Wie schade.",
    "Jedens Jahr, meiner Familie und ich fahren nach Deutschland. Im Juni, ist es richtig heiss, das ist nervig. Pech gehabt!",
    "Letzen Sommer, bin ich mit meinen Cousins nach Frankreich gefloggen. Wir haben Eiffel Tower besucht. Ich wurde einen Standurlaub in Frankreich empfehlen.",
    "In der Zukunft, mochte ich ein Hochhaus kaufen, wo ich ziemlich ungesund essen kann. Es muss oft zu letser sein. Ich freue mich darauf.",
    "Ich habe keine Annung. Meiner Mutter interessiert sich fur Tecknologien und ich denke sie arbeitet als Informatikerin. Ich wurde sagen die Gehalt ist grosszugig und zuverlassig. Meiner Vater hat letzen Monat gekundigt.",
    "Letzen Zeit, arbeitetete ich in der Scule. Ich habe meinen Arbetispraktikum geniessen obwhol ich mit Kinder arbeitetete. Es war gemutlich fur mich.",
    "Nachstes Jahr, hoffe ich ein Auslandjahr zu machen. Es ware so ausgezeichnet und angenehm denn ich werde nie die Nase voll haben.",
    "Ich lerne gern Musik weil es oft einfach ist. Aber ich lerne nicht gern Biologie denn ess kann ziemlich anstregend sein. Ich hasse Biologie, wir durfen nicht in das Klasszimer essen.",
    "Meine ideale Schule ware velleicht mich so streng. Es gabe eine Freizeitpark und keine Hausaufgaben. Wenn ich Direktor ware, hatte ich einen kurzen Schultag.",
    "Letze Jahr, bin ich nach Deutschland mit dem Bus gefahren. Es ware eine Katastrophe weil es kein WiFi gab. Ich denke es war schlecht.",
]

# Define the color palette
background_color = "#222222"
text_color = "#00FF00"
button_color = "#333333"
button_text_color = "#00FF00"
entry_background_color = "#444444"
entry_text_color = "#00FF00"

class FlashcardGame:
    def __init__(self, root, language):
        self.root = root
        self.language = language
        self.root.title(f"{language} Flashcard Game")
        self.root.configure(bg=background_color)

        self.paragraphs = spanish_paragraphs if language == "Spanish" else german_paragraphs
        self.paragraph_index = 0
        self.errors = []
        self.current_start_index = 0
        self.current_end_index = 8
        self.step = 3
        self.completed = False

        self.skip_mode = tk.BooleanVar()
        self.settings_frame = tk.Frame(root, bg=background_color)
        self.settings_frame.pack(pady=10)

        self.skip_checkbox = tk.Checkbutton(
            self.settings_frame, text="Skip Mode (Full Paragraph)", variable=self.skip_mode,
            onvalue=True, offvalue=False, font=("Helvetica", 12),
            fg=text_color, bg=background_color, selectcolor=background_color,
            activeforeground=text_color, activebackground=background_color,
        )
        self.skip_checkbox.pack()

        self.label = tk.Label(root, text="", wraplength=600, justify="left", font=("Helvetica", 16), fg=text_color, bg=background_color)
        self.label.pack(pady=20)

        self.hint_label = tk.Label(root, text="", font=("Helvetica", 14), fg=text_color, bg=background_color)
        self.hint_label.pack(pady=10)

        self.text_entry = tk.Text(root, height=10, width=50, font=("Helvetica", 14), bg=entry_background_color, fg=entry_text_color)
        self.text_entry.pack(pady=20)

        self.submit_button = tk.Button(root, text="Submit", command=self.check_part, font=("Helvetica", 14), bg=button_color, fg=button_text_color, activebackground=button_text_color, activeforeground=button_color)
        self.submit_button.pack(pady=10)

        self.next_button = tk.Button(root, text="Next", command=self.next_part, font=("Helvetica", 14), state=tk.DISABLED, bg=button_color, fg=button_text_color, activebackground=button_text_color, activeforeground=button_color)
        self.next_button.pack(pady=10)

        self.retry_button = tk.Button(root, text="Retry", command=self.retry_part, font=("Helvetica", 14), state=tk.DISABLED, bg=button_color, fg=button_text_color, activebackground=button_text_color, activeforeground=button_color)
        self.retry_button.pack(pady=10)

        self.review_button = tk.Button(root, text="Review Errors", command=self.review_errors, font=("Helvetica", 14), state=tk.DISABLED, bg=button_color, fg=button_text_color, activebackground=button_text_color, activeforeground=button_color)
        self.review_button.pack(pady=10)

        self.paragraph_buttons = []
        for i in range(len(self.paragraphs)):
            btn = tk.Button(root, text=f"Paragraph {i+1}", command=lambda idx=i: self.select_paragraph(idx), font=("Helvetica", 14), bg=button_color, fg=button_text_color, activebackground=button_text_color, activeforeground=button_color)
            btn.pack(side=tk.LEFT, padx=10)
            self.paragraph_buttons.append(btn)

        self.show_part()

    def select_paragraph(self, index):
        self.paragraph_index = index
        self.current_start_index = 0
        self.current_end_index = 8
        self.completed = False
        self.errors = []
        self.show_part()

    def show_part(self):
        words = self.paragraphs[self.paragraph_index].split()
        if self.skip_mode.get():
            self.current_part = ' '.join(words)
            self.completed = True
        else:
            if self.completed:
                self.current_part = ' '.join(words[:self.current_end_index])
            else:
                self.current_part = ' '.join(words[self.current_start_index:self.current_end_index])
        self.label.config(text=self.current_part)
        read_time = len(self.current_part.split()) * 300
        self.root.after(read_time, self.hide_part)

    def hide_part(self):
        self.label.config(text="Time's up! Now write the part from memory.")
        first_word, last_word = self.get_first_and_last_words(self.current_part)
        self.hint_label.config(text=f"Hint: {first_word} ... {last_word}")
        self.text_entry.delete("1.0", tk.END)
        self.submit_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)
        self.retry_button.config(state=tk.DISABLED)

    def get_first_and_last_words(self, text):
        words = text.split()
        if len(words) > 1:
            return words[0], words[-1]
        elif words:
            return words[0], words[0]
        return "", ""

    def check_part(self):
        user_input = self.text_entry.get("1.0", tk.END).strip()
        normalized_user_input = unidecode.unidecode(user_input)
        normalized_current_part = unidecode.unidecode(self.current_part)

        if normalized_user_input == normalized_current_part:
            messagebox.showinfo("Correct!", "Well done!")
            self.submit_button.config(state=tk.DISABLED)
            self.retry_button.config(state=tk.DISABLED)
            if self.completed:
                self.current_end_index += self.step
            else:
                self.current_start_index += self.step
                self.current_end_index += self.step

            if self.skip_mode.get():
                messagebox.showinfo("Skip Mode", "You've completed the paragraph!")
                self.submit_button.config(state=tk.DISABLED)
                self.next_button.config(state=tk.DISABLED)
                self.retry_button.config(state=tk.DISABLED)
                self.review_button.config(state=tk.NORMAL)
            elif self.current_start_index >= len(self.paragraphs[self.paragraph_index].split()):
                self.completed = True
                self.current_start_index = 0
                self.current_end_index = 8
                self.next_part()
            elif self.completed and self.current_end_index > len(self.paragraphs[self.paragraph_index].split()):
                messagebox.showinfo("End", "You've completed the paragraph!")
                self.submit_button.config(state=tk.DISABLED)
                self.next_button.config(state=tk.DISABLED)
                self.retry_button.config(state=tk.DISABLED)
                self.review_button.config(state=tk.NORMAL)
            else:
                self.next_button.config(state=tk.NORMAL)
        else:
            self.errors = self.find_errors(normalized_current_part, normalized_user_input)
            error_message = "\n".join([f"Word {index+1}: Expected '{correct}' but got '{user}'"
                                       for index, correct, user in self.errors])
            messagebox.showerror("Errors", f"That was not correct. Here are the mistakes:\n{error_message}")
            self.retry_button.config(state=tk.NORMAL)

        self.submit_button.config(state=tk.DISABLED)

    def retry_part(self):
        self.show_part()
        self.submit_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)
        self.retry_button.config(state=tk.DISABLED)

    def next_part(self):
        if self.skip_mode.get():
            messagebox.showinfo("Skip Mode", "You've completed the paragraph!")
            self.submit_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.retry_button.config(state=tk.DISABLED)
            self.review_button.config(state=tk.NORMAL)
            return

        if self.completed:
            self.show_part()
        else:
            self.current_start_index += self.step
            self.current_end_index = self.current_start_index + self.step
            self.show_part()

    def find_errors(self, original, user_input):
        original_words = original.split()
        user_words = user_input.split()
        errors = []
        for i, (orig_word, user_word) in enumerate(zip(original_words, user_words)):
            if orig_word != user_word:
                errors.append((i, orig_word, user_word))
        if len(original_words) > len(user_words):
            for i in range(len(user_words), len(original_words)):
                errors.append((i, original_words[i], ""))
        elif len(original_words) < len(user_words):
            for i in range(len(original_words), len(user_words)):
                errors.append((i, "", user_words[i]))
        return errors

    def review_errors(self):
        if not self.errors:
            messagebox.showinfo("No Errors", "No errors to review. Well done!")
            return

        self.current_sentence_index = 0
        self.error_sentences = [self.find_sentence_with_word(self.paragraphs, correct_word) for _, correct_word, _ in self.errors]
        self.error_sentences = list(filter(None, self.error_sentences))  # Remove None values
        self.show_error_sentence()

    def show_error_sentence(self):
        if self.current_sentence_index < len(self.error_sentences):
            self.current_sentence = self.error_sentences[self.current_sentence_index]
            self.label.config(text=self.current_sentence)
            read_time = len(self.current_sentence.split()) * 300
            self.root.after(read_time, self.hide_error_sentence)
        else:
            messagebox.showinfo("Review Complete", "You've reviewed all errors!")
            self.current_sentence_index = 0

    def hide_error_sentence(self):
        self.label.config(text="Time's up! Now write the sentence from memory.")
        first_word, last_word = self.get_first_and_last_words(self.current_sentence)
        self.hint_label.config(text=f"Hint: {first_word} ... {last_word}")
        self.text_entry.delete("1.0", tk.END)
        self.submit_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)
        self.review_button.config(state=tk.DISABLED)
        self.submit_button.config(command=self.check_sentence)

    def check_sentence(self):
        user_input = self.text_entry.get("1.0", tk.END).strip()
        normalized_user_input = unidecode.unidecode(user_input)
        normalized_current_sentence = unidecode.unidecode(self.current_sentence)

        if normalized_user_input == normalized_current_sentence:
            messagebox.showinfo("Correct!", "Well done!")
        else:
            messagebox.showerror("Error", f"That was not correct. The correct sentence is:\n{self.current_sentence}")

        self.current_sentence_index += 1
        self.show_error_sentence()

        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)
        self.review_button.config(state=tk.NORMAL)
        self.submit_button.config(command=self.check_part)

    def find_sentence_with_word(self, paragraphs, word):
        for paragraph in paragraphs:
            sentences = paragraph.split('. ')
            for sentence in sentences:
                if word in sentence:
                    return sentence
        return None

def start_app():
    root = tk.Tk()
    root.title("Language Selection")

    tk.Button(root, text="Spanish", command=lambda: start_game("Spanish", root), font=("Helvetica", 14), bg=button_color, fg=button_text_color).pack(side=tk.LEFT, padx=20, pady=20)
    tk.Button(root, text="German", command=lambda: start_game("German", root), font=("Helvetica", 14), bg=button_color, fg=button_text_color).pack(side=tk.LEFT, padx=20, pady=20)

    root.mainloop()

def start_game(language, root):
    root.destroy()
    new_root = tk.Tk()
    game = FlashcardGame(new_root, language)
    new_root.mainloop()

if __name__ == "__main__":
    start_app()
