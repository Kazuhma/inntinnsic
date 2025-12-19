# Inntinnsic .NET MAUI UI Redesign Specification

## Overview
This document provides detailed specifications for improving the Inntinnsic Image Safety Checker UI built with .NET MAUI. The changes focus on layout stability, visual hierarchy, and better use of space.

---

## MAIN SCREEN CHANGES

### 1. Header Section (Keep As-Is)
The blue "Inntinnsic" header bar and the "Image Safety Checker" card with shield icon are good. No changes needed.

### 2. Action Buttons Row - MAJOR CHANGES

**Current Problem:** 
- Settings button is too prominent (same size as primary actions)
- Three equal-width buttons create confusion about primary action
- "Quick Scan" should be the hero button

**New Layout:**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│  [📁 Add Folder]                    [⚡ Quick Scan]                    [⚙️] │
│     (secondary)                        (primary)                      (icon)│
│     width: 1fr                         width: 1fr                      44px │
└─────────────────────────────────────────────────────────────────────────────┘
```

**MAUI Implementation:**
```xml
<Grid ColumnDefinitions="*, *, 50" ColumnSpacing="12" Padding="20,10">
    <!-- Add Folder Button - Secondary style -->
    <Button Grid.Column="0"
            Text="📁 Add Folder"
            BackgroundColor="#1E293B"
            TextColor="White"
            CornerRadius="8"
            HeightRequest="44"
            BorderColor="#334155"
            BorderWidth="1"/>
    
    <!-- Quick Scan Button - Primary/Accent style -->
    <Button Grid.Column="1"
            Text="⚡ Quick Scan"
            BackgroundColor="#3B82F6"
            TextColor="White"
            CornerRadius="8"
            HeightRequest="44"
            FontAttributes="Bold"/>
    
    <!-- Settings Button - Icon only -->
    <Button Grid.Column="2"
            Text="⚙️"
            BackgroundColor="#1E293B"
            TextColor="#9CA3AF"
            CornerRadius="8"
            WidthRequest="44"
            HeightRequest="44"
            BorderColor="#334155"
            BorderWidth="1"/>
</Grid>
```

### 3. Selected Folders Section - MAJOR CHANGES

**Current Problem:**
- Section is too small/cramped
- No visual feedback when empty
- Needs more vertical space for folder list

**New Layout:**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Selected Folders                                           [Clear All]      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   📁 C:\Users\Kazhuma\Downloads                                    [✕]     │
│   ─────────────────────────────────────────────────────────────────────     │
│   📁 C:\Users\Kazhuma\Pictures                                     [✕]     │
│   ─────────────────────────────────────────────────────────────────────     │
│   📁 C:\Users\Kazhuma\Documents                                    [✕]     │
│   ─────────────────────────────────────────────────────────────────────     │
│   📁 C:\Users\Kazhuma\Desktop                                      [✕]     │
│                                                                             │
│   (empty state: "No folders selected. Click 'Add Folder' above.")          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**MAUI Implementation:**
```xml
<Border BackgroundColor="#1E293B" 
        StrokeShape="RoundRectangle 12"
        Stroke="#334155"
        StrokeThickness="1"
        Padding="0"
        Margin="20,10"
        MinHeightRequest="180"
        MaxHeightRequest="220">
    <Grid RowDefinitions="Auto, *">
        <!-- Header Row -->
        <Grid Grid.Row="0" 
              ColumnDefinitions="*, Auto" 
              Padding="16,12"
              BackgroundColor="#1E293B">
            <Label Text="Selected Folders"
                   TextColor="White"
                   FontSize="15"
                   FontAttributes="Bold"
                   VerticalOptions="Center"/>
            <Button Grid.Column="1"
                    Text="Clear All"
                    BackgroundColor="#EF4444"
                    TextColor="White"
                    CornerRadius="6"
                    HeightRequest="32"
                    Padding="12,0"
                    FontSize="12"
                    IsVisible="{Binding HasFolders}"/>
        </Grid>
        
        <!-- Folder List with ScrollView -->
        <ScrollView Grid.Row="1" Padding="8,0,8,8">
            <CollectionView ItemsSource="{Binding SelectedFolders}"
                            SelectionMode="None">
                <CollectionView.ItemTemplate>
                    <DataTemplate>
                        <Border BackgroundColor="#0F172A"
                                StrokeShape="RoundRectangle 6"
                                Stroke="#334155"
                                Padding="12,10"
                                Margin="0,4">
                            <Grid ColumnDefinitions="Auto, *, Auto">
                                <Label Grid.Column="0" 
                                       Text="📁" 
                                       FontSize="16"
                                       VerticalOptions="Center"
                                       Margin="0,0,10,0"/>
                                <Label Grid.Column="1"
                                       Text="{Binding Path}"
                                       TextColor="#E2E8F0"
                                       FontSize="13"
                                       FontFamily="CascadiaCode"
                                       VerticalOptions="Center"
                                       LineBreakMode="MiddleTruncation"/>
                                <Button Grid.Column="2"
                                        Text="✕"
                                        BackgroundColor="Transparent"
                                        TextColor="#EF4444"
                                        WidthRequest="32"
                                        HeightRequest="32"
                                        CornerRadius="4"
                                        Command="{Binding RemoveCommand}"/>
                            </Grid>
                        </Border>
                    </DataTemplate>
                </CollectionView.ItemTemplate>
                
                <!-- Empty State -->
                <CollectionView.EmptyView>
                    <StackLayout VerticalOptions="Center" 
                                 HorizontalOptions="Center"
                                 Padding="20">
                        <Label Text="📂" 
                               FontSize="32" 
                               HorizontalOptions="Center"
                               Opacity="0.5"/>
                        <Label Text="No folders selected"
                               TextColor="#64748B"
                               FontSize="14"
                               HorizontalOptions="Center"
                               Margin="0,8,0,4"/>
                        <Label Text="Click 'Add Folder' to choose locations to scan"
                               TextColor="#475569"
                               FontSize="12"
                               HorizontalOptions="Center"/>
                    </StackLayout>
                </CollectionView.EmptyView>
            </CollectionView>
        </ScrollView>
    </Grid>
</Border>
```

### 4. Scan Status Section - MAJOR CHANGES

**Current Problem:**
- "View Results" button is too dominant and positioned oddly
- The whole section shifts when scanning starts
- Need fixed height to prevent layout shift

**New Layout:**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Ready to Scan                                       [👁️ View Results]      │
│ Select folders above to begin scanning                  (secondary button)  │
│                                                                             │
│ ════════════════════════════════════════════════════════════════════════   │
│                                                                             │
│                                                  [▶ Start Scan]            │
│                                                  (larger, prominent)        │
└─────────────────────────────────────────────────────────────────────────────┘

During scan:
┌─────────────────────────────────────────────────────────────────────────────┐
│ Analyzing 6145 Images...                            [👁️ View Results]      │
│ Analyzing: Screenshot 2025-12-08 150136.png (199/6145)                      │
│                                                                             │
│ ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│                                                                             │
│                                                  [■ Stop Scan]             │
│                                                  (larger, prominent)        │
└─────────────────────────────────────────────────────────────────────────────┘
```

**MAUI Implementation:**
```xml
<Border BackgroundColor="#1E293B"
        StrokeShape="RoundRectangle 12"
        Stroke="#334155"
        Padding="16,16,16,16"
        Margin="20,10"
        HeightRequest="160">  <!-- FIXED HEIGHT prevents shifting -->
    <Grid RowDefinitions="Auto, Auto, Auto">
        <!-- Row 0: Title + View Results button (with bottom margin) -->
        <Grid Grid.Row="0" ColumnDefinitions="*, Auto" Margin="0,0,0,12">
            <StackLayout Grid.Column="0" VerticalOptions="Center">
                <Label Text="{Binding ScanStatusTitle}"
                       TextColor="White"
                       FontSize="16"
                       FontAttributes="Bold"/>
                <Label Text="{Binding ScanStatusSubtitle}"
                       TextColor="#94A3B8"
                       FontSize="13"
                       Margin="0,4,0,0"/>
            </StackLayout>
            <!-- View Results - EXACT same size as Start Scan (160px width) -->
            <Button Grid.Column="1"
                    Text="⦿ View Results"
                    BackgroundColor="#1E293B"
                    TextColor="White"
                    FontSize="15"
                    FontAttributes="Bold"
                    CornerRadius="8"
                    BorderColor="#334155"
                    BorderWidth="1"
                    WidthRequest="160"
                    HeightRequest="48"
                    Command="{Binding ViewResultsCommand}"/>
        </Grid>
        
        <!-- Row 1: Progress Bar -->
        <ProgressBar Grid.Row="1"
                     Progress="{Binding ScanProgress}"
                     ProgressColor="#3B82F6"
                     BackgroundColor="#334155"
                     HeightRequest="6"
                     VerticalOptions="Center"/>
        
        <!-- Row 2: Start/Stop Scan Button - same margin from progress bar as View Results (12px) -->
        <Button Grid.Row="2"
                Text="{Binding ScanButtonText}"
                BackgroundColor="{Binding ScanButtonColor}"
                TextColor="White"
                CornerRadius="8"
                HeightRequest="48"
                WidthRequest="160"
                FontSize="15"
                FontAttributes="Bold"
                HorizontalOptions="End"
                Margin="0,12,0,0"
                Command="{Binding ScanCommand}"/>
        <!-- ScanButtonColor: #3B82F6 (blue) for Start, #EF4444 (red) for Stop -->
        <!-- ScanButtonText: "▶ Start Scan" or "■ Stop Scan" -->
    </Grid>
</Border>
```

**Key spacing notes:**
- View Results button: 12px margin-bottom (from header row to progress bar)
- Start Scan button: 12px margin-top (from progress bar to button)
- Both buttons: exactly 160px width, 48px height
- Container height: 160px (increased from 140px to accommodate proper spacing)

### 5. Stats Cards Row - NO ICONS

**Current layout is good, just remove the icons:**
```xml
<Grid ColumnDefinitions="*, *, *" ColumnSpacing="15" Padding="20,10">
    <!-- Images Scanned -->
    <Border Grid.Column="0" BackgroundColor="#3B82F6" StrokeShape="RoundRectangle 12" Padding="16">
        <StackLayout>
            <Label Text="{Binding ImagesScanned}" TextColor="White" FontSize="32" FontAttributes="Bold"/>
            <Label Text="Images Scanned" TextColor="#BFDBFE" FontSize="12"/>
        </StackLayout>
    </Border>
    
    <!-- Flagged -->
    <Border Grid.Column="1" BackgroundColor="#F59E0B" StrokeShape="RoundRectangle 12" Padding="16">
        <StackLayout>
            <Label Text="{Binding FlaggedCount}" TextColor="White" FontSize="32" FontAttributes="Bold"/>
            <Label Text="Flagged" TextColor="#FEF3C7" FontSize="12"/>
        </StackLayout>
    </Border>
    
    <!-- Status -->
    <Border Grid.Column="2" BackgroundColor="#10B981" StrokeShape="RoundRectangle 12" Padding="16">
        <StackLayout>
            <Label Text="{Binding StatusText}" TextColor="White" FontSize="24" FontAttributes="Bold"/>
            <Label Text="Status" TextColor="#D1FAE5" FontSize="12"/>
        </StackLayout>
    </Border>
</Grid>
```

### 6. Remove Debug Footer
Remove the "🎉 Dark/Blue theme applied! Ready to migrate functionality." message in production.

---

## SETTINGS PAGE CHANGES

### Current Problems:
1. "Settings" header is redundant (already in blue bar)
2. Sections need better visual separation
3. Checkbox layout in "Content to Flag" is cramped
4. Buttons at bottom need better positioning

### New Layout:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ←  Inntinnsic                                               [─] [□] [✕]    │
├═════════════════════════════════════════════════════════════════════════════┤
│ Settings                                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─ Detection Sensitivity ────────────────────────────────────────────┐    │
│  │                                                                     │    │
│  │  Higher values = more strict detection (fewer false positives)      │    │
│  │                                                                     │    │
│  │  Low ════════════════════●══════════════════════════════════ High   │    │
│  │                                                                     │    │
│  │                        Current: 0.60                                │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─ Content to Flag ──────────────────────────────────────────────────┐    │
│  │                                                                     │    │
│  │  Select which content types should trigger a flag                   │    │
│  │                                                                     │    │
│  │  ┌──────────────────────┐  ┌──────────────────────┐                │    │
│  │  │ ☑ Female Breast      │  │ ☑ Female Genitalia   │                │    │
│  │  └──────────────────────┘  └──────────────────────┘                │    │
│  │  ┌──────────────────────┐  ┌──────────────────────┐                │    │
│  │  │ ☑ Male Genitalia     │  │ ☑ Buttocks Exposed   │                │    │
│  │  └──────────────────────┘  └──────────────────────┘                │    │
│  │  ┌──────────────────────┐  ┌──────────────────────┐                │    │
│  │  │ ☐ Belly Exposed      │  │ ☐ Feet Exposed       │                │    │
│  │  └──────────────────────┘  └──────────────────────┘                │    │
│  │                                                                     │    │
│  │  ⓘ Note: Anus Exposed is always flagged                            │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─ Scan Options ─────────────────────────────────────────────────────┐    │
│  │                                                                     │    │
│  │  ☐  Auto Export Results                                             │    │
│  │     Automatically save scan results to a file                       │    │
│  │                                                                     │    │
│  │  ☑  Skip Hidden Files                                               │    │
│  │     Don't scan files with hidden attribute                          │    │
│  │                                                                     │    │
│  │  ☑  Confirm File Deletions                                          │    │
│  │     Ask for confirmation before deleting files                      │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│         [Reset to Defaults]                    [Save Settings]              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### MAUI Implementation for Settings Page:

```xml
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             BackgroundColor="#0F172A">
    
    <Grid RowDefinitions="Auto, *">
        <!-- Blue Header Bar -->
        <Grid Grid.Row="0" BackgroundColor="#2563EB" Padding="16,12">
            <Grid ColumnDefinitions="Auto, *, Auto">
                <Button Grid.Column="0" 
                        Text="←" 
                        BackgroundColor="Transparent"
                        TextColor="White"
                        FontSize="20"
                        Command="{Binding GoBackCommand}"/>
                <Label Grid.Column="1" 
                       Text="Settings" 
                       TextColor="White" 
                       FontSize="20"
                       FontAttributes="Bold"
                       VerticalOptions="Center"
                       Margin="12,0,0,0"/>
            </Grid>
        </Grid>
        
        <!-- Scrollable Content -->
        <ScrollView Grid.Row="1" Padding="20">
            <StackLayout Spacing="16">
                
                <!-- Detection Sensitivity Section -->
                <Border BackgroundColor="#1E293B" 
                        StrokeShape="RoundRectangle 12"
                        Stroke="#334155"
                        Padding="20">
                    <StackLayout Spacing="12">
                        <Label Text="Detection Sensitivity"
                               TextColor="White"
                               FontSize="16"
                               FontAttributes="Bold"/>
                        <Label Text="Higher values = more strict detection (fewer false positives)"
                               TextColor="#94A3B8"
                               FontSize="13"/>
                        
                        <Grid ColumnDefinitions="Auto, *, Auto" Margin="0,8">
                            <Label Grid.Column="0" Text="Low" TextColor="#64748B" FontSize="12"/>
                            <Slider Grid.Column="1" 
                                    Minimum="0" 
                                    Maximum="1" 
                                    Value="{Binding Sensitivity}"
                                    ThumbColor="#3B82F6"
                                    MinimumTrackColor="#3B82F6"
                                    MaximumTrackColor="#475569"
                                    Margin="12,0"/>
                            <Label Grid.Column="2" Text="High" TextColor="#64748B" FontSize="12"/>
                        </Grid>
                        
                        <Label Text="{Binding Sensitivity, StringFormat='Current: {0:F2}'}"
                               TextColor="#60A5FA"
                               FontSize="14"
                               HorizontalOptions="Center"/>
                    </StackLayout>
                </Border>
                
                <!-- Content to Flag Section -->
                <Border BackgroundColor="#1E293B"
                        StrokeShape="RoundRectangle 12"
                        Stroke="#334155"
                        Padding="20">
                    <StackLayout Spacing="12">
                        <Label Text="Content to Flag"
                               TextColor="White"
                               FontSize="16"
                               FontAttributes="Bold"/>
                        <Label Text="Select which content types should trigger a flag"
                               TextColor="#94A3B8"
                               FontSize="13"/>
                        
                        <!-- 2-column grid for checkboxes -->
                        <Grid ColumnDefinitions="*, *" 
                              RowDefinitions="Auto, Auto, Auto"
                              ColumnSpacing="12"
                              RowSpacing="8"
                              Margin="0,8">
                            
                            <!-- Row 0 -->
                            <Border Grid.Row="0" Grid.Column="0" 
                                    BackgroundColor="#0F172A" 
                                    StrokeShape="RoundRectangle 8"
                                    Stroke="#334155"
                                    Padding="12,10">
                                <HorizontalStackLayout Spacing="10">
                                    <CheckBox IsChecked="{Binding FlagFemaleBreast}" 
                                              Color="#3B82F6"/>
                                    <Label Text="Female Breast Exposed" 
                                           TextColor="#E2E8F0" 
                                           VerticalOptions="Center"
                                           FontSize="13"/>
                                </HorizontalStackLayout>
                            </Border>
                            
                            <Border Grid.Row="0" Grid.Column="1"
                                    BackgroundColor="#0F172A"
                                    StrokeShape="RoundRectangle 8"
                                    Stroke="#334155"
                                    Padding="12,10">
                                <HorizontalStackLayout Spacing="10">
                                    <CheckBox IsChecked="{Binding FlagFemaleGenitalia}"
                                              Color="#3B82F6"/>
                                    <Label Text="Female Genitalia Exposed"
                                           TextColor="#E2E8F0"
                                           VerticalOptions="Center"
                                           FontSize="13"/>
                                </HorizontalStackLayout>
                            </Border>
                            
                            <!-- Row 1 -->
                            <Border Grid.Row="1" Grid.Column="0"
                                    BackgroundColor="#0F172A"
                                    StrokeShape="RoundRectangle 8"
                                    Stroke="#334155"
                                    Padding="12,10">
                                <HorizontalStackLayout Spacing="10">
                                    <CheckBox IsChecked="{Binding FlagMaleGenitalia}"
                                              Color="#3B82F6"/>
                                    <Label Text="Male Genitalia Exposed"
                                           TextColor="#E2E8F0"
                                           VerticalOptions="Center"
                                           FontSize="13"/>
                                </HorizontalStackLayout>
                            </Border>
                            
                            <Border Grid.Row="1" Grid.Column="1"
                                    BackgroundColor="#0F172A"
                                    StrokeShape="RoundRectangle 8"
                                    Stroke="#334155"
                                    Padding="12,10">
                                <HorizontalStackLayout Spacing="10">
                                    <CheckBox IsChecked="{Binding FlagButtocks}"
                                              Color="#3B82F6"/>
                                    <Label Text="Buttocks Exposed"
                                           TextColor="#E2E8F0"
                                           VerticalOptions="Center"
                                           FontSize="13"/>
                                </HorizontalStackLayout>
                            </Border>
                            
                            <!-- Row 2 -->
                            <Border Grid.Row="2" Grid.Column="0"
                                    BackgroundColor="#0F172A"
                                    StrokeShape="RoundRectangle 8"
                                    Stroke="#334155"
                                    Padding="12,10">
                                <HorizontalStackLayout Spacing="10">
                                    <CheckBox IsChecked="{Binding FlagBelly}"
                                              Color="#3B82F6"/>
                                    <Label Text="Belly Exposed"
                                           TextColor="#E2E8F0"
                                           VerticalOptions="Center"
                                           FontSize="13"/>
                                </HorizontalStackLayout>
                            </Border>
                            
                            <Border Grid.Row="2" Grid.Column="1"
                                    BackgroundColor="#0F172A"
                                    StrokeShape="RoundRectangle 8"
                                    Stroke="#334155"
                                    Padding="12,10">
                                <HorizontalStackLayout Spacing="10">
                                    <CheckBox IsChecked="{Binding FlagFeet}"
                                              Color="#3B82F6"/>
                                    <Label Text="Feet Exposed"
                                           TextColor="#E2E8F0"
                                           VerticalOptions="Center"
                                           FontSize="13"/>
                                </HorizontalStackLayout>
                            </Border>
                        </Grid>
                        
                        <!-- Note -->
                        <Border BackgroundColor="#1E3A5F"
                                StrokeShape="RoundRectangle 6"
                                Padding="12,8"
                                Margin="0,4,0,0">
                            <HorizontalStackLayout Spacing="8">
                                <Label Text="ℹ️" FontSize="14"/>
                                <Label Text="Note: Anus Exposed is always flagged"
                                       TextColor="#93C5FD"
                                       FontSize="12"
                                       FontAttributes="Italic"/>
                            </HorizontalStackLayout>
                        </Border>
                    </StackLayout>
                </Border>
                
                <!-- Scan Options Section -->
                <Border BackgroundColor="#1E293B"
                        StrokeShape="RoundRectangle 12"
                        Stroke="#334155"
                        Padding="20">
                    <StackLayout Spacing="4">
                        <Label Text="Scan Options"
                               TextColor="White"
                               FontSize="16"
                               FontAttributes="Bold"
                               Margin="0,0,0,12"/>
                        
                        <!-- Option 1 -->
                        <Grid ColumnDefinitions="Auto, *" Padding="0,8">
                            <CheckBox Grid.Column="0" 
                                      IsChecked="{Binding AutoExport}"
                                      Color="#3B82F6"/>
                            <StackLayout Grid.Column="1" Margin="8,0,0,0">
                                <Label Text="Auto Export Results"
                                       TextColor="White"
                                       FontSize="14"/>
                                <Label Text="Automatically save scan results to a file"
                                       TextColor="#64748B"
                                       FontSize="12"/>
                            </StackLayout>
                        </Grid>
                        
                        <BoxView HeightRequest="1" Color="#334155" Margin="0,4"/>
                        
                        <!-- Option 2 -->
                        <Grid ColumnDefinitions="Auto, *" Padding="0,8">
                            <CheckBox Grid.Column="0"
                                      IsChecked="{Binding SkipHidden}"
                                      Color="#3B82F6"/>
                            <StackLayout Grid.Column="1" Margin="8,0,0,0">
                                <Label Text="Skip Hidden Files"
                                       TextColor="White"
                                       FontSize="14"/>
                                <Label Text="Don't scan files with hidden attribute"
                                       TextColor="#64748B"
                                       FontSize="12"/>
                            </StackLayout>
                        </Grid>
                        
                        <BoxView HeightRequest="1" Color="#334155" Margin="0,4"/>
                        
                        <!-- Option 3 -->
                        <Grid ColumnDefinitions="Auto, *" Padding="0,8">
                            <CheckBox Grid.Column="0"
                                      IsChecked="{Binding ConfirmDeletions}"
                                      Color="#3B82F6"/>
                            <StackLayout Grid.Column="1" Margin="8,0,0,0">
                                <Label Text="Confirm File Deletions"
                                       TextColor="White"
                                       FontSize="14"/>
                                <Label Text="Ask for confirmation before deleting files"
                                       TextColor="#64748B"
                                       FontSize="12"/>
                            </StackLayout>
                        </Grid>
                    </StackLayout>
                </Border>
                
                <!-- Action Buttons - No icons needed, labels are self-explanatory -->
                <Grid ColumnDefinitions="*, *" ColumnSpacing="15" Margin="0,8,0,20">
                    <Button Grid.Column="0"
                            Text="Reset to Defaults"
                            BackgroundColor="#374151"
                            TextColor="White"
                            CornerRadius="8"
                            HeightRequest="48"
                            Command="{Binding ResetCommand}"/>
                    <Button Grid.Column="1"
                            Text="Save Settings"
                            BackgroundColor="#3B82F6"
                            TextColor="White"
                            CornerRadius="8"
                            HeightRequest="48"
                            FontAttributes="Bold"
                            Command="{Binding SaveCommand}"/>
                </Grid>
                
            </StackLayout>
        </ScrollView>
    </Grid>
</ContentPage>
```

---

## COLOR PALETTE REFERENCE

```
Background (darkest):    #0F172A
Card background:         #1E293B
Card border:             #334155
Input background:        #0F172A

Primary accent (blue):   #3B82F6
Primary hover:           #2563EB
Header bar:              #2563EB

Text primary:            #FFFFFF
Text secondary:          #94A3B8
Text muted:              #64748B
Text link:               #60A5FA

Success (green):         #10B981
Warning (orange):        #F59E0B
Danger (red):            #EF4444
```

---

## SUMMARY OF KEY CHANGES

### Main Screen:
1. **Settings button → small icon button** (right side of action row)
2. **Add Folder & Quick Scan → equal width** (1fr each in grid)
3. **Selected Folders → taller with ScrollView** (MinHeight 180, MaxHeight 220)
4. **Scan Status section → fixed height (160px)** to prevent layout shift
5. **View Results → secondary button with ⦿ icon** (exact same size as Start Scan: 160x48)
6. **Start Scan → BLUE (#3B82F6)**, Stop Scan → RED (#EF4444)
7. **Equal spacing: 12px** from progress bar to both buttons (above and below)
8. **Stats cards → NO icons** (just numbers and labels)
9. **Remove debug footer** in production

### Settings Page:
1. **Remove redundant "Settings" header with icon** (keep only in blue bar)
2. **Content to Flag → 2-column grid** with bordered checkbox items
3. **Add info note styling** (blue tinted background)
4. **Better spacing between sections** (16px gap)
5. **Action buttons → no icons** (labels are self-explanatory)
6. **Scroll entire page** for smaller screens

### General:
- Use consistent 12px border radius on cards
- Use consistent padding (16-20px) inside cards
- Use consistent margins (20px horizontal, 10px vertical between sections)
- View Results and Start/Stop Scan buttons: exactly 160px × 48px
