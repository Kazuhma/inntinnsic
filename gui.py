"""
Modern graphical user interface for Inntinnsic Image Safety Checker
Built with CustomTkinter for Windows 11 Fluent Design aesthetics
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import threading
import logging
from datetime import datetime

from config import get_common_locations, APP_NAME, APP_VERSION, DETECTION_THRESHOLD
from scanner import FileScanner
from detector import ImageDetector


# Set appearance and color theme
ctk.set_appearance_mode("light")  # Light mode by default
ctk.set_default_color_theme("blue")  # Will customize colors


class ModernSafetyCheckerApp:
    """Modern UI for Inntinnsic Image Safety Checker"""

    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)

        # Set window icon
        try:
            icon_path = Path(__file__).parent / "icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception:
            pass  # Icon not critical, continue without it

        # Application state
        self.detector = None
        self.scanner = None
        self.scan_paths = []
        self.results = []
        self.is_scanning = False
        self.current_tab = "scan"
        self.active_tooltips = []  # Track all active tooltip windows

        # Settings
        self.sensitivity_var = ctk.StringVar(value="Medium (balanced)")
        self.auto_export_var = ctk.BooleanVar(value=False)
        self.skip_hidden_var = ctk.BooleanVar(value=True)
        self.include_system_var = ctk.BooleanVar(value=False)
        self.confirm_delete_var = ctk.BooleanVar(value=True)

        # Color scheme (Purple/Violet theme from mockup)
        self.colors = {
            'primary': '#7C3AED',      # Purple
            'primary_dark': '#6D28D9',  # Darker purple
            'secondary': '#EC4899',     # Pink accent
            'success': '#10B981',       # Green
            'warning': '#F59E0B',       # Orange
            'danger': '#EF4444',        # Red
            'bg_light': '#F9FAFB',      # Light gray background
            'bg_white': '#FFFFFF',      # White
            'text_dark': '#111827',     # Dark text
            'text_gray': '#6B7280',     # Gray text
            'border': '#E5E7EB',        # Border gray
        }

        self.setup_logging()
        self.create_ui()

    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def create_ui(self):
        """Create the main user interface"""
        # Main container
        self.main_container = ctk.CTkFrame(self.root, fg_color=self.colors['bg_light'])
        self.main_container.pack(fill='both', expand=True)

        # Header with app icon and title
        self.create_header()

        # Tab navigation
        self.create_tab_navigation()

        # Content area (will show different content based on active tab)
        self.content_container = ctk.CTkFrame(
            self.main_container,
            fg_color=self.colors['bg_light']
        )
        self.content_container.pack(fill='both', expand=True, padx=30, pady=20)

        # Footer/Status bar
        self.create_footer()

        # Show scan tab by default
        self.show_scan_tab()

    def create_header(self):
        """Create the header with app title and subtitle"""
        header = ctk.CTkFrame(self.main_container, fg_color=self.colors['bg_white'], height=100)
        header.pack(fill='x', padx=0, pady=0)
        header.pack_propagate(False)

        # App icon placeholder (you can add an icon later)
        icon_label = ctk.CTkLabel(
            header,
            text="🛡️",
            font=ctk.CTkFont(size=32)
        )
        icon_label.pack(side='left', padx=(30, 10), pady=20)

        # Title and subtitle
        title_container = ctk.CTkFrame(header, fg_color='transparent')
        title_container.pack(side='left', fill='y', pady=20)

        title = ctk.CTkLabel(
            title_container,
            text="Image Safety Checker",
            font=ctk.CTkFont(size=28, weight='bold'),
            text_color=self.colors['text_dark']
        )
        title.pack(anchor='w')

        subtitle = ctk.CTkLabel(
            title_container,
            text="Scan your computer for potentially inappropriate images",
            font=ctk.CTkFont(size=13),
            text_color=self.colors['text_gray']
        )
        subtitle.pack(anchor='w')

    def create_tab_navigation(self):
        """Create the tab navigation bar"""
        tab_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=self.colors['bg_light'],
            height=70
        )
        tab_frame.pack(fill='x', padx=30, pady=(10, 0))
        tab_frame.pack_propagate(False)

        # Tab buttons
        self.tab_buttons = {}

        # Scan tab
        scan_btn = self.create_tab_button(
            tab_frame,
            "🔍  Scan",
            "scan",
            lambda: self.switch_tab("scan")
        )
        scan_btn.pack(side='left', padx=(0, 10))
        self.tab_buttons['scan'] = scan_btn

        # Results tab with badge
        results_container = ctk.CTkFrame(tab_frame, fg_color='transparent')
        results_container.pack(side='left', padx=(0, 10))

        results_btn = self.create_tab_button(
            results_container,
            "📋  Results",
            "results",
            lambda: self.switch_tab("results")
        )
        results_btn.pack(side='left')

        # Badge for results count
        self.results_badge = ctk.CTkLabel(
            results_container,
            text="0",
            font=ctk.CTkFont(size=11, weight='bold'),
            text_color='white',
            fg_color=self.colors['danger'],
            width=24,
            height=24,
            corner_radius=12
        )
        self.results_badge.pack(side='left', padx=(5, 0))
        self.results_badge.pack_forget()  # Hide initially

        self.tab_buttons['results'] = results_btn

        # Settings button (on the right side)
        settings_btn = ctk.CTkButton(
            tab_frame,
            text="⚙️  Settings",
            command=lambda: self.switch_tab("settings"),
            fg_color='transparent',
            text_color=self.colors['text_gray'],
            hover_color=self.colors['bg_white'],
            font=ctk.CTkFont(size=18),
            height=45,
            corner_radius=10,
            border_width=0
        )
        settings_btn.pack(side='right')
        self.tab_buttons['settings'] = settings_btn

    def create_tab_button(self, parent, text, tab_id, command):
        """Create a styled tab button"""
        btn = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color='transparent',
            text_color=self.colors['text_gray'],
            hover_color=self.colors['bg_white'],
            font=ctk.CTkFont(size=18, weight='normal'),
            height=45,
            corner_radius=10,
            border_width=0
        )
        return btn

    def switch_tab(self, tab_name):
        """Switch between tabs"""
        self.current_tab = tab_name

        # Update tab button styles
        for tab_id, btn in self.tab_buttons.items():
            if tab_id == tab_name:
                btn.configure(
                    fg_color=self.colors['bg_white'],
                    text_color=self.colors['primary'],
                    font=ctk.CTkFont(size=18, weight='normal', underline=True)
                )
            else:
                btn.configure(
                    fg_color='transparent',
                    text_color=self.colors['text_gray'],
                    font=ctk.CTkFont(size=18, weight='normal', underline=False)
                )

        # Destroy all active tooltips before switching
        self.destroy_all_tooltips()

        # Clear current content
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Show appropriate tab content
        if tab_name == "scan":
            self.show_scan_tab()
        elif tab_name == "results":
            self.show_results_tab()
        elif tab_name == "settings":
            self.show_settings_tab()

    def show_scan_tab(self):
        """Show the scan tab content"""
        # Scan Locations section
        locations_section = ctk.CTkFrame(
            self.content_container,
            fg_color=self.colors['bg_white'],
            corner_radius=15
        )
        locations_section.pack(fill='both', expand=True, pady=(0, 20))

        # Header with title and action buttons
        header_frame = ctk.CTkFrame(locations_section, fg_color='transparent')
        header_frame.pack(fill='x', padx=25, pady=(20, 15))

        # Left side - title
        title_frame = ctk.CTkFrame(header_frame, fg_color='transparent')
        title_frame.pack(side='left', fill='y')

        ctk.CTkLabel(
            title_frame,
            text="Scan Locations",
            font=ctk.CTkFont(size=18, weight='bold'),
            text_color=self.colors['text_dark']
        ).pack(anchor='w')

        self.location_count_label = ctk.CTkLabel(
            title_frame,
            text="0 locations selected",
            font=ctk.CTkFont(size=13),
            text_color=self.colors['text_gray']
        )
        self.location_count_label.pack(anchor='w')

        # Right side - action buttons
        btn_frame = ctk.CTkFrame(header_frame, fg_color='transparent')
        btn_frame.pack(side='right')

        ctk.CTkButton(
            btn_frame,
            text="📁 Add Folder",
            command=self.add_folder,
            fg_color=self.colors['bg_light'],
            text_color=self.colors['text_dark'],
            hover_color=self.colors['border'],
            font=ctk.CTkFont(size=13),
            height=40,
            corner_radius=10,
            border_width=1,
            border_color=self.colors['border']
        ).pack(side='left', padx=5)

        ctk.CTkButton(
            btn_frame,
            text="⚡ Quick Scan",
            command=self.use_common_locations,
            fg_color=self.colors['primary'],
            text_color='white',
            hover_color=self.colors['primary_dark'],
            font=ctk.CTkFont(size=13),
            height=40,
            corner_radius=10
        ).pack(side='left', padx=5)

        # Scrollable frame for path chips
        self.paths_container = ctk.CTkScrollableFrame(
            locations_section,
            fg_color='transparent',
            height=200
        )
        self.paths_container.pack(fill='both', expand=True, padx=25, pady=(0, 15))

        # Repopulate path chips from existing scan_paths
        for path in self.scan_paths:
            self.add_path_chip(path)

        # System directories checkbox
        checkbox_frame = ctk.CTkFrame(locations_section, fg_color='transparent')
        checkbox_frame.pack(fill='x', padx=25, pady=(0, 20))

        self.system_checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="Include system directories and caches",
            variable=self.include_system_var,
            font=ctk.CTkFont(size=14),
            text_color=self.colors['text_dark'],
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_dark'],
            corner_radius=6,
            border_width=2
        )
        self.system_checkbox.pack(anchor='w')

        ctk.CTkLabel(
            checkbox_frame,
            text="More thorough scan, but significantly slower",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_gray']
        ).pack(anchor='w', padx=(30, 0))

        # Bottom section - Ready to scan
        bottom_section = ctk.CTkFrame(
            self.content_container,
            fg_color=self.colors['bg_white'],
            corner_radius=15,
            height=120
        )
        bottom_section.pack(fill='x')
        bottom_section.pack_propagate(False)

        bottom_content = ctk.CTkFrame(bottom_section, fg_color='transparent')
        bottom_content.pack(fill='both', expand=True, padx=25, pady=20)

        # Left side - status text
        status_frame = ctk.CTkFrame(bottom_content, fg_color='transparent')
        status_frame.pack(side='left', fill='y')

        ctk.CTkLabel(
            status_frame,
            text="Scanner",
            font=ctk.CTkFont(size=18, weight='bold'),
            text_color=self.colors['text_dark']
        ).pack(anchor='w')

        self.scan_status_label = ctk.CTkLabel(
            status_frame,
            text="Select locations above to begin",
            font=ctk.CTkFont(size=13),
            text_color=self.colors['text_gray']
        )
        self.scan_status_label.pack(anchor='w')

        # Right side - scan button
        self.start_scan_btn = ctk.CTkButton(
            bottom_content,
            text="▶ Start Scan",
            command=self.start_or_stop_scan,
            fg_color=self.colors['primary'],
            text_color='white',
            hover_color=self.colors['primary_dark'],
            font=ctk.CTkFont(size=15, weight='bold'),
            height=60,
            width=200,
            corner_radius=12,
            state='disabled'
        )
        self.start_scan_btn.pack(side='right')

        # Update button text if scan is in progress (after tab recreation)
        if self.is_scanning:
            self.start_scan_btn.configure(text="⏹️ Stop Scan")

        # Progress bar (hidden initially)
        self.progress_bar = ctk.CTkProgressBar(
            self.content_container,
            progress_color=self.colors['primary'],
            height=8,
            corner_radius=4
        )
        self.progress_bar.set(0)

        # Show progress bar if scan is in progress (after tab recreation)
        if self.is_scanning:
            self.progress_bar.pack(fill='x', pady=(10, 0))

        # Update scan button state based on existing paths
        self.update_scan_ui()

    def show_results_tab(self):
        """Show the results tab content"""
        # Header with title and actions
        header_frame = ctk.CTkFrame(self.content_container, fg_color='transparent')
        header_frame.pack(fill='x', pady=(0, 20))

        # Left side
        title_frame = ctk.CTkFrame(header_frame, fg_color='transparent')
        title_frame.pack(side='left')

        ctk.CTkLabel(
            title_frame,
            text="Flagged Images",
            font=ctk.CTkFont(size=20, weight='bold'),
            text_color=self.colors['text_dark']
        ).pack(anchor='w')

        count_text = f"{len(self.results)} potentially inappropriate images found"
        ctk.CTkLabel(
            title_frame,
            text=count_text,
            font=ctk.CTkFont(size=13),
            text_color=self.colors['text_gray']
        ).pack(anchor='w')

        # Right side - action buttons
        btn_frame = ctk.CTkFrame(header_frame, fg_color='transparent')
        btn_frame.pack(side='right')

        ctk.CTkButton(
            btn_frame,
            text="💾 Export Results",
            command=self.export_results,
            fg_color=self.colors['bg_light'],
            text_color=self.colors['text_dark'],
            hover_color=self.colors['border'],
            font=ctk.CTkFont(size=13),
            height=40,
            corner_radius=10,
            border_width=1,
            border_color=self.colors['border']
        ).pack(side='left', padx=5)

        ctk.CTkButton(
            btn_frame,
            text="🗑️ Clear All",
            command=self.clear_results,
            fg_color=self.colors['bg_light'],
            text_color=self.colors['text_dark'],
            hover_color=self.colors['border'],
            font=ctk.CTkFont(size=13),
            height=40,
            corner_radius=10,
            border_width=1,
            border_color=self.colors['border']
        ).pack(side='left', padx=5)

        # Results list
        results_container = ctk.CTkScrollableFrame(
            self.content_container,
            fg_color=self.colors['bg_white'],
            corner_radius=15
        )
        results_container.pack(fill='both', expand=True)

        if not self.results:
            # Empty state
            empty_frame = ctk.CTkFrame(results_container, fg_color='transparent')
            empty_frame.pack(expand=True, pady=100)

            ctk.CTkLabel(
                empty_frame,
                text="📂",
                font=ctk.CTkFont(size=64)
            ).pack()

            ctk.CTkLabel(
                empty_frame,
                text="No flagged images yet",
                font=ctk.CTkFont(size=18, weight='bold'),
                text_color=self.colors['text_dark']
            ).pack(pady=(10, 5))

            ctk.CTkLabel(
                empty_frame,
                text="Run a scan to find potentially inappropriate images",
                font=ctk.CTkFont(size=13),
                text_color=self.colors['text_gray']
            ).pack()
        else:
            # Display results
            for result in self.results:
                self.create_result_item(results_container, result)

    def create_result_item(self, parent, result):
        """Create a result item card"""
        item_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_light'],
            corner_radius=12,
            height=90
        )
        item_frame.pack(fill='x', padx=15, pady=8)
        item_frame.pack_propagate(False)

        content = ctk.CTkFrame(item_frame, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=15, pady=15)

        # Left side - file info (no thumbnail to avoid creating copies)
        left_side = ctk.CTkFrame(content, fg_color='transparent')
        left_side.pack(side='left', fill='y')

        # File info
        info_frame = ctk.CTkFrame(left_side, fg_color='transparent')
        info_frame.pack(side='left', fill='y')

        filename = Path(result['path']).name
        ctk.CTkLabel(
            info_frame,
            text=filename,
            font=ctk.CTkFont(size=14, weight='bold'),
            text_color=self.colors['text_dark']
        ).pack(anchor='w')

        ctk.CTkLabel(
            info_frame,
            text=str(result['path']),
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_gray']
        ).pack(anchor='w')

        # Right side - confidence badge and actions
        right_side = ctk.CTkFrame(content, fg_color='transparent')
        right_side.pack(side='right', fill='y')

        # Confidence badge with tooltip
        if result['detections']:
            max_confidence = max(d['confidence'] for d in result['detections'])
            confidence_pct = int(max_confidence * 100)

            # Color based on confidence
            if confidence_pct >= 80:
                badge_color = self.colors['danger']
            elif confidence_pct >= 60:
                badge_color = self.colors['warning']
            else:
                badge_color = self.colors['text_gray']

            badge = ctk.CTkLabel(
                right_side,
                text=f"{confidence_pct}% match",
                font=ctk.CTkFont(size=12, weight='bold'),
                text_color='white',
                fg_color=badge_color,
                corner_radius=8,
                padx=12,
                pady=6
            )
            badge.pack(side='left', padx=5)

        # Action buttons (placeholders)
        action_frame = ctk.CTkFrame(right_side, fg_color='transparent')
        action_frame.pack(side='left', padx=(10, 0))

        # View button
        view_btn = ctk.CTkButton(
            action_frame,
            text="👁️",
            width=38,
            height=38,
            corner_radius=8,
            fg_color='transparent',
            text_color=self.colors['text_gray'],
            hover_color=self.colors['bg_light'],
            font=ctk.CTkFont(size=18),
            command=lambda: self.view_image(result['path'])
        )
        view_btn.pack(side='left', padx=1)

        # Open folder button
        folder_btn = ctk.CTkButton(
            action_frame,
            text="📁",
            width=38,
            height=38,
            corner_radius=8,
            fg_color='transparent',
            text_color=self.colors['text_gray'],
            hover_color=self.colors['bg_light'],
            font=ctk.CTkFont(size=18),
            command=lambda: self.open_folder(result['path'])
        )
        folder_btn.pack(side='left', padx=1)

        # Delete button
        delete_btn = ctk.CTkButton(
            action_frame,
            text="🗑️",
            width=38,
            height=38,
            corner_radius=8,
            fg_color='transparent',
            text_color=self.colors['text_gray'],
            hover_color=self.colors['bg_light'],
            font=ctk.CTkFont(size=18),
            command=lambda: self.delete_image(result['path'])
        )
        delete_btn.pack(side='left', padx=1)

        # Ignore button (remove from list)
        ignore_btn = ctk.CTkButton(
            action_frame,
            text="✓",
            width=38,
            height=38,
            corner_radius=8,
            fg_color='transparent',
            text_color=self.colors['text_gray'],
            hover_color=self.colors['bg_light'],
            font=ctk.CTkFont(size=18),
            command=lambda: self.ignore_result(result['path'])
        )
        ignore_btn.pack(side='left', padx=1)

    def show_settings_tab(self):
        """Show the settings tab content"""
        settings_container = ctk.CTkFrame(
            self.content_container,
            fg_color=self.colors['bg_white'],
            corner_radius=15
        )
        settings_container.pack(fill='both', expand=True)

        # Title
        ctk.CTkLabel(
            settings_container,
            text="Scan Settings",
            font=ctk.CTkFont(size=20, weight='bold'),
            text_color=self.colors['text_dark']
        ).pack(anchor='w', padx=30, pady=(30, 20))

        # Detection Sensitivity
        self.create_setting_row(
            settings_container,
            "Detection Sensitivity",
            "Higher values may increase false positives",
            "combobox",
            {
                'values': ["Low (strict)", "Medium (balanced)", "High (sensitive)"],
                'variable': self.sensitivity_var,
            }
        )

        # Auto-export results
        self.create_setting_row(
            settings_container,
            "Auto-export results",
            "Automatically save scan results to a file",
            "switch",
            {'variable': self.auto_export_var}
        )

        # Skip hidden files
        self.create_setting_row(
            settings_container,
            "Skip hidden files",
            "Exclude hidden system files from scan",
            "switch",
            {'variable': self.skip_hidden_var}
        )

        # Confirm file deletions
        self.create_setting_row(
            settings_container,
            "Confirm file deletions",
            "Ask for confirmation before deleting flagged images",
            "switch",
            {'variable': self.confirm_delete_var}
        )

    def create_setting_row(self, parent, title, description, control_type, control_config):
        """Create a settings row with title, description, and control"""
        row_frame = ctk.CTkFrame(parent, fg_color='transparent', height=80)
        row_frame.pack(fill='x', padx=30, pady=10)
        row_frame.pack_propagate(False)

        # Left side - text
        text_frame = ctk.CTkFrame(row_frame, fg_color='transparent')
        text_frame.pack(side='left', fill='y', anchor='w')

        ctk.CTkLabel(
            text_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight='bold'),
            text_color=self.colors['text_dark']
        ).pack(anchor='w')

        ctk.CTkLabel(
            text_frame,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_gray']
        ).pack(anchor='w')

        # Right side - control
        if control_type == "combobox":
            control = ctk.CTkComboBox(
                row_frame,
                values=control_config.get('values', []),
                variable=control_config.get('variable'),
                font=ctk.CTkFont(size=13),
                dropdown_font=ctk.CTkFont(size=12),
                width=200,
                height=40,
                corner_radius=8,
                border_width=1,
                button_color=self.colors['primary'],
                button_hover_color=self.colors['primary_dark']
            )
            control.pack(side='right', anchor='e')
        elif control_type == "switch":
            control = ctk.CTkSwitch(
                row_frame,
                text="",
                variable=control_config.get('variable'),
                fg_color=self.colors['border'],
                progress_color=self.colors['primary'],
                button_color='white',
                button_hover_color=self.colors['bg_light']
            )
            control.pack(side='right', anchor='e')

    def create_footer(self):
        """Create the footer/status bar"""
        footer = ctk.CTkFrame(
            self.main_container,
            fg_color=self.colors['bg_white'],
            height=40
        )
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)

        self.status_label = ctk.CTkLabel(
            footer,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_gray']
        )
        self.status_label.pack(side='left', padx=30)

        self.last_scan_label = ctk.CTkLabel(
            footer,
            text="Last scan: Never",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_gray']
        )
        self.last_scan_label.pack(side='right', padx=30)

    def add_folder(self):
        """Add a folder to scan list"""
        folder = filedialog.askdirectory(title="Select Folder to Scan")
        if folder:
            if folder not in self.scan_paths:
                self.scan_paths.append(folder)
                self.add_path_chip(folder)
                self.update_scan_ui()

    def select_drive(self):
        """Allow user to select a drive"""
        scanner = FileScanner()
        drives = scanner.get_available_drives()

        if not drives:
            messagebox.showerror("Error", "No drives detected")
            return

        # Create dialog for drive selection
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Select Drive")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Select a drive to scan:",
            font=ctk.CTkFont(size=14, weight='bold')
        ).pack(pady=20)

        ctk.CTkLabel(
            dialog,
            text="⚠️ Scanning entire drives may take considerable time",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['warning']
        ).pack(pady=10)

        # Drive list
        for drive in drives:
            btn = ctk.CTkButton(
                dialog,
                text=drive,
                command=lambda d=drive: self.add_drive_and_close(d, dialog),
                height=40,
                font=ctk.CTkFont(size=13)
            )
            btn.pack(pady=5, padx=20, fill='x')

    def add_drive_and_close(self, drive, dialog):
        """Add drive to scan list and close dialog"""
        if drive not in self.scan_paths:
            self.scan_paths.append(drive)
            self.add_path_chip(drive)
            self.update_scan_ui()
        dialog.destroy()

    def use_common_locations(self):
        """Add common locations to scan list"""
        locations = get_common_locations()
        added_count = 0

        for category, paths in locations.items():
            for path in paths:
                if path.exists() and str(path) not in self.scan_paths:
                    self.scan_paths.append(str(path))
                    self.add_path_chip(str(path))
                    added_count += 1

        if added_count > 0:
            self.update_scan_ui()

    def add_path_chip(self, path):
        """Add a path chip to the UI"""
        chip_frame = ctk.CTkFrame(
            self.paths_container,
            fg_color=self.colors['bg_light'],
            corner_radius=10,
            height=50
        )
        chip_frame.pack(fill='x', pady=5)
        chip_frame.pack_propagate(False)

        content = ctk.CTkFrame(chip_frame, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=15, pady=10)

        # Folder icon and path
        ctk.CTkLabel(
            content,
            text="📁",
            font=ctk.CTkFont(size=18)
        ).pack(side='left', padx=(0, 10))

        ctk.CTkLabel(
            content,
            text=path,
            font=ctk.CTkFont(size=13),
            text_color=self.colors['text_dark']
        ).pack(side='left')

        # Remove button
        remove_btn = ctk.CTkButton(
            content,
            text="✕",
            width=30,
            height=30,
            corner_radius=15,
            fg_color='transparent',
            text_color=self.colors['text_gray'],
            hover_color=self.colors['danger'],
            hover=True,
            command=lambda: self.remove_path(path, chip_frame)
        )
        remove_btn.pack(side='right')

    def remove_path(self, path, chip_frame):
        """Remove a path from scan list"""
        if path in self.scan_paths:
            self.scan_paths.remove(path)
        chip_frame.destroy()
        self.update_scan_ui()

    def update_scan_ui(self):
        """Update UI elements based on scan paths"""
        count = len(self.scan_paths)
        self.location_count_label.configure(
            text=f"{count} location{'s' if count != 1 else ''} selected"
        )

        if count > 0:
            self.start_scan_btn.configure(state='normal')
        else:
            self.start_scan_btn.configure(state='disabled')

    def start_or_stop_scan(self):
        """Toggle between starting and stopping scan"""
        if self.is_scanning:
            self.stop_scan()
        else:
            self.start_scan()

    def start_scan(self):
        """Start the scanning process"""
        if not self.scan_paths:
            messagebox.showwarning("No Paths", "Please add folders or drives to scan")
            return

        # Clear previous results
        self.results = []
        self.update_results_badge()

        # Confirm scanning entire drives
        for path in self.scan_paths:
            if len(path) <= 3 and ':' in path:
                response = messagebox.askyesno(
                    "Scan Entire Drive?",
                    f"You are about to scan the entire {path} drive.\n\n"
                    "This may take a very long time.\n\nContinue?",
                    icon='warning'
                )
                if not response:
                    return
                break

        # Update UI
        self.is_scanning = True
        self.start_scan_btn.configure(text="⏹️ Stop Scan")
        self.scan_status_label.configure(text="Scanning...")

        # Show progress bar
        self.progress_bar.pack(fill='x', pady=(10, 0))

        # Run scan in separate thread
        scan_thread = threading.Thread(target=self.run_scan, daemon=True)
        scan_thread.start()

    def stop_scan(self):
        """Stop the current scan"""
        if self.scanner:
            self.scanner.stop()
        self.is_scanning = False
        self.start_scan_btn.configure(text="▶ Start Scan")
        self.scan_status_label.configure(text="Scan stopped")
        self.progress_bar.pack_forget()

    def run_scan(self):
        """Execute the scan (runs in separate thread)"""
        try:
            # Initialize detector if needed
            # Convert sensitivity setting to threshold
            sensitivity = self.sensitivity_var.get()
            if "Low" in sensitivity:
                threshold = 0.8  # Strict - only very confident detections
            elif "High" in sensitivity:
                threshold = 0.4  # Sensitive - more detections, more false positives
            else:  # Medium
                threshold = 0.6  # Balanced default

            if not self.detector:
                self.update_status("Loading AI model...")
                self.detector = ImageDetector(threshold)
            else:
                # Update threshold for existing detector
                self.detector.threshold = threshold

            # Initialize scanner
            self.scanner = FileScanner(self.update_status)

            # Apply skip hidden files setting
            self.scanner.skip_hidden = self.skip_hidden_var.get()

            # Find images
            self.update_status("Scanning for images...")
            include_system = self.include_system_var.get()
            image_files = self.scanner.find_images(self.scan_paths, include_system)

            if not image_files:
                self.update_status("Scan complete - no images found")
                self.show_completion_message(0, 0)
                return

            self.update_status(f"Found {len(image_files)} images. Analyzing...")

            # Analyze images
            flagged_count = 0

            def progress_callback(current, total, result):
                nonlocal flagged_count

                # Check if scan was stopped
                if not self.is_scanning:
                    raise InterruptedError("Scan stopped by user")

                if result['flagged']:
                    flagged_count += 1
                    self.results.append(result)
                    self.update_results_badge()

                # Update progress
                progress = current / total
                self.root.after(0, lambda: self.progress_bar.set(progress))
                self.update_status(
                    f"Analyzed {current}/{total} images | Flagged: {flagged_count}"
                )

            self.detector.batch_analyze(image_files, progress_callback)

            # Complete
            self.update_status(f"Scan complete! {flagged_count}/{len(image_files)} images flagged")
            self.last_scan_label.configure(text=f"Last scan: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

            # Auto-export results if enabled
            if self.auto_export_var.get() and flagged_count > 0:
                self.export_results()

            # Play system sound
            try:
                import winsound
                winsound.MessageBeep(winsound.MB_OK)
            except:
                pass

        except InterruptedError:
            # Scan was stopped by user - this is expected
            self.update_status("Scan stopped by user")
            logging.info("Scan stopped by user")

        except Exception as e:
            logging.error(f"Scan error: {e}", exc_info=True)
            self.update_status(f"Error during scan: {e}")
            messagebox.showerror("Scan Error", f"An error occurred:\n\n{e}")

        finally:
            self.is_scanning = False
            self.root.after(0, lambda: self.start_scan_btn.configure(text="▶ Start Scan"))
            self.root.after(0, lambda: self.scan_status_label.configure(text="Ready to scan"))

    def update_status(self, message):
        """Update status label (thread-safe)"""
        self.root.after(0, lambda: self.status_label.configure(text=message))

    def update_results_badge(self):
        """Update the results tab badge"""
        count = len(self.results)
        if count > 0:
            self.root.after(0, lambda: self.results_badge.configure(text=str(count)))
            self.root.after(0, lambda: self.results_badge.pack(side='left', padx=(5, 0)))
        else:
            self.root.after(0, lambda: self.results_badge.pack_forget())

    def export_results(self):
        """Export results to file"""
        if not self.results:
            messagebox.showinfo("No Results", "No results to export")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"inntinnsic_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"{APP_NAME} - Scan Results\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("="*80 + "\n\n")

                    for result in self.results:
                        f.write(f"\nFile: {result['path']}\n")
                        for detection in result['detections']:
                            category = detection['category'].replace('_', ' ').title()
                            confidence = detection['confidence'] * 100
                            f.write(f"  - {category}: {confidence:.1f}% confidence\n")
                        f.write("\n")

                # Export successful - no confirmation message needed
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export results:\n{e}")

    def clear_results(self):
        """Clear all results"""
        if self.results:
            response = messagebox.askyesno(
                "Clear Results",
                "Are you sure you want to clear all results?"
            )
            if response:
                self.results = []
                self.update_results_badge()
                self.switch_tab("results")  # Properly refresh the view

    def create_tooltip(self, widget, text):
        """Create a tooltip that shows on hover"""
        tooltip = None

        def show_tooltip(event):
            nonlocal tooltip
            if tooltip:
                return

            # Destroy all existing tooltips first to prevent stickiness
            self.destroy_all_tooltips()

            # Create tooltip window
            tooltip = ctk.CTkToplevel(self.root)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_attributes("-topmost", True)

            # Track this tooltip
            self.active_tooltips.append(tooltip)

            # Position tooltip near mouse
            x = event.x_root + 10
            y = event.y_root + 10
            tooltip.wm_geometry(f"+{x}+{y}")

            # Create tooltip content
            label = ctk.CTkLabel(
                tooltip,
                text=text,
                fg_color=self.colors['text_dark'],
                text_color='white',
                corner_radius=6,
                padx=10,
                pady=6,
                font=ctk.CTkFont(size=11)
            )
            label.pack()

        def hide_tooltip(event):
            nonlocal tooltip
            if tooltip:
                try:
                    tooltip.destroy()
                    if tooltip in self.active_tooltips:
                        self.active_tooltips.remove(tooltip)
                except:
                    pass
                tooltip = None

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def destroy_all_tooltips(self):
        """Destroy all active tooltip windows"""
        for tooltip in self.active_tooltips[:]:  # Copy list to avoid modification during iteration
            try:
                tooltip.destroy()
            except:
                pass
        self.active_tooltips.clear()

    # Result action methods
    def ignore_result(self, path):
        """Remove result from the list without confirmation"""
        # Remove from results list
        self.results = [r for r in self.results if r['path'] != path]

        # Update badge count
        self.update_results_badge()

        # Refresh the results view
        self.switch_tab("results")

    def delete_image(self, path):
        """Delete the image file from disk"""
        import os
        from pathlib import Path

        # Check if confirmation is needed
        if self.confirm_delete_var.get():
            response = messagebox.askyesno(
                "Delete File?",
                f"Are you sure you want to permanently delete this file?\n\n{Path(path).name}\n\nThis action cannot be undone.",
                icon='warning'
            )
            if not response:
                return

        # Try to delete the file
        try:
            os.remove(path)
            logging.info(f"Deleted file: {path}")

            # Remove from results list
            self.results = [r for r in self.results if r['path'] != path]

            # Update badge count
            self.update_results_badge()

            # Refresh the results view
            self.switch_tab("results")

            # No success message needed - confirmation dialog was already shown if enabled

        except Exception as e:
            logging.error(f"Failed to delete file {path}: {e}")
            messagebox.showerror("Delete Failed", f"Could not delete file:\n\n{str(e)}")

    def open_folder(self, path):
        """Open the folder containing the image in Windows Explorer"""
        import subprocess
        from pathlib import Path

        try:
            folder_path = Path(path).parent
            # Use Windows explorer to open and select the file
            subprocess.run(['explorer', '/select,', str(path)])
        except Exception as e:
            logging.error(f"Failed to open folder for {path}: {e}")
            messagebox.showerror("Error", f"Could not open folder:\n\n{str(e)}")

    def view_image(self, path):
        """View image in a modal dialog with detection bounding boxes"""
        from pathlib import Path

        # Check if file exists
        if not Path(path).exists():
            messagebox.showerror("File Not Found", f"The image file no longer exists:\n\n{path}")
            # Remove from results
            self.results = [r for r in self.results if r['path'] != path]
            self.update_results_badge()
            self.switch_tab("results")
            return

        # Find the result data for this image to get detections
        result_data = None
        for result in self.results:
            if result['path'] == path:
                result_data = result
                break

        # Load image first to get dimensions for modal sizing
        from PIL import Image
        try:
            img = Image.open(path)
            original_width, original_height = img.size
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
            return

        # Calculate modal size based on image (max 1200px on long side)
        max_dimension = 1200
        longest_side = max(original_width, original_height)

        if longest_side > max_dimension:
            scale = max_dimension / longest_side
            display_width = int(original_width * scale)
            display_height = int(original_height * scale)
        else:
            display_width = original_width
            display_height = original_height

        # Add padding for header (50px), margins (20px), and footer text (40px)
        modal_width = display_width + 0
        modal_height = display_height + 40

        # Create modal dialog
        modal = ctk.CTkToplevel(self.root)

        # Remove window decorations (no title bar)
        modal.wm_overrideredirect(True)

        # Make it modal
        modal.transient(self.root)
        modal.grab_set()
        modal.wm_attributes("-topmost", True)

        # Center on screen
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (modal_width // 2)
        y = (modal.winfo_screenheight() // 2) - (modal_height // 2)
        modal.geometry(f"{modal_width}x{modal_height}+{x}+{y}")

        # Give focus to modal for keyboard events
        modal.focus_set()

        # Bind Escape key to close
        modal.bind("<Escape>", lambda e: modal.destroy())

        # Make window draggable by tracking mouse position
        def start_move(event):
            modal.x = event.x
            modal.y = event.y

        def do_move(event):
            deltax = event.x - modal.x
            deltay = event.y - modal.y
            x = modal.winfo_x() + deltax
            y = modal.winfo_y() + deltay
            modal.geometry(f"+{x}+{y}")

        # Create container
        container = ctk.CTkFrame(modal, fg_color=self.colors['bg_light'])
        container.pack(fill='both', expand=True)

        # Header with filename and close button (draggable)
        header = ctk.CTkFrame(container, fg_color=self.colors['bg_white'], height=60)
        header.pack(fill='x', padx=20, pady=20)
        header.pack_propagate(False)

        # Make header draggable
        header.bind("<Button-1>", start_move)
        header.bind("<B1-Motion>", do_move)

        ctk.CTkLabel(
            header,
            text=Path(path).name,
            font=ctk.CTkFont(size=16, weight='bold'),
            text_color=self.colors['text_dark']
        ).pack(side='left', padx=15, pady=15)

        close_btn = ctk.CTkButton(
            header,
            text="✕",
            width=30,
            height=30,
            corner_radius=20,
            fg_color=self.colors['bg_light'],
            text_color=self.colors['text_gray'],
            hover_color=self.colors['danger'],
            font=ctk.CTkFont(size=18),
            command=modal.destroy
        )
        close_btn.pack(side='right', padx=15)

        # Image display area
        image_frame = ctk.CTkFrame(container, fg_color=self.colors['bg_white'])
        image_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        try:
            from PIL import ImageTk, ImageDraw, ImageFont

            # Calculate scaling first - scale down images larger than 1200px on the long side
            max_dimension = 1200
            longest_side = max(original_width, original_height)

            # Determine scale factor
            if longest_side > max_dimension:
                scale_factor = max_dimension / longest_side
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                scale_factor = 1.0

            # Draw bounding boxes AFTER scaling, so font stays readable
            if result_data and result_data.get('detections'):
                # Create a drawing context
                draw = ImageDraw.Draw(img)

                # Draw each detection bounding box
                for detection in result_data['detections']:
                    if 'bbox' in detection and detection['bbox']:
                        bbox = detection['bbox']
                        # bbox format is [x, y, width, height] - scale coordinates
                        x, y, w, h = bbox

                        # Scale bounding box coordinates
                        x = int(x * scale_factor)
                        y = int(y * scale_factor)
                        w = int(w * scale_factor)
                        h = int(h * scale_factor)

                        # Draw rectangle
                        draw.rectangle(
                            [x, y, x + w, y + h],
                            outline='#EF4444',  # Red color
                            width=4
                        )

                        # Prepare label text
                        category = detection['category'].replace('_', ' ').title()
                        confidence = int(detection['confidence'] * 100)
                        label_text = f"{confidence}% {category}"

                        # Draw label background with fixed font size
                        try:
                            font = ImageFont.truetype("arial.ttf", 16)
                        except:
                            font = ImageFont.load_default()

                        # Get text bounding box
                        text_bbox = draw.textbbox((x, y - 25), label_text, font=font)
                        text_width = text_bbox[2] - text_bbox[0]
                        text_height = text_bbox[3] - text_bbox[1]

                        # Draw background rectangle for text
                        draw.rectangle(
                            [x, y - 25, x + text_width + 10, y - 25 + text_height + 6],
                            fill='#EF4444'
                        )

                        # Draw text
                        draw.text((x + 5, y - 23), label_text, fill='white', font=font)

            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)

            # Display image
            image_label = ctk.CTkLabel(image_frame, text="", image=photo)
            image_label.image = photo  # Keep a reference
            image_label.pack(expand=True)

        except Exception as e:
            logging.error(f"Failed to load image {path}: {e}")
            ctk.CTkLabel(
                image_frame,
                text=f"Error loading image:\n{str(e)}",
                font=ctk.CTkFont(size=14),
                text_color=self.colors['danger']
            ).pack(expand=True)

        # Image info (resolution and path)
        info_container = ctk.CTkFrame(container, fg_color='transparent')
        info_container.pack(pady=(0, 15))

        # Image resolution
        resolution_label = ctk.CTkLabel(
            info_container,
            text=f"Size: {original_width} x {original_height}",
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_gray']
        )
        resolution_label.pack()

        # File path
        path_label = ctk.CTkLabel(
            info_container,
            text=str(path),
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_gray']
        )
        path_label.pack()


def main():
    """Main entry point for the GUI application"""
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    app = ModernSafetyCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
