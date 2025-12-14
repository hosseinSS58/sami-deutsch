import json
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.db import transaction
from assessments.models import (
    Assessment,
    Question,
    Choice,
    AnswerPattern,
    OrderingItem,
    MatchPair,
    QuestionMedia,
    HintResource,
)


class Command(BaseCommand):
    help = "Import assessment data from JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            'input_file',
            type=str,
            help='Input JSON file path'
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear all existing assessment data before import'
        )
        parser.add_argument(
            '--skip-submissions',
            action='store_true',
            help='Skip importing submissions even if they exist in the file'
        )
        parser.add_argument(
            '--media-dir',
            type=str,
            help='Directory containing media files to import'
        )

    def handle(self, *args, **options):
        input_file = options['input_file']
        clear_existing = options['clear_existing']
        skip_submissions = options['skip_submissions']
        media_dir = options.get('media_dir')

        if not os.path.exists(input_file):
            self.stdout.write(self.style.ERROR(f'File not found: {input_file}'))
            return

        self.stdout.write(self.style.WARNING('Starting import...'))

        # Load data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Clear existing data if requested
        if clear_existing:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            QuestionMedia.objects.all().delete()
            HintResource.objects.all().delete()
            # Import Submission models only if needed
            if 'submissions' in data:
                from assessments.models import Submission, SubmissionItem
                SubmissionItem.objects.all().delete()
                Submission.objects.all().delete()
            MatchPair.objects.all().delete()
            OrderingItem.objects.all().delete()
            AnswerPattern.objects.all().delete()
            Choice.objects.all().delete()
            Question.objects.all().delete()
            Assessment.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Existing data cleared'))

        # Import in transaction
        try:
            with transaction.atomic():
                # Import Assessments
                assessment_map = {}  # export_id -> new_db_id
                for assessment_data in data.get('assessments', []):
                    assessment = Assessment.objects.create(
                        title=assessment_data['title'],
                        level=assessment_data['level'],
                        is_active=assessment_data.get('is_active', True),
                        time_limit_seconds=assessment_data.get('time_limit_seconds', 600),
                        attempt_limit=assessment_data.get('attempt_limit', 3),
                    )
                    assessment_map[assessment_data['export_id']] = assessment.id
                    self.stdout.write(f'  ✓ Created assessment: {assessment.title}')

                # Import Questions
                question_map = {}  # export_id -> new_db_id
                for question_data in data.get('questions', []):
                    assessment_id = assessment_map.get(question_data['assessment_export_id'])
                    if not assessment_id:
                        self.stdout.write(self.style.ERROR(
                            f"  ✗ Skipping question {question_data['export_id']}: assessment not found"
                        ))
                        continue

                    question = Question.objects.create(
                        assessment_id=assessment_id,
                        text=question_data['text'],
                        type=question_data['type'],
                        target_level=question_data.get('target_level', 'A1'),
                        difficulty=question_data.get('difficulty', 'medium'),
                        weight=question_data.get('weight', 1),
                        explanation=question_data.get('explanation', ''),
                        correct_boolean=question_data.get('correct_boolean'),
                        hint_text=question_data.get('hint_text', ''),
                        hint_links=question_data.get('hint_links', []),
                    )
                    question_map[question_data['export_id']] = question.id

                self.stdout.write(self.style.SUCCESS(
                    f'✓ Imported {len(question_map)} questions'
                ))

                # Import Choices
                choice_count = 0
                for choice_data in data.get('choices', []):
                    question_id = question_map.get(choice_data['question_export_id'])
                    if not question_id:
                        continue

                    Choice.objects.create(
                        question_id=question_id,
                        text=choice_data['text'],
                        is_correct=choice_data['is_correct'],
                    )
                    choice_count += 1

                self.stdout.write(self.style.SUCCESS(f'✓ Imported {choice_count} choices'))

                # Import AnswerPatterns
                pattern_count = 0
                for pattern_data in data.get('answer_patterns', []):
                    question_id = question_map.get(pattern_data['question_export_id'])
                    if not question_id:
                        continue

                    AnswerPattern.objects.create(
                        question_id=question_id,
                        pattern=pattern_data['pattern'],
                        kind=pattern_data.get('kind', 'icase'),
                    )
                    pattern_count += 1

                self.stdout.write(self.style.SUCCESS(
                    f'✓ Imported {pattern_count} answer patterns'
                ))

                # Import OrderingItems
                ordering_count = 0
                for item_data in data.get('ordering_items', []):
                    question_id = question_map.get(item_data['question_export_id'])
                    if not question_id:
                        continue

                    OrderingItem.objects.create(
                        question_id=question_id,
                        text=item_data['text'],
                        correct_position=item_data['correct_position'],
                    )
                    ordering_count += 1

                self.stdout.write(self.style.SUCCESS(
                    f'✓ Imported {ordering_count} ordering items'
                ))

                # Import MatchPairs
                match_count = 0
                for pair_data in data.get('match_pairs', []):
                    question_id = question_map.get(pair_data['question_export_id'])
                    if not question_id:
                        continue

                    MatchPair.objects.create(
                        question_id=question_id,
                        left_text=pair_data['left_text'],
                        right_text=pair_data['right_text'],
                    )
                    match_count += 1

                self.stdout.write(self.style.SUCCESS(
                    f'✓ Imported {match_count} match pairs'
                ))

                # Import QuestionMedia
                media_count = 0
                media_import_map = {}  # export_id -> media_data for later file handling
                
                for media_data in data.get('question_media', []):
                    question_id = question_map.get(media_data['question_export_id'])
                    if not question_id:
                        continue

                    media = QuestionMedia.objects.create(
                        question_id=question_id,
                        media_type=media_data['media_type'],
                        caption=media_data.get('caption', ''),
                        order=media_data.get('order', 0),
                    )
                    media_import_map[media_data['export_id']] = {
                        'media': media,
                        'file_path': media_data.get('file_path'),
                        'filename': os.path.basename(media_data.get('file_path', '')) if media_data.get('file_path') else None,
                    }
                    media_count += 1

                self.stdout.write(self.style.SUCCESS(
                    f'✓ Imported {media_count} media records'
                ))

                # Handle media files if directory provided
                if media_dir and os.path.exists(media_dir) and media_import_map:
                    self.stdout.write(self.style.WARNING('Copying media files...'))
                    files_copied = 0
                    
                    for export_id, media_info in media_import_map.items():
                        # Try to find file in media_dir
                        # Files should be named: {export_id}_{original_filename}
                        if media_info['filename']:
                            expected_filename = f"{export_id}_{media_info['filename']}"
                            file_path = os.path.join(media_dir, expected_filename)
                            
                            if os.path.exists(file_path):
                                try:
                                    with open(file_path, 'rb') as f:
                                        media_info['media'].file.save(
                                            media_info['filename'],
                                            File(f),
                                            save=True
                                        )
                                    files_copied += 1
                                    self.stdout.write(f'  ✓ Copied: {media_info["filename"]}')
                                except Exception as e:
                                    self.stdout.write(self.style.ERROR(
                                        f'  ✗ Failed to copy {expected_filename}: {e}'
                                    ))
                            else:
                                # Try alternative: just the filename without export_id prefix
                                alt_path = os.path.join(media_dir, media_info['filename'])
                                if os.path.exists(alt_path):
                                    try:
                                        with open(alt_path, 'rb') as f:
                                            media_info['media'].file.save(
                                                media_info['filename'],
                                                File(f),
                                                save=True
                                            )
                                        files_copied += 1
                                        self.stdout.write(f'  ✓ Copied: {media_info["filename"]}')
                                    except Exception as e:
                                        self.stdout.write(self.style.ERROR(
                                            f'  ✗ Failed to copy {media_info["filename"]}: {e}'
                                        ))
                    
                    if files_copied > 0:
                        self.stdout.write(self.style.SUCCESS(
                            f'✓ Copied {files_copied} media files'
                        ))
                    else:
                        self.stdout.write(self.style.WARNING(
                            'No media files were copied. You may need to upload them manually.'
                        ))

                # Import HintResources
                hint_count = 0
                for hint_data in data.get('hint_resources', []):
                    question_id = question_map.get(hint_data['question_export_id'])
                    if not question_id:
                        continue
                    HintResource.objects.create(
                        question_id=question_id,
                        title=hint_data.get('title', ''),
                        url=hint_data.get('url', ''),
                        order=hint_data.get('order', 0),
                    )
                    hint_count += 1
                if hint_count:
                    self.stdout.write(self.style.SUCCESS(f'✓ Imported {hint_count} hint resources'))

                # Import Submissions if available and not skipped
                if 'submissions' in data and not skip_submissions:
                    from assessments.models import Submission, SubmissionItem
                    
                    submission_map = {}
                    submission_count = 0
                    
                    for submission_data in data.get('submissions', []):
                        assessment_id = assessment_map.get(submission_data['assessment_export_id'])
                        if not assessment_id:
                            continue

                        submission = Submission.objects.create(
                            assessment_id=assessment_id,
                            user_identifier=submission_data['user_identifier'],
                            full_name=submission_data.get('full_name', ''),
                            email=submission_data.get('email', ''),
                            score=submission_data.get('score', 0),
                            total_weight=submission_data.get('total_weight', 0),
                            ratio=submission_data.get('ratio', 0),
                            duration_seconds=submission_data.get('duration_seconds', 0),
                            recommended_level=submission_data['recommended_level'],
                        )
                        submission_map[submission_data['export_id']] = submission.id
                        submission_count += 1

                    self.stdout.write(self.style.SUCCESS(
                        f'✓ Imported {submission_count} submissions'
                    ))

                    # Import SubmissionItems
                    item_count = 0
                    for item_data in data.get('submission_items', []):
                        submission_id = submission_map.get(item_data['submission_export_id'])
                        question_id = question_map.get(item_data['question_export_id'])
                        
                        if not submission_id or not question_id:
                            continue

                        SubmissionItem.objects.create(
                            submission_id=submission_id,
                            question_id=question_id,
                            selected_choice_id=item_data.get('selected_choice_id'),
                            user_text=item_data.get('user_text', ''),
                            is_correct=item_data.get('is_correct', False),
                            gained_score=item_data.get('gained_score', 0),
                        )
                        item_count += 1

                    self.stdout.write(self.style.SUCCESS(
                        f'✓ Imported {item_count} submission items'
                    ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Import failed: {e}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
            raise

        self.stdout.write(self.style.SUCCESS('\n✓ Import completed successfully!'))


