"""
main.py – View / Controller for the Spanish SVO Constructor.

Dark-themed customtkinter GUI with MVC pattern.
"""

import customtkinter as ctk

from data import (
    NOUNS, ADJECTIVES, VERBS, DETERMINERS,
    PERSONS, PERSON_LABELS, TENSES, MOODS,
    GENDERS, NUMBERS, IMPERATIVE_PERSONS,
)
from grammar import SentenceBuilder


# ──────────────────────────── HELPERS ─────────────────────────────

def _noun_choices(gender_filter=None):
    """Return sorted list of noun keys filtered by gender."""
    if gender_filter:
        return sorted(k for k, v in NOUNS.items() if v["gender"] == gender_filter)
    return sorted(NOUNS.keys())


def _noun_label(key):
    """Display label for noun dropdown: 'gato (cat)'."""
    d = NOUNS[key]
    return f"{key} ({d['meaning']})"


def _adj_choices():
    """Return sorted list of adjective keys with (ninguno) first."""
    return ["(ninguno)"] + sorted(ADJECTIVES.keys())


def _adj_label(key):
    if key == "(ninguno)":
        return "(ninguno)"
    d = ADJECTIVES[key]
    return f"{key} ({d['meaning']})"


def _verb_choices():
    return sorted(VERBS.keys())


def _verb_label(key):
    d = VERBS[key]
    return f"{key} ({d['meaning']})"


def _det_choices():
    return list(DETERMINERS.keys())


def _person_choices():
    return [(p, f"{p} – {PERSON_LABELS[p]}") for p in PERSONS]


def _imp_person_choices():
    return [(p, p) for p in IMPERATIVE_PERSONS]


# ──────────────────────────── APP ─────────────────────────────────

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Spanish SVO Constructor – Konstruktor zdań SVO")
        self.geometry("1020x780")
        self.minsize(900, 700)

        self._build_ui()
        self._connect_events()
        self._sync_ui()

    # ──────────── UI CONSTRUCTION ────────────

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        row = 0

        # ── 1. SUBJECT ──
        subj_frame = ctk.CTkFrame(self)
        subj_frame.grid(row=row, column=0, padx=10, pady=(10, 5), sticky="ew")
        subj_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        row += 1

        ctk.CTkLabel(subj_frame, text="1. SUBJECT / Podmiot",
                      font=ctk.CTkFont(size=15, weight="bold")).grid(
            row=0, column=0, columnspan=4, padx=10, pady=(8, 4), sticky="w")

        # Gender
        ctk.CTkLabel(subj_frame, text="Gender:").grid(row=1, column=0, padx=(10, 2), pady=4, sticky="w")
        self.subj_gender = ctk.CTkSegmentedButton(subj_frame, values=GENDERS)
        self.subj_gender.set("M")
        self.subj_gender.grid(row=1, column=1, padx=4, pady=4, sticky="w")

        # Number
        ctk.CTkLabel(subj_frame, text="Number:").grid(row=1, column=2, padx=(10, 2), pady=4, sticky="w")
        self.subj_number = ctk.CTkSegmentedButton(subj_frame, values=NUMBERS)
        self.subj_number.set("singular")
        self.subj_number.grid(row=1, column=3, padx=4, pady=4, sticky="w")

        # Noun
        ctk.CTkLabel(subj_frame, text="Noun:").grid(row=2, column=0, padx=(10, 2), pady=4, sticky="w")
        self.subj_noun_var = ctk.StringVar()
        self.subj_noun = ctk.CTkOptionMenu(subj_frame, variable=self.subj_noun_var, width=220)
        self.subj_noun.grid(row=2, column=1, padx=4, pady=4, sticky="w")

        # Adjective
        ctk.CTkLabel(subj_frame, text="Adjective:").grid(row=2, column=2, padx=(10, 2), pady=4, sticky="w")
        self.subj_adj_var = ctk.StringVar(value="(ninguno)")
        self.subj_adj = ctk.CTkOptionMenu(subj_frame, variable=self.subj_adj_var, width=220)
        self.subj_adj.grid(row=2, column=3, padx=4, pady=4, sticky="w")

        # Determiner + preview
        ctk.CTkLabel(subj_frame, text="Determiner:").grid(row=3, column=0, padx=(10, 2), pady=4, sticky="w")
        self.subj_det_var = ctk.StringVar(value="Definido")
        self.subj_det = ctk.CTkOptionMenu(subj_frame, variable=self.subj_det_var,
                                           values=_det_choices(), width=220)
        self.subj_det.grid(row=3, column=1, padx=4, pady=4, sticky="w")

        ctk.CTkLabel(subj_frame, text="Preview:").grid(row=3, column=2, padx=(10, 2), pady=4, sticky="w")
        self.subj_det_preview = ctk.CTkLabel(subj_frame, text="el",
                                              font=ctk.CTkFont(size=14, weight="bold"))
        self.subj_det_preview.grid(row=3, column=3, padx=4, pady=4, sticky="w")

        # ── 2. VERB ──
        verb_frame = ctk.CTkFrame(self)
        verb_frame.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        verb_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        row += 1

        ctk.CTkLabel(verb_frame, text="2. VERB / Czasownik",
                      font=ctk.CTkFont(size=15, weight="bold")).grid(
            row=0, column=0, columnspan=4, padx=10, pady=(8, 4), sticky="w")

        # Verb
        ctk.CTkLabel(verb_frame, text="Verb:").grid(row=1, column=0, padx=(10, 2), pady=4, sticky="w")
        self.verb_var = ctk.StringVar()
        self.verb_menu = ctk.CTkOptionMenu(verb_frame, variable=self.verb_var, width=220)
        self.verb_menu.grid(row=1, column=1, padx=4, pady=4, sticky="w")

        # Person
        ctk.CTkLabel(verb_frame, text="Person:").grid(row=1, column=2, padx=(10, 2), pady=4, sticky="w")
        self.person_var = ctk.StringVar()
        self.person_menu = ctk.CTkOptionMenu(verb_frame, variable=self.person_var, width=220)
        self.person_menu.grid(row=1, column=3, padx=4, pady=4, sticky="w")

        # Mood
        ctk.CTkLabel(verb_frame, text="Mood:").grid(row=2, column=0, padx=(10, 2), pady=4, sticky="w")
        self.mood_seg = ctk.CTkSegmentedButton(verb_frame, values=MOODS)
        self.mood_seg.set("Afirmativo")
        self.mood_seg.grid(row=2, column=1, columnspan=3, padx=4, pady=4, sticky="w")

        # Tense
        ctk.CTkLabel(verb_frame, text="Tense:").grid(row=3, column=0, padx=(10, 2), pady=4, sticky="w")
        self.tense_seg = ctk.CTkSegmentedButton(verb_frame, values=TENSES)
        self.tense_seg.set("Presente")
        self.tense_seg.grid(row=3, column=1, columnspan=3, padx=4, pady=4, sticky="w")

        # ── 3. OBJECT ──
        obj_frame = ctk.CTkFrame(self)
        obj_frame.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        obj_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        row += 1

        ctk.CTkLabel(obj_frame, text="3. OBJECT / Dopełnienie",
                      font=ctk.CTkFont(size=15, weight="bold")).grid(
            row=0, column=0, columnspan=4, padx=10, pady=(8, 4), sticky="w")

        # Gender
        ctk.CTkLabel(obj_frame, text="Gender:").grid(row=1, column=0, padx=(10, 2), pady=4, sticky="w")
        self.obj_gender = ctk.CTkSegmentedButton(obj_frame, values=GENDERS)
        self.obj_gender.set("F")
        self.obj_gender.grid(row=1, column=1, padx=4, pady=4, sticky="w")

        # Number
        ctk.CTkLabel(obj_frame, text="Number:").grid(row=1, column=2, padx=(10, 2), pady=4, sticky="w")
        self.obj_number = ctk.CTkSegmentedButton(obj_frame, values=NUMBERS)
        self.obj_number.set("singular")
        self.obj_number.grid(row=1, column=3, padx=4, pady=4, sticky="w")

        # Noun
        ctk.CTkLabel(obj_frame, text="Noun:").grid(row=2, column=0, padx=(10, 2), pady=4, sticky="w")
        self.obj_noun_var = ctk.StringVar()
        self.obj_noun = ctk.CTkOptionMenu(obj_frame, variable=self.obj_noun_var, width=220)
        self.obj_noun.grid(row=2, column=1, padx=4, pady=4, sticky="w")

        # Adjective
        ctk.CTkLabel(obj_frame, text="Adjective:").grid(row=2, column=2, padx=(10, 2), pady=4, sticky="w")
        self.obj_adj_var = ctk.StringVar(value="(ninguno)")
        self.obj_adj = ctk.CTkOptionMenu(obj_frame, variable=self.obj_adj_var, width=220)
        self.obj_adj.grid(row=2, column=3, padx=4, pady=4, sticky="w")

        # Determiner + preview
        ctk.CTkLabel(obj_frame, text="Determiner:").grid(row=3, column=0, padx=(10, 2), pady=4, sticky="w")
        self.obj_det_var = ctk.StringVar(value="Indefinido")
        self.obj_det = ctk.CTkOptionMenu(obj_frame, variable=self.obj_det_var,
                                          values=_det_choices(), width=220)
        self.obj_det.grid(row=3, column=1, padx=4, pady=4, sticky="w")

        ctk.CTkLabel(obj_frame, text="Preview:").grid(row=3, column=2, padx=(10, 2), pady=4, sticky="w")
        self.obj_det_preview = ctk.CTkLabel(obj_frame, text="una",
                                             font=ctk.CTkFont(size=14, weight="bold"))
        self.obj_det_preview.grid(row=3, column=3, padx=4, pady=4, sticky="w")

        # ── Buttons ──
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)
        row += 1

        self.build_btn = ctk.CTkButton(btn_frame, text="Build Sentence / Zbuduj zdanie",
                                        font=ctk.CTkFont(size=14, weight="bold"),
                                        height=40, command=self._on_build_sentence)
        self.build_btn.grid(row=0, column=0, padx=(0, 5), pady=4, sticky="ew")

        self.clear_btn = ctk.CTkButton(btn_frame, text="Clear / Wyczyść",
                                        font=ctk.CTkFont(size=14),
                                        height=40, fg_color="gray30",
                                        command=self._on_clear)
        self.clear_btn.grid(row=0, column=1, padx=(5, 0), pady=4, sticky="ew")

        # ── 4. RESULT ──
        res_frame = ctk.CTkFrame(self)
        res_frame.grid(row=row, column=0, padx=10, pady=(5, 10), sticky="nsew")
        res_frame.grid_columnconfigure(0, weight=1)
        res_frame.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(row, weight=1)
        row += 1

        ctk.CTkLabel(res_frame, text="4. RESULT / Wynik",
                      font=ctk.CTkFont(size=15, weight="bold")).grid(
            row=0, column=0, padx=10, pady=(8, 2), sticky="w")

        self.sentence_label = ctk.CTkLabel(res_frame, text="",
                                            font=ctk.CTkFont(size=18, weight="bold"),
                                            wraplength=950, justify="left")
        self.sentence_label.grid(row=0, column=0, padx=10, pady=(8, 2), sticky="e")

        self.log_box = ctk.CTkTextbox(res_frame, state="disabled",
                                       font=ctk.CTkFont(family="Courier", size=12),
                                       wrap="word")
        self.log_box.grid(row=1, column=0, padx=10, pady=(2, 10), sticky="nsew")

    # ──────────── EVENT WIRING ────────────

    def _connect_events(self):
        self.subj_gender.configure(command=lambda v: self._on_subj_gender_change())
        self.subj_number.configure(command=lambda v: self._on_subj_det_change())
        self.subj_det.configure(command=lambda v: self._on_subj_det_change())

        self.obj_gender.configure(command=lambda v: self._on_obj_gender_change())
        self.obj_number.configure(command=lambda v: self._on_obj_det_change())
        self.obj_det.configure(command=lambda v: self._on_obj_det_change())

        self.mood_seg.configure(command=lambda v: self._on_mood_change())

    # ──────────── SYNC / REFRESH ────────────

    def _sync_ui(self):
        """Initial population of all dynamic widgets."""
        self._populate_subj_nouns()
        self._populate_obj_nouns()
        self._populate_adjectives()
        self._populate_verbs()
        self._populate_persons()
        self._update_subj_det_preview()
        self._update_obj_det_preview()

    def _populate_subj_nouns(self):
        gender = self.subj_gender.get()
        nouns = _noun_choices(gender)
        labels = [_noun_label(n) for n in nouns]
        self.subj_noun.configure(values=labels)
        if labels:
            self.subj_noun_var.set(labels[0])

    def _populate_obj_nouns(self):
        gender = self.obj_gender.get()
        nouns = _noun_choices(gender)
        labels = ["(ninguno)"] + [_noun_label(n) for n in nouns]
        self.obj_noun.configure(values=labels)
        if labels:
            self.obj_noun_var.set(labels[0])

    def _populate_adjectives(self):
        labels = [_adj_label(a) for a in _adj_choices()]
        self.subj_adj.configure(values=labels)
        self.subj_adj_var.set(labels[0])
        self.obj_adj.configure(values=labels)
        self.obj_adj_var.set(labels[0])

    def _populate_verbs(self):
        labels = [_verb_label(v) for v in _verb_choices()]
        self.verb_menu.configure(values=labels)
        if labels:
            self.verb_var.set(labels[0])

    def _populate_persons(self, imperative=False):
        if imperative:
            choices = _imp_person_choices()
        else:
            choices = _person_choices()
        labels = [lbl for _, lbl in choices]
        self.person_menu.configure(values=labels)
        if labels:
            self.person_var.set(labels[0])

    def _update_subj_det_preview(self):
        det_type = self.subj_det_var.get()
        gender = self.subj_gender.get()
        number = self.subj_number.get()
        table = DETERMINERS.get(det_type, {})
        form = table.get((gender, number), "—")
        self.subj_det_preview.configure(text=form if form else "—")

    def _update_obj_det_preview(self):
        det_type = self.obj_det_var.get()
        gender = self.obj_gender.get()
        number = self.obj_number.get()
        table = DETERMINERS.get(det_type, {})
        form = table.get((gender, number), "—")
        self.obj_det_preview.configure(text=form if form else "—")

    # ──────────── EVENT HANDLERS ────────────

    def _on_subj_gender_change(self):
        self._populate_subj_nouns()
        self._update_subj_det_preview()

    def _on_subj_det_change(self):
        self._update_subj_det_preview()

    def _on_obj_gender_change(self):
        self._populate_obj_nouns()
        self._update_obj_det_preview()

    def _on_obj_det_change(self):
        self._update_obj_det_preview()

    def _on_mood_change(self):
        mood = self.mood_seg.get()
        if mood == "Imperativo":
            self._populate_persons(imperative=True)
            self.tense_seg.configure(state="disabled")
        elif mood == "Condicional":
            self._populate_persons(imperative=False)
            self.tense_seg.configure(state="disabled")
        else:
            self._populate_persons(imperative=False)
            self.tense_seg.configure(state="normal")

    # ──────────── EXTRACT KEY FROM LABEL ────────────

    @staticmethod
    def _key_from_label(label):
        """Extract dict key from display label like 'gato (cat)' -> 'gato'."""
        if not label or label == "(ninguno)":
            return None
        return label.split(" (")[0] if " (" in label else label

    def _person_key_from_label(self, label):
        """Extract person code from label like '3s – él/ella/usted' -> '3s'
        or imperative person label -> itself."""
        if " – " in label:
            return label.split(" – ")[0]
        return label  # imperative person label

    # ──────────── BUILD / CLEAR ────────────

    def _on_build_sentence(self):
        # Subject
        subj_noun = self._key_from_label(self.subj_noun_var.get())
        subj_number = self.subj_number.get()
        subj_det = self.subj_det_var.get()
        subj_adj = self._key_from_label(self.subj_adj_var.get())

        # Verb
        verb_inf = self._key_from_label(self.verb_var.get())
        person = self._person_key_from_label(self.person_var.get())
        tense = self.tense_seg.get()
        mood = self.mood_seg.get()

        # Object
        obj_noun = self._key_from_label(self.obj_noun_var.get())
        obj_number = self.obj_number.get()
        obj_det = self.obj_det_var.get()
        obj_adj = self._key_from_label(self.obj_adj_var.get())

        sentence, log_text = SentenceBuilder.build_full(
            subj_noun=subj_noun, subj_number=subj_number,
            subj_det=subj_det, subj_adj=subj_adj,
            verb_inf=verb_inf, person=person,
            tense=tense, mood=mood,
            obj_noun=obj_noun, obj_number=obj_number,
            obj_det=obj_det, obj_adj=obj_adj,
        )

        self.sentence_label.configure(text=sentence)
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.insert("1.0", log_text)
        self.log_box.configure(state="disabled")

    def _on_clear(self):
        # Reset subject
        self.subj_gender.set("M")
        self.subj_number.set("singular")
        self.subj_det_var.set("Definido")
        self._populate_subj_nouns()
        self.subj_adj_var.set("(ninguno)")
        self._update_subj_det_preview()

        # Reset verb
        self._populate_verbs()
        self.mood_seg.set("Afirmativo")
        self.tense_seg.configure(state="normal")
        self.tense_seg.set("Presente")
        self._populate_persons(imperative=False)

        # Reset object
        self.obj_gender.set("F")
        self.obj_number.set("singular")
        self.obj_det_var.set("Indefinido")
        self._populate_obj_nouns()
        self.obj_adj_var.set("(ninguno)")
        self._update_obj_det_preview()

        # Clear result
        self.sentence_label.configure(text="")
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()
