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

        # Seed A1 (at least 12)
        mcq(a1, "Wählen Sie den richtigen Artikel: ___ Apfel", ["der", "die", "das"], correct_idx=0)
        mcq(a1, "Er ___ in Berlin.", ["wohne", "wohnt", "wohnst"], correct_idx=1)
        mcq(a1, "Ich ___ Kaffee.", ["trinkt", "trinke", "trinken"], correct_idx=1)
        tf(a1, "Deutsch ist eine germanische Sprache.", True)
        fill(a1, "Sie ____ eine Lehrerin.", [("ist", AnswerPattern.PatternType.ICASE)])
        fill(a1, "Ich ____ Hossein.", [("heiße", AnswerPattern.PatternType.EXACT), ("heisse", AnswerPattern.PatternType.ICASE)])
        multi(a1, "Wählen Sie die Vokale.", ["a", "b", "e", "k", "i"], correct_indices=[0,2,4])
        order(a1, "Ordnen Sie die Wörter:", ["Ich", "bin", "Student"], weight=1)
        match(a1, "Ordnen Sie zu (DE→EN)", [("Haus", "House"), ("Buch", "Book"), ("Auto", "Car")])
        mcq(a1, "Wie geht's? — ___", ["Guten Tag", "Gut, danke", "Tschüss"], correct_idx=1)
        mcq(a1, "Er ___ Fußball.", ["spielt", "spielen", "spielst"], correct_idx=0)
        tf(a1, "Artikel von 'Mädchen' ist 'das'.", True)

        # Seed A2 (10)
        mcq(a2, "Wir ___ gestern im Park.", ["waren", "seid", "ist"], correct_idx=0, diff=Question.Difficulty.MEDIUM)
        mcq(a2, "Er hat ___ Auto.", ["ein", "eine", "einen"], correct_idx=0)
        fill(a2, "Ich habe gestern viel _____. (arbeiten)", [("gearbeitet", AnswerPattern.PatternType.ICASE)])
        tf(a2, "Perfekt von 'gehen' ist 'gegangen'.", True)
        multi(a2, "Wählen Sie Trennbare Verben.", ["aufstehen", "verstehen", "mitkommen", "besuchen"], correct_indices=[0,2])
        order(a2, "Ordnen Sie den Satz:", ["Morgen", "gehe", "ich", "ins Kino"])
        match(a2, "Präteritum zu Präsens", [("ging", "geht"), ("war", "ist"), ("hatte", "hat")])
        mcq(a2, "Welche Präposition passt? Ich warte ___ dich.", ["auf", "zu", "mit"], correct_idx=0)
        mcq(a2, "_____ du mir helfen?", ["Kannst", "Kann", "Können"], correct_idx=0)
        fill(a2, "Er hat das Buch ____. (lesen)", [("gelesen", AnswerPattern.PatternType.EXACT)])

        # Seed B1 (10)
        mcq(b1, "Wenn ich Zeit hätte, ___ ich mehr lesen.", ["würde", "werde", "wäre"], correct_idx=0)
        tf(b1, "Konjunktiv II drückt Irrealität aus.", True)
        fill(b1, "Er tat so, als ____ er nichts wüsste.", [("ob", AnswerPattern.PatternType.ICASE)])
        multi(b1, "Wählen Sie Modalverben.", ["dürfen", "können", "macht", "haben"], correct_indices=[0,1])
        order(b1, "Ordnen Sie:", ["Obwohl", "es", "regnete", ",", "ging", "er", "spazieren"]) 
        match(b1, "Synonyme", [("beginnen", "anfangen"), ("kaufen", "erwerben")])
        mcq(b1, "Er hat die Prüfung ___ bestanden.", ["leider", "zum Glück", "kaum"], correct_idx=1)
        mcq(b1, "Das ist der Mann, ___ ich geholfen habe.", ["dem", "den", "dessen"], correct_idx=0)
        fill(b1, "Er verhielt sich, ___ es ihn nichts anginge.", [("als", AnswerPattern.PatternType.ICASE)])
        tf(b1, "Passiv Präsens: Das Haus wird gebaut.", True)

        # Seed B2 (10)
        mcq(b2, "Je mehr er lernt, ___ versteht er.", ["desto mehr", "so mehr", "mehr"], correct_idx=0)
        multi(b2, "Wählen Sie korrekte Konnektoren.", ["denn", "obwohl", "aber", "weil"], correct_indices=[0,1,3])
        tf(b2, "Relativsatz mit Präposition: 'auf den' kann 'worauf' werden.", True)
        fill(b2, "Er fragte, ___ ich kommen könne.", [("ob", AnswerPattern.PatternType.ICASE)])
        order(b2, "Ordnen Sie die Satzteile:", ["Der Lehrer", "hat", "den Schüler", "für seine Leistung", "gelobt"]) 
        match(b2, "Deutsch → Bedeutung", [("doch", "however"), ("eher", "rather"), ("zwar", "indeed")])
        mcq(b2, "Das ist das Beste, ___ ich je gesehen habe.", ["was", "das", "wie"], correct_idx=0)
        mcq(b2, "Er tat so, ___ er krank wäre.", ["als ob", "wenn", "ob"], correct_idx=0)
        fill(b2, "Er arbeitet, ___ er die Prüfung besteht.", [("damit", AnswerPattern.PatternType.ICASE)])
        tf(b2, "'zu' vor Infinitiv ist immer notwendig.", False)

        self.stdout.write(self.style.SUCCESS("Assessments seeded with many questions."))


