"""
grammar.py – Model / Logic layer for the Spanish SVO Constructor.

Three static-method classes:
    AgreementEngine  – adjective inflection
    ConjugationEngine – verb conjugation
    SentenceBuilder   – noun-phrase & sentence assembly
"""

from data import (
    NOUNS, ADJECTIVES, VERBS, DETERMINERS,
    REGULAR_ENDINGS, FUTURO_ENDINGS, CONDICIONAL_ENDINGS,
    IMPERATIVE_ENDINGS, PERSON_LABELS, IMPERATIVE_PERSONS,
)


class AgreementEngine:
    """Inflects adjectives for gender and number agreement."""

    @staticmethod
    def inflect_adjective(base, gender, number):
        """
        Return (inflected_form, log_lines).
        base: masculine singular citation form (e.g. 'rojo')
        gender: 'M' or 'F'
        number: 'singular' or 'plural'
        """
        logs = []
        adj_data = ADJECTIVES.get(base)
        if not adj_data:
            return base, [f"Adjective: '{base}' not found in dictionary"]

        # 1. Check irregular override
        if adj_data["irregular_forms"]:
            form = adj_data["irregular_forms"].get((gender, number), base)
            logs.append(f"Adjective: {base} -> {form} (irregular override for {gender}/{number})")
            return form, logs

        logs.append(f"Adjective base: {base} ({adj_data['meaning']})")

        # 2. Gender inflection
        if base.endswith("o"):
            if gender == "F":
                form = base[:-1] + "a"
                logs.append(f"Gender: {base} -> {form} (-o class: masculine -o changed to feminine -a)")
            else:
                form = base
                logs.append(f"Gender: {base} -> {form} (-o class: masculine form unchanged)")
        elif base.endswith("e"):
            form = base
            logs.append(f"Gender: {base} -> {form} (-e class: invariable for gender)")
        else:
            form = base
            logs.append(f"Gender: {base} -> {form} (consonant class: invariable for gender)")

        # 3. Number inflection
        if number == "plural":
            singular_form = form
            if form.endswith(("a", "e", "i", "o", "u")):
                form = form + "s"
                logs.append(f"Number: {singular_form} -> {form} (vowel ending: +s)")
            elif form.endswith("z"):
                form = form[:-1] + "ces"
                logs.append(f"Number: {singular_form} -> {form} (-z ending: -z -> -ces)")
            else:
                form = form + "es"
                logs.append(f"Number: {singular_form} -> {form} (consonant ending: +es)")
        else:
            logs.append(f"Number: {form} -> {form} (singular: no change)")

        return form, logs


class ConjugationEngine:
    """Conjugates verbs by person, tense, and mood."""

    @staticmethod
    def conjugate(infinitive, person, tense, mood):
        """
        Return (conjugated_form, log_lines).
        person: '1s','2s','3s','1p','2p','3p' or imperative person label
        tense: 'Presente','Pretérito','Futuro'
        mood: 'Afirmativo','Negativo','Interrogativo','Imperativo','Condicional'
        """
        logs = []
        verb_data = VERBS.get(infinitive)
        if not verb_data:
            return infinitive, [f"Verb: '{infinitive}' not found in dictionary"]

        group = verb_data["group"]
        irregular = verb_data["irregular"]
        stem = infinitive[:-2]  # remove -ar/-er/-ir

        logs.append(f"Verb: {infinitive} ({verb_data['meaning']}), group: -{group}")

        # ── Imperativo ──
        if mood == "Imperativo":
            imp_person = person  # already an imperative person label
            logs.append(f"Mood: Imperativo, person: {imp_person}")

            if irregular and "imperativo" in irregular:
                form = irregular["imperativo"].get(imp_person)
                if form:
                    logs.append(f"Conjugation: {infinitive} -> {form} (irregular imperativo for {imp_person})")
                    return form, logs

            # Regular imperative
            ending = IMPERATIVE_ENDINGS.get(group, {}).get(imp_person, "")
            form = stem + ending
            logs.append(f"Conjugation: stem '{stem}' + ending '-{ending}' -> {form} (regular imperativo)")
            return form, logs

        # ── Condicional ──
        if mood == "Condicional":
            logs.append(f"Mood: Condicional, person: {person} ({PERSON_LABELS.get(person, person)})")

            if irregular and "condicional" in irregular:
                form = irregular["condicional"].get(person)
                if form:
                    logs.append(f"Conjugation: {infinitive} -> {form} (irregular condicional)")
                    return form, logs

            ending = CONDICIONAL_ENDINGS.get(person, "")
            form = infinitive + ending
            logs.append(f"Conjugation: infinitive '{infinitive}' + ending '-{ending}' -> {form} (regular condicional)")
            return form, logs

        # ── Standard tenses: Presente, Pretérito, Futuro ──
        tense_key = tense.lower()
        logs.append(f"Tense: {tense}, Person: {person} ({PERSON_LABELS.get(person, person)})")

        # Check irregular override
        if irregular and tense_key in irregular:
            form = irregular[tense_key].get(person)
            if form:
                logs.append(f"Conjugation: {infinitive} -> {form} (irregular {tense_key})")
                if mood == "Negativo":
                    neg_form = "no " + form
                    logs.append(f"Negation: {form} -> {neg_form}")
                    return neg_form, logs
                return form, logs

        # Regular conjugation
        if tense_key == "futuro":
            ending = FUTURO_ENDINGS.get(person, "")
            form = infinitive + ending
            logs.append(f"Conjugation: infinitive '{infinitive}' + ending '-{ending}' -> {form} (regular futuro)")
        else:
            # Presente or Pretérito
            endings = REGULAR_ENDINGS.get(group, {}).get(tense_key, {})
            ending = endings.get(person, "")
            form = stem + ending
            logs.append(f"Conjugation: stem '{stem}' + ending '-{ending}' -> {form} (regular {tense_key})")

        if mood == "Negativo":
            neg_form = "no " + form
            logs.append(f"Negation: {form} -> {neg_form}")
            return neg_form, logs

        return form, logs


class SentenceBuilder:
    """Assembles noun phrases and full SVO sentences."""

    @staticmethod
    def build_noun_phrase(noun_key, number, det_type, adj_key=None):
        """
        Return (noun_phrase_string, log_lines).
        noun_key: key into NOUNS dict, or None / "(ninguno)"
        """
        if not noun_key or noun_key == "(ninguno)":
            return "", ["Noun phrase: (none)"]

        logs = []
        noun_data = NOUNS.get(noun_key)
        if not noun_data:
            return noun_key, [f"Noun: '{noun_key}' not found"]

        gender = noun_data["gender"]
        logs.append(f"Noun: {noun_key} ({noun_data['meaning']}), gender: {gender}")

        # Noun form
        noun_form = noun_data["singular"] if number == "singular" else noun_data["plural"]
        logs.append(f"Number: {noun_data['singular']} -> {noun_form} ({number})")

        # Determiner
        det_form = ""
        if det_type and det_type != "Ninguno":
            det_table = DETERMINERS.get(det_type, {})
            det_form = det_table.get((gender, number), "")
            logs.append(f"Determiner: {det_type} ({gender}/{number}) -> '{det_form}'")
        else:
            logs.append("Determiner: none")

        # Adjective
        adj_form = ""
        if adj_key and adj_key != "(ninguno)":
            adj_form, adj_logs = AgreementEngine.inflect_adjective(adj_key, gender, number)
            logs.extend(adj_logs)

        # Assemble: [det] noun [adj]
        parts = []
        if det_form:
            parts.append(det_form)
        parts.append(noun_form)
        if adj_form:
            parts.append(adj_form)

        np_string = " ".join(parts)
        logs.append(f"Noun phrase assembled: '{np_string}'")
        return np_string, logs

    @staticmethod
    def build_sentence(subject_np, verb_form, mood, object_np=""):
        """
        Return (sentence_string, log_lines).
        Applies punctuation rules per mood.
        """
        logs = []

        parts = []
        if subject_np:
            parts.append(subject_np)
        if verb_form:
            parts.append(verb_form)
        if object_np:
            parts.append(object_np)

        raw = " ".join(parts)
        logs.append(f"Word order: {raw}")

        # Capitalise first letter
        if raw:
            raw = raw[0].upper() + raw[1:]

        # Punctuation per mood
        if mood == "Interrogativo":
            sentence = f"¿{raw}?"
            logs.append(f"Punctuation: Interrogativo -> ¿...?")
        elif mood == "Imperativo":
            sentence = f"¡{raw}!"
            logs.append(f"Punctuation: Imperativo -> ¡...!")
        else:
            sentence = f"{raw}."
            logs.append(f"Punctuation: -> statement with period")

        logs.append(f"Final sentence: {sentence}")
        return sentence, logs

    @staticmethod
    def build_full(
        subj_noun, subj_number, subj_det, subj_adj,
        verb_inf, person, tense, mood,
        obj_noun=None, obj_number="singular", obj_det="Ninguno", obj_adj=None,
    ):
        """
        Orchestrator: build subject NP, conjugate verb, build object NP,
        assemble sentence. Returns (sentence, full_log_text).
        """
        all_logs = []

        # ── Subject ──
        all_logs.append("=" * 50)
        all_logs.append("=== SUBJECT (Podmiot) ===")
        all_logs.append("=" * 50)

        subj_gender = NOUNS[subj_noun]["gender"] if subj_noun and subj_noun in NOUNS else "M"
        subj_np, subj_logs = SentenceBuilder.build_noun_phrase(
            subj_noun, subj_number, subj_det, subj_adj
        )
        all_logs.extend(subj_logs)

        # ── Verb ──
        all_logs.append("")
        all_logs.append("=" * 50)
        all_logs.append("=== VERB (Czasownik) ===")
        all_logs.append("=" * 50)

        verb_form, verb_logs = ConjugationEngine.conjugate(verb_inf, person, tense, mood)
        all_logs.extend(verb_logs)

        # ── Object ──
        all_logs.append("")
        all_logs.append("=" * 50)
        all_logs.append("=== OBJECT (Dopełnienie) ===")
        all_logs.append("=" * 50)

        obj_np, obj_logs = SentenceBuilder.build_noun_phrase(
            obj_noun, obj_number, obj_det, obj_adj
        )
        all_logs.extend(obj_logs)

        # ── Sentence Assembly ──
        all_logs.append("")
        all_logs.append("=" * 50)
        all_logs.append("=== SENTENCE ASSEMBLY ===")
        all_logs.append("=" * 50)

        sentence, sent_logs = SentenceBuilder.build_sentence(
            subj_np, verb_form, mood, obj_np
        )
        all_logs.extend(sent_logs)

        return sentence, "\n".join(all_logs)
