"""
Graphical user interface for Inntinnsic Image Safety Checker
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import os
import logging
from datetime import datetime

from config import get_common_locations, APP_NAME, APP_VERSION
from scanner import FileScanner
from detector import ImageDetector


class SafetyCheckerApp:
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title(f"{APP_NAME} - Image Safety Checker v{APP_VERSION}")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # Application state
        self.detector = None
        self.scanner = None
        self.scan_paths = []
        self.results = []
        self.is_scanning = False

        # Create UI
        self.create_widgets()
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for the application"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def create_widgets(self):
        """Create all UI widgets"""
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill='both', expand=True)

        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill='x', pady=(0, 10))

        header = ttk.Label(
            header_frame,
            text=f"{APP_NAME} - Image Safety Checker",
            font=('Arial', 16, 'bold')
        )
        header.pack()

        subtitle = ttk.Label(
            header_frame,
            text="Scan your computer for potentially inappropriate images",
            font=('Arial', 9)
        )
        subtitle.pack()

        # Path selection frame
        path_frame = ttk.LabelFrame(main_container, text="Scan Locations", padding=10)
        path_frame.pack(fill='both', expand=True, pady=(0, 10))

        # Button frame
        btn_frame = ttk.Frame(path_frame)
        btn_frame.pack(fill='x', pady=(0, 5))

        ttk.Button(
            btn_frame,
            text="📁 Add Folder",
            command=self.add_folder
        ).pack(side='left', padx=2)

        ttk.Button(
            btn_frame,
            text="💾 Select Drive",
            command=self.select_drive
        ).pack(side='left', padx=2)

        ttk.Button(
            btn_frame,
            text="⚡ Quick Scan (Common Locations)",
            command=self.use_common_locations
        ).pack(side='left', padx=2)

        ttk.Button(
            btn_frame,
            text="🗑️ Clear All",
            command=self.clear_paths
        ).pack(side='left', padx=2)

        # Path listbox with scrollbar
        list_frame = ttk.Frame(path_frame)
        list_frame.pack(fill='both', expand=True, pady=5)

        list_scroll = ttk.Scrollbar(list_frame)
        list_scroll.pack(side='right', fill='y')

        self.path_listbox = tk.Listbox(
            list_frame,
            height=6,
            yscrollcommand=list_scroll.set,
            selectmode='extended'
        )
        self.path_listbox.pack(fill='both', expand=True, side='left')
        list_scroll.config(command=self.path_listbox.yview)

        # Remove selected path button
        ttk.Button(
            path_frame,
            text="Remove Selected",
            command=self.remove_selected_paths
        ).pack(anchor='e')

        # Options frame
        options_frame = ttk.LabelFrame(main_container, text="Scan Options", padding=10)
        options_frame.pack(fill='x', pady=(0, 10))

        self.include_system_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame,
            text="Include system directories and caches (slower but more thorough)",
            variable=self.include_system_var
        ).pack(anchor='w')

        # Scan control frame
        control_frame = ttk.Frame(main_container)
        control_frame.pack(fill='x', pady=(0, 10))

        self.scan_btn = ttk.Button(
            control_frame,
            text="🔍 Start Scan",
            command=self.start_scan,
            state='disabled',
            style='Accent.TButton'
        )
        self.scan_btn.pack(side='left', padx=5)

        self.stop_btn = ttk.Button(
            control_frame,
            text="⏹️ Stop Scan",
            command=self.stop_scan,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=5)

        # Progress frame
        progress_frame = ttk.LabelFrame(main_container, text="Progress", padding=10)
        progress_frame.pack(fill='x', pady=(0, 10))

        self.progress_label = ttk.Label(
            progress_frame,
            text="Ready to scan. Select locations above.",
            font=('Arial', 9)
        )
        self.progress_label.pack(fill='x')

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=700
        )
        self.progress_bar.pack(fill='x', pady=5)

        # Results frame
        results_frame = ttk.LabelFrame(main_container, text="Flagged Images", padding=10)
        results_frame.pack(fill='both', expand=True)

        # Results toolbar
        results_toolbar = ttk.Frame(results_frame)
        results_toolbar.pack(fill='x', pady=(0, 5))

        ttk.Button(
            results_toolbar,
            text="💾 Export Results",
            command=self.export_results
        ).pack(side='left', padx=2)

        ttk.Button(
            results_toolbar,
            text="🗑️ Clear Results",
            command=self.clear_results
        ).pack(side='left', padx=2)

        self.flagged_count_label = ttk.Label(
            results_toolbar,
            text="No flagged images",
            font=('Arial', 9, 'bold')
        )
        self.flagged_count_label.pack(side='right')

        # Results text with scrollbar
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=15,
            wrap=tk.WORD,
            font=('Consolas', 9)
        )
        self.results_text.pack(fill='both', expand=True)

        # Configure text tags for colored output
        self.results_text.tag_config('warning', foreground='#d97706', font=('Consolas', 9, 'bold'))
        self.results_text.tag_config('path', foreground='#2563eb')
        self.results_text.tag_config('category', foreground='#dc2626')
        self.results_text.tag_config('info', foreground='#059669')

    def add_folder(self):
        """Add a folder to the scan list"""
        folder = filedialog.askdirectory(title="Select Folder to Scan")
        if folder:
            if folder not in self.scan_paths:
                self.scan_paths.append(folder)
                self.path_listbox.insert(tk.END, folder)
                self.scan_btn.config(state='normal')
            else:
                messagebox.showinfo("Already Added", "This folder is already in the scan list.")

    def select_drive(self):
        """Allow user to select a drive to scan"""
        scanner = FileScanner()
        drives = scanner.get_available_drives()

        if not drives:
            messagebox.showerror("Error", "No drives detected")
            return

        # Create drive selection dialog
        drive_dialog = tk.Toplevel(self.root)
        drive_dialog.title("Select Drive to Scan")
        drive_dialog.geometry("300x250")
        drive_dialog.transient(self.root)
        drive_dialog.grab_set()

        ttk.Label(
            drive_dialog,
            text="Select a drive to scan:",
            font=('Arial', 10, 'bold')
        ).pack(pady=10)

        ttk.Label(
            drive_dialog,
            text="⚠️ Scanning entire drives may take considerable time",
            font=('Arial', 8),
            foreground='#d97706'
        ).pack(pady=5)

        drive_listbox = tk.Listbox(drive_dialog, height=len(drives))
        drive_listbox.pack(fill='both', expand=True, padx=10, pady=5)

        for drive in drives:
            drive_listbox.insert(tk.END, drive)

        def on_select():
            selection = drive_listbox.curselection()
            if selection:
                selected_drive = drives[selection[0]]
                if selected_drive not in self.scan_paths:
                    self.scan_paths.append(selected_drive)
                    self.path_listbox.insert(tk.END, selected_drive)
                    self.scan_btn.config(state='normal')
                drive_dialog.destroy()

        ttk.Button(drive_dialog, text="Add Drive", command=on_select).pack(pady=10)

    def use_common_locations(self):
        """Add common user locations to scan list"""
        locations = get_common_locations()
        added_count = 0

        for category, paths in locations.items():
            for path in paths:
                if path.exists() and str(path) not in self.scan_paths:
                    self.scan_paths.append(str(path))
                    self.path_listbox.insert(tk.END, f"{path} ({category})")
                    added_count += 1

        if added_count > 0:
            self.scan_btn.config(state='normal')
            messagebox.showinfo(
                "Locations Added",
                f"Added {added_count} common locations to scan list."
            )
        else:
            messagebox.showinfo(
                "No New Locations",
                "All common locations are already in the scan list or don't exist."
            )

    def remove_selected_paths(self):
        """Remove selected paths from the scan list"""
        selection = self.path_listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select paths to remove")
            return

        # Remove in reverse order to maintain indices
        for index in reversed(selection):
            self.scan_paths.pop(index)
            self.path_listbox.delete(index)

        if not self.scan_paths:
            self.scan_btn.config(state='disabled')

    def clear_paths(self):
        """Clear all paths from the scan list"""
        self.scan_paths = []
        self.path_listbox.delete(0, tk.END)
        self.scan_btn.config(state='disabled')

    def clear_results(self):
        """Clear the results display"""
        self.results_text.delete('1.0', tk.END)
        self.results = []
        self.flagged_count_label.config(text="No flagged images")

    def start_scan(self):
        """Start the scanning process"""
        if self.is_scanning:
            messagebox.showwarning("Scan in Progress", "A scan is already running")
            return

        if not self.scan_paths:
            messagebox.showwarning("No Paths", "Please add folders or drives to scan")
            return

        # Confirm if scanning entire drives
        for path in self.scan_paths:
            if len(path) <= 3 and ':' in path:  # Likely a drive like C:\
                response = messagebox.askyesno(
                    "Scan Entire Drive?",
                    f"You are about to scan the entire {path} drive.\n\n"
                    "This may take a very long time and consume significant resources.\n\n"
                    "Continue?",
                    icon='warning'
                )
                if not response:
                    return
                break

        # Reset state
        self.clear_results()
        self.is_scanning = True
        self.scan_btn.config(state='disabled')
        self.stop_btn.config(state='normal')

        # Run scan in separate thread
        scan_thread = threading.Thread(target=self.run_scan, daemon=True)
        scan_thread.start()

    def stop_scan(self):
        """Stop the current scan"""
        if self.scanner:
            self.scanner.stop()
        self.update_progress("⏹️ Stopping scan...")
        self.stop_btn.config(state='disabled')

    def run_scan(self):
        """Execute the scan (runs in separate thread)"""
        try:
            # Initialize detector if needed
            if not self.detector:
                self.update_progress("🔄 Loading AI model (first time only)...")
                self.detector = ImageDetector()

            # Initialize scanner
            self.scanner = FileScanner(self.update_progress)

            # Find images
            self.update_progress("🔍 Scanning for images...")
            include_system = self.include_system_var.get()
            image_files = self.scanner.find_images(self.scan_paths, include_system)

            if not image_files:
                self.update_progress("✓ Scan complete - no images found")
                self.show_completion_message(0, 0)
                return

            self.update_progress(f"📊 Found {len(image_files)} images. Analyzing...")

            # Analyze images
            flagged_count = 0

            def progress_callback(current, total, result):
                nonlocal flagged_count
                if result['flagged']:
                    flagged_count += 1
                    self.add_result(result)

                self.progress_bar.config(maximum=total, value=current)
                self.update_progress(
                    f"🔎 Analyzed {current}/{total} images | Flagged: {flagged_count}"
                )

            self.detector.batch_analyze(image_files, progress_callback)

            # Complete
            self.update_progress(
                f"✅ Scan complete! {flagged_count}/{len(image_files)} images flagged"
            )
            self.show_completion_message(flagged_count, len(image_files))

        except Exception as e:
            logging.error(f"Scan error: {e}", exc_info=True)
            self.update_progress(f"❌ Error during scan: {e}")
            messagebox.showerror("Scan Error", f"An error occurred:\n\n{e}")

        finally:
            self.is_scanning = False
            self.root.after(0, lambda: self.scan_btn.config(state='normal'))
            self.root.after(0, lambda: self.stop_btn.config(state='disabled'))

    def show_completion_message(self, flagged, total):
        """Show completion dialog"""
        self.root.after(0, lambda: messagebox.showinfo(
            "Scan Complete",
            f"Scan finished!\n\n"
            f"Total images scanned: {total}\n"
            f"Flagged images: {flagged}\n"
            f"Clean images: {total - flagged}"
        ))

    def update_progress(self, message):
        """Update progress label (thread-safe)"""
        self.root.after(0, lambda: self.progress_label.config(text=message))

    def add_result(self, result):
        """Add flagged result to text widget (thread-safe)"""
        def _add():
            self.results.append(result)

            # Add separator
            self.results_text.insert(tk.END, "\n" + "="*80 + "\n")

            # Add warning icon and path
            self.results_text.insert(tk.END, "⚠️  ", 'warning')
            self.results_text.insert(tk.END, f"{result['path']}\n", 'path')

            # Add detection details
            for detection in result['detections']:
                category = detection['category'].replace('_', ' ').title()
                confidence = detection['confidence'] * 100
                self.results_text.insert(tk.END, f"   • ", 'info')
                self.results_text.insert(tk.END, f"{category}", 'category')
                self.results_text.insert(tk.END, f": {confidence:.1f}% confidence\n")

            self.results_text.see(tk.END)

            # Update count
            self.flagged_count_label.config(
                text=f"{len(self.results)} flagged image(s)",
                foreground='#dc2626'
            )

        self.root.after(0, _add)

    def export_results(self):
        """Export results to a text file"""
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

                messagebox.showinfo("Export Complete", f"Results exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export results:\n{e}")


def main():
    """Main entry point for the GUI application"""
    root = tk.Tk()

    # Try to use a nice theme
    try:
        style = ttk.Style()
        # Use a modern theme if available
        available_themes = style.theme_names()
        if 'vista' in available_themes:
            style.theme_use('vista')
        elif 'clam' in available_themes:
            style.theme_use('clam')
    except:
        pass  # Use default theme

    app = SafetyCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
