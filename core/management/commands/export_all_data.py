"""
دستور جامع برای استخراج تمام داده‌های سایت
"""
import json
import os
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.apps import apps


class Command(BaseCommand):
    help = "Export all site data to JSON file for migration"

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='site_data_export.json',
            help='Output JSON file path (default: site_data_export.json)'
        )
        parser.add_argument(
            '--include-stats',
            action='store_true',
            help='Include statistics data (visits, clicks, etc.) (default: False)'
        )
        parser.add_argument(
            '--include-users',
            action='store_true',
            help='Include user data and profiles (default: False)'
        )
        parser.add_argument(
            '--include-submissions',
            action='store_true',
            help='Include assessment submissions (default: False)'
        )
        parser.add_argument(
            '--include-orders',
            action='store_true',
            help='Include shop orders (default: False)'
        )
        parser.add_argument(
            '--include-media-files',
            action='store_true',
            help='Copy media files to export directory (default: False)'
        )
        parser.add_argument(
            '--media-dir',
            type=str,
            default='site_export_media',
            help='Directory to copy media files (default: site_export_media)'
        )
        parser.add_argument(
            '--apps',
            type=str,
            nargs='+',
            help='Specific apps to export (e.g., --apps assessments courses blog). If not specified, exports all apps.'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        include_stats = options['include_stats']
        include_users = options['include_users']
        include_submissions = options['include_submissions']
        include_orders = options['include_orders']
        include_media = options['include_media_files']
        media_dir = options['media_dir']
        specific_apps = options.get('apps', [])

        self.stdout.write(self.style.WARNING('Starting full site export...'))

        # Define export configuration
        export_config = {
            'assessments': {
                'models': [
                    'Assessment', 'Question', 'Choice', 'AnswerPattern',
                    'OrderingItem', 'MatchPair', 'QuestionMedia'
                ],
                'conditional_models': {
                    'Submission': include_submissions,
                    'SubmissionItem': include_submissions,
                }
            },
            'courses': {
                'models': ['Video', 'VideoImage', 'YouTubeLink', 'VideoTag']
            },
            'blog': {
                'models': ['Category', 'Post']
            },
            'shop': {
                'models': ['Product'],
                'conditional_models': {
                    'Order': include_orders,
                    'OrderItem': include_orders,
                }
            },
            'accounts': {
                'models': [],
                'conditional_models': {
                    'Profile': include_users,
                }
            },
            'core': {
                'models': [],
                'conditional_models': {
                    'ContactMessage': True,
                    'AnonymousVisitor': include_stats,
                    'SiteVisit': include_stats,
                    'YouTubeClick': include_stats,
                }
            },
            'siteconfig': {
                'models': [
                    'SiteSettings', 'NavLink', 'FooterLink', 'HomeFeature',
                    'HomeSlider', 'Slide', 'Menu', 'MenuItem', 'HomePageSection', 'SocialLink'
                ]
            }
        }

        # Filter apps if specific apps requested
        if specific_apps:
            export_config = {k: v for k, v in export_config.items() if k in specific_apps}

        data = {
            'export_info': {
                'include_stats': include_stats,
                'include_users': include_users,
                'include_submissions': include_submissions,
                'include_orders': include_orders,
            },
            'data': {},
            'id_mappings': {},
            'file_references': []
        }

        # First pass: export all models and build id mappings
        for app_name, config in export_config.items():
            self.stdout.write(f'\nExporting {app_name}...')
            
            try:
                app = apps.get_app_config(app_name)
                app_data = {}
                app_id_maps = {}
                
                # Export regular models
                all_models = list(config.get('models', []))
                
                # Add conditional models
                for model_name, should_include in config.get('conditional_models', {}).items():
                    if should_include:
                        all_models.append(model_name)
                
                # Export models in dependency order
                for model_name in all_models:
                    try:
                        model = app.get_model(model_name)
                        model_data, id_map, file_refs = self.export_model(
                            model, include_media, data['id_mappings']
                        )
                        
                        if model_data:
                            app_data[model_name] = model_data
                            app_id_maps[model_name] = id_map
                            data['file_references'].extend(file_refs)
                            
                            self.stdout.write(
                                self.style.SUCCESS(f'  ✓ Exported {len(model_data)} {model_name}')
                            )
                    except LookupError:
                        self.stdout.write(
                            self.style.WARNING(f'  ⚠ Model {model_name} not found in {app_name}')
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ Error exporting {model_name}: {e}')
                        )
                
                if app_data:
                    data['data'][app_name] = app_data
                    data['id_mappings'][app_name] = app_id_maps
                    
            except LookupError:
                self.stdout.write(
                    self.style.WARNING(f'⚠ App {app_name} not found')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error exporting {app_name}: {e}')
                )

        # Save JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f'\n✓ Data exported to: {output_file}'))

        # Copy media files if requested
        if include_media and data['file_references']:
            os.makedirs(media_dir, exist_ok=True)
            copied_count = 0
            
            for file_ref in data['file_references']:
                source_path = file_ref.get('source_path')
                export_id = file_ref.get('export_id')
                relative_path = file_ref.get('relative_path')
                
                if source_path and os.path.exists(source_path):
                    filename = os.path.basename(source_path)
                    dest_path = os.path.join(media_dir, f"{export_id}_{filename}")
                    
                    try:
                        import shutil
                        shutil.copy2(source_path, dest_path)
                        copied_count += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f'Failed to copy {source_path}: {e}'
                        ))
                elif relative_path:
                    # Try to find file by relative path
                    try:
                        from django.conf import settings
                        media_root = getattr(settings, 'MEDIA_ROOT', '')
                        if media_root:
                            full_path = os.path.join(media_root, relative_path)
                            if os.path.exists(full_path):
                                filename = os.path.basename(full_path)
                                dest_path = os.path.join(media_dir, f"{export_id}_{filename}")
                                import shutil
                                shutil.copy2(full_path, dest_path)
                                copied_count += 1
                    except Exception as e:
                        pass
            
            if copied_count > 0:
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Copied {copied_count} media files to: {media_dir}'
                ))
                self.stdout.write(self.style.WARNING(
                    'Note: You will need to manually upload these files to the new server.'
                ))

    def export_model(self, model, track_files=False, all_id_mappings=None):
        """Export a model to JSON-serializable format"""
        if all_id_mappings is None:
            all_id_mappings = {}
            
        data = []
        id_map = {}  # old_id -> export_id
        file_refs = []
        
        objects = model.objects.all().order_by('id')
        
        for idx, obj in enumerate(objects, start=1):
            old_id = obj.id
            export_id = idx
            id_map[old_id] = export_id
            
            # Get all fields
            obj_data = {'export_id': export_id}
            
            # Get model fields
            for field in model._meta.get_fields():
                if field.name == 'id':
                    continue
                
                try:
                    value = getattr(obj, field.name)
                    
                    # Handle ForeignKey - convert to export_id
                    if field.many_to_one and value is not None:
                        related_app = field.related_model._meta.app_label
                        related_model_name = field.related_model.__name__
                        
                        # Try to find export_id in already exported mappings
                        if related_app in all_id_mappings:
                            if related_model_name in all_id_mappings[related_app]:
                                old_id_map = all_id_mappings[related_app][related_model_name]
                                if value.id in old_id_map:
                                    obj_data[field.name + '_id'] = old_id_map[value.id]
                                else:
                                    # FK not exported yet, keep old_id for now
                                    obj_data[field.name + '_id'] = value.id
                            else:
                                obj_data[field.name + '_id'] = value.id
                        else:
                            obj_data[field.name + '_id'] = value.id
                    # Handle ManyToMany - convert to export_ids
                    elif field.many_to_many:
                        related_app = field.related_model._meta.app_label
                        related_model_name = field.related_model.__name__
                        export_ids = []
                        
                        for v in value.all():
                            if related_app in all_id_mappings:
                                if related_model_name in all_id_mappings[related_app]:
                                    old_id_map = all_id_mappings[related_app][related_model_name]
                                    if v.id in old_id_map:
                                        export_ids.append(old_id_map[v.id])
                                        continue
                            # If not found, keep original ID (shouldn't happen if exported in order)
                            export_ids.append(v.id)
                        
                        obj_data[field.name + '_ids'] = export_ids
                    # Handle FileField/ImageField
                    elif hasattr(field, 'upload_to') and value:
                        obj_data[field.name] = str(value.name) if value else None
                        if track_files and value:
                            try:
                                file_path = value.path if hasattr(value, 'path') else None
                                obj_data[field.name + '_url'] = value.url if hasattr(value, 'url') else None
                                
                                file_refs.append({
                                    'export_id': export_id,
                                    'model': f"{model._meta.app_label}.{model.__name__}",
                                    'field': field.name,
                                    'source_path': file_path,
                                    'relative_path': str(value.name),
                                })
                            except:
                                pass
                    # Handle DateTimeField
                    elif hasattr(value, 'isoformat'):
                        obj_data[field.name] = value.isoformat() if value else None
                    # Handle other fields
                    else:
                        obj_data[field.name] = value
                        
                except Exception as e:
                    # Skip problematic fields
                    pass
            
            data.append(obj_data)
        
        return data, id_map, file_refs



