from django.core.management.base import BaseCommand
from assessments.models import Assessment, Question, Choice, AnswerPattern, OrderingItem, MatchPair


class Command(BaseCommand):
    help = "Seed sample assessments with questions and choices"

    def handle(self, *args, **options):
        # Create assessments A1-B2 if not exist
        a1, _ = Assessment.objects.get_or_create(title="General Test A1", level="A1", is_active=True)
        a2, _ = Assessment.objects.get_or_create(title="General Test A2", level="A2", is_active=True)
        b1, _ = Assessment.objects.get_or_create(title="General Test B1", level="B1", is_active=True)
        b2, _ = Assessment.objects.get_or_create(title="General Test B2", level="B2", is_active=True)

        # Clear existing questions/choices to fully replace with the new content
        for asm in (a1, a2, b1, b2):
            asm.questions.all().delete()

        def mcq(assessment, text, options, correct_idx=0, diff=Question.Difficulty.EASY, weight=1):
            q, created = Question.objects.get_or_create(
                assessment=assessment, text=text,
                defaults={"type": Question.QuestionType.MCQ_SINGLE, "difficulty": diff, "weight": weight}
            )
            if created or q.choices.count() == 0:
                for i, opt in enumerate(options):
                    Choice.objects.create(question=q, text=opt, is_correct=(i == correct_idx))
            return q

        def multi(assessment, text, options, correct_indices, diff=Question.Difficulty.MEDIUM, weight=2):
            q, created = Question.objects.get_or_create(
                assessment=assessment, text=text,
                defaults={"type": Question.QuestionType.MULTI, "difficulty": diff, "weight": weight}
            )
            if created or q.choices.count() == 0:
                for i, opt in enumerate(options):
                    Choice.objects.create(question=q, text=opt, is_correct=(i in correct_indices))
            return q

        def tf(assessment, text, correct_true=True, diff=Question.Difficulty.EASY, weight=1):
            q, _ = Question.objects.get_or_create(
                assessment=assessment, text=text,
                defaults={"type": Question.QuestionType.TF, "difficulty": diff, "weight": weight, "correct_boolean": correct_true}
            )
            return q

        def fill(assessment, text, answers, diff=Question.Difficulty.MEDIUM, weight=2):
            q, created = Question.objects.get_or_create(
                assessment=assessment, text=text,
                defaults={"type": Question.QuestionType.FILL, "difficulty": diff, "weight": weight}
            )
            if created or q.answer_patterns.count() == 0:
                for patt, kind in answers:
                    AnswerPattern.objects.create(question=q, pattern=patt, kind=kind)
            return q

        def order(assessment, text, items, diff=Question.Difficulty.MEDIUM, weight=2):
            q, created = Question.objects.get_or_create(
                assessment=assessment, text=text,
                defaults={"type": Question.QuestionType.ORDER, "difficulty": diff, "weight": weight}
            )
            if created or q.ordering_items.count() == 0:
                for i, t in enumerate(items, start=1):
                    OrderingItem.objects.create(question=q, text=t, correct_position=i)
            return q

        def match(assessment, text, pairs, diff=Question.Difficulty.MEDIUM, weight=2):
            q, created = Question.objects.get_or_create(
                assessment=assessment, text=text,
                defaults={"type": Question.QuestionType.MATCH, "difficulty": diff, "weight": weight}
            )
            if created or q.match_pairs.count() == 0:
                for l, r in pairs:
                    MatchPair.objects.create(question=q, left_text=l, right_text=r)
            return q

        # ----------------------
        # A1 (from user content)
        # ----------------------
        mcq(a1, "Wir ___ in Köln.", ["wohnen", "wohne", "wohnt", "wohntest"], correct_idx=0, diff=Question.Difficulty.EASY, weight=1)
        mcq(a1, "„Ich heiße Ali. Ich komme aus dem Iran und ich wohne in Berlin.“ – Wo wohnt Ali?", ["In Köln", "In Hamburg", "In Berlin", "In München"], correct_idx=2, diff=Question.Difficulty.EASY, weight=1)
        mcq(a1, "Ich komme ___ Deutschland.", ["in", "auf", "aus", "an"], correct_idx=2, diff=Question.Difficulty.EASY, weight=1)
        mcq(a1, "___ ist das? – Das ist meine Mutter.", ["Wo", "Wer", "Wie", "Wann"], correct_idx=1, diff=Question.Difficulty.EASY, weight=1)
        mcq(a1, "Welche Zahl ist richtig? „siebenundsiebzig“", ["17", "77", "70", "707"], correct_idx=1, diff=Question.Difficulty.MEDIUM, weight=2)
        mcq(a1, "Das ist ___ Auto.", ["meiner", "meine", "mein", "meines"], correct_idx=2, diff=Question.Difficulty.EASY, weight=1)
        mcq(a1, "Das ist ___ Tisch.", ["eine", "ein", "einen", "einem"], correct_idx=1, diff=Question.Difficulty.EASY, weight=1)
        mcq(a1, "Ich kaufe ___ Tisch.", ["ein", "einen", "eine", "einer"], correct_idx=1, diff=Question.Difficulty.EASY, weight=1)
        mcq(a1, "Hast du Kinder? – Nein, ich habe ___ Kinder.", ["keine", "nicht", "nichts", "keinen"], correct_idx=0, diff=Question.Difficulty.EASY, weight=1)
        mcq(a1, "Wie spät ist es? – 8:30 Uhr", ["halb neun", "halb acht", "viertel nach acht", "viertel vor acht"], correct_idx=0, diff=Question.Difficulty.HARD, weight=3)
        mcq(a1, "Wir gehen ___ Kino.", ["auf", "ins", "im", "nach"], correct_idx=1, diff=Question.Difficulty.MEDIUM, weight=2)
        mcq(a1, "Welcher Satz ist richtig?", ["Ich kann gut schwimmen.", "Ich kann schwimmt gut.", "Ich schwimmen gut kann.", "Ich kann schwimmen gut."], correct_idx=0, diff=Question.Difficulty.MEDIUM, weight=2)
        mcq(a1, "Ich habe gestern einen Brief ___.", ["schreibt", "schreiben", "geschrieben", "schreibe"], correct_idx=2, diff=Question.Difficulty.HARD, weight=3)
        mcq(a1, "Wo ist das Buch? – Das Buch liegt ___ dem Tisch.", ["zwischen", "in", "auf", "über"], correct_idx=2, diff=Question.Difficulty.HARD, weight=3)
        mcq(a1, "Ich _____ gern nach Deutschland fliegen.", ["war", "bin", "würde", "würden"], correct_idx=2, diff=Question.Difficulty.HARD, weight=3)

        # ----------------------
        # A2
        # Cloze test with multiple blanks (enter as numbered pairs: e.g., 1=meiner)
        match(
            a2,
            (
                "CLOZE: Antworten را به‌صورت جفت عدد=کلمه در هر خط وارد کنید (نمونه: 1=meiner).\\n"
                "Text: Letztes Wochenende war ich bei ___(1)___ Freundin. Wir sind zusammen in ___(2)___ Park gegangen "
                "und haben dort ___(3)___ Kaffee getrunken. Ich war sehr glücklich, ___(4)___ das Wetter schön war. "
                "Sie hat mir erzählt, ___(5)___ sie nächste Woche nach Berlin fährt. Das Hotel, ___(6)___ sie gebucht hat, "
                "liegt in der Nähe vom Bahnhof. Ich habe ihr gesagt, dass ich sie besuchen möchte, ___(7)___ ich Zeit habe."
            ),
            [
                ("1", "meiner"),
                ("2", "den"),
                ("3", "einen"),
                ("4", "weil"),
                ("5", "dass"),
                ("6", "das"),
                ("7", "wenn"),
            ],
            diff=Question.Difficulty.HARD,
            weight=3,
        )
        mcq(a2, "Ich möchte gern wissen, ___ du denkst.", ["was", "wer", "ob", "wo"], correct_idx=0, diff=Question.Difficulty.MEDIUM, weight=2)
        mcq(a2, "Der Brief _______ jeden Tag von der Sekretärin geschrieben.", ["wird", "ist", "war", "wurde"], correct_idx=0, diff=Question.Difficulty.MEDIUM, weight=2)
        mcq(a2, "Ich habe gestern einen _______ Film gesehen.", ["interessanter", "interessanten", "interessante", "interessantes"], correct_idx=1, diff=Question.Difficulty.MEDIUM, weight=2)
        mcq(a2, "Am Morgen _______ ich ______ immer schnell.", ["wasche….  mich", "wäscht….. dich", "gewaschen…   sich", "wusch…..mich"], correct_idx=0, diff=Question.Difficulty.MEDIUM, weight=2)
        mcq(a2, "Ich schenke _______ Mutter _______ Blumen.", ["die / einen", "meiner / die", "meiner / einen", "die / einen"], correct_idx=2, diff=Question.Difficulty.EASY, weight=1)
        mcq(a2, "Wir fahren heute Nachmittag _______ Strand.", ["an den", "an dem", "auf  den", "auf dem"], correct_idx=0, diff=Question.Difficulty.MEDIUM, weight=2)
        mcq(a2, "Letztes Jahr _______ ich jeden Tag im Park spazieren.", ["gehe", "ging", "gingst", "gegangen"], correct_idx=1, diff=Question.Difficulty.EASY, weight=1)

        # ----------------------
        # B1
        # Cloze with connectors (enter as numbered pairs: e.g., 1=damit)
        match(
            b1,
            (
                "CLOZE: Konnektoren را به‌صورت جفت عدد=کلمه وارد کنید (نمونه: 1=damit).\\n"
                "Lisa interessiert sich sehr für Fotografie. "
                "Sie hat sich eine neue Kamera gekauft, ___1___ sie bessere Bilder machen kann. "
                "___2___ ist sie oft draußen, um Landschaften zu fotografieren. "
                "___3___ das Wetter schlecht ist, bleibt sie zu Hause und bearbeitet ihre Fotos. "
                "Ihre Freundin Julia, die ___4___ ihrer großen Erfahrung in diesem Bereich hilft, unterstützt sie manchmal. "
                "Lisa möchte bald einen Kurs besuchen, ___5___ mehr über Licht und Farben zu lernen. "
                "Sie findet Fotografie spannend, weil sie ___6___  Kunstform  als auch Ausdruck ihrer Gefühle sieht. "
                "Julia macht nicht nur Porträts, ___7___ Naturfotos sehr gut. "
                "Lisa ist ___8___ noch Anfängerin, ___8___ sie lernt schnell. "
                "___9___ des Kurses will sie eine kleine Ausstellung organisieren."
            ),
            [
                ("1", "damit"),
                ("2", "daher"),
                ("3", "während"),
                ("4", "aufgrund"),
                ("5", "um"),
                ("6", "sowohl"),
                ("7", "sondern auch"),
                ("8", "zwar … aber"),
                ("9", "während"),
            ],
            diff=Question.Difficulty.MEDIUM,
            weight=2,
        )

        # ----------------------
        # B2 (from user content)
        mcq(b2, "Das Problem muss schnell ___ werden.", ["lösen", "gelöst", "löst", "wurde"], correct_idx=1, diff=Question.Difficulty.EASY, weight=1)
        mcq(b2, "Er hat viel gearbeitet, ___ er müde ist.", ["sodass", "obwohl", "dass", "aber"], correct_idx=0, diff=Question.Difficulty.MEDIUM, weight=2)
        mcq(b2, "Was bedeutet „ausnahmsweise“?", ["immer", "zufällig", "nur in einem besonderen Fall", "normal"], correct_idx=2, diff=Question.Difficulty.HARD, weight=3)
        mcq(
            b2,
            "Text: „Viele Menschen kaufen heute im Internet ein, weil es schneller und bequemer ist. Allerdings gibt es auch Risiken, zum Beispiel Betrug.“\nFrage: Was bedeutet das Wort „Betrug“?",
            ["ein Sonderangebot", "eine Lüge oder Täuschung", "ein Rabatt", "eine Lieferung"],
            correct_idx=1,
            diff=Question.Difficulty.MEDIUM,
            weight=2
        )
        mcq(b2, "Hätte ich gestern mehr gelernt, ___ ich die Prüfung bestanden.", ["werde", "hätte", "würde", "war"], correct_idx=1, diff=Question.Difficulty.EASY, weight=1)
        mcq(b2, "Er hat so getan, ___ er nichts gehört hätte.", ["als ob", "wenn", "obwohl", "weil"], correct_idx=0, diff=Question.Difficulty.EASY, weight=1)
        mcq(b2, "Kaum hatte er das Haus verlassen, ___ es zu regnen.", ["beginnt", "begann", "beginnen", "begann hat"], correct_idx=1, diff=Question.Difficulty.HARD, weight=3)
        mcq(b2, "Kaum war die Tür zu, ___ klingelte das Telefon.", ["dann", "schon", "daher", "so"], correct_idx=1, diff=Question.Difficulty.HARD, weight=3)
        mcq(b2, "------- er ankommt, beginnen wir das Essen.", ["sobald", "sowohl", "dafür", "sodass"], correct_idx=0, diff=Question.Difficulty.MEDIUM, weight=2)

        self.stdout.write(self.style.SUCCESS("Assessments seeded with many questions."))


