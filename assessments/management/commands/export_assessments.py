import json
import os
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.conf import settings
from assessments.models import (
    Assessment, Question, Choice, AnswerPattern, 
    OrderingItem, MatchPair, QuestionMedia
)


class Command(BaseCommand):
    help = "Export all assessment data to JSON file for migration"

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='assessments_export.json',
            help='Output JSON file path (default: assessments_export.json)'
        )
        parser.add_argument(
            '--include-submissions',
            action='store_true',
            help='Include submission data (default: False)'
        )
        parser.add_argument(
            '--include-media-files',
            action='store_true',
            help='Copy media files to export directory (default: False)'
        )
        parser.add_argument(
            '--media-dir',
            type=str,
            default='assessments_export_media',
            help='Directory to copy media files (default: assessments_export_media)'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        include_submissions = options['include_submissions']
        include_media = options['include_media_files']
        media_dir = options['media_dir']

        self.stdout.write(self.style.WARNING('Starting export...'))

        # Collect all data
        data = {
            'assessments': [],
            'questions': [],
            'choices': [],
            'answer_patterns': [],
            'ordering_items': [],
            'match_pairs': [],
            'question_media': [],
            'id_mapping': {}
        }

        # Export Assessments
        assessments = Assessment.objects.all().order_by('id')
        assessment_id_map = {}
        for idx, assessment in enumerate(assessments, start=1):
            old_id = assessment.id
            new_id = idx
            assessment_id_map[old_id] = new_id
            
            data['assessments'].append({
                'export_id': new_id,
                'title': assessment.title,
                'level': assessment.level,
                'is_active': assessment.is_active,
                'time_limit_seconds': assessment.time_limit_seconds,
                'attempt_limit': assessment.attempt_limit,
                'created_at': assessment.created_at.isoformat() if assessment.created_at else None,
            })

        data['id_mapping']['assessments'] = assessment_id_map

        # Export Questions
        questions = Question.objects.all().order_by('assessment_id', 'id')
        question_id_map = {}
        question_idx = 1
        for question in questions:
            old_id = question.id
            new_id = question_idx
            question_id_map[old_id] = new_id
            question_idx += 1

            data['questions'].append({
                'export_id': new_id,
                'assessment_export_id': assessment_id_map.get(question.assessment_id),
                'text': question.text,
                'type': question.type,
                'target_level': question.target_level,
                'difficulty': question.difficulty,
                'weight': question.weight,
                'explanation': question.explanation,
                'correct_boolean': question.correct_boolean,
            })

        data['id_mapping']['questions'] = question_id_map

        # Export Choices
        choices = Choice.objects.all().order_by('question_id', 'id')
        choice_id_map = {}
        choice_idx = 1
        for choice in choices:
            old_id = choice.id
            new_id = choice_idx
            choice_id_map[old_id] = new_id
            choice_idx += 1

            data['choices'].append({
                'export_id': new_id,
                'question_export_id': question_id_map.get(choice.question_id),
                'text': choice.text,
                'is_correct': choice.is_correct,
            })

        # Export AnswerPatterns
        patterns = AnswerPattern.objects.all().order_by('question_id', 'id')
        pattern_idx = 1
        for pattern in patterns:
            data['answer_patterns'].append({
                'export_id': pattern_idx,
                'question_export_id': question_id_map.get(pattern.question_id),
                'pattern': pattern.pattern,
                'kind': pattern.kind,
            })
            pattern_idx += 1

        # Export OrderingItems
        ordering_items = OrderingItem.objects.all().order_by('question_id', 'correct_position')
        ordering_idx = 1
        for item in ordering_items:
            data['ordering_items'].append({
                'export_id': ordering_idx,
                'question_export_id': question_id_map.get(item.question_id),
                'text': item.text,
                'correct_position': item.correct_position,
            })
            ordering_idx += 1

        # Export MatchPairs
        match_pairs = MatchPair.objects.all().order_by('question_id', 'id')
        match_idx = 1
        for pair in match_pairs:
            data['match_pairs'].append({
                'export_id': match_idx,
                'question_export_id': question_id_map.get(pair.question_id),
                'left_text': pair.left_text,
                'right_text': pair.right_text,
            })
            match_idx += 1

        # Export QuestionMedia
        media_files = QuestionMedia.objects.all().order_by('question_id', 'order', 'created_at')
        media_idx = 1
        media_files_info = []
        
        for media in media_files:
            file_path = None
            file_url = None
            
            if media.file:
                file_path = str(media.file.name)
                # Get full file path if possible
                if default_storage.exists(media.file.name):
                    try:
                        file_url = media.file.url
                    except:
                        pass
            
            media_data = {
                'export_id': media_idx,
                'question_export_id': question_id_map.get(media.question_id),
                'media_type': media.media_type,
                'file_path': file_path,
                'file_url': file_url,
                'caption': media.caption,
                'order': media.order,
                'created_at': media.created_at.isoformat() if media.created_at else None,
            }
            
            data['question_media'].append(media_data)
            media_files_info.append({
                'export_id': media_idx,
                'source_path': media.file.path if media.file and hasattr(media.file, 'path') else None,
                'relative_path': file_path,
            })
            media_idx += 1

        # Optionally include submissions
        if include_submissions:
            from assessments.models import Submission, SubmissionItem
            data['submissions'] = []
            data['submission_items'] = []
            
            submissions = Submission.objects.all().order_by('id')
            submission_id_map = {}
            submission_idx = 1
            
            for submission in submissions:
                old_id = submission.id
                new_id = submission_idx
                submission_id_map[old_id] = new_id
                submission_idx += 1

                data['submissions'].append({
                    'export_id': new_id,
                    'assessment_export_id': assessment_id_map.get(submission.assessment_id),
                    'user_id': submission.user_id,  # May not exist in new DB
                    'user_identifier': submission.user_identifier,
                    'full_name': submission.full_name,
                    'email': submission.email,
                    'score': float(submission.score),
                    'total_weight': float(submission.total_weight),
                    'ratio': float(submission.ratio),
                    'duration_seconds': submission.duration_seconds,
                    'recommended_level': submission.recommended_level,
                    'created_at': submission.created_at.isoformat() if submission.created_at else None,
                })

            submission_items = SubmissionItem.objects.all().order_by('submission_id', 'id')
            item_idx = 1
            for item in submission_items:
                data['submission_items'].append({
                    'export_id': item_idx,
                    'submission_export_id': submission_id_map.get(item.submission_id),
                    'question_export_id': question_id_map.get(item.question_id),
                    'selected_choice_id': item.selected_choice_id,
                    'user_text': item.user_text,
                    'is_correct': item.is_correct,
                    'gained_score': float(item.gained_score),
                })
                item_idx += 1

            data['id_mapping']['submissions'] = submission_id_map

        # Save JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(
            f'✓ Exported {len(data["assessments"])} assessments'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'✓ Exported {len(data["questions"])} questions'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'✓ Exported {len(data["choices"])} choices'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'✓ Exported {len(data["answer_patterns"])} answer patterns'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'✓ Exported {len(data["ordering_items"])} ordering items'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'✓ Exported {len(data["match_pairs"])} match pairs'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'✓ Exported {len(data["question_media"])} media files'
        ))
        
        if include_submissions:
            self.stdout.write(self.style.SUCCESS(
                f'✓ Exported {len(data["submissions"])} submissions'
            ))
            self.stdout.write(self.style.SUCCESS(
                f'✓ Exported {len(data["submission_items"])} submission items'
            ))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Data exported to: {output_file}'))

        # Copy media files if requested
        if include_media and media_files_info:
            os.makedirs(media_dir, exist_ok=True)
            copied_count = 0
            
            for media_info in media_files_info:
                if media_info['source_path'] and os.path.exists(media_info['source_path']):
                    filename = os.path.basename(media_info['source_path'])
                    dest_path = os.path.join(media_dir, f"{media_info['export_id']}_{filename}")
                    
                    try:
                        import shutil
                        shutil.copy2(media_info['source_path'], dest_path)
                        copied_count += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f'Failed to copy {media_info["source_path"]}: {e}'
                        ))
            
            if copied_count > 0:
                self.stdout.write(self.style.SUCCESS(
                    f'\n✓ Copied {copied_count} media files to: {media_dir}'
                ))
                self.stdout.write(self.style.WARNING(
                    f'Note: You will need to manually upload these files to the new server.'
                ))


