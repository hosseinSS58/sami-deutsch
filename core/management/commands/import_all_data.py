"""
دستور جامع برای وارد کردن تمام داده‌های سایت
"""
import json
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.db import transaction
from django.apps import apps


class Command(BaseCommand):
    help = "Import all site data from JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            'input_file',
            type=str,
            help='Input JSON file path'
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear all existing data before import'
        )
        parser.add_argument(
            '--media-dir',
            type=str,
            help='Directory containing media files to import'
        )
        parser.add_argument(
            '--apps',
            type=str,
            nargs='+',
            help='Specific apps to import (e.g., --apps assessments courses blog). If not specified, imports all apps.'
        )
        parser.add_argument(
            '--skip-foreign-keys',
            action='store_true',
            help='Skip foreign key resolution (use when IDs are preserved)'
        )

    def handle(self, *args, **options):
        input_file = options['input_file']
        clear_existing = options['clear_existing']
        media_dir = options.get('media_dir')
        specific_apps = options.get('apps')
        skip_foreign_keys = options['skip_foreign_keys']

        if not os.path.exists(input_file):
            self.stdout.write(self.style.ERROR(f'File not found: {input_file}'))
            return

        self.stdout.write(self.style.WARNING('Starting import...'))

        # Load data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        export_info = data.get('export_info', {})
        app_data = data.get('data', {})
        id_mappings = data.get('id_mappings', {})  # old_db_id -> export_id
        file_references = data.get('file_references', [])

        # Filter apps if specific apps requested
        if specific_apps:
            app_data = {k: v for k, v in app_data.items() if k in specific_apps}

        # Define import order (respecting dependencies)
        import_order = {
            'siteconfig': ['SiteSettings', 'NavLink', 'FooterLink', 'HomeFeature', 'HomeSlider', 'Slide', 'Menu', 'MenuItem', 'HomePageSection', 'SocialLink'],
            'blog': ['Category', 'Post'],
            'courses': ['Video', 'VideoImage', 'YouTubeLink', 'VideoTag'],
            'assessments': ['Assessment', 'Question', 'Choice', 'AnswerPattern', 'OrderingItem', 'MatchPair', 'QuestionMedia', 'Submission', 'SubmissionItem'],
            'shop': ['Product', 'Order', 'OrderItem'],
            'accounts': ['Profile'],
            'core': ['ContactMessage', 'AnonymousVisitor', 'SiteVisit', 'YouTubeClick'],
        }

        try:
            with transaction.atomic():
                # Clear existing data if requested
                if clear_existing:
                    self.stdout.write(self.style.WARNING('Clearing existing data...'))
                    self.clear_existing_data(app_data)
                    self.stdout.write(self.style.SUCCESS('✓ Existing data cleared'))

                # Import apps in order
                all_id_maps = {}  # app_name -> model_name -> export_id -> new_db_id

                for app_name in import_order.keys():
                    if app_name not in app_data:
                        continue

                    self.stdout.write(f'\nImporting {app_name}...')
                    
                    try:
                        app = apps.get_app_config(app_name)
                        app_id_map = {}
                        
                        # Import models in dependency order
                        model_order = import_order.get(app_name, [])
                        models_to_import = app_data[app_name].keys()
                        
                        # Sort by dependency order
                        sorted_models = [m for m in model_order if m in models_to_import]
                        sorted_models.extend([m for m in models_to_import if m not in sorted_models])
                        
                        for model_name in sorted_models:
                            if model_name not in app_data[app_name]:
                                continue
                                
                            try:
                                model = app.get_model(model_name)
                                model_data = app_data[app_name][model_name]
                                # id_mappings contains: old_db_id -> export_id
                                # We need reverse: export_id -> old_db_id for foreign key resolution
                                old_id_map = id_mappings.get(app_name, {}).get(model_name, {})
                                reverse_old_map = {v: k for k, v in old_id_map.items()} if old_id_map else {}
                                
                                new_id_map = self.import_model(
                                    model, model_data, reverse_old_map, all_id_maps, skip_foreign_keys
                                )
                                
                                app_id_map[model_name] = new_id_map
                                
                                self.stdout.write(
                                    self.style.SUCCESS(f'  ✓ Imported {len(model_data)} {model_name}')
                                )
                                
                            except LookupError:
                                self.stdout.write(
                                    self.style.WARNING(f'  ⚠ Model {model_name} not found')
                                )
                            except Exception as e:
                                self.stdout.write(
                                    self.style.ERROR(f'  ✗ Error importing {model_name}: {e}')
                                )
                                import traceback
                                self.stdout.write(self.style.ERROR(traceback.format_exc()))
                        
                        all_id_maps[app_name] = app_id_map
                        
                    except LookupError:
                        self.stdout.write(
                            self.style.WARNING(f'⚠ App {app_name} not found')
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'✗ Error importing {app_name}: {e}')
                        )

                # Handle media files
                if media_dir and os.path.exists(media_dir) and file_references:
                    self.stdout.write(self.style.WARNING('\nImporting media files...'))
                    self.import_media_files(file_references, all_id_maps, media_dir)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Import failed: {e}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
            raise

        self.stdout.write(self.style.SUCCESS('\n✓ Import completed successfully!'))

    def clear_existing_data(self, app_data):
        """Clear existing data in reverse dependency order"""
        clear_order = [
            ('assessments', ['SubmissionItem', 'Submission', 'QuestionMedia', 'MatchPair', 'OrderingItem', 'AnswerPattern', 'Choice', 'Question', 'Assessment']),
            ('shop', ['OrderItem', 'Order', 'Product']),
            ('courses', ['VideoTag', 'YouTubeLink', 'VideoImage', 'Video']),
            ('blog', ['Post', 'Category']),
            ('accounts', ['Profile']),
            ('core', ['YouTubeClick', 'SiteVisit', 'AnonymousVisitor', 'ContactMessage']),
            ('siteconfig', ['HomePageSection', 'SocialLink', 'MenuItem', 'Menu', 'Slide', 'HomeSlider', 'HomeFeature', 'FooterLink', 'NavLink', 'SiteSettings']),
        ]
        
        for app_name, model_names in clear_order:
            if app_name not in app_data:
                continue
                
            try:
                app = apps.get_app_config(app_name)
                for model_name in model_names:
                    try:
                        model = app.get_model(model_name)
                        model.objects.all().delete()
                    except LookupError:
                        pass
            except LookupError:
                pass

    def import_model(self, model, model_data, old_id_map, all_id_maps, skip_foreign_keys):
        """Import a model from JSON data"""
        new_id_map = {}  # export_id -> new_db_id
        
        for item_data in model_data:
            export_id = item_data.pop('export_id')
            
            # Prepare fields
            fields = {}
            m2m_fields = {}
            file_fields = {}
            
            for key, value in item_data.items():
                # Handle ManyToMany fields
                if key.endswith('_ids'):
                    field_name = key[:-4]  # Remove '_ids'
                    try:
                        field = model._meta.get_field(field_name)
                        if field.many_to_many:
                            m2m_fields[field_name] = value
                            continue
                    except:
                        pass
                
                # Handle ForeignKey fields
                if key.endswith('_id'):
                    field_name = key[:-3]  # Remove '_id'
                    try:
                        field = model._meta.get_field(field_name)
                        if field.many_to_one:
                            # value should be export_id from the related model
                            if not skip_foreign_keys and value:
                                resolved_id = self.resolve_foreign_key(
                                    field.related_model, value, old_id_map, all_id_maps
                                )
                                if resolved_id:
                                    fields[field_name + '_id'] = resolved_id
                                else:
                                    # Foreign key not resolved yet, set to None
                                    fields[field_name + '_id'] = None
                            else:
                                fields[key] = value
                            continue
                    except:
                        pass
                
                # Handle FileField/ImageField
                if self.is_file_field(model, key):
                    file_fields[key] = value
                    continue
                
                # Regular fields
                fields[key] = value
            
            # Create object
            try:
                obj = model.objects.create(**fields)
                new_id_map[export_id] = obj.id
                
                # Handle ManyToMany
                for field_name, ids in m2m_fields.items():
                    resolved_ids = self.resolve_m2m_ids(
                        model._meta.get_field(field_name).related_model,
                        ids,
                        old_id_map,
                        all_id_maps
                    )
                    getattr(obj, field_name).set(resolved_ids)
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'    ✗ Error creating {model.__name__} (export_id={export_id}): {e}')
                )
                # Continue with next item
        
        return new_id_map

    def is_file_field(self, model, field_name):
        """Check if field is a FileField or ImageField"""
        try:
            field = model._meta.get_field(field_name)
            return hasattr(field, 'upload_to')
        except:
            return False

    def resolve_foreign_key(self, related_model, export_id, reverse_old_map, all_id_maps):
        """Resolve foreign key from export_id to new DB ID"""
        # export_id is the export_id in the JSON
        # all_id_maps maps: export_id -> new_db_id
        
        app_label = related_model._meta.app_label
        model_name = related_model.__name__
        
        if app_label in all_id_maps and model_name in all_id_maps[app_label]:
            if export_id in all_id_maps[app_label][model_name]:
                return all_id_maps[app_label][model_name][export_id]
        
        return None

    def resolve_m2m_ids(self, related_model, export_ids, old_id_map, all_id_maps):
        """Resolve ManyToMany IDs from export_ids to new DB IDs"""
        resolved_ids = []
        app_label = related_model._meta.app_label
        model_name = related_model.__name__
        
        if app_label in all_id_maps and model_name in all_id_maps[app_label]:
            for export_id in export_ids:
                if export_id in all_id_maps[app_label][model_name]:
                    resolved_ids.append(all_id_maps[app_label][model_name][export_id])
        
        return resolved_ids

    def import_media_files(self, file_references, all_id_maps, media_dir):
        """Import media files"""
        copied_count = 0
        
        for file_ref in file_references:
            export_id = file_ref.get('export_id')
            model_path = file_ref.get('model', '')
            field_name = file_ref.get('field', '')
            relative_path = file_ref.get('relative_path', '')
            
            if not model_path or not field_name:
                continue
            
            try:
                app_label, model_name = model_path.split('.')
                
                # Find the new object ID
                if app_label in all_id_maps and model_name in all_id_maps[app_label]:
                    if export_id in all_id_maps[app_label][model_name]:
                        new_obj_id = all_id_maps[app_label][model_name][export_id]
                        
                        # Get the model and object
                        app = apps.get_app_config(app_label)
                        model = app.get_model(model_name)
                        obj = model.objects.get(id=new_obj_id)
                        
                        # Find the file
                        filename = os.path.basename(relative_path)
                        expected_filename = f"{export_id}_{filename}"
                        file_path = os.path.join(media_dir, expected_filename)
                        
                        if not os.path.exists(file_path):
                            # Try without export_id prefix
                            file_path = os.path.join(media_dir, filename)
                        
                        if os.path.exists(file_path):
                            try:
                                with open(file_path, 'rb') as f:
                                    getattr(obj, field_name).save(
                                        filename,
                                        File(f),
                                        save=True
                                    )
                                copied_count += 1
                                self.stdout.write(f'  ✓ Copied: {filename}')
                            except Exception as e:
                                self.stdout.write(self.style.ERROR(
                                    f'  ✗ Failed to copy {filename}: {e}'
                                ))
            except Exception as e:
                pass
        
        if copied_count > 0:
            self.stdout.write(self.style.SUCCESS(
                f'✓ Copied {copied_count} media files'
            ))
